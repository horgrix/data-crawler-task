# 模块描述
这是一个基于Python数据操作程序，负责 xd_game_steam_weekly_hotlist 的 CURD

# 代码实现
data/xd/hotlist/xd_game_steam_weekly_hotlist_dao.py 它继承 data/xd/xd_game_steam_dao.py 的 XdGameSteamDao


# MySQL表
xd_game_steam_weekly_hotlist
字段如下：
start_ts bigint 开始时间
end_ts bigint 结束时间
rank int 排名
steam_id int SteamID
region str 区域
主键：steam_id，region，start_ts，end_ts

# 抽象代码实现
_get_create_sql: 返回建表语句
_get_saveorupdate_sql: 返回插入语句，要满足冲突则覆盖的需求