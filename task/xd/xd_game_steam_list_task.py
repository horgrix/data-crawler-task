"""
心动游戏 Steam 榜单数据任务
继承 XdBaseTask 基类，实现三个榜单任务子类。
"""

import sys
import os
from datetime import datetime, timezone, timedelta
from typing import Any, List, Tuple

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from task.xd.xd_base_task import XdBaseTask
from steam.crawler.hotlist.topselling_steam_hotlist_crawler import TopsellingSteamHotlistCrawler
from steam.crawler.hotlist.mostplayer_steam_hotlist_crawler import MostplayerSteamHotlistCrawler
from steam.crawler.hotlist.topsellers_steam_hotlist_crawler import TopsellersSteamHotlistCrawler
from data.xd.hotlist.xd_game_steam_rt_hotlist_dao import XdGameSteamRtHotlistDao
from data.xd.hotlist.xd_game_steam_rt_playerslist_dao import XdGameSteamRtPlayerslistDao
from data.xd.hotlist.xd_game_steam_weekly_hotlist_dao import XdGameSteamWeeklyHotlistDao
from logger.xd_logger_cfg import logger


# ============================================================
# XdGameSteamRTHotListTask - 实时热销榜
# ============================================================
class XdGameSteamRTHotListTask(XdBaseTask):
    """Steam 实时热销榜任务"""

    def __init__(self, region: str, steam_ids: List[int]):
        """
        Args:
            region: 地区代码，如 global, CN, JP 等
            steam_ids: 心动游戏 Steam ID 列表
        """
        super().__init__()
        self._region = region
        self._steam_ids = set(int(s) for s in steam_ids)

    def _get_data(self) -> Any:
        """使用 TopsellingSteamHotlistCrawler 获取实时热销榜数据"""
        logger.info(f"正在获取地区 {self._region} 的实时热销榜数据...")
        crawler = TopsellingSteamHotlistCrawler(self._region)
        data = crawler.fetch_data()
        logger.info(f"实时热销榜数据获取完成，共 {len(data)} 条记录")
        return data

    def _handle_data(self, records: Any) -> List[Tuple[int, int, int, str]]:
        """
        处理和清洗数据，只保留 steam_id 在 steam_ids 中的记录。

        Args:
            records: [(steam_id, rank, col3, col4, col5, col6), ...]

        Returns:
            [(stat_ts, rank, steam_id, region), ...]
        """
        logger.info("开始处理和清洗实时热销榜数据...")
        now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
        result = []
        for steam_id, rank, *_ in records:
            if steam_id in self._steam_ids:
                result.append((now_ms, rank, steam_id, self._region))
        logger.info(f"数据处理完成，共 {len(result)} 条记录（过滤后）")
        return result

    def _save_data(self, records: List[Tuple[int, int, int, str]]):
        """使用 XdGameSteamRtHotlistDao 保存到数据库"""
        if not records:
            logger.warning("无数据需要保存")
            return
        logger.info(f"正在将 {len(records)} 条实时热销榜数据存入数据库...")
        dao = XdGameSteamRtHotlistDao()
        affected = dao.save_or_update(records)
        logger.info(f"成功存入 {affected} 条数据！")


# ============================================================
# XdGameSteamRTPlayersListTask - 实时热玩榜
# ============================================================
class XdGameSteamRTPlayersListTask(XdBaseTask):
    """Steam 实时热玩榜任务"""

    def __init__(self, steam_ids: List[int]):
        """
        Args:
            steam_ids: 心动游戏 Steam ID 列表
        """
        super().__init__()
        self._steam_ids = set(int(s) for s in steam_ids)

    def _get_data(self) -> Any:
        """使用 MostplayerSteamHotlistCrawler 获取实时热玩榜数据"""
        logger.info("正在获取实时热玩榜数据...")
        crawler = MostplayerSteamHotlistCrawler()
        data = crawler.fetch_data()
        logger.info(f"实时热玩榜数据获取完成，共 {len(data)} 条记录")
        return data

    def _handle_data(self, records: Any) -> List[Tuple[int, int, int, int, int]]:
        """
        处理和清洗数据，只保留 steam_id 在 steam_ids 中的记录。

        Args:
            records: [(steam_id, rank, col3, col4, cur_players_text, peak_24h_text), ...]

        Returns:
            [(stat_ts, rank, steam_id, cur_players, last_24h_peak_players), ...]
        """
        logger.info("开始处理和清洗实时热玩榜数据...")
        now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
        result = []
        for row in records:
            steam_id = row[0]
            if steam_id not in self._steam_ids:
                continue

            rank = row[1]
            cur_players_text = row[4] if len(row) > 4 else 0
            peak_24h_text = row[5] if len(row) > 5 else 0

            # 清洗数值（去除逗号等）
            cur_players = int(str(cur_players_text).replace(',', '')) if cur_players_text else 0
            last_24h_peak_players = int(str(peak_24h_text).replace(',', '')) if peak_24h_text else 0

            result.append((now_ms, rank, steam_id, cur_players, last_24h_peak_players))

        logger.info(f"数据处理完成，共 {len(result)} 条记录（过滤后）")
        return result

    def _save_data(self, records: List[Tuple[int, int, int, int, int]]):
        """使用 XdGameSteamRtPlayerslistDao 保存到数据库"""
        if not records:
            logger.warning("无数据需要保存")
            return
        logger.info(f"正在将 {len(records)} 条实时热玩榜数据存入数据库...")
        dao = XdGameSteamRtPlayerslistDao()
        affected = dao.save_or_update(records)
        logger.info(f"成功存入 {affected} 条数据！")


# ============================================================
# XdGameSteamWeeklyHotListTask - 周热销榜
# ============================================================
class XdGameSteamWeeklyHotListTask(XdBaseTask):
    """Steam 周热销榜任务"""

    def __init__(self, region: str, date: str, steam_ids: List[int]):
        """
        Args:
            region: 地区代码，如 global, CN, JP 等
            date: 日期字符串，格式 yyyy-mm-dd，如 2026-05-05
            steam_ids: 心动游戏 Steam ID 列表
        """
        super().__init__()
        self._region = region
        self._date = date
        self._steam_ids = set(int(s) for s in steam_ids)

    def _get_data(self) -> Any:
        """使用 TopsellersSteamHotlistCrawler 获取周热销榜数据"""
        logger.info(f"正在获取地区 {self._region} 日期 {self._date} 的周热销榜数据...")
        crawler = TopsellersSteamHotlistCrawler(self._region, self._date)
        data = crawler.fetch_data()
        logger.info(f"周热销榜数据获取完成，共 {len(data)} 条记录")
        return data

    def _handle_data(self, records: Any) -> List[Tuple[int, int, int, int, str]]:
        """
        处理和清洗数据，只保留 steam_id 在 steam_ids 中的记录。

        Args:
            records: [(steam_id, rank, col3, col4, col5, col6), ...]

        Returns:
            [(start_ts, end_ts, rank, steam_id, region), ...]
        """
        logger.info("开始处理和清洗周热销榜数据...")
        # start_ts: date 的 UTC 时区下的时间戳(ms)
        date_obj = datetime.strptime(self._date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        start_ts = int(date_obj.timestamp() * 1000)
        # end_ts: date 下周二（Tuesday）的 UTC 时间戳(ms)
        days_until_next_tuesday = (1 - date_obj.weekday()) % 7
        if days_until_next_tuesday == 0:
            days_until_next_tuesday = 7
        next_tuesday = date_obj + timedelta(days=days_until_next_tuesday)
        next_tuesday = next_tuesday.replace(hour=0, minute=0, second=0, microsecond=0)
        end_ts = int(next_tuesday.timestamp() * 1000)

        result = []
        for steam_id, rank, *_ in records:
            if steam_id in self._steam_ids:
                result.append((start_ts, end_ts, rank, steam_id, self._region))

        logger.info(f"数据处理完成，共 {len(result)} 条记录（过滤后）")
        return result

    def _save_data(self, records: List[Tuple[int, int, int, int, str]]):
        """使用 XdGameSteamWeeklyHotlistDao 保存到数据库"""
        if not records:
            logger.warning("无数据需要保存")
            return
        logger.info(f"正在将 {len(records)} 条周热销榜数据存入数据库...")
        dao = XdGameSteamWeeklyHotlistDao()
        affected = dao.save_or_update(records)
        logger.info(f"成功存入 {affected} 条数据！")