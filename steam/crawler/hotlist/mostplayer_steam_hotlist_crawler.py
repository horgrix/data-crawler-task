"""
Steam 实时最多玩家榜爬虫（Hotlist 基类版）
继承 SteamHotlistCrawler 基类，实现最多玩家榜单的解析逻辑。
"""

from typing import Any

from steam.crawler.hotlist.steam_hotlist_crawler import SteamHotlistCrawler


class MostplayerSteamHotlistCrawler(SteamHotlistCrawler):
    """Steam 实时最多玩家榜爬虫"""

    def _get_url(self) -> str:
        return "https://store.steampowered.com/charts/mostplayed"

    def _parse_col3(self, cell) -> Any:
        return None

    def _parse_col4(self, cell) -> Any:
        return None

    def _parse_col5(self, cell) -> Any:
        """第5列：当前玩家数"""
        return cell.get_text(strip=True)

    def _parse_col6(self, cell) -> Any:
        """第6列：24小时内峰值玩家数"""
        return cell.get_text(strip=True)