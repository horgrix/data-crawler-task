# 模块描述
这是一个基于python的Steam爬虫程序，它是一个基类

# 代码路径
steam/crawler/hotlist/steam_hotlist_crawler.py 日志配置使用logger/xd_logger_cfg.py 的 logger

# 页面加载处理
页面加载完毕后，若页面有button class=DialogButton _DialogLayout Primary Focusable 的按钮，说明榜单没有完全加载，则需要点击该按钮，然后等待榜单加载完毕。

# abstractmethod
_get_url : 子类提供的爬虫目标地址
_parse_col3: 解析第3列
_parse_col4: 解析第4列
_parse_col5: 解析第5列
_parse_col6: 解析第6列


# 解析排行榜
找到页面table class=_3arZn0BMPzyhcYNADe193m 的表格，该表格的内容就排行榜的内容。
表格总共有6列
返回数据：_parse_col1，_parse_col2，_parse_col3，_parse_col4，_parse_col5，_parse_col6

# 父类提供的解析方法
## 第1列 解析Steam ID
_parse_col1: 
表格第1列：a href属性值中获取steam_id, 例如 https://store.steampowered.com/app/4025700/，app/后面的数据4025700就是steam_id
## 第2列 解析rank
_parse_col2:
表格第2列：内容就是排名
