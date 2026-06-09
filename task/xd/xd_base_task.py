"""
心动任务基类
定义任务执行的模板方法，子类需实现 _get_data、_handle_data、_save_data。
"""

import sys
import os
from abc import ABC, abstractmethod
from typing import Any

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from logger.xd_logger_cfg import logger


class XdBaseTask(ABC):
    """心动任务基类"""

    @abstractmethod
    def _get_data(self) -> Any:
        """获取指定数据，返回原始数据"""
        pass

    @abstractmethod
    def _handle_data(self, records: Any) -> Any:
        """处理和清洗数据，返回处理后的数据"""
        pass

    @abstractmethod
    def _save_data(self, records: Any):
        """保存数据到数据库"""
        pass

    def execute(self):
        """
        任务执行的模板方法：
        1. _get_data: 获取指定数据
        2. _handle_data: 处理和清洗数据
        3. _save_data: 保存数据
        """
        logger.info(f"========== 任务开始: {self.__class__.__name__} ==========")

        logger.info("步骤1：开始获取数据...")
        raw_data = self._get_data()
        logger.info("步骤1：数据获取完毕！")

        logger.info("步骤2：开始处理和清洗数据...")
        processed_data = self._handle_data(raw_data)
        logger.info("步骤2：数据处理完毕！")

        logger.info("步骤3：开始保存数据...")
        self._save_data(processed_data)
        logger.info("步骤3：数据保存完毕！")

        logger.info(f"========== 任务完成: {self.__class__.__name__} ==========")