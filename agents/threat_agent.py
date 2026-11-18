#Identifies threats and analyzes potential risks.
from groq import Groq

from config import GROQ_API_KEY

from collaboration.agent_messenger import AgentMessenger
from collaboration.decision_engine import DecisionEngine

from utils.logger import logger

client = Groq(api_key=GROQ_API_KEY)


class ThreatAgent:

    def __init__(self):

        self.messenger = AgentMessenger()

        self.decision_engine = DecisionEngine()

    def analyze_threat(self, data):

        self.messenger.send_message(
            "Threat Agent",
            "Report Agent",
            "Threat analysis initiated."
        )

        logger.info("ThreatAgent: Starting threat analysis...")

        prompt = f"""
You are the AEIOS Threat Intelligence Agent.

Responsibilities:
- Analyze cybersecurity threats.
- Estimate severity.
- Identify attack vectors.
- Suggest mitigation strategies.
- Explain risks clearly.

Research Data:
{data}

Generate a detailed cybersecurity threat analysis report.
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

        response_content = completion.choices[0].message.content

        logger.info("ThreatAgent: Threat analysis completed successfully.")

        next_agent = self.decision_engine.decide_next_agent(
            "ThreatAgent",
            response_content
        )

        logger.info(f"ThreatAgent: Next Agent -> {next_agent}")

        return {
            "content": response_content,
            "next_agent": next_agent
}