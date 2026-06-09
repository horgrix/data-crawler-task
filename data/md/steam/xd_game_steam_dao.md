# 模块描述
这是一个基于Python数据操作程序，是一个基类

# 代码实现
data/xd/xd_game_steam_dao.py 

# 父类方法
ensure_table_exists：确保操作的表是否存在
save_or_update(records: List[tuple]) -> int：保存数据，若主键冲突就覆盖

# 抽象方法
_get_create_sql: 建表SQL
_get_saveorupdate_sql: 保存SQL