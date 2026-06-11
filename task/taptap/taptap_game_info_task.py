"""
TapTap 游戏信息抓取任务
继承 XdBaseTask 基类，通过 GameDetailTaptapCrawler 获取数据，
由 GameDetailTaptapDao 保存到 xd_game_steam_players 表。
"""

import sys
import os
from datetime import datetime, timezone
from typing import Any, List, Tuple

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from task.xd.xd_base_task import XdBaseTask
from taptap.crawler.app.game_detail_taptap_crawler import GameDetailTaptapCrawler
from data.taptap.app.game_detail_taptap_dao import GameDetailTaptapDao
from logger.xd_logger_cfg import logger


class TapTapGameInfoTask(XdBaseTask):
    """TapTap 游戏信息抓取任务"""

    def __init__(self, app_id: int):
        """
        Args:
            app_id: TapTap 游戏 ID，例如 45213
        """
        super().__init__()
        self._app_id = app_id

    def _get_data(self) -> Any:
        """
        使用 GameDetailTaptapCrawler 从 TapTap 获取游戏详情数据。

        Returns:
            [(app_id, title, hits_total, pc_download_count, review_count,
              fans_count, vote_1, vote_2, vote_3, vote_4, vote_5,
              score, latest_score, latest_review_count,
              latest_version_score, latest_version_review_count), ...]
        """
        logger.info(f"正在获取 TapTap 游戏数据，app_id={self._app_id}")
        crawler = GameDetailTaptapCrawler(self._app_id)
        data = crawler.fetch_data()
        logger.info(f"数据获取完成，共 {len(data)} 条记录")
        return data

    def _handle_data(self, records: Any) -> List[Tuple]:
        """
        处理和清洗数据，为每条记录添加统计时间戳。

        Args:
            records: 爬虫返回的原始数据列表，每条包含 16 个字段

        Returns:
            处理后的数据列表，每条包含 17 个字段：
            [(stat_ts, app_id, title, hits_total, pc_download_count,
              review_count, fans_count,
              vote_1, vote_2, vote_3, vote_4, vote_5,
              score, latest_score, latest_review_count,
              latest_version_score, latest_version_review_count), ...]
        """
        logger.info("开始处理和清洗 TapTap 游戏数据...")
        now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
        result = []
        for row in records:
            # row 结构: (app_id, title, hits_total, pc_download_count, review_count,
            #              fans_count, vote_1, vote_2, vote_3, vote_4, vote_5,
            #              score, latest_score, latest_review_count,
            #              latest_version_score, latest_version_review_count)
            # 在前面插入 stat_ts
            result.append((now_ms,) + tuple(row))
        logger.info(f"数据处理完成，共 {len(result)} 条记录")
        return result

    def _save_data(self, records: List[Tuple]):
        """
        使用 GameDetailTaptapDao 将数据保存到远程数据库。

        Args:
            records: 处理后数据列表
        """
        if not records:
            logger.warning("无数据需要保存")
            return
        logger.info(f"正在将 {len(records)} 条 TapTap 游戏数据存入数据库...")
        dao = GameDetailTaptapDao()
        affected = dao.save_or_update(records)
        logger.info(f"成功存入 {affected} 条数据！")

TapTapGameInfoTask(45213).execute()