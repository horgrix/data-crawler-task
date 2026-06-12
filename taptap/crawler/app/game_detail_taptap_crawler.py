"""
TapTap 游戏详情爬虫
通过 TapTap WebAPI v2 获取指定游戏的厂商侧边栏列表数据，
包含游戏基础信息、统计数据、评分数据和投票分布。
"""

import sys
import os
import time
import json
from typing import Any, Dict, List, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import requests

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from logger.xd_logger_cfg import logger


class GameDetailTaptapCrawler:
    """TapTap 游戏详情爬虫，通过 sidebar/v1/list 接口获取游戏数据"""

    BASE_TAPTAP_URL = "https://www.taptap.cn/app/"

    # TapTap API 基础 URL（X-UA 参数为固定值）
    BASE_URL = (
        "https://www.taptap.cn/webapiv2/sidebar/v1/list"
        "?X-UA=V%3D1%26PN%3DWebApp%26LANG%3Dzh_CN%26VN_CODE%3D102"
        "%26LOC%3DCN%26PLT%3DPC%26DS%3DPC"
        "%26OS%3DWindows%26OSV%3D10%26DT%3DPC"
        "&type=app_detail&app_id="
    )

    # 请求超时时间（秒）
    REQUEST_TIMEOUT = 30

    # 请求头
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
    }

    def __init__(self, app_id: int):
        """
        Args:
            app_id: TapTap 游戏 ID，例如 45213
        """
        self._app_id = app_id
        self._url = self.BASE_URL + str(app_id)
        self._taptap_url = self.BASE_TAPTAP_URL + str(app_id)

    # ---------- WebDriver 管理 ----------
    def _init_driver(self) -> webdriver.Chrome:
        """初始化 Chrome 无头浏览器"""
        chrome_options = Options()
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.7827.55 Safari/537.36'
        )
        return webdriver.Chrome(options=chrome_options)

    def _quit_driver(self):
        """安全关闭 WebDriver"""
        if self._driver:
            try:
                self._driver.quit()
            except Exception:
                pass
            self._driver = None

    # ---------- 数据获取 ----------
    def _request_api(self) -> Optional[Dict[str, Any]]:
        """
        请求 TapTap API 并返回 JSON 响应。

        Returns:
            JSON 响应字典，失败返回 None
        """
        logger.info(f"正在请求 TapTap API，app_id={self._app_id}")
        try:
            resp = requests.get(self._url, headers=self.HEADERS, timeout=self.REQUEST_TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
            logger.info(f"API 请求成功，app_id={self._app_id}")
            return data
        except requests.RequestException as e:
            logger.error(f"API 请求失败，app_id={self._app_id}，错误: {e}")
            return None
        except ValueError as e:
            logger.error(f"JSON 解析失败，app_id={self._app_id}，错误: {e}")
            return None
        
    def _load_page(self, url: str, timeout: int = None) -> Optional[str]:
        """加载页面，等待表格出现后返回页面源码"""

        logger.info(f"正在加载页面: {self._taptap_url}")
        self._driver.get(self._taptap_url)
        try:
            time.sleep(5)
            logger.info("页面加载完成")

            js_code = f"""
            return fetch("{url}", {{
                method: "GET",
                headers: {{
                    "User-Agent": navigator.userAgent,
                    "Accept": "application/json, text/plain, */*",
                }}
            }})
            .then(response => response.json())
            .then(data => {{ return data; }})
            .catch(error => {{ return {{error: error.toString()}}; }});
            """
            result = self._driver.execute_script(js_code)
            return result
        except Exception as e:
            logger.error(f"页面加载失败: {e}")
            return None
        
    def _request_api_by_brower(self) -> Optional[Dict[str, Any]]:
        self._driver = self._init_driver()
        try:
            html = self._load_page(self._url)
            if not html:
                logger.warning("页面加载失败，返回空数据")
                return []

            return html
            # soup = BeautifulSoup(html, 'html.parser')
            # data = soup.find('html')
            # if data != None:
            #     logger.info(f"API 请求成功，app_id={self._app_id}")
            #     return json.loads(data.text)
        except Exception as e:
            logger.error(f"API 请求失败，app_id={self._app_id}，错误: {e}")
            logger.error(f"API 请求失败，app_id={self._app_id}，data: {data}")
            return None
        finally:
            self._quit_driver()

    # ---------- 数据解析 ----------
    def _parse_response(self, json_data: Dict[str, Any]) -> List[Tuple]:
        """
        解析 API 返回的 JSON 数据。

        解析流程：
        1. 检查 success 字段
        2. 取 data 数组第一个元素，验证 label == "厂商"
        3. 遍历该元素下 data.data 数组，提取各游戏字段

        Args:
            json_data: API 返回的完整 JSON

        Returns:
            [(app_id, title, hits_total, pc_download_count, review_count,
              fans_count, vote_1, vote_2, vote_3, vote_4, vote_5,
              score, latest_score, latest_review_count,
              latest_version_score, latest_version_review_count), ...]
        """
        if not json_data.get("success"):
            logger.warning(f"API 返回 success=false，app_id={self._app_id}")
            return []

        now_ts = json_data.get("now")
        logger.info(f"数据返回时间戳: {now_ts}")

        sidebar_list: List[Dict[str, Any]] = json_data.get("data", [])
        if not sidebar_list:
            logger.warning(f"sidebar data 数组为空，app_id={self._app_id}")
            return []

        # 取第一个元素，验证 label
        first_item = sidebar_list[0]
        label = first_item.get("label", "")
        # if label != "厂商":
        #     logger.warning(
        #         f'第一个元素 label 不是"厂商"，实际为: {label}，app_id={self._app_id}'
        #     )
        #     return []

        # 进入内部 data 对象
        inner_data: Dict[str, Any] = first_item.get("data", {})
        inner_data2: Dict[str, Any] = inner_data.get("data", {})
        game_list: List[Dict[str, Any]] = inner_data2.get("data", [])
        if not game_list:
            logger.warning(f"inner data.data 数组为空，app_id={self._app_id}")
            return []

        logger.info(f"共找到 {len(game_list)} 款游戏数据")
        result = []
        for game in game_list:
            row = self._parse_game_item(game)
            if row:
                result.append(row)

        logger.info(f"成功解析 {len(result)} 条游戏数据")
        return result

    def _parse_game_item(self, game: Dict[str, Any]) -> Optional[Tuple]:
        """
        解析单个游戏条目，提取所有需要的字段。

        Args:
            game: 游戏数据字典

        Returns:
            包含 16 个字段的元组，解析失败返回 None
        """
        try:
            app_id = game.get("id")
            title = game.get("title", "")

            stat: Dict[str, Any] = game.get("stat", {})
            hits_total = stat.get("hits_total_val", 0)
            pc_download_count = stat.get("pc_download_count", 0)
            review_count = stat.get("review_count", 0)
            fans_count = stat.get("fans_count", 0)

            # 投票分布
            vote_info: Dict[str, Any] = stat.get("vote_info", {})
            vote_1 = vote_info.get("1", 0)
            vote_2 = vote_info.get("2", 0)
            vote_3 = vote_info.get("3", 0)
            vote_4 = vote_info.get("4", 0)
            vote_5 = vote_info.get("5", 0)

            # 评分数据
            rating: Dict[str, Any] = stat.get("rating", {})
            score = rating.get("score", 0.0)
            latest_score = rating.get("latest_score", 0.0)
            latest_review_count = rating.get("latest_review_count", 0)
            latest_version_score = rating.get("latest_version_score", 0.0)
            latest_version_review_count = rating.get("latest_version_review_count", 0)

            return (
                app_id,
                title,
                hits_total,
                pc_download_count,
                review_count,
                fans_count,
                vote_1,
                vote_2,
                vote_3,
                vote_4,
                vote_5,
                score,
                latest_score,
                latest_review_count,
                latest_version_score,
                latest_version_review_count,
            )
        except Exception as e:
            logger.error(f"解析游戏条目失败: {e}")
            return None

    # ---------- 模板方法 ----------
    def fetch_data(self) -> List[Tuple]:
        """
        执行完整的数据获取和解析流程。

        Returns:
            解析后的游戏数据列表，每条记录包含 16 个字段
        """
        logger.info(f"========== 开始爬取 TapTap 游戏数据，app_id={self._app_id} ==========")

        json_data = self._request_api_by_brower()
        if json_data is None:
            logger.warning("API 请求失败，返回空数据")
            return []

        result = self._parse_response(json_data)
        logger.info(f"========== 爬取完成，共 {len(result)} 条记录 ==========")
        return result
    
print(GameDetailTaptapCrawler(172664).fetch_data())