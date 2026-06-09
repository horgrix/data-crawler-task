# 模块描述
这是一个基于Python实现的代码块，负责实现心动游戏在steam上评价数据

# 代码路径
task/xd/xd_game_steam_recommendation_task.py 继承 task/xd/xd_base_task.py 的 XdBaseTask 类

# 子类实现
XdGameSteamRecommendationsTask

# 模块依赖
steam/crawler/recommendations/steam_recommendations_crawler.py SteamRecommendationsCrawler
data/xd/recommendations/xxd_game_steam_commendations_dao.py XdGameSteamCommendationsDao

# 抽象方法实现
_get_data(): 使用SteamRecommendationsCrawler上获取评价数据
_handle_data(records): 处理和清洗全部数据
_save_data(records): 使用XdGameSteamCommendationsDao将数据保存到远程数据库中
