"""
Steam 周热销榜爬虫（Hotlist 基类版）
继承 SteamHotlistCrawler 基类，实现周热销榜单的解析逻辑。
"""

from typing import Any

from steam.crawler.hotlist.steam_hotlist_crawler import SteamHotlistCrawler


class TopsellersSteamHotlistCrawler(SteamHotlistCrawler):
    """Steam 周热销榜爬虫"""

    def __init__(self, region: str, date: str):
        """
        Args:
            region: 地区代码，如 global, CN, JP 等
            date: 日期字符串，格式 yyyy-mm-dd，如 2026-05-05
        """
        super().__init__()
        self._region = region
        self._date = date

    def _get_url(self) -> str:
        return f"https://store.steampowered.com/charts/topsellers/{self._region}/{self._date}"

    def _parse_col3(self, cell) -> Any:
        return None

    def _parse_col4(self, cell) -> Any:
        return None

    def _parse_col5(self, cell) -> Any:
        return None

    def _parse_col6(self, cell) -> Any:
        return None