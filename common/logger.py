from loguru import logger
import sys
import os

# 日志目录
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "logs")
os.makedirs(log_dir, exist_ok=True)

# 配置日志输出
logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
)
logger.add(
    os.path.join(log_dir, "test_{time:YYYYMMDD_HHmmss}.log"),
    level="DEBUG",
    rotation="10 MB",
    encoding="utf-8",
)
