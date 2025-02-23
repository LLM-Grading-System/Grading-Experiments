### Решение
```Python
import os
import json
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document


class JSONVectorStore:
    def __init__(self, embedding: Embeddings) -> None:
        self.embedding = embedding
        self.store = {}

    def delete(self, ids: list[str]) -> None:
        for id in ids:
            if id in self.store:
                del self.store[id]

    def add_documents(self, documents: list[Document], ids: list[str] = None) -> None:
        if ids is None:
            ids = [str(i) for i in range(len(documents))]

        for doc, id in zip(documents, ids):
            vector = self.embedding.embed_query(doc.text)
            self.store[id] = {
                "document": doc,
                "vector": vector
            }

    def get_by_ids(self, ids: list[str]) -> list[Document]:
        return [self.store[id]["document"] for id in ids if id in self.store]

    @classmethod
    def load(cls, path: str, embedding: Embeddings) -> "JSONVectorStore":
        if not os.path.exists(path):
            raise FileNotFoundError(f"The file {path} does not exist.")

        with open(path, 'r') as f:
            data = json.load(f)

        instance = cls(embedding)
        instance.store = data
        return instance

    def dump(self, path: str) -> None:
        with open(path, 'w') as f:
            json.dump(self.store, f, default=lambda o: o.__dict__, indent=4)
```
