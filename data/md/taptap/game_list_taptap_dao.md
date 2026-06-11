# 模块描述
这是一个基于Python数据操作程序，负责 xd_game_steam_players 的 CURD

# 模块依赖
数据库连接可以从db/xd_db_cfg.py中获取 

# 代码实现
data/taptap/app/game_list_taptap_dao.py 它继承 data/xd/xd_game_steam_dao.py 的 XdGameSteamDao

# MySQL表
game_list_taptap
字段如下：
app_id bigint 游戏id,
list_type str 榜单类型
title str 游戏名称
主键：list_type, app_id

# 抽象代码实现
_get_create_sql: 返回建表语句
_get_saveorupdate_sql: 返回插入语句，要满足冲突则覆盖的需求

# 查询方法
query_list(list_type): 查询最新的榜单列表