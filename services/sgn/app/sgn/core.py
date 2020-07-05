import time
import logging
import argparse
import random
import pickle
import numpy as np

import torch
import torch.nn.functional as F
from torch.optim import lr_scheduler
from torch_geometric.data import Data, DataLoader
from torch_geometric.nn import GCNConv, global_mean_pool
from torch_geometric.utils import add_self_loops

from .utils.loader import *
from .models import *

def train(device, model, optimizer, data_loader, data_size):
    model.train()

    total_loss = 0
    correct = 0
    for data in data_loader:
        data = data.to(device)
        optimizer.zero_grad()
        out = model(data)
        loss = F.nll_loss(out, data.y)
        loss.backward()
        total_loss += loss.item() * data.num_graphs
        optimizer.step()

        correct += out.max(dim=1)[1].eq(data.y).sum().item()

    train_loss = total_loss / data_size
    train_acc = correct / data_size
    
    return train_loss, train_acc

def test(device, model, data_loader, data_size):
    model.eval()

    total_loss = 0
    correct = 0
    predicted_y = []
    original_y = []
    for data in data_loader:
        data = data.to(device)
        with torch.no_grad():
            out = model(data)
            loss = F.nll_loss(out, data.y)
        total_loss += loss.item() * data.num_graphs
        predicted_y.extend(out.max(dim=1)[1])
        original_y.extend(data.y)
        correct += out.max(dim=1)[1].eq(data.y).sum().item()

    test_loss = total_loss / data_size
    test_acc = correct / data_size
    test_out = (predicted_y, original_y)
    
    return test_loss, test_acc, test_out

def run_model(taskid, tasktype, traindata, valdata, enabletest, testdata, model, paramset):
    ## Hyper-parameter setting
    SEED          = 1 # seed for random state
    DATA_PATH     = '/' # where to locate the data
    LOG_PATH      = 'sgn/logs/test.log' # where to save the log
    BATCH_SIZE    = paramset['batch_size'] # batch size of data loader
    LEARNING_RATE = paramset['learning_rate'] # initial learning rate
    LR_STEP_SIZE  = paramset['lr_step_size'] # epochs before each lr decay
    LR_DECAY      = paramset['lr_decay'] # multiplied by for lr decay
    NUM_EPOCHS    = paramset['epochs'] # number of epochs for training
    SAVE_MODEL    = paramset['save_model_state'] # whether save model
    SAVE_PATH     = '/nld_sgn/models/checkpoints/' + taskid + '.pth' # name of the model

    ## Configure logging
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(levelname)s] %(message)s')
    logging.basicConfig(level=logging.ERROR, format='[%(asctime)s %(levelname)s] %(message)s')
    logger = logging.getLogger()
    hdlr = logging.FileHandler(LOG_PATH)
    # hdlr = logging.FileHandler('logs/train_val_' + time.strftime('%Y-%m-%d-%H-%M-%S') + '.log')
    hdlr.setFormatter(logging.Formatter('[%(asctime)s %(levelname)s] %(message)s'))
    logger.addHandler(hdlr)

    ## Ensure reproducibility, refering to https://blog.csdn.net/hyk_1996/article/details/84307108
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)

    ## Create dataset with multiple data
    # train_dataset, test_dataset = fromPickle2Dataset('/workspace/schizo_graph_net/data/bennyray_191107_347_bcn.pkl')
    # train_dataset, test_dataset = fromPickle2DatasetWithFeature('/workspace/schizo_graph_net/data/bennyray_191107_347_bcn.pkl', '/workspace/schizo_graph_net/data/RANIAC_181210_345_sfMRI_90.csv')
    # train_dataset, test_dataset = fromTxt2Dataset('/workspace/schizo_graph_net/data/ByDPABI/')
    train_dataset, test_dataset = fromTxt2DatasetWithFeature(DATA_PATH + '/nld_sgn/app/sgn/data/test_dpabi/', DATA_PATH + '/nld_sgn/app/sgn/data/RANIAC_181210_345_sfMRI_90.csv')

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

    if torch.cuda.is_available():
        logging.info('Using GPU')
    else:
        logging.info('Using CPU')
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = Net_191225().to(device)
    ## for fine-tune tasks, load model state
    if tasktype == 'dl_ft':
        try:
            loaded_model_state = torch.load(paramset['model_state_path'])
            model.load_state_dict(loaded_model_state['state_dict'])
        except:
            raise Exception("Model state not found.")

    ## 1. Train new model from scratch
    # model = Net_191225().to(device)
    ## 2.1. Load model parameters with network structure
    # model = torch.load(modelpath)
    ## 2.2. Load model parameters
    # model = Net_191225().to(device)
    # model.load_state_dict(torch.load(modelpath))
    ## 2.3. Load model parameters by pickle
    # loaded_model_state = pickle.loads(modelstatepickle)
    # model = Net_191225()
    # model.load_state_dict(loaded_model_state['state_dict'])

    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    if tasktype == 'dl_ft':
        try:
            optimizer.load_state_dict(loaded_model_state['optimizer'])
        except:
            raise Exception("Model state not found.")

    ## learning-rate scheduler.
    scheduler = lr_scheduler.StepLR(optimizer, step_size=LR_STEP_SIZE, gamma=LR_DECAY)

    train_epochs = []
    for epoch in range(1, NUM_EPOCHS+1):
        scheduler.step()
        train_loss, train_acc = train(device, model, optimizer, train_loader, len(train_dataset))
        test_loss, test_acc, _ = test(device, model, test_loader, len(test_dataset))
        epoch_res = 'Epoch {:03d}, Train Loss: {:.4f}, Train Accuracy: {:.4f}, Test Loss: {:.4f}, Test Accuracy: {:.4f}'.format(epoch, train_loss, train_acc, test_loss, test_acc)
        logging.info(epoch_res)
        train_epochs.append(epoch_res)

    ## checking final test results
    test_loss, test_acc, test_out = test(device, model, test_loader, len(test_dataset))
    test_check = []
    for idx in range(len(test_out[0])):
        test_out[0][idx] = test_out[0][idx].item()
        test_out[1][idx] = test_out[1][idx].item()
        if test_out[0][idx] == test_out[1][idx]:
            test_check.append(1)
        else:
            test_check.append(0)
    print(test_out[0])
    print(test_out[1])
    print(test_check)

    ## TODO save model and parameters to pickle, referring to https://blog.csdn.net/fendoubasaonian/article/details/88552370
    ## 1. Save model parameters and network structure
    # torch.save(model, SAVE_PATH)
    ## 2. Save model parameters
    # torch.save(model.state_dict(), SAVE_PATH)
    ## 3. Serialize model parameters by pickle
    ## save model state in the deployed server and the path in the database
    if SAVE_MODEL:
        model_state = {
            'state_dict': model.state_dict(),
            'optimizer': optimizer.state_dict()
        }
        torch.save(model_state, SAVE_PATH)

    ## return model training results and model state path
    ## to store them in database
    result_dict = {}
    result_dict['train_epochs'] = train_epochs
    result_dict['model_state_path'] = SAVE_PATH

    return result_dict