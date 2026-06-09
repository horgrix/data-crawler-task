# 模块描述
这是一个基于Python实现的代码块，负责实现心动游戏在steam上游玩人数获取

# 代码路径
task/xd/xd_game_steam_players_task.py 继承 task/xd/xd_base_task.py 的 XdBaseTask 类

# 子类实现
XdGameSteamPlayersTask - 处理全量数据
XdGameSteamPlayersIncrementTask - 最新的24条数据

# 模块依赖
steam/crawler/players/steam_gameplayers_crawler.py SteamGamePlayersCrawler
data/xd/players/xd_game_steam_players_dao.py XdGameSteamPlayersDao

# 抽象方法实现
_get_data(): 使用SteamGamePlayersCrawler从Steam上获取玩家人数
_save_data(records): 使用XdGameSteamPlayersDao将数据保存到远程数据库中

## XdGameSteamPlayersTask
_handle_data(records): 处理和清洗全部数据

## XdGameSteamPlayersIncrementTask
_handle_data(records): 只处理和清洗最新的24条数据, 如何判断最新的24条记录，hourly是最新的数据集合，取最后24条记录
