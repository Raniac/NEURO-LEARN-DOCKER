def fromConnMat2Edges(conn_mat, label, node_feat):
    """
    :type conn_mat: List
    :type label: int
    :type node_feat: List
    :rtype: Torch Data Object
    """
    import torch
    from torch_geometric.data import Data
    import numpy as np

    edge_index_tmp = [[], []]
    edge_attr_tmp = []

    ## data preprocessing
    conn_mat -= conn_mat.mean()
    conn_mat /= conn_mat.std()

    for idx, itm in enumerate(conn_mat):
        edge_index_tmp[0].extend([idx for i in range(idx, len(itm))])
        edge_index_tmp[1].extend([i for i in range(idx, len(itm))])
        for jdx in range(idx, len(itm)):
            edge_attr_tmp.append([itm[jdx]])

    edge_index = torch.tensor(edge_index_tmp, dtype=torch.long)
    # where 0, 1 are the node indeces
    # the shape of edge_index is [2, num_edges]

    edge_attr = torch.tensor(edge_attr_tmp, dtype=torch.float)
    # where the list items are the edge feature vectors
    # the shape of edge_attr is [num_edges, num_edge_features]

    x = torch.tensor(node_feat, dtype=torch.float)
    # where the list items are the node feature vectors
    # the shape of x is [num_nodes, num_node_features]

    y = torch.tensor([label], dtype=torch.long)

    data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr, y=y)
    return data

def fromPickle2Dataset(pkl_path):
    """
    :type pkl_path: String
    :rtype train_dataset: List
    :rtype test_dataset: List
    """
    import pickle
    import logging
    import random

    with open(pkl_path, 'rb') as pkl_file:
        conn_mats = pickle.load(pkl_file)
    logging.info('Data size: {:d}'.format(len(conn_mats)))

    train_dataset = []
    test_dataset = []
    nc_counter = 0
    sz_counter = 0
    conn_mats_keys = list(conn_mats.keys())
    random.shuffle(conn_mats_keys)
    for subj in conn_mats_keys:
        if subj[:2] == 'NC':
            if nc_counter < 150:
                train_dataset.append(fromConnMat2Edges(conn_mats[subj], 0, [[1] for i in range(90)]))
            else:
                test_dataset.append(fromConnMat2Edges(conn_mats[subj], 0, [[1] for i in range(90)]))
            nc_counter += 1
        else:
            if sz_counter < 100:
                train_dataset.append(fromConnMat2Edges(conn_mats[subj], 1, [[1] for i in range(90)]))
            else:
                test_dataset.append(fromConnMat2Edges(conn_mats[subj], 1, [[1] for i in range(90)]))
            sz_counter += 1

    return train_dataset, test_dataset

def fromPickle2DatasetWithFeature(pkl_path, feat_path):
    """
    :type pkl_path: String
    :type feat_path: String
    :rtype train_dataset: List
    :rtype test_dataset: List
    """
    import pickle
    import logging
    import random
    import pandas as pd

    with open(pkl_path, 'rb') as pkl_file:
        conn_mats = pickle.load(pkl_file)
    # logging.info('Data size: {:d}'.format(len(conn_mats)))

    features = pd.read_csv(feat_path, index_col='ID').drop(['LABEL'], axis = 1)

    train_dataset = []
    test_dataset = []
    nc_counter = 0
    sz_counter = 0
    conn_mats_keys = list(conn_mats.keys())
    random.shuffle(conn_mats_keys)
    for subj in conn_mats_keys:
        if subj not in features.index.to_list():
            continue
        node_feat_all = features.loc[subj, :].to_list()
        node_feat_gmv = node_feat_all[:90]
        node_feat_reho = node_feat_all[90:180]
        node_feat_alff = node_feat_all[180:270]
        node_feat_dc = node_feat_all[270:]
        node_feat = []
        for idx in range(len(node_feat_gmv)):
            node_feat.append([node_feat_gmv[idx], node_feat_reho[idx], node_feat_alff[idx], node_feat_dc[idx]])
        if subj[:2] == 'NC':
            if nc_counter < 150:
                train_dataset.append(fromConnMat2Edges(conn_mats[subj], 0, node_feat))
            else:
                test_dataset.append(fromConnMat2Edges(conn_mats[subj], 0, node_feat))
            nc_counter += 1
        else:
            if sz_counter < 100:
                train_dataset.append(fromConnMat2Edges(conn_mats[subj], 1, node_feat))
            else:
                test_dataset.append(fromConnMat2Edges(conn_mats[subj], 1, node_feat))
            sz_counter += 1

    logging.info('Data size: {:d} train, {:d} test; {:d} NC, {:d} SZ.'.format(len(train_dataset), len(test_dataset), nc_counter, sz_counter))

    return train_dataset, test_dataset

def fromTxt2Dataset(txt_path):
    """
    :type txt_path: String
    :rtype train_dataset: List
    :rtype test_dataset: List
    """
    import numpy as np
    import logging
    import random
    import os

    train_dataset = []
    test_dataset = []
    nc_counter = 0
    sz_counter = 0
    txt_filename_list = os.listdir(txt_path)
    random.shuffle(txt_filename_list)
    for txt_filename in txt_filename_list:
        conn_mat = np.loadtxt(txt_path + txt_filename)
        subj = txt_filename[15:25]
        if subj[:2] == 'NC':
            if nc_counter < 150:
                train_dataset.append(fromConnMat2Edges(conn_mat, 0, [[1] for i in range(90)]))
            else:
                test_dataset.append(fromConnMat2Edges(conn_mat, 0, [[1] for i in range(90)]))
            nc_counter += 1
        else:
            if sz_counter < 100:
                train_dataset.append(fromConnMat2Edges(conn_mat, 1, [[1] for i in range(90)]))
            else:
                test_dataset.append(fromConnMat2Edges(conn_mat, 1, [[1] for i in range(90)]))
            sz_counter += 1

    logging.info('Data size: {:d} train, {:d} test; {:d} NC, {:d} SZ.'.format(len(train_dataset), len(test_dataset), nc_counter, sz_counter))

    return train_dataset, test_dataset

def fromTxt2DatasetWithFeature(txt_path, feat_path):
    """
    :type txt_path: String
    :type feat_path: String
    :rtype train_dataset: List
    :rtype test_dataset: List
    """
    import numpy as np
    import pandas as pd
    import logging
    import random
    import os

    features = pd.read_csv(feat_path, index_col='ID').drop(['LABEL'], axis = 1)

    train_dataset = []
    test_dataset = []
    nc_counter = 0
    sz_counter = 0
    txt_filename_list = os.listdir(txt_path)
    random.shuffle(txt_filename_list)
    for txt_filename in txt_filename_list:
        conn_mat = np.loadtxt(txt_path + txt_filename)
        subj = txt_filename[15:25]
        if subj not in features.index.to_list():
            continue
        node_feat_all = features.loc[subj, :].to_list()
        node_feat_gmv = node_feat_all[:90]
        node_feat_reho = node_feat_all[90:180]
        node_feat_alff = node_feat_all[180:270]
        node_feat_dc = node_feat_all[270:]
        node_feat = []
        for idx in range(len(node_feat_gmv)):
            node_feat.append([node_feat_gmv[idx], node_feat_reho[idx], node_feat_alff[idx], node_feat_dc[idx]])
        if subj[:2] == 'NC':
            if nc_counter < 100:
                train_dataset.append(fromConnMat2Edges(conn_mat, 0, node_feat))
            elif nc_counter >= 100 and nc_counter < 140:
                test_dataset.append(fromConnMat2Edges(conn_mat, 0, node_feat))
            else:
                continue
            nc_counter += 1
        else:
            if sz_counter < 100:
                train_dataset.append(fromConnMat2Edges(conn_mat, 1, node_feat))
            else:
                test_dataset.append(fromConnMat2Edges(conn_mat, 1, node_feat))
            sz_counter += 1

    logging.info('Data size: {:d} train, {:d} test; {:d} NC, {:d} SZ.'.format(len(train_dataset), len(test_dataset), nc_counter, sz_counter))

    return train_dataset, test_dataset