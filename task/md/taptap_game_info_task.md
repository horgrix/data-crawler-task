# 模块描述
这是一个基于Python实现的代码块，负责实现抓取taptap游戏信息

# 代码路径
task/taptap/taptap_game_info_task.py 继承 task/xd/xd_base_task.py 的 XdBaseTask 类

# 子类实现
TapTapGameInfoTask 

# 模块依赖
taptap/crawler/app/game_detail_taptap_crawler.py GameDetailTaptapCrawler
data/taptap/app/game_detail_taptap_dao.py GameDetailTaptapDao

# 抽象方法实现
_get_data(): 使用GameDetailTaptapCrawler从Tap上获取玩家人数
_handle_data(records): 处理和清洗全部数据
_save_data(records): 使用XdGameSteamPlayersDao将数据保存到远程数据库中
