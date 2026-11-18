#Supports retrying operations when configured conditions or failures require it.
from utils.logger import logger


class RetryEngine:

    def __init__(self):

        self.max_retries = 2

    def should_retry(self, evaluation):

        score = 100

        for line in evaluation.splitlines():

            if "Overall Score:" in line:

                try:
                    score = int(
                        line.split(":")[1].strip()
                    )

                except:

                    score = 100

        logger.info(f"Evaluation Score : {score}")

        if score < 85:

            logger.info(
                "Retry Required"
            )

            return True

        logger.info(
            "Retry Not Required"
        )

        return False