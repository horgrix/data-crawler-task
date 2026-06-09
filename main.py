"""
定时任务主入口
使用 APScheduler 实现定时调度，任务持久化到 MySQL。
时区以 UTC 时间为准。
"""

import os
import time
from datetime import datetime, timezone, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from urllib.parse import quote_plus

# 添加项目根目录到 sys.path
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from task.xd.xd_game_steam_list_task import (
    XdGameSteamRTHotListTask,
    XdGameSteamRTPlayersListTask,
    XdGameSteamWeeklyHotListTask,
)
from task.xd.xd_game_steam_players_task import (
    XdGameSteamPlayersTask,
    XdGameSteamPlayersIncrementTask,
)
from task.xd.xd_game_steam_recommendation_task import (
    XdGameSteamRecommendationsTask,
)
from logger.xd_logger_cfg import logger

load_dotenv()

# ============================================================
# 配置项读取 & 解析
# ============================================================

_regions_keys = os.getenv("STEAM_CRAWLER_XD_GAMES_REGIONS", "").split(",")
_regions_names = os.getenv("STEAM_CRAWLER_XD_GAMES_REGIONS_NAMES", "").split(",")
STEAM_CRAWLER_REGIONS = dict(zip(
    [k.strip() for k in _regions_keys if k.strip()],
    [n.strip() for n in _regions_names if n.strip()],
))

_games_ids = os.getenv("STEAM_CRAWLER_XD_GAMES_IDS", "").split(",")
_games_names = os.getenv("STEAM_CRAWLER_XD_GAMES_NAMES", "").split(",")
XD_STEAM_GAMES = dict(zip(
    [g.strip() for g in _games_ids if g.strip()],
    [n.strip() for n in _games_names if n.strip()],
))


# ============================================================
# 任务函数定义
# ============================================================

# ---- XD Steam 实时热销榜 ----
def crawling_xd_steam_rt_hot_list():
    """每个小时第2分钟执行一次"""
    try:
        logger.info("定时任务[实时热销榜]执行中...")
        for region_code in STEAM_CRAWLER_REGIONS:
            region_name = STEAM_CRAWLER_REGIONS[region_code]
            logger.info(f"正在抓取地区 {region_code}({region_name}) 的实时热销榜...")
            XdGameSteamRTHotListTask(region_code, list(XD_STEAM_GAMES.keys())).execute()
        logger.info("定时任务[实时热销榜]执行完毕!")
    except Exception as e:
        logger.error(f"定时任务[实时热销榜]执行失败! {e}")


# ---- XD Steam 实时热玩榜 ----
def crawling_xd_steam_rt_players_list():
    """每个小时第4分钟执行一次"""
    try:
        logger.info("定时任务[实时热玩榜]执行中...")
        XdGameSteamRTPlayersListTask(list(XD_STEAM_GAMES.keys())).execute()
        logger.info("定时任务[实时热玩榜]执行完毕!")
    except Exception as e:
        logger.error(f"定时任务[实时热玩榜]执行失败! {e}")


# ---- XD Steam 周热销榜 ----
def _get_weekly_date() -> str:
    """
    计算周热销榜的 date 参数。
    UTC 时间，每周第一天为周一。
    若当前时间大于本周二，则 date 取上周二（yyyy-mm-dd）。
    若小于等于本周二，则 date 取上上周二。
    """
    now = datetime.now(timezone.utc)
    today = now.date()
    # 本周二（weekday=1）
    this_tuesday = today - timedelta(days=today.weekday() - 1)

    if today > this_tuesday:
        target = this_tuesday - timedelta(weeks=1)
    else:
        target = this_tuesday - timedelta(weeks=2)

    return target.strftime("%Y-%m-%d")


def crawling_xd_steam_weekly_hot_list():
    """每周3 8点 执行一次"""
    try:
        date = _get_weekly_date()
        logger.info(f"定时任务[周热销榜]执行中... date={date}")
        for region_code in STEAM_CRAWLER_REGIONS:
            region_name = STEAM_CRAWLER_REGIONS[region_code]
            logger.info(f"正在抓取地区 {region_code}({region_name}) 的周热销榜...")
            XdGameSteamWeeklyHotListTask(region_code, date, list(XD_STEAM_GAMES.keys())).execute()
        logger.info("定时任务[周热销榜]执行完毕!")
    except Exception as e:
        logger.error(f"定时任务[周热销榜]执行失败! {e}")


# ---- XD Steam 增量峰值玩家 ----
def crawling_xd_steam_players_increment():
    """每个小时第6分钟执行一次"""
    try:
        logger.info("定时任务[玩家数据增量]执行中...")
        for steam_id in XD_STEAM_GAMES:
            game_name = XD_STEAM_GAMES[steam_id]
            logger.info(f"正在抓取游戏 {steam_id}({game_name}) 的玩家数据(增量)...")
            XdGameSteamPlayersIncrementTask(steam_id).execute()
        logger.info("定时任务[玩家数据增量]执行完毕!")
    except Exception as e:
        logger.error(f"定时任务[玩家数据增量]执行失败! {e}")


# ---- XD Steam 全量峰值玩家 ----
def crawling_xd_steam_players_full():
    """每个月第3天 4点 执行一次"""
    try:
        logger.info("定时任务[玩家数据全量]执行中...")
        for steam_id in XD_STEAM_GAMES:
            game_name = XD_STEAM_GAMES[steam_id]
            logger.info(f"正在抓取游戏 {steam_id}({game_name}) 的玩家数据(全量)...")
            XdGameSteamPlayersTask(steam_id).execute()
        logger.info("定时任务[玩家数据全量]执行完毕!")
    except Exception as e:
        logger.error(f"定时任务[玩家数据全量]执行失败! {e}")


# ---- XD Steam 推荐数据 ----
def crawling_xd_steam_recommendations():
    """每天 2点 执行一次"""
    try:
        logger.info("定时任务[评价数据]执行中...")
        for steam_id in XD_STEAM_GAMES:
            game_name = XD_STEAM_GAMES[steam_id]
            logger.info(f"正在抓取游戏 {steam_id}({game_name}) 的评价数据...")
            XdGameSteamRecommendationsTask(steam_id).execute()
        logger.info("定时任务[评价数据]执行完毕!")
    except Exception as e:
        logger.error(f"定时任务[评价数据]执行失败! {e}")


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

# ---- 注册定时任务 ----
# 实时热销榜：每小时第2分钟
scheduler.add_job(
    crawling_xd_steam_rt_hot_list,
    trigger=CronTrigger(minute=2),
    id='xd_steam_rt_hot_list',
    replace_existing=True,
    name='每小时第2分钟 抓取Steam实时热销榜',
)

# 实时热玩榜：每小时第4分钟
scheduler.add_job(
    crawling_xd_steam_rt_players_list,
    trigger=CronTrigger(minute=4),
    id='xd_steam_rt_players_list',
    replace_existing=True,
    name='每小时第4分钟 抓取Steam实时热玩榜',
)

# 周热销榜：每周3 8点
scheduler.add_job(
    crawling_xd_steam_weekly_hot_list,
    trigger=CronTrigger(day_of_week='wed', hour=8, minute=0),
    id='xd_steam_weekly_hot_list',
    replace_existing=True,
    name='每周3 8点 抓取Steam周热销榜',
)

# 玩家数据增量：每小时第6分钟
scheduler.add_job(
    crawling_xd_steam_players_increment,
    trigger=CronTrigger(minute=6),
    id='xd_steam_players_increment',
    replace_existing=True,
    name='每小时第6分钟 抓取Steam玩家数据(增量)',
)

# 玩家数据全量：每个月第3天 4点
scheduler.add_job(
    crawling_xd_steam_players_full,
    trigger=CronTrigger(day=3, hour=4, minute=0),
    id='xd_steam_players_full',
    replace_existing=True,
    name='每月第3天4点 抓取Steam玩家数据(全量)',
)

# 评价数据：每天 2点
scheduler.add_job(
    crawling_xd_steam_recommendations,
    trigger=CronTrigger(hour=2, minute=0),
    id='xd_steam_recommendations',
    replace_existing=True,
    name='每天2点 抓取Steam评价数据',
)

# ============================================================
# 启动
# ============================================================
scheduler.start()
logger.info("调度器已启动 (时区: UTC)，任务信息已持久化到 MySQL")

try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    logger.info("收到终止信号，正在关闭调度器...")
    scheduler.shutdown()

#crawling_xd_steam_players_full()
#crawling_xd_steam_weekly_hot_list()
#crawling_xd_steam_rt_hot_list()
# crawling_xd_steam_rt_players_list()
#crawling_xd_steam_recommendations()