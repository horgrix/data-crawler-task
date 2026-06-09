# 项目描述
这是一个基于 Python 的网络爬虫程序，爬取Steam实时销榜单。

# 代码路径
steam/crawler/hotlist/topselling_steam_hotlist_crawler.py 继承 steam/crawler/hotlist/steam_hotlist_crawler.py 的 SteamHotlistCrawler 父类

# 实现方法
_get_url：https://store.steampowered.com/charts/topselling/{region}  region str
_parse_col3: 返回None
_parse_col4: 返回None
_parse_col5: 返回None
_parse_col6: 返回None