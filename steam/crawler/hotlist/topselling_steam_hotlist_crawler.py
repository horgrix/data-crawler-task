"""
Steam 实时热销榜爬虫（Hotlist 基类版）
继承 SteamHotlistCrawler 基类，实现实时热销榜单的解析逻辑。
"""

from typing import Any

from steam.crawler.hotlist.steam_hotlist_crawler import SteamHotlistCrawler


class TopsellingSteamHotlistCrawler(SteamHotlistCrawler):
    """Steam 实时热销榜爬虫"""

    def __init__(self, region: str):
        """
        Args:
            region: 地区代码，如 global, CN, JP 等
        """
        super().__init__()
        self._region = region

    def _get_url(self) -> str:
        return f"https://store.steampowered.com/charts/topselling/{self._region}"
    
    def _is_need_showmore(self) -> int:
        return 0

    def _parse_col3(self, cell) -> Any:
        return None

    def _parse_col4(self, cell) -> Any:
        return None

    def _parse_col5(self, cell) -> Any:
        return None

    def _parse_col6(self, cell) -> Any:
        return None