"""
Steam 数据表的 DAO 基类。
子类需实现 _get_create_sql 和 _get_saveorupdate_sql 两个抽象方法。
数据库连接依赖 db/xd_db_cfg.py。
"""

import sys
import os
from abc import ABC, abstractmethod
from typing import List

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.xd_db_cfg import get_db


class XdGameSteamDao(ABC):
    """Steam 数据 DAO 基类"""

    # ---------- 子类需实现的抽象方法 ----------
    @abstractmethod
    def _get_create_sql(self) -> str:
        """返回建表 SQL"""
        pass

    @abstractmethod
    def _get_saveorupdate_sql(self) -> str:
        """返回保存（主键冲突时覆盖）SQL"""
        pass

    # ---------- 父类提供的通用方法 ----------
    def ensure_table_exists(self):
        """确保操作的表存在，不存在则创建。"""
        with get_db() as conn:  # 直接获取连接
            with conn.cursor() as cursor:
                cursor.execute(self._get_create_sql())
                conn.commit()

    def save_or_update(self, records: List[tuple]) -> int:
        """
        批量插入或更新数据。主键冲突时覆盖。

        Args:
            records: 记录列表，每条记录为 tuple

        Returns:
            受影响的行数
        """
        if not records:
            return 0

        self.ensure_table_exists()
        with get_db() as conn:  # 直接获取连接
            try:
                with conn.cursor() as cursor:
                    affected = cursor.executemany(self._get_saveorupdate_sql(), records)
                    conn.commit()
                    return affected
            except Exception:
                conn.rollback()
                raise