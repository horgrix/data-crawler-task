"""
Steam 游戏玩家数据爬虫基类
从 SteamCharts JSON API 获取玩家峰值数据，按时间间隔自动分类为 hourly/daily/monthly。
"""

import requests
from typing import List, Tuple, Dict

from logger.xd_logger_cfg import logger


# 30天毫秒数：用于区分 hourly 与 daily
_HOURLY_THRESHOLD_MS = 2_592_000_000
# 90天毫秒数：用于区分 daily 与 monthly
_DAILY_THRESHOLD_MS = 7_776_000_000
# 1小时毫秒数：用于整小时取整
_HOUR_MS = 3_600_000


class SteamGamePlayersCrawler:
    """Steam 游戏玩家数据爬虫"""

    @staticmethod
    def _fetch_json(steam_id: str) -> List[List]:
        """
        从 SteamCharts API 获取原始 JSON 数据。

        Args:
            steam_id: 游戏的 Steam App ID

        Returns:
            原始数据列表，格式 [(timestamp_ms, peak_players), ...]
        """
        url = f"https://steamcharts.com/app/{steam_id}/chart-data.json"
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
            logger.info(f"成功获取游戏 {steam_id} 的玩家数据，共 {len(data)} 条原始记录")
            return data
        except Exception as e:
            logger.error(f"获取游戏 {steam_id} 数据失败: {e}")
            return []

    @staticmethod
    def _classify_and_format(raw_data: List[List]) -> Dict[str, List[Tuple[int, int]]]:
        """
        根据时间戳差距分类数据为 hourly / daily / monthly。

        Args:
            raw_data: 原始 JSON 数据

        Returns:
            {'hourly': [(时间戳, 峰值玩家数), ...],
             'daily': [(时间戳, 峰值玩家数), ...],
             'monthly': [(时间戳, 峰值玩家数), ...]}
        """
        result = {
            'hourly': [],
            'daily': [],
            'monthly': [],
        }

        if not raw_data:
            return result

        # 最后一条记录的时间戳作为基准
        last_entry = raw_data[-1]
        if not isinstance(last_entry, list) or len(last_entry) < 2:
            return result

        last_timestamp = last_entry[0]

        for entry in raw_data:
            if not isinstance(entry, list) or len(entry) < 2:
                continue

            timestamp_ms = entry[0]
            peak_players = entry[1]
            gap = last_timestamp - timestamp_ms

            if gap < _HOURLY_THRESHOLD_MS:
                # 小时级别：整数除法取整到整小时，避免时区影响
                rounded_ts = timestamp_ms // _HOUR_MS * _HOUR_MS
                result['hourly'].append((rounded_ts, peak_players))
            elif gap < _DAILY_THRESHOLD_MS:
                # 天级别
                result['daily'].append((timestamp_ms, peak_players))
            else:
                # 月级别
                result['monthly'].append((timestamp_ms, peak_players))

        logger.info(
            f"数据分类完成: hourly {len(result['hourly'])}条, "
            f"daily {len(result['daily'])}条, "
            f"monthly {len(result['monthly'])}条"
        )
        return result

    def fetch_data(self, steam_id: str) -> Dict[str, List[Tuple[int, int]]]:
        """
        获取并解析指定游戏的玩家峰值数据。

        Args:
            steam_id: 游戏的 Steam App ID

        Returns:
            {'hourly': [(时间戳(ms), 峰值玩家数), ...],
             'daily': [(时间戳(ms), 峰值玩家数), ...],
             'monthly': [(时间戳(ms), 峰值玩家数), ...]}
        """
        raw_data = self._fetch_json(steam_id)
        return self._classify_and_format(raw_data)