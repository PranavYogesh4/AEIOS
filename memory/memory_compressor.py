#Compresses stored information to reduce memory usage while preserving useful details.
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


class MemoryCompressor:

    def compress_memory(self, memory_text):

        prompt = f"""
You are the Memory Compression Agent of AEIOS.

Your task is to compress the following memory while preserving all
important information.

Rules:
- Preserve important facts.
- Preserve technical details.
- Preserve conclusions.
- Remove repetition.
- Keep the summary concise.
- Maximum length: 200 words.

Memory:

{memory_text}
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