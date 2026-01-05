import os
import uuid
import pandas as pd
import chromadb

class Portfolio:
    def __init__(self, file_path: str | None = None):
        # ✅ Default to a relative path inside your repo
        # Example repo structure:
        #   app.py
        #   portfolio.py
        #   resources/my_portfolio.csv
        base_dir = os.path.dirname(os.path.abspath(__file__))
        default_path = os.path.join(base_dir, "resources", "my_portfolio.csv")
        self.file_path = file_path or default_path

        if not os.path.exists(self.file_path):
            raise FileNotFoundError(
                f"Portfolio CSV not found at: {self.file_path}. "
                f"Make sure it's committed to GitHub."
            )

        self.data = pd.read_csv(self.file_path)

        # ✅ Writable path on Streamlit Cloud
        persist_dir = "/tmp/vectorstore"
        os.makedirs(persist_dir, exist_ok=True)

        self.chroma_client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        # ✅ Only load once
        if self.collection.count() == 0:
            for _, row in self.data.iterrows():
                tech = str(row.get("Techstack", "")).strip()
                link = str(row.get("Links", "")).strip()
                if not tech:
                    continue

                self.collection.add(
                    documents=[tech],  # ✅ must be a list
                    metadatas=[{"links": link}],
                    ids=[str(uuid.uuid4())],
                )

    def query_links(self, skills: list[str] | str, n_results: int = 2):
        # Chroma expects list[str]
        if isinstance(skills, str):
            skills = [skills]

        res = self.collection.query(query_texts=skills, n_results=n_results)
        # returns something like: [[{"links": "..."} , ...]]
        return res.get("metadatas", [])
