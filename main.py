from agents.orchestrator import OrchestratorAgent
from utils.logger import logger

logger.info("========================================")
logger.info("AEIOS Intelligent Multi-Agent System")
logger.info("System Started Successfully")
logger.info("Type 'exit' to quit.")
logger.info("========================================")

orchestrator = OrchestratorAgent()

while True:

    user_input = input("\nEnter Request: ")

    if user_input.lower() == "exit":
        logger.info("AEIOS Shutdown Complete.")
        break

    response = orchestrator.process_request(user_input)

    print("\nAEIOS Response:\n")
    print(response)