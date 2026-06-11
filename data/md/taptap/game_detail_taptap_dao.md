# 模块描述
这是一个基于Python数据操作程序，负责 xd_game_steam_players 的 CURD

# 模块依赖
数据库连接可以从db/xd_db_cfg.py中获取 

# 代码实现
data/taptap/app/game_detail_taptap_dao.py 它继承 data/xd/xd_game_steam_dao.py 的 XdGameSteamDao

# MySQL表
game_detail_taptap
字段如下：
stat_ts bigint 统计时间
app_id bigint 游戏id,
title str 游戏名称,
hits_total bigint 下载数,
pc_download_count bigint pc下载数,
review_count bigint 评论数,
fans_count bigint 关注数,
vote_1 bigint 1分票数,
vote_2 bigint 2分票数,
vote_3 bigint 3分票数,
vote_4 bigint 4分票数,
vote_5 bigint 5分票数,
score str 游戏评分,
latest_score str 最近游戏评分,
latest_review_count bigint 最近评价数,
latest_version_score str 上个版本游戏评分,
latest_version_review_count bigint 上个版本评价数,
主键：app_id，stat_ts

# 抽象代码实现
_get_create_sql: 返回建表语句
_get_saveorupdate_sql: 返回插入语句，要满足冲突则覆盖的需求