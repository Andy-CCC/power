import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from config.config import config


class Logger:
    """日志管理类"""

    def __init__(self, name='api_test'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # 避免重复添加handler
        if not self.logger.handlers:
            self._setup_handlers()

    def _setup_handlers(self):
        """配置日志处理器"""

        # 创建日志目录
        config.LOG_DIR.mkdir(parents=True, exist_ok=True)

        # 控制台handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_format)

        # 文件handler
        file_handler = RotatingFileHandler(
            config.LOG_DIR / 'api_test.log',
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_format)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger

# 创建全局日志实例
logger = Logger().get_logger()