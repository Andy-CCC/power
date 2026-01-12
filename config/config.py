import os
import yaml
from pathlib import Path


class Config:
    """配置文件管理类"""

    BASE_DIR = Path(__file__).parent.parent

    # 环境配置
    ENVIRONMENTS = {
        'dev': {
            'base_url': 'http://dev.api.example.com',
            'username': 'dev_user',
            'password': 'dev_pass'
        },
        'test': {
            'base_url': 'http://test.api.example.com',
            'username': 'test_user',
            'password': 'test_pass'
        },
        'prod': {
            'base_url': 'https://api.example.com',
            'username': 'prod_user',
            'password': 'prod_pass'
        }
    }

    # 当前环境（从环境变量获取或默认）
    CURRENT_ENV = os.getenv('API_TEST_ENV', 'test')

    # 当前环境配置
    @property
    def current_config(self):
        return self.ENVIRONMENTS.get(self.CURRENT_ENV, self.ENVIRONMENTS['test'])

    @property
    def BASE_URL(self):
        return self.current_config['base_url']

    # 路径配置
    TEST_DATA_DIR = BASE_DIR / 'test_data'
    REPORT_DIR = BASE_DIR / 'reports'
    LOG_DIR = REPORT_DIR / 'logs'

    # 请求配置
    TIMEOUT = 30
    MAX_RETRIES = 3

    # 数据库配置
    DATABASE = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'password',
        'database': 'test_db'
    }
config = Config()