#Evaluates the quality of the generated response.
import time

from groq import Groq, RateLimitError
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


class SelfEvaluationAgent:

    def evaluate(self, user_query, response):

        # Limit input size to reduce token consumption.
        query_text = str(user_query)[:2000]
        response_text = str(response)[:8000]

        prompt = f"""
You are the Self Evaluation Agent of AEIOS.

Critically evaluate the generated response.

Evaluate:
1. Accuracy
2. Completeness
3. Technical Correctness
4. Clarity
5. Structure

Be concise. Return ONLY this format:

Overall Score: <0-100>

Strengths:
- ...

Weaknesses:
- ...

Missing Information:
- ...

Recommendation:
KEEP
or
IMPROVE

User Query:
{query_text}

Generated Response:
{response_text}
"""

        for attempt in range(3):
            try:
                completion = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    max_tokens=500,
                    temperature=0.2
                )

                result = completion.choices[0].message.content
                return result or (
                    "Overall Score: 0\n\n"
                    "Strengths:\n- Evaluation returned no content.\n\n"
                    "Weaknesses:\n- Unable to evaluate the response.\n\n"
                    "Missing Information:\n- Evaluation unavailable.\n\n"
                    "Recommendation:\nIMPROVE"
                )

            except RateLimitError:
                if attempt < 2:
                    wait_seconds = 15 * (attempt + 1)
                    time.sleep(wait_seconds)
                else:
                    # Allow orchestration to continue if evaluation
                    # remains unavailable after retries.
                    return (
                        "Overall Score: 0\n\n"
                        "Strengths:\n- Evaluation service temporarily unavailable.\n\n"
                        "Weaknesses:\n- Response could not be evaluated.\n\n"
                        "Missing Information:\n- Self-evaluation pending retry.\n\n"
                        "Recommendation:\nIMPROVE"
                    )
