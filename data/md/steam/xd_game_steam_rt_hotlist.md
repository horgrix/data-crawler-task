# 模块描述
这是一个基于Python数据操作程序，负责 xd_game_steam_rt_hotlist 的 CURD

# 代码实现
data/xd/hotlist/xd_game_steam_rt_hotlist_dao.py 它继承 data/xd/xd_game_steam_dao.py 的 XdGameSteamDao

# MySQL表
xd_game_steam_rt_hotlist
字段如下：
stat_ts bigint 统计时间
rank int 排名
steam_id int SteamID
region str 区域
主键：steam_id，region，stat_ts

# 抽象代码实现
_get_create_sql: 返回建表语句
_get_saveorupdate_sql: 返回插入语句，要满足冲突则覆盖的需求