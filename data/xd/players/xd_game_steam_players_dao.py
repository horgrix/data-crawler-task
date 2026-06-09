"""
xd_game_steam_players 表的数据操作模块。
继承 XdGameSteamDao 基类。
"""

import sys
import os

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from data.xd.xd_game_steam_dao import XdGameSteamDao


class XdGameSteamPlayersDao(XdGameSteamDao):
    """xd_game_steam_players 表 DAO"""

    # ========================
    # 建表 SQL
    # ========================
    CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS xd_game_steam_players (
        stat_ts      BIGINT      NOT NULL COMMENT '统计时间',
        `type`       VARCHAR(20) NOT NULL COMMENT '时间类型',
        peak_players INT         NOT NULL COMMENT '峰值玩家',
        steam_id     INT         NOT NULL COMMENT 'SteamID',
        PRIMARY KEY (steam_id, `type`, stat_ts)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """

    # ========================
    # 插入 / 更新 SQL（主键冲突则覆盖）
    # ========================
    UPSERT_SQL = """
    INSERT INTO xd_game_steam_players
        (stat_ts, `type`, peak_players, steam_id)
    VALUES
        (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        peak_players = VALUES(peak_players)
    """

    def _get_create_sql(self) -> str:
        return self.CREATE_TABLE_SQL

    def _get_saveorupdate_sql(self) -> str:
        return self.UPSERT_SQL