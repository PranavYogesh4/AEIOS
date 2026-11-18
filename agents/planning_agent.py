#Creates a plan for processing the user's request.
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


class PlanningAgent:

    def create_plan(self, user_input):

        prompt = f"""
        You are the AEIOS Autonomous Planning Agent.

        Your responsibilities:
        - understand complex objectives
        - break tasks into subtasks
        - determine required agents
        - generate execution strategy

        Available Agents:
        1. Research Agent
        2. Threat Agent
        3. Report Agent

        User Request:
        {user_input}

        Generate:
        - objective
        - required agents
        - execution order
        - reasoning
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

        return completion.choices[0].message.content

