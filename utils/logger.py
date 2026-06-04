from loguru import logger

logger.remove()
logger.add("data/logs/agent.log" , level="INFO")