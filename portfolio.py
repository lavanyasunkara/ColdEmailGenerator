"""import pandas as pd
import os
import chromadb
import uuid

class Portfolio:
    def __init__(self,file_path="C:/Users/lavan/Documents/copy/app/resource/my_portfolio.csv"):
        self.file_path=file_path
        self.data= pd.read_csv(file_path)
        print(file_path)
        print(self.data.head())
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                print(row["Techstack"])
                self.collection.add(documents=row["Techstack"],
                               metadatas={"links": row["Links"]},
                               ids=[str(uuid.uuid4())]
                               )
    def query_links(self, skills):
        print(self.collection.query(query_texts=skills,n_results=2).get('metadatas',[]))
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
"""