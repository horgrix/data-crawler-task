# 模块描述
这是一个基于Python实现的代码块，负责实现心动游戏steam榜单数据

# 代码路径
task/xd/xd_game_steam_list_task.py 继承 task/xd/xd_base_task.py 的 XdBaseTask 类

# 子类实现
XdGameSteamRTHotListTask - 实时热销榜
XdGameSteamRTPlayersListTask - 实时热玩榜
XdGameSteamWeeklyHotListTask - 周热销榜

# 构造函数
XdGameSteamRTHotListTask(region: str, steam_ids: list)
XdGameSteamRTPlayersListTask(steam_ids: list)
XdGameSteamWeeklyHotListTask(region: str, date: str, steam_ids: list)

# XdGameSteamRTHotListTask
## 模块依赖
steam/crawler/hotlist/topselling_steam_hotlist_crawler.py TopsellingSteamHotlistCrawler
data/xd/hotlist/xd_game_steam_rt_hotlist_dao.py XdGameSteamRtHotlistDao
## 抽象方法实现
_get_data(): 使用TopsellingSteamHotlistCrawler从Steam上获取实时排行
_handle_data(records): 判断是否是xd的游戏，判断逻辑为stea_id在steam_ids中,处理和清洗全部数据
_save_data(records): 使用XdGameSteamRtHotlistDao将数据保存到远程数据库中


# XdGameSteamRTPlayersListTask
## 模块依赖
steam/crawler/hotlist/mostplayer_steam_hotlist_crawler.py MostplayerSteamHotlistCrawler
data/xd/hotlist/xd_game_steam_rt_playerslist_dao.py XdGameSteamRtPlayerslistDao
## 抽象方法实现
_get_data(): 使用MostplayerSteamHotlistCrawler从Steam上获取实时排行
_handle_data(records): 判断是否是xd的游戏，判断逻辑为stea_id在steam_ids中,处理和清洗全部数据
_save_data(records): 使用XdGameSteamRtPlayerslistDao将数据保存到远程数据库中


# XdGameSteamWeeklyHotListTask
## 模块依赖
steam/crawler/hotlist/topsellers_steam_hotlist_crawler.py TopsellersSteamHotlistCrawler
data/xd/hotlist/xd_game_steam_weekly_hotlist_dao.py XdGameSteamWeeklyHotlistDao
## 抽象方法实现
_get_data(): 使用TopsellersSteamHotlistCrawler从Steam上获取周排行
_handle_data(records): 判断是否是xd的游戏，判断逻辑为stea_id在steam_ids中,start_ts, end_ts获取逻辑 start_ts = date的utc时区下的时间戳， end_ts=date下周二的utc时间戳
_save_data(records): 使用XdGameSteamWeeklyHotlistDao将数据保存到远程数据库中