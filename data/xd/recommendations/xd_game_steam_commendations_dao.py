"""
xd_game_steam_commendations 表的数据操作模块。
继承 XdGameSteamDao 基类。
"""

import sys
import os

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from data.xd.xd_game_steam_dao import XdGameSteamDao


class XdGameSteamCommendationsDao(XdGameSteamDao):
    """xd_game_steam_commendations 表 DAO"""

    # ========================
    # 建表 SQL
    # ========================
    CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS xd_game_steam_commendations (
        stat_ts  BIGINT      NOT NULL COMMENT '统计时间',
        steam_id INT         NOT NULL COMMENT 'SteamID',
        `type`   VARCHAR(10) NOT NULL COMMENT '类型 recent|rollup',
        `up`     INT         NOT NULL COMMENT '推荐',
        `down`   INT         NOT NULL COMMENT '不推荐',
        `all`    INT         NOT NULL COMMENT '评价数',
        PRIMARY KEY (steam_id, `type`, stat_ts)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """

    # ========================
    # 插入 / 更新 SQL（主键冲突则覆盖）
    # ========================
    UPSERT_SQL = """
    INSERT INTO xd_game_steam_commendations
        (stat_ts, steam_id, `type`, `up`, `down`, `all`)
    VALUES
        (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        `up`   = VALUES(`up`),
        `down` = VALUES(`down`),
        `all`  = VALUES(`all`)
    """

    def _get_create_sql(self) -> str:
        return self.CREATE_TABLE_SQL

    def _get_saveorupdate_sql(self) -> str:
        return self.UPSERT_SQL