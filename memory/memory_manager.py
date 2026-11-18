#Coordinates memory operations, such as storing, retrieving, and managing memories.
import chromadb
from datetime import datetime

from utils.logger import logger


class MemoryManager:

    def __init__(self):
        self.client = chromadb.Client()

        self.collection = self.client.get_or_create_collection(
            name="aeios_memory"
        )

    def store_memory(self, user_input, response):
        memory_text = (
            f"USER:\n{user_input}\n\n"
            f"RESPONSE:\n{response}"
        )

        # Use a unique ID so repeated queries can also be stored.
        memory_id = datetime.now().strftime("%Y%m%d%H%M%S%f")

        self.collection.add(
            documents=[memory_text],
            ids=[memory_id],
            metadatas=[{
                "timestamp": datetime.now().isoformat(),
                "user_input": user_input
            }]
        )

        logger.info("MEMORY STORED SUCCESSFULLY")
        logger.info(f"Query: {user_input}")

    def retrieve_memory(self, query):
        logger.info("Searching memory...")

        results = self.collection.query(
            query_texts=[query],
            n_results=2
        )

        documents = results.get("documents", [])

        if documents and documents[0]:
            logger.info(
                f"Retrieved {len(documents[0])} relevant memory item(s)."
            )
        else:
            logger.info("No relevant memory found.")

        return documents

    def get_all_memories(self):
        """Return stored memories for the Memory Explorer."""
        results = self.collection.get(
            include=["documents", "metadatas"]
        )

        memories = []
        ids = results.get("ids", [])
        documents = results.get("documents") or []
        metadatas = results.get("metadatas") or []

        for index, memory_id in enumerate(ids):
            memories.append({
                "id": memory_id,
                "document": (
                    documents[index]
                    if index < len(documents)
                    else ""
                ),
                "metadata": (
                    metadatas[index]
                    if index < len(metadatas)
                    else {}
                )
            })

        # Show newest memories first when timestamps are available.
        memories.sort(
            key=lambda item: item["metadata"].get("timestamp", ""),
            reverse=True
        )

        return memories

    def search_memories(self, query, limit=10):
        """Find memories relevant to a search query."""
        query = query.strip()

        if not query:
            return self.get_all_memories()

        results = self.collection.query(
            query_texts=[query],
            n_results=min(max(limit, 1), 100)
        )

        ids = results.get("ids", [[]])[0]
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        return [
            {
                "id": memory_id,
                "document": documents[index] if index < len(documents) else "",
                "metadata": metadatas[index] if index < len(metadatas) else {}
            }
            for index, memory_id in enumerate(ids)
        ]

    def delete_memory(self, memory_id):
        """Delete one memory by its ID."""
        self.collection.delete(ids=[memory_id])
        logger.info(f"Deleted memory: {memory_id}")

    def clear_memories(self):
        """Delete all stored memories from the AEIOS collection."""
        results = self.collection.get(include=[])

        ids = results.get("ids", [])

        if ids:
            self.collection.delete(ids=ids)

        logger.info("All AEIOS memories cleared.")
