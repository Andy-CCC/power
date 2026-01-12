import json
import random
import string
import hashlib
import datetime
from typing import Dict, Any, List
import yaml
import pandas as pd
from pathlib import Path


class Utils:
    """工具函数类"""

    @staticmethod
    def generate_random_string(length: int = 10) -> str:
        """生成随机字符串"""
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for _ in range(length))

    @staticmethod
    def generate_random_email() -> str:
        """生成随机邮箱"""
        return f"test_{Utils.generate_random_string(8)}@example.com"

    @staticmethod
    def generate_timestamp() -> str:
        """生成时间戳"""
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    @staticmethod
    def md5(text: str) -> str:
        """计算MD5值"""
        return hashlib.md5(text.encode()).hexdigest()

    @staticmethod
    def read_yaml(file_path: Path) -> Dict[str, Any]:
        """读取YAML文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    @staticmethod
    def write_yaml(data: Dict[str, Any], file_path: Path):
        """写入YAML文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True)

    @staticmethod
    def read_excel(file_path: Path, sheet_name: str = None) -> List[Dict[str, Any]]:
        """读取Excel文件"""
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            df = pd.read_excel(file_path)

        # 替换NaN为None
        df = df.where(pd.notnull(df), None)

        return df.to_dict('records')

    @staticmethod
    def extract_json(response_text: str, start_str: str, end_str: str) -> Dict[str, Any]:
        """从文本中提取JSON"""
        start = response_text.find(start_str)
        end = response_text.find(end_str, start)

        if start == -1 or end == -1:
            raise ValueError("未找到指定的JSON字符串")

        json_str = response_text[start + len(start_str):end]
        return json.loads(json_str)

    @staticmethod
    def wait_until(condition_func, timeout: int = 30, interval: int = 1) -> bool:
        """等待直到条件满足"""
        start_time = datetime.datetime.now()

        while (datetime.datetime.now() - start_time).seconds < timeout:
            if condition_func():
                return True
            time.sleep(interval)

        return False