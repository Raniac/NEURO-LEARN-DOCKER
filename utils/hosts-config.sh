# CHANGE the corresponding host IP's
commons_hostip="127.0.0.1";
ml_hostip="127.0.0.1";
sgn_hostip="127.0.0.1";

# !!!! DO NOT change the code below !!!!
echo ${commons_hostip}" commons.neurolearn.com" >> /etc/hosts;
echo ${ml_hostip}" ml.neurolearn.com" >> /etc/hosts;
echo ${sgn_hostip}" sgn.neurolearn.com" >> /etc/hosts;
