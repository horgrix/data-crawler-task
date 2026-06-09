"""
心动游戏 Steam 评价数据获取任务
继承 XdBaseTask 基类。
"""

import sys
import os
from typing import Any, List, Tuple, Dict

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from task.xd.xd_base_task import XdBaseTask
from steam.crawler.recommendations.steam_recommendations_crawler import SteamRecommendationsCrawler
from data.xd.recommendations.xd_game_steam_commendations_dao import XdGameSteamCommendationsDao
from logger.xd_logger_cfg import logger


class XdGameSteamRecommendationsTask(XdBaseTask):
    """心动游戏 Steam 评价数据获取任务"""

    def __init__(self, steam_id: str):
        """
        Args:
            steam_id: 游戏的 Steam App ID，例如 "4025700"
        """
        super().__init__()
        self._steam_id = steam_id
        self.crawler = SteamRecommendationsCrawler()
        self.dao = XdGameSteamCommendationsDao()

    def _get_data(self) -> Dict[str, Any]:
        """
        使用 SteamRecommendationsCrawler 从 Steam 上获取评价数据。

        Returns:
            {
                'rollup': {'rollup_type': str, 'data': [...]},
                'recent': [...]
            }
        """
        logger.info(f"正在获取游戏 {self._steam_id} 的评价数据...")
        data = self.crawler.fetch_data(self._steam_id)
        logger.info(f"评价数据获取完成: rollup {len(data.get('rollup', {}).get('data', []))}条, "
                     f"recent {len(data.get('recent', []))}条")
        return data

    def _handle_data(self, records: Dict[str, Any]) -> List[Tuple[int, int, int, int, int]]:
        """
        处理和清洗评价数据，将 rollup 和 recent 数据合并转换。

        Args:
            records: 原始数据字典

        Returns:
            [(stat_ts, steam_id, up, down, all), ...] 列表
        """
        logger.info("开始处理和清洗评价数据...")
        result = []

        # 处理 rollup 数据
        rollup = records.get('rollup', {})
        for item in rollup.get('data', []):
            stat_ts = item.get('date', 0)
            up = item.get('recommendations_up', 0)
            down = item.get('recommendations_down', 0)
            all_count = up + down
            result.append((stat_ts * 1000, int(self._steam_id), 'rollup', up, down, all_count))

        # 处理 recent 数据
        for item in records.get('recent', []):
            stat_ts = item.get('date', 0)
            up = item.get('recommendations_up', 0)
            down = item.get('recommendations_down', 0)
            all_count = up + down
            result.append((stat_ts * 1000, int(self._steam_id), 'recent', up, down, all_count))

        logger.info(f"数据处理完成，共 {len(result)} 条记录")
        return result

    def _save_data(self, records: List[Tuple[int, int, int, int, int]]):
        """
        使用 XdGameSteamCommendationsDao 将数据保存到远程数据库中。

        Args:
            records: 处理后数据列表
        """
        if not records:
            logger.warning("无数据需要保存")
            return

        logger.info(f"正在将 {len(records)} 条评价数据存入数据库...")
        affected = self.dao.save_or_update(records)
        logger.info(f"成功存入 {affected} 条数据！")