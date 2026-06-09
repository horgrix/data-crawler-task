"""
Steam 热榜爬虫基类
提供通用的 Selenium WebDriver 初始化、页面抓取与按列解析的模板方法。
子类需实现 _get_url、_parse_col3、_parse_col4、_parse_col5、_parse_col6。
"""

import re
from abc import ABC, abstractmethod
from typing import Optional, List, Any

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from logger.xd_logger_cfg import logger


class SteamHotlistCrawler(ABC):
    """Steam 热榜爬虫基类，封装 Selenium 无头浏览器操作与按列解析"""

    TABLE_CLASS = "_3arZn0BMPzyhcYNADe193m"
    SHOW_MORE_CSS = ".DialogButton._DialogLayout.Primary.Focusable"
    DEFAULT_WAIT_TIMEOUT = 30

    def __init__(self):
        self._driver: Optional[webdriver.Chrome] = None

    # ---------- 子类需实现的抽象方法 ----------
    @abstractmethod
    def _get_url(self) -> str:
        """子类提供的爬虫目标地址"""
        pass

    @abstractmethod
    def _parse_col3(self, cell) -> Any:
        """解析第3列"""
        pass

    @abstractmethod
    def _parse_col4(self, cell) -> Any:
        """解析第4列"""
        pass

    @abstractmethod
    def _parse_col5(self, cell) -> Any:
        """解析第5列"""
        pass

    @abstractmethod
    def _parse_col6(self, cell) -> Any:
        """解析第6列"""
        pass

    # ---------- 父类提供的解析方法 ----------
    def _parse_col1(self, cell) -> Optional[int]:
        """
        解析第1列：从 a href 中提取 steam_id。

        Args:
            cell: BeautifulSoup td 元素

        Returns:
            steam_id 整数，解析失败返回 None
        """
        a_tag = cell.find('a')
        if a_tag and a_tag.get('href'):
            match = re.search(r'/app/(\d+)', a_tag['href'])
            if match:
                return int(match.group(1))
        return None

    def _parse_col2(self, cell) -> Optional[int]:
        """
        解析第2列：排名。

        Args:
            cell: BeautifulSoup td 元素

        Returns:
            排名整数，解析失败返回 None
        """
        text = cell.get_text(strip=True)
        return int(text) if text.isdigit() else None

    # ---------- WebDriver 管理 ----------
    def _init_driver(self) -> webdriver.Chrome:
        """初始化 Chrome 无头浏览器"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
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

    # ---------- 页面加载 ----------
    def _wait_for_element(self, by: By, value: str, timeout: int = None):
        """等待页面上指定元素出现"""
        if timeout is None:
            timeout = self.DEFAULT_WAIT_TIMEOUT
        WebDriverWait(self._driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def _wait_for_element_clickable(self, by: By, value: str, timeout: int = None):
        """等待页面上指定元素可点击"""
        if timeout is None:
            timeout = self.DEFAULT_WAIT_TIMEOUT
        return WebDriverWait(self._driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )

    def _load_page(self, url: str, timeout: int = None) -> Optional[str]:
        """加载页面，等待表格出现后返回页面源码"""
        logger.info(f"正在加载页面: {url}")
        self._driver.get(url)
        try:
            self._wait_for_element(By.CLASS_NAME, self.TABLE_CLASS, timeout)
            logger.info("页面加载完成")
            return self._driver.page_source
        except Exception as e:
            logger.error(f"页面加载失败: {e}")
            return None

    def _click_show_more(self, timeout: int = None) -> bool:
        """点击"显示更多"按钮以展开完整榜单，并等待 Ajax 数据加载完成"""
        try:
            btn = self._wait_for_element_clickable(By.CSS_SELECTOR, self.SHOW_MORE_CSS, timeout)
            if timeout is None:
                timeout = self.DEFAULT_WAIT_TIMEOUT

            # 记录点击前的行数
            pre_rows = len(self._driver.find_elements(By.CSS_SELECTOR, f"table.{self.TABLE_CLASS} tbody tr"))
            btn.click()
            logger.info("已点击'显示更多'按钮，等待数据加载...")

            # 等待 tbody 中 tr 行数增多，说明 Ajax 已渲染新数据
            WebDriverWait(self._driver, timeout).until(
                lambda d: len(d.find_elements(By.CSS_SELECTOR, f"table.{self.TABLE_CLASS} tbody tr")) > pre_rows
            )
            logger.info("显示更多数据加载完成")
            return True
        except Exception as e:
            logger.warning(f"点击按钮或等待数据加载失败: {e}")
            return False

    # ---------- 模板方法 ----------
    def fetch_data(self) -> List[Any]:
        """
        模板方法：获取URL → 加载页面 → 反复点击"显示更多"直到加载全部数据 → 解析数据。

        Returns:
            解析后的数据列表，每条记录包含6列数据
        """
        url = self._get_url()
        self._driver = self._init_driver()
        try:
            html = self._load_page(url)
            if not html:
                logger.warning("页面加载失败，返回空数据")
                return []

            # 反复点击"显示更多"，直到按钮消失或数据不再增长（最多尝试10次防止死循环）
            for i in range(10):
                if not self._click_show_more():
                    logger.info("'显示更多'按钮已不可用，数据已全部加载")
                    break

            html = self._driver.page_source

            data = self._parse_table(html)
            logger.info(f"数据解析完成，共 {len(data)} 条记录")
            return data
        except Exception as e:
            logger.error(f"fetch_data 执行异常: {e}")
            return []
        finally:
            self._quit_driver()

    def _parse_table(self, html: str) -> List[Any]:
        """
        解析排行榜表格，逐行调用6个列解析方法。

        Args:
            html: 页面 HTML 源码

        Returns:
            数据列表，每条记录为 (_parse_col1~6 的返回值)
        """
        if not html:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', class_=self.TABLE_CLASS)
        if not table:
            logger.error("未找到目标表格")
            return []

        tbody = table.find('tbody')
        if not tbody:
            logger.error("表格中无 tbody")
            return []

        result = []
        for tr in tbody.find_all('tr'):
            cells = tr.find_all('td')
            if len(cells) < 6:
                continue

            col1 = self._parse_col1(cells[0])
            col2 = self._parse_col2(cells[1])
            col3 = self._parse_col3(cells[2])
            col4 = self._parse_col4(cells[3])
            col5 = self._parse_col5(cells[4])
            col6 = self._parse_col6(cells[5])

            if col1 is not None and col2 is not None:
                result.append((col1, col2, col3, col4, col5, col6))

        logger.info(f"成功解析 {len(result)} 条排行榜数据")
        return result