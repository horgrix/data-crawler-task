# 模块描述
这是一个基于Python数据操作程序，负责 xd_game_steam_commendations 的 CURD

# 模块依赖
数据库连接可以从db/xd_db_cfg.py中获取 

# 代码实现
data/xd/recommendations/xd_game_steam_commendations_dao.py 它继承 data/xd/xd_game_steam_dao.py 的 XdGameSteamDao

# MySQL表
xd_game_steam_commendations
字段如下：
stat_ts bigint 统计时间
steam_id int SteamID
type str 类型 recent|rollup
up int 推荐
down int 不推荐
all int 评价数
主键：steam_id，type，stat_ts

# 抽象代码实现
_get_create_sql: 返回建表语句
_get_saveorupdate_sql: 返回插入语句，要满足冲突则覆盖的需求