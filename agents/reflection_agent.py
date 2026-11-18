#Reviews the output and reflects on possible improvements.
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


class ReflectionAgent:

    def improve_response(
        self,
        user_query,
        original_response,
        evaluation
    ):
        prompt = f"""
You are the Reflection Agent of AEIOS.

Improve the original response using the evaluation report.

Rules:
1. Do not invent facts or statistics.
2. Do not introduce unsupported information.
3. Improve clarity, structure, formatting, and readability.
4. Correct grammar and organization.
5. If information is missing, state that further research is needed.

Keep the response concise and preserve its technical meaning.

User Query:
{user_query}

Original Response:
{original_response}

Evaluation Report:
{evaluation}

Return only the improved response.
"""

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=700,
            temperature=0.2
        )

        return (
            completion.choices[0].message.content
            or original_response
        )

    # Compatibility method used by the Orchestrator
    def reflect(
        self,
        user_query,
        original_response,
        evaluation
    ):
        return self.improve_response(
            user_query,
            original_response,
            evaluation
        )
