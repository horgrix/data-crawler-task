"""
xd_game_steam_rt_hotlist 表的数据操作模块。
继承 XdGameSteamDao 基类。
"""

import sys
import os

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from data.xd.xd_game_steam_dao import XdGameSteamDao
from typing import List, Dict, Any, Optional


class XdGameSteamRtHotlistDao(XdGameSteamDao):
    """xd_game_steam_rt_hotlist 表 DAO"""

    # ========================
    # 建表 SQL
    # ========================
    CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS xd_game_steam_rt_hotlist (
        stat_ts     BIGINT      NOT NULL COMMENT '统计时间',
        `rank`      INT         NOT NULL COMMENT '排名',
        steam_id    INT         NOT NULL COMMENT 'SteamID',
        region      VARCHAR(50) NOT NULL COMMENT '区域',
        PRIMARY KEY (steam_id, region, stat_ts)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """

    # ========================
    # 插入 / 更新 SQL（主键冲突则覆盖）
    # ========================
    UPSERT_SQL = """
    INSERT INTO xd_game_steam_rt_hotlist
        (stat_ts, `rank`, steam_id, region)
    VALUES
        (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        `rank` = VALUES(`rank`)
    """

    # ========================
    # 查询 SQL
    # ========================
    QUERY_BY_STEAM_ID_SQL = """
    SELECT stat_ts, `rank`, steam_id, region
    FROM xd_game_steam_rt_hotlist
    WHERE steam_id = %s
    ORDER BY stat_ts DESC
    """

    QUERY_BY_STEAM_ID_REGION_SQL = """
    SELECT stat_ts, `rank`, steam_id, region
    FROM xd_game_steam_rt_hotlist
    WHERE steam_id = %s AND region = %s
    ORDER BY stat_ts DESC
    """

    QUERY_BY_STEAM_ID_REGION_RANGE_SQL = """
    SELECT stat_ts, `rank`, steam_id, region
    FROM xd_game_steam_rt_hotlist
    WHERE steam_id = %s AND region = %s AND stat_ts >= %s AND stat_ts <= %s
    ORDER BY stat_ts DESC
    """

    def _get_create_sql(self) -> str:
        return self.CREATE_TABLE_SQL

    def _get_saveorupdate_sql(self) -> str:
        return self.UPSERT_SQL

    # ---------- 查询方法 ----------
    def query_by_option(
        self,
        steam_id: int,
        region: Optional[str] = None,
        start: Optional[int] = None,
        end: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        根据 steam_id 查询数据，可选按 region 和时间范围过滤。

        Args:
            steam_id: SteamID（必传）
            region:   区域（可选）
            start:    开始时间戳，需与 end 同时传入（可选）
            end:      结束时间戳，需与 start 同时传入（可选）

        Returns:
            查询结果列表，每条为字典格式
        """
        if region is None:
            sql = self.QUERY_BY_STEAM_ID_SQL
            params = (steam_id,)
        elif start is None or end is None:
            sql = self.QUERY_BY_STEAM_ID_REGION_SQL
            params = (steam_id, region)
        else:
            sql = self.QUERY_BY_STEAM_ID_REGION_RANGE_SQL
            params = (steam_id, region, start, end)

        with self._conn.cursor() as cursor:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in rows]