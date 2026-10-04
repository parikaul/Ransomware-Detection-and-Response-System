from pathlib import Path
from loguru import logger

def setup_logging(log_dir="logs"):
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    logger.remove()
    logger.add(Path(log_dir)/"system.log", rotation="1 MB")
    logger.add(Path(log_dir)/"events.log", rotation="1 MB")
    logger.add(Path(log_dir)/"alerts.log", rotation="1 MB")
    logger.add(Path(log_dir)/"errors.log", rotation="1 MB", level="ERROR")
    logger.add(Path(log_dir)/"audit.log", rotation="1 MB")
    return logger
