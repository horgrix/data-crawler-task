"""
game_list_taptap 表的数据操作模块。
继承 data/xd/xd_game_steam_dao.py 的 XdGameSteamDao 基类。
"""

import sys
import os
from typing import Any, Dict, List

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from data.xd.xd_game_steam_dao import XdGameSteamDao
from db.xd_db_cfg import get_db


class GameListTaptapDao(XdGameSteamDao):
    """game_list_taptap 表 DAO"""

    # ========================
    # 建表 SQL
    # ========================
    CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS game_list_taptap (
        app_id      BIGINT      NOT NULL COMMENT '游戏ID',
        list_type   VARCHAR(50) NOT NULL COMMENT '榜单类型',
        title       VARCHAR(255) DEFAULT '' COMMENT '游戏名称',
        PRIMARY KEY (list_type, app_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """

    # ========================
    # 插入 / 更新 SQL（主键冲突则覆盖）
    # ========================
    UPSERT_SQL = """
    INSERT INTO game_list_taptap
        (app_id, list_type, title)
    VALUES
        (%s, %s, %s)
    ON DUPLICATE KEY UPDATE
        title = VALUES(title)
    """

    # ========================
    # 查询 SQL
    # ========================
    QUERY_LIST_SQL = """
    SELECT app_id, list_type, title
    FROM game_list_taptap
    WHERE list_type = %s
    """

    def _get_create_sql(self) -> str:
        return self.CREATE_TABLE_SQL

    def _get_saveorupdate_sql(self) -> str:
        return self.UPSERT_SQL

    # ---------- 查询方法 ----------
    def query_list(self, list_type: str) -> List[Dict[str, Any]]:
        """
        根据榜单类型查询最新的游戏列表。

        Args:
            list_type: 榜单类型

        Returns:
            查询结果列表，每条为字典格式
        """
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(self.QUERY_LIST_SQL, (list_type,))
                rows = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                return [dict(zip(columns, row)) for row in rows]