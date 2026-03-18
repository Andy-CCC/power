import os
from loguru import logger
from config.env_config import BASE_DIR
#日志封装，无需改
# 日志保存路径
LOG_PATH = os.path.join(BASE_DIR, "logs", "api_auto.log")
# 日志配置：按10MB分割、保留7天、UTF-8编码
logger.add(
    LOG_PATH,
    rotation="10 MB",
    retention="7 days",
    encoding="utf-8",
    enqueue=True,
    level="INFO"
)
log = logger