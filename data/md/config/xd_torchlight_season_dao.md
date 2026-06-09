# 模块描述
这是一个基于Python数据操作程序, 负责 xd_torchlight_season 的 CURD

# 代码实现
data/xd/config/xd_torchlight_season_dao.py 

# MySQL表
xd_torchlight_season
字段如下：
start_ts bigint 赛季开始时间
end_ts bigint 赛季结束时间
is_enable int 默认值为0，是否有效，1有效，0无效
ss int 第几赛季
steam_id int SteamID
主键：steam_id，ss, start_ts

# 方法
query_：确保操作的表是否存在
