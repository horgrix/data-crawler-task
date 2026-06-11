"""
xd_game_steam_players 表的数据操作模块。
继承 data/xd/xd_game_steam_dao.py 的 XdGameSteamDao 基类。
"""

import sys
import os

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from data.xd.xd_game_steam_dao import XdGameSteamDao


class GameDetailTaptapDao(XdGameSteamDao):
    """game_detail_taptap 表 DAO"""

    # ========================
    # 建表 SQL
    # ========================
    CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS game_detail_taptap (
        stat_ts                     BIGINT      NOT NULL COMMENT '统计时间',
        app_id                      BIGINT      NOT NULL COMMENT '游戏ID',
        title                       VARCHAR(255) DEFAULT ''  COMMENT '游戏名称',
        hits_total                  BIGINT      DEFAULT 0    COMMENT '下载数',
        pc_download_count           BIGINT      DEFAULT 0    COMMENT 'PC下载数',
        review_count                BIGINT      DEFAULT 0    COMMENT '评论数',
        fans_count                  BIGINT      DEFAULT 0    COMMENT '关注数',
        vote_1                      BIGINT      DEFAULT 0    COMMENT '1分票数',
        vote_2                      BIGINT      DEFAULT 0    COMMENT '2分票数',
        vote_3                      BIGINT      DEFAULT 0    COMMENT '3分票数',
        vote_4                      BIGINT      DEFAULT 0    COMMENT '4分票数',
        vote_5                      BIGINT      DEFAULT 0    COMMENT '5分票数',
        score                       VARCHAR(50) DEFAULT ''   COMMENT '游戏评分',
        latest_score                VARCHAR(50) DEFAULT ''   COMMENT '最近游戏评分',
        latest_review_count         BIGINT      DEFAULT 0    COMMENT '最近评价数',
        latest_version_score        VARCHAR(50) DEFAULT ''   COMMENT '上个版本游戏评分',
        latest_version_review_count BIGINT      DEFAULT 0    COMMENT '上个版本评价数',
        PRIMARY KEY (app_id, stat_ts)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """

    # ========================
    # 插入 / 更新 SQL（主键冲突则覆盖）
    # ========================
    UPSERT_SQL = """
    INSERT INTO game_detail_taptap
        (stat_ts, app_id, title, hits_total, pc_download_count,
         review_count, fans_count,
         vote_1, vote_2, vote_3, vote_4, vote_5,
         score, latest_score, latest_review_count,
         latest_version_score, latest_version_review_count)
    VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        title                       = VALUES(title),
        hits_total                  = VALUES(hits_total),
        pc_download_count           = VALUES(pc_download_count),
        review_count                = VALUES(review_count),
        fans_count                  = VALUES(fans_count),
        vote_1                      = VALUES(vote_1),
        vote_2                      = VALUES(vote_2),
        vote_3                      = VALUES(vote_3),
        vote_4                      = VALUES(vote_4),
        vote_5                      = VALUES(vote_5),
        score                       = VALUES(score),
        latest_score                = VALUES(latest_score),
        latest_review_count         = VALUES(latest_review_count),
        latest_version_score        = VALUES(latest_version_score),
        latest_version_review_count = VALUES(latest_version_review_count)
    """

    def _get_create_sql(self) -> str:
        return self.CREATE_TABLE_SQL

    def _get_saveorupdate_sql(self) -> str:
        return self.UPSERT_SQL