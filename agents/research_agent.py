#Researches the topic and gathers relevant information.
from groq import Groq

from config import GROQ_API_KEY

from tools.web_search import WebSearchTool
from knowledge_base.rag_engine import RAGEngine

from collaboration.agent_messenger import AgentMessenger
from collaboration.decision_engine import DecisionEngine

from utils.logger import logger

client = Groq(api_key=GROQ_API_KEY)


class ResearchAgent:

    def __init__(self):

        self.web_tool = WebSearchTool()

        self.rag_engine = RAGEngine()

        self.messenger = AgentMessenger()

        self.decision_engine = DecisionEngine()

    def research_topic(self, topic):

        self.messenger.send_message(
            "Research Agent",
            "Threat Agent",
            "Research phase initiated."
        )

        logger.info("ResearchAgent: Using Web Intelligence Tool...")

        web_results = self.web_tool.search(topic)

        logger.info("ResearchAgent: Retrieving Knowledge Base Context...")

        knowledge_context = self.rag_engine.retrieve_knowledge(
            topic
        )

        prompt = f"""
You are the AEIOS Research Agent.

Responsibilities:
- Perform detailed research.
- Summarize findings.
- Provide technical insights.
- Use both the live web and the internal knowledge base.

LIVE WEB DATA:
{web_results}

KNOWLEDGE BASE CONTEXT:
{knowledge_context}

User Query:
{topic}

Generate a detailed research report.
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

        logger.info("ResearchAgent: Research completed successfully.")

        next_agent = self.decision_engine.decide_next_agent(
            "ResearchAgent",
            response_content
        )

        logger.info(f"ResearchAgent: Next Agent -> {next_agent}")

        return {
            "content": response_content,
            "next_agent": next_agent
        }