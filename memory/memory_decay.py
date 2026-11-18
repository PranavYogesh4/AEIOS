#Reduces the importance of older memories over time, according to the implemented rules.
import re


class MemoryDecay:

    def filter_memories(self, memories):

        if not memories:
            return []

        retained_memories = []

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

            # Keep memories with importance >= 5
            if importance >= 5:

                retained_memories.append(
                    memory
                )

        return retained_memories