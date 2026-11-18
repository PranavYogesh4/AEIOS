#Retrieves relevant context from stored memory for a new query.
class ContextRetriever:

    def retrieve_context(self, memories):

        if not memories:
            return []

        filtered_memories = []

        seen = set()

        for memory in memories:

            cleaned_memory = memory.strip()

            if cleaned_memory not in seen:

                seen.add(cleaned_memory)

                filtered_memories.append(
                    cleaned_memory
                )

        return filtered_memories