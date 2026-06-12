"""
定时任务主入口
使用 APScheduler 实现定时调度，任务持久化到 MySQL。
时区以 UTC 时间为准。
"""

import os
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.triggers.cron import CronTrigger
from urllib.parse import quote_plus

# 添加项目根目录到 sys.path
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from task.taptap.taptap_game_info_task import TapTapGameInfoTask
from data.taptap.app.game_list_taptap_dao import GameListTaptapDao
from logger.xd_logger_cfg import logger

# ---- TapTap 游戏信息采集 ----
def crawling_taptap_game_info():
    """每小时第15分执行一次"""
    try:
        logger.info("定时任务[TapTap游戏信息采集]执行中...")
        dao = GameListTaptapDao()
        # 查询游戏列表
        games = dao.query_list("download")
        logger.info(f"从游戏列表中查询到 {len(games)} 款游戏")
        for game in games:
            app_id = game.get("app_id")
            if app_id:
                logger.info(f"正在抓取 TapTap 游戏 app_id={app_id} 的信息...")
                TapTapGameInfoTask(int(app_id)).execute()
                time.sleep(10)
        logger.info("定时任务[TapTap游戏信息采集]执行完毕!")
    except Exception as e:
        logger.error(f"定时任务[TapTap游戏信息采集]执行失败! {e}")

# ============================================================
# 调度器配置
# ============================================================

username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
encoded_password = quote_plus(password)
host = os.getenv('DB_HOST')
port = int(os.getenv('DB_PORT'))
database = os.getenv('DB_DATABASE')

DB_URL = f"mysql+pymysql://{username}:{encoded_password}@{host}:{port}/{database}?charset=utf8mb4"

jobstores = {
    'default': SQLAlchemyJobStore(url=DB_URL)
}
executors = {
    'default': ThreadPoolExecutor(max_workers=10)
}
job_defaults = {
    'coalesce': True,
    'max_instances': 4,
}

scheduler = BackgroundScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
    timezone='UTC',
)

# TapTap游戏信息采集：每小时第15分
scheduler.add_job(
    crawling_taptap_game_info,
    trigger=CronTrigger(minute=5),
    id='taptap_game_info',
    replace_existing=True,
    name='每小时第15分 抓取TapTap游戏信息',
)

# ============================================================
# 启动
# ============================================================
# scheduler.start()
# logger.info("调度器已启动 (时区: UTC)，任务信息已持久化到 MySQL")

# try:
#     while True:
#         time.sleep(60)
# except KeyboardInterrupt:
#     logger.info("收到终止信号，正在关闭调度器...")
#     scheduler.shutdown()

crawling_taptap_game_info()