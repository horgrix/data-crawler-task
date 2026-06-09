"""
Steam 游戏推荐评价爬虫
从 Steam 评价直方图 API 获取游戏的推荐/不推荐汇总数据。
"""

import requests
from typing import Dict, List, Any

from logger.xd_logger_cfg import logger


class SteamRecommendationsCrawler:
    """Steam 游戏推荐评价爬虫"""

    @staticmethod
    def _fetch_json(steam_id: str) -> Dict[str, Any]:
        """
        从 Steam 评价直方图 API 获取原始 JSON 数据。

        Args:
            steam_id: 游戏的 Steam App ID

        Returns:
            API 返回的原始 JSON 数据；失败返回空字典
        """
        url = f"https://store.steampowered.com/appreviewhistogram/{steam_id}"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()
            logger.info(f"成功获取游戏 {steam_id} 的推荐评价数据")
            return data
        except requests.RequestException as e:
            logger.error(f"请求 Steam 评价 API 失败, steam_id={steam_id}, error={e}")
            return {}
        except ValueError as e:
            logger.error(f"解析 Steam 评价 API JSON 失败, steam_id={steam_id}, error={e}")
            return {}

    @staticmethod
    def _parse_response(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析 API 响应，提取 rollup 和 recent 数据。

        Args:
            data: API 返回的原始 JSON 数据

        Returns:
            {
                'rollup': {'rollup_type': str, 'data': [...]},
                'recent': [...]
            }
        """
        if data.get("success") != 1:
            logger.warning(f"Steam API 返回失败, response={data}")
            return {"rollup": {}, "recent": []}

        results = data.get("results", {})
        rollups = results.get("rollups", [])
        rollup_type = results.get("rollup_type", "")
        recent = results.get("recent", [])

        return {
            "rollup": {
                "rollup_type": rollup_type,
                "data": rollups,
            },
            "recent": recent,
        }

    def fetch_data(self, steam_id: str) -> Dict[str, Any]:
        """
        获取并解析指定游戏的推荐评价数据。

        Args:
            steam_id: 游戏的 Steam App ID

        Returns:
            {
                'rollup': {'rollup_type': str, 'data': [{"date": timestamp, "recommendations_up": int, "recommendations_down": int}, ...]},
                'recent': [{"date": timestamp, "recommendations_up": int, "recommendations_down": int}, ...]
            }
        """
        data = self._fetch_json(steam_id)
        return self._parse_response(data)