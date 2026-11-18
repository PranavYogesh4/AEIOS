#Identifies the user's intent so AEIOS can determine what kind of request it needs to handle.
from groq import Groq

from config import GROQ_API_KEY

from utils.logger import logger


client = Groq(api_key=GROQ_API_KEY)


class IntentClassifier:

    def classify(self, user_input):

        logger.info("Intent Classifier Activated")

        prompt = f"""
You are the Intent Classification Engine of the AEIOS AI System.

Your task is to classify the user's request into ONE of the following categories.

Categories:

1. GREETING
2. RESEARCH
3. THREAT_ANALYSIS
4. REPORT
5. GENERAL
6. MULTI_AGENT

Rules:

- Return ONLY one category.
- Do not explain.
- Do not generate any additional text.

User Request:
{user_input}
"""

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        intent = completion.choices[0].message.content.strip().upper()

        logger.info(f"Detected Intent : {intent}")

        return intent