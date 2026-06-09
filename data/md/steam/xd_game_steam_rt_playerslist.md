# 模块描述
这是一个基于Python数据操作程序，负责 xd_game_steam_rt_playerslist 的 CURD

# 代码实现
data/xd/hotlist/xd_game_steam_rt_playerslist_dao.py 它继承 data/xd/xd_game_steam_dao.py 的 XdGameSteamDao

# MySQL表
xd_game_steam_rt_playerslist
字段如下：
stat_ts bigint 统计时间
rank int 排名
steam_id int SteamID
cur_players int 当前玩家
last_24h_peak_players int 过去24小时峰值玩家数
主键：steam_id，stat_ts

# 抽象代码实现
_get_create_sql: 返回建表语句
_get_saveorupdate_sql: 返回插入语句，要满足冲突则覆盖的需求