import datetime
import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.triggers.cron import CronTrigger

from dotenv import load_dotenv
from urllib.parse import quote_plus
from steam_top_rank_task import execute_4_topseller_weekly_rank, execute_4_topselling_daily_rank
from steam_game_players_task import excute_4_fetch_daily_data, execute_4_fetch_monthly_data
from steam_game_recommendations_task import execute_4_fetch_daily_recommendations, execute_4_fetch_monthly_recommendations

from logging_cfg import logger

load_dotenv()  # 自动寻找 .env 文件

username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
encoded_password = quote_plus(password)
host = os.getenv('DB_HOST')
port = int(os.getenv('DB_PORT'))
database = os.getenv('DB_DATABASE')

# 1. 定义要定时执行的任务
def crawling_steam_xd_games_top_rank_daily_task():
    try:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"定时任务[crawling_steam_xd_games_top_rank_daily_task]执行中... 当前时间: {current_time}")

        valid_steam_ids = os.getenv("STEAM_CRAWLER_XD_GAMES_ID_LIST").split(",")
        valid_region_list = os.getenv("STEAM_CRAWLER_XD_GAMES_REGIONS").split(",")
        logger.info(f"涉及游戏SteamIDs={valid_steam_ids}，涉及区域Regions={valid_region_list}")
        execute_4_topselling_daily_rank(valid_region_list, valid_steam_ids)
        logger.info(f"定时任务[crawling_steam_xd_games_top_rank_daily_task]执行完毕!")
    except Exception as e:
        logger.error(f"定时任务[crawling_steam_xd_games_top_rank_daily_task]执行失败! {e}")

def crawling_steam_xd_games_top_rank_weekly_task():
    try:
        """每周3 10：30执行一次的业务逻辑"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"定时任务[crawling_steam_xd_games_top_rank_weekly_task]执行中... 当前时间: {current_time}")
        valid_steam_ids = os.getenv("STEAM_CRAWLER_XD_GAMES_ID_LIST").split(",")
        valid_region_list = os.getenv("STEAM_CRAWLER_XD_GAMES_REGIONS").split(",")
        logger.info(f"涉及游戏SteamIDs={valid_steam_ids}，涉及区域Regions={valid_region_list}")
        execute_4_topseller_weekly_rank(valid_region_list, valid_steam_ids)
        logger.info(f"定时任务[crawling_steam_xd_games_top_rank_weekly_task]执行完毕!")
    except Exception as e:
        logger.error(f"定时任务[crawling_steam_xd_games_top_rank_weekly_task]执行失败! {e}")

def crawling_steam_xd_games_players_daily_task():
    try:
        """每1小时执行一次的业务逻辑"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"定时任务[crawling_steam_xd_games_players_daily_task]执行中... 当前时间: {current_time}")

        torchlight_cn_steam_id = os.getenv('TORCHLIGHT_INFINITE_CN_STEAM_ID')
        torchlight_cn_steam_name = os.getenv('TORCHLIGHT_INFINITE_CN_STEAM_NAME')
        logger.info(f"SteamId={torchlight_cn_steam_id},Game-{torchlight_cn_steam_name}抓取中...")
        excute_4_fetch_daily_data(torchlight_cn_steam_id, torchlight_cn_steam_name)

        torchlight_global_steam_id = os.getenv('TORCHLIGHT_INFINITE_GLOBAL_STEAM_ID')
        torchlight_global_steam_name = os.getenv('TORCHLIGHT_INFINITE_GLOBAL_STEAM_NAME')
        excute_4_fetch_daily_data(torchlight_global_steam_id, torchlight_global_steam_name)
        logger.info(f"SteamId={torchlight_global_steam_id},Game-{torchlight_global_steam_name}抓取中...")

        heartopia_global_steam_id = os.getenv('HEARTOPIA_GLOBAL_STEAM_ID')
        heartopia_global_steam_name = os.getenv('HEARTOPIA_GLOBAL_STEAM_NAME')
        excute_4_fetch_daily_data(heartopia_global_steam_id, heartopia_global_steam_name)
        logger.info(f"SteamId={heartopia_global_steam_id},Game-{heartopia_global_steam_name}抓取中...")
        
        logger.info(f"定时任务[crawling_steam_xd_games_players_daily_task]执行完毕!")
    except Exception as e:
        logger.error(f"定时任务[crawling_steam_xd_games_players_daily_task]执行失败! {e}")

def crawling_steam_xd_games_players_monthly_task():
    try:
        """每月第2天8点执行一次的业务逻辑"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"定时任务[crawling_steam_xd_games_players_monthly_task]执行中... 当前时间: {current_time}")

        torchlight_cn_steam_id = os.getenv('TORCHLIGHT_INFINITE_CN_STEAM_ID')
        torchlight_cn_steam_name = os.getenv('TORCHLIGHT_INFINITE_CN_STEAM_NAME')
        logger.info(f"SteamId={torchlight_cn_steam_id},Game-{torchlight_cn_steam_name}抓取中...")
        execute_4_fetch_monthly_data(torchlight_cn_steam_id, torchlight_cn_steam_name)

        torchlight_global_steam_id = os.getenv('TORCHLIGHT_INFINITE_GLOBAL_STEAM_ID')
        torchlight_global_steam_name = os.getenv('TORCHLIGHT_INFINITE_GLOBAL_STEAM_NAME')
        execute_4_fetch_monthly_data(torchlight_global_steam_id, torchlight_global_steam_name)
        logger.info(f"SteamId={torchlight_global_steam_id},Game-{torchlight_global_steam_name}抓取中...")

        heartopia_global_steam_id = os.getenv('HEARTOPIA_GLOBAL_STEAM_ID')
        heartopia_global_steam_name = os.getenv('HEARTOPIA_GLOBAL_STEAM_NAME')
        execute_4_fetch_monthly_data(heartopia_global_steam_id, heartopia_global_steam_name)
        logger.info(f"SteamId={heartopia_global_steam_id},Game-{heartopia_global_steam_name}抓取中...")
        
        logger.info(f"定时任务[crawling_steam_xd_games_players_monthly_task]执行完毕!")
    except Exception as e:
        logger.error(f"定时任务[crawling_steam_xd_games_players_monthly_task]执行失败! {e}")

def crawling_steam_xd_games_recommendations_task():
    try:
        """每天12点执行一次的业务逻辑"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"定时任务[crawling_steam_xd_games_recommendations_task]执行中... 当前时间: {current_time}")

        torchlight_cn_steam_id = os.getenv('TORCHLIGHT_INFINITE_CN_STEAM_ID')
        torchlight_cn_steam_name = os.getenv('TORCHLIGHT_INFINITE_CN_STEAM_NAME')
        logger.info(f"SteamId={torchlight_cn_steam_id},Game-{torchlight_cn_steam_name}抓取中...")
        execute_4_fetch_daily_recommendations(torchlight_cn_steam_id, torchlight_cn_steam_name)
        execute_4_fetch_monthly_recommendations(torchlight_cn_steam_id, torchlight_cn_steam_name)

        torchlight_global_steam_id = os.getenv('TORCHLIGHT_INFINITE_GLOBAL_STEAM_ID')
        torchlight_global_steam_name = os.getenv('TORCHLIGHT_INFINITE_GLOBAL_STEAM_NAME')
        logger.info(f"SteamId={torchlight_global_steam_id},Game-{torchlight_global_steam_name}抓取中...")
        execute_4_fetch_daily_recommendations(torchlight_global_steam_id, torchlight_global_steam_name)
        execute_4_fetch_monthly_recommendations(torchlight_global_steam_id, torchlight_global_steam_name)

        heartopia_global_steam_id = os.getenv('HEARTOPIA_GLOBAL_STEAM_ID')
        heartopia_global_steam_name = os.getenv('HEARTOPIA_GLOBAL_STEAM_NAME')
        logger.info(f"SteamId={heartopia_global_steam_id},Game-{heartopia_global_steam_name}抓取中...")
        execute_4_fetch_daily_recommendations(heartopia_global_steam_id, heartopia_global_steam_name)
        execute_4_fetch_monthly_recommendations(heartopia_global_steam_id, heartopia_global_steam_name)
        
        logger.info(f"定时任务[crawling_steam_xd_games_recommendations_task]执行完毕!")
    except Exception as e:
        logger.error(f"定时任务[crawling_steam_xd_games_recommendations_task]执行失败! {e}")

# 2. 配置调度器（使用 MySQL 作为 job store）
#    替换下面的数据库连接信息
DB_URL = f"mysql+pymysql://{username}:{encoded_password}@{host}:{port}/{database}?charset=utf8mb4"

jobstores = {
    'default': SQLAlchemyJobStore(url=DB_URL)
}
executors = {
    'default': ThreadPoolExecutor(max_workers=10)
}
job_defaults = {
    'coalesce': True,      # 如果错过多次触发，是否合并为一次执行
    'max_instances': 4     # 同一作业最大并发实例数
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors,
                                job_defaults=job_defaults, timezone='Asia/Shanghai')

# 3. 添加任务：每1小时执行一次
#    注意：如果 job_id 相同且已存在于数据库中，APScheduler 会自动恢复（不会重复添加）
scheduler.add_job(
    crawling_steam_xd_games_top_rank_daily_task,
    trigger=CronTrigger(minute=5),     # 每1小时第5分钟
    id='crawling_steam_xd_games_top_rank_daily_task',               # 唯一标识符，用于持久化恢复
    replace_existing=True,              # 如果数据库中已有同名作业，替换其配置
    name='每小时 第5分钟 抓取心动旗下游戏实时热销榜情况'
)

scheduler.add_job(
    crawling_steam_xd_games_top_rank_weekly_task,
    trigger=CronTrigger(day_of_week='wed', hour=8, minute=30), # 每周3 8点30分
    id='crawling_steam_xd_games_top_rank_weekly_task',
    replace_existing=True,
    name='每周3 8点30 抓取心动旗下游戏周热销榜情况'
)

scheduler.add_job(
    crawling_steam_xd_games_players_daily_task,
    trigger=CronTrigger(minute=10),     # 每1小时第10分钟
    id='crawling_steam_xd_games_players_daily_task',
    replace_existing=True,
    name='每小时 第10分钟 抓取心动旗下游戏实时游玩人数数据'
)

scheduler.add_job(
    crawling_steam_xd_games_players_monthly_task,
    trigger=CronTrigger(hour=11, minute=30),     # 每月2号0点30分
    id='crawling_steam_xd_games_players_monthly_task',
    replace_existing=True,
    name='每天 11点30分 抓取心动旗下游戏月度游玩人数数据'
)

scheduler.add_job(
    crawling_steam_xd_games_recommendations_task,
    trigger=CronTrigger(hour=12, minute=30),     # 每天12点30分
    id='crawling_steam_xd_games_recommendations_task',
    replace_existing=True,
    name='每天12点30分 抓取心动旗下游戏玩家评价数'
)

# 4. 启动调度器
scheduler.start()
logger.info("调度器已启动，任务信息已持久化到MySQL")

# 5. 保持主线程运行（实际部署中可以用 while True + sleep 或 嵌入Web服务）
try:
    while True:
        # 调度器在后台运行，这里可以让主线程休眠或做其他事情
        import time
        time.sleep(60)
except KeyboardInterrupt:
    logger.info("收到终止信号，正在关闭调度器...")
    scheduler.shutdown()