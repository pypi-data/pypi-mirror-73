import os
from pymodm.connection import connect

# ==== Configuration ====

DB_CONFIG = 'cfg'

CN_SEQUENCE = 'sequence'
CN_CCXT_CONFIG = 'cxt'


def connect_db(user, password, host, db_name):
    # 连接到数据库
    uri = "mongodb://{}:{}@{}/{}?authSource=admin".format(user, password, host, db_name)
    connect(uri, db_name)


def connect_db_env(host, db_name):
    connect_db(os.environ['DB_MNR_USER'], os.environ['DB_MNR_PWD'], host, db_name)
