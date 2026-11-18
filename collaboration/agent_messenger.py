#Enables communication and message sharing between agents and records agent interactions.
from utils.logger import logger


class AgentMessenger:

    def send_message(
        self,
        sender,
        receiver,
        message
    ):

        logger.info("=" * 60)
        logger.info("AGENT COMMUNICATION")
        logger.info(f"FROM     : {sender}")
        logger.info(f"TO       : {receiver}")
        logger.info(f"MESSAGE  : {message}")
        logger.info("=" * 60)