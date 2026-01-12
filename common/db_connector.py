import pymysql
import sqlite3
from typing import List, Dict, Any, Optional
from config.config import config
from common.logger import logger


class DatabaseConnector:
    """数据库连接类"""

    def __init__(self, db_type: str = 'mysql', **kwargs):
        self.db_type = db_type
        self.connection = None
        self.connect(**kwargs)

    def connect(self, **kwargs):
        """连接数据库"""
        try:
            if self.db_type == 'mysql':
                db_config = config.DATABASE.copy()
                db_config.update(kwargs)
                self.connection = pymysql.connect(**db_config)
            elif self.db_type == 'sqlite':
                db_path = kwargs.get('db_path', ':memory:')
                self.connection = sqlite3.connect(db_path)

            logger.info(f"成功连接{self.db_type}数据库")
        except Exception as e:
            logger.error(f"数据库连接失败: {str(e)}")
            raise

    def execute_query(self, sql: str, params: tuple = None) -> List[Dict[str, Any]]:
        """执行查询语句"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params or ())
                result = cursor.fetchall()

                # 转换为字典列表
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in result]
        except Exception as e:
            logger.error(f"查询执行失败: {str(e)}")
            raise

    def execute_update(self, sql: str, params: tuple = None) -> int:
        """执行更新语句"""
        try:
            with self.connection.cursor() as cursor:
                affected_rows = cursor.execute(sql, params or ())
                self.connection.commit()
                return affected_rows
        except Exception as e:
            self.connection.rollback()
            logger.error(f"更新执行失败: {str(e)}")
            raise

    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            logger.info("数据库连接已关闭")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()