#Ranks retrieved memories by relevance or another configured scoring method.
import re


class MemoryRanker:

    def rank_memories(self, memories):

        ranked_memories = []

        if not memories:
            return []

        for memory in memories:

            try:

                match = re.search(
                    r"IMPORTANCE:\s*(\d+)",
                    memory
                )

                if match:
                    importance = int(match.group(1))
                else:
                    importance = 5

            except:

                importance = 5

            ranked_memories.append(
                (
                    importance,
                    memory
                )
            )

        ranked_memories.sort(
            reverse=True,
            key=lambda x: x[0]
        )

        return [
            memory
            for _, memory in ranked_memories
        ]