"""
心动游戏 Steam 玩家数据获取任务
继承 XdBaseTask 基类，提供全量任务和增量任务两个子类。
"""

import sys
import os
from typing import Any, List, Tuple

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from task.xd.xd_base_task import XdBaseTask
from steam.crawler.players.steam_gameplayers_crawler import SteamGamePlayersCrawler
from data.xd.players.xd_game_steam_players_dao import XdGameSteamPlayersDao
from logger.xd_logger_cfg import logger


class _BaseGameSteamPlayersTask(XdBaseTask):
    """游戏玩家数据任务共享基类，提供 _get_data 和 _save_data 通用实现"""

    def __init__(self, steam_id: str):
        """
        Args:
            steam_id: 游戏的 Steam App ID，例如 "4025700"
        """
        super().__init__()
        self._steam_id = steam_id
        self.crawler = SteamGamePlayersCrawler()
        self.dao = XdGameSteamPlayersDao()

    def _get_data(self) -> Any:
        """
        使用 SteamGamePlayersCrawler 从 Steam 上获取玩家人数。

        Returns:
            {'hourly': [...], 'daily': [...], 'monthly': [...]}
        """
        logger.info(f"正在获取游戏 {self._steam_id} 的玩家数据...")
        data = self.crawler.fetch_data(self._steam_id)
        logger.info(f"数据获取完成: hourly {len(data.get('hourly', []))}条, "
                     f"daily {len(data.get('daily', []))}条, "
                     f"monthly {len(data.get('monthly', []))}条")
        return data

    def _save_data(self, records: List[Tuple[int, str, int, int]]):
        """
        使用 XdGameSteamPlayersDao 将数据保存到远程数据库中。

        Args:
            records: 处理后数据列表
        """
        if not records:
            logger.warning("无数据需要保存")
            return

        logger.info(f"正在将 {len(records)} 条玩家数据存入数据库...")
        affected = self.dao.save_or_update(records)
        logger.info(f"成功存入 {affected} 条数据！")


class XdGameSteamPlayersTask(_BaseGameSteamPlayersTask):
    """处理全量玩家数据"""

    def _handle_data(self, records: Any) -> List[Tuple[int, str, int, int]]:
        """
        处理和清洗全部数据。

        Args:
            records: 原始数据字典 {'hourly': [...], 'daily': [...], 'monthly': [...]}

        Returns:
            [(stat_ts, type, peak_players, steam_id), ...] 列表
        """
        logger.info("开始处理和清洗全部数据...")
        result = []
        for stat_type in ('hourly', 'daily', 'monthly'):
            for timestamp_ms, peak_players in records.get(stat_type, []):
                result.append((timestamp_ms, stat_type, peak_players, int(self._steam_id)))
        logger.info(f"数据处理完成，共 {len(result)} 条记录")
        return result


class XdGameSteamPlayersIncrementTask(_BaseGameSteamPlayersTask):
    """只处理最新的24条玩家数据"""

    def _handle_data(self, records: Any) -> List[Tuple[int, str, int, int]]:
        """
        只处理和清洗最新的24条数据。

        Args:
            records: 原始数据字典 {'hourly': [...], 'daily': [...], 'monthly': [...]}

        Returns:
            [(stat_ts, type, peak_players, steam_id), ...] 列表
        """
        logger.info("开始处理和清洗最新的24条数据...")
        result = []
        # hourly 是最新的数据集合，取最后24条记录
        items = records.get('hourly', [])
        latest_24 = items[-24:] if len(items) > 24 else items
        for timestamp_ms, peak_players in latest_24:
            result.append((timestamp_ms, 'hourly', peak_players, int(self._steam_id)))
        logger.info(f"数据处理完成，共 {len(result)} 条记录")
        return result
