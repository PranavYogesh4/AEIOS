#Scores memories by importance to help decide which information is worth retaining.
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


class MemoryImportanceScorer:

    def score_memory(self, user_query, response):

        prompt = f"""
You are an AI Memory Evaluation Agent.

Your job is to evaluate how important this interaction is
for long-term memory.

Consider:

- technical depth
- planning value
- future usefulness
- decision making
- learning value

Return ONLY one integer between 1 and 10.

User Query:
{user_query}

Response:
{response}
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

        score = completion.choices[0].message.content.strip()

        try:
            score = int(score)
        except:
            score = 5

        score = max(1, min(score, 10))

        return score