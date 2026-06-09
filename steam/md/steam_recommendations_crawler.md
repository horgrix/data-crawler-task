# 模块描述
这是一个基于python的Steam爬虫程序，它是一个基类

# 代码路径
steam/crawler/recommendations/steam_recommendations_crawler.py 日志配置使用logger/xd_logger_cfg.py 的 logger

# 数据获取
https://store.steampowered.com/appreviewhistogram/{steam_id} steam_id是steam游戏id 例如4025700

# 数据解析
数据是josn数据例如：
{
    success: 1
    results:{
        rollups: 按rollup_type聚合的历史数据, [{"date": timestamp, "recommendations_up": int, "recommendations_down": int}, ...]
        rollup_type: rollup的类型 例如 week
        recent: 最近30天的每日数据, [{"date": timestamp, "recommendations_up": int, "recommendations_down": int}, ...] 
    }
}
返回数据：{
    'rollup'：{'rollup_type'：rollup_type，'data': rollups}
    'recent': recent
}

