"""
数据库连接配置模块。
配置项来源（优先级从高到低）：
1. 系统环境变量
2. xd.env 文件
"""

import os
import pymysql

from contextlib import contextmanager
from dotenv import load_dotenv

# 定位项目根目录下的 xd.env 文件
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_XD_ENV_PATH = os.path.join(_BASE_DIR, '..', 'xd.env')

# load_dotenv 默认不覆盖已存在的环境变量，因此系统环境变量优先级更高
load_dotenv(_XD_ENV_PATH)

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE'),
    'charset': os.getenv('DB_CHARSET'),
}

def get_connection():
    """获取数据库连接"""
    return pymysql.connect(**DB_CONFIG)


@contextmanager
def get_db():
    """数据库连接上下文管理器"""
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()