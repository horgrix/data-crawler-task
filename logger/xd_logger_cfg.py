"""
日志配置模块
支持按周滚动的文件日志，日志文件保存在项目目录的 log/ 子目录下。
"""

import os
import logging
from logging.handlers import TimedRotatingFileHandler


# 获取项目根目录（logger 的父目录）
_PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LOG_DIR = os.path.join(_PROJECT_DIR, 'log')

# 确保日志目录存在
os.makedirs(_LOG_DIR, exist_ok=True)

# 创建 Logger
logger = logging.getLogger('xd')
logger.setLevel(logging.INFO)

# 日志文件完整路径
_LOG_FILE = os.path.join(_LOG_DIR, 'data-crawler-task.log')

# 创建 TimedRotatingFileHandler，按周滚动（每周一凌晨切分）
handler = TimedRotatingFileHandler(
    _LOG_FILE,
    when='W0',         # 按周滚动，W0=周一
    interval=1,        # 每隔1周
    backupCount=8,     # 保留最近8周的日志
    encoding='utf-8',
)

# 日志格式
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

# 避免重复添加 handler
if not logger.handlers:
    logger.addHandler(handler)