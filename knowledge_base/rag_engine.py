#AI agents retrieve relevant information from stored documents or memory and use that information when generating responses.
import os
from pypdf import PdfReader
import chromadb


class RAGEngine:

    def __init__(self):

        self.client = chromadb.Client()

        self.collection = self.client.get_or_create_collection(
            name="aeios_knowledge"
        )

    def ingest_documents(self):

        folder_path = "knowledge_base/documents"

        document_id = 0

        for filename in os.listdir(folder_path):

            if filename.endswith(".pdf"):

                pdf_path = os.path.join(folder_path, filename)

                reader = PdfReader(pdf_path)

                text = ""

                for page in reader.pages:
                    text += page.extract_text()

                chunks = self.chunk_text(text)

                for chunk in chunks:

                    self.collection.add(
                        documents=[chunk],
                        ids=[str(document_id)]
                    )

                    document_id += 1

        print("\n[AEIOS] Document ingestion completed.\n")

    def chunk_text(self, text, chunk_size=500):

        chunks = []

        for i in range(0, len(text), chunk_size):

            chunks.append(text[i:i + chunk_size])

        return chunks

    def retrieve_knowledge(self, query):

        results = self.collection.query(
            query_texts=[query],
            n_results=3
        )

        return results["documents"]

