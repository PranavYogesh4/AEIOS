#Retrieves relevant information from memory and past interactions.
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


class ReconstructionAgent:

    def reconstruct_memory(self, user_input, memory_context):

        prompt = f"""
        You are the AEIOS Memory Reconstruction Agent.

        Responsibilities:
        - analyze historical memories
        - reconstruct contextual understanding
        - identify relationships between memories
        - infer relevant context
        - generate continuity reasoning

        CURRENT USER REQUEST:
        {user_input}

        HISTORICAL MEMORY:
        {memory_context}

        Generate:
        - reconstructed context
        - relevant historical insights
        - inferred relationships
        - continuity analysis
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

