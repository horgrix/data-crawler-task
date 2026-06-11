# 项目描述
这是一个基于 Python 的网络爬虫程序，爬取TapTap平台游戏数据。

# 代码路径
taptap/crawler/app/game_detail_taptap_crawler.py 日志配置使用logger/xd_logger_cfg.py 的 logger

# 数据获取
https://www.taptap.cn/webapiv2/sidebar/v1/list?X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D102%26LOC%3DCN%26PLT%3DPC%26DS%3DPC%26UID%3D3984d25f-315d-4e3e-8f7c-df617ec49dc5%26OS%3DWindows%26OSV%3D10%26DT%3DPC&type=app_detail&app_id={appid} appid是taptap游戏id 例如45213

# 数据解析
数据是josn数据例如：
{
    "data":[...]，
    "now": 1781153875，
    "success": true
}
success = true 代表查询成功
now 是数据返回时间戳
data是一个数组，面元素的格式如下：
{
    "label": 字符串，
    "web_url": 字符串，
    data:{...}
}
你需要的是取出第一个元素，并检查其label是否等于"厂商"
data{}的数据格式：
{
    data: [...],
    developer:{...}
}
你需要遍历data数组，里面每一个元素需要关注的属性：
{
    id: 45213,
    title: 心动小镇,
    stat: {...}
}
stat的数据结构中需要关注的属性：
{
    hits_total：57265218，
    pc_download_count：297647，
    topic_count：308893，
    video_count：221，
    official_topic_count：762，
    official_video_count：8，
    review_count：219968，
    fans_count：37939494，
    wish_count：4386，
    vote_info：{
        1：19068，
        2：7453，
        3：20423，
        4：39248，
        5：131111
    }，
    rating：{
        score：8.7，
        max：10，
        latest_score：8.0，
        latest_version_score：7.9，
        latest_review_count：2685，
        latest_version_review_count：7025
    }

}
最后数据返回的格式：
id，title，hits_total， pc_download_count，review_count，fans_count， vote_info.1，vote_info.2，vote_info.3，vote_info.4，vote_info.5，rating.score, rating.latest_score, rating.latest_review_count, rating.latest_version_score, rating.latest_version_review_count