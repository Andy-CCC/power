import os
from loguru import logger
from config.env_config import BASE_DIR, LOG_LEVEL

# 日志路径
LOG_PATH = os.path.join(BASE_DIR, "logs", "api_auto.log")
# 日志配置
logger.add(
    LOG_PATH,
    rotation="10 MB",       # 按10MB分割日志
    retention="7 days",     # 保留7天
    encoding="utf-8",
    level=LOG_LEVEL,
    enqueue=True            # 异步日志，不阻塞
)
log = logger