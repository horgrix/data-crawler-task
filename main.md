# 项目描述
这是一个基于Python实现的定时任务应用，定时任务框架使用apscheduler实现

# 代码路径
main.py

# 定时任务的数据表
存储到远程mysql中

# 配置项读取
STEAM_CRAWLER_XD_GAMES_REGIONS 爬取数据的地区代码
STEAM_CRAWLER_XD_GAMES_REGIONS_NAMES 爬取数据的地区的名称
STEAM_CRAWLER_XD_GAMES_IDS 心动游戏代码
STEAM_CRAWLER_XD_GAMES_NAMES 心动游戏名称
生成2个配置字典：
STEAM_CRAWLER_REGIONS = {STEAM_CRAWLER_XD_GAMES_REGIONS: STEAM_CRAWLER_XD_GAMES_REGIONS_NAMES}
XD_STEAM_GAMES = {STEAM_CRAWLER_XD_GAMES_IDS: STEAM_CRAWLER_XD_GAMES_NAMES}

# 时区
以UTC时间为准

# 任务描述
## XD Steam 实时热销榜
### 模块依赖
task/xd/xd_game_steam_list_task.py XdGameSteamRTHotListTask
### 定时配置
每个小时第2分钟执行一次

## XD Steam 实时热玩榜
### 模块依赖
task/xd/xd_game_steam_list_task.py XdGameSteamRTPlayersListTask
### 定时配置
每个小时第4分钟执行一次 

## XD Steam 周热销榜
### 模块依赖
task/xd/xd_game_steam_list_task.py XdGameSteamWeeklyHotListTask
### 定时配置
每周3 8点 执行一次
### 参数处理逻辑
date取值： 当前系统时间，utc时间，每周第一天为周1，若大于本周二则date取上周二，若小于本周二则date取上上周二

## XD Steam 增量峰值玩家
### 模块依赖
task/xd/xd_game_steam_players_task.py XdGameSteamPlayersIncrementTask
### 定时配置
每个小时第6分钟执行一次 

## XD Steam 全量峰值玩家
### 模块依赖
task/xd/xd_game_steam_players_task.py XdGameSteamPlayersTask
### 定时配置
每个月第3天 4点 执行一次 

## XD Steam 推荐数据
### 模块依赖
task/xd/xd_game_steam_recommendation_task.py XdGameSteamRecommendationsTask
### 定时配置
每天 2点 执行一次

## TapTap 游戏信息采集
### 模块依赖
task/taptap/taptap_game_info_task.py TapTapGameInfoTask
data/taptap/app/game_list_taptap_dao.py GameListTaptapDao
### 业务逻辑
从GameListTaptapDao查询出game列表,然后遍历游戏列表
从TapTapGameInfoTask抓取信息
### 定时配置
每小时第15分执行一次