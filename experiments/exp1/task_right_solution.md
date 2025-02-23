### Решение
```Python
import os
import json
import uuid
import numpy as np
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document


import json
import os
import uuid
from typing import Optional, List
import numpy as np
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document


class JSONVectorStore:
    def __init__(self, path: str, embedding: Embeddings) -> None:
        self.__path = path
        self.__embedding = embedding
        self.__data = {}

    def load_data(self) -> None:
        if os.path.exists(self.__path):
            with open(self.__path, 'r', encoding="utf-8") as f:
                self.__data = json.load(f)

    def save_data(self) -> None:
        with open(self.__path, 'w', encoding="utf-8") as f:
            json.dump(self.__data, f)

    def delete(self, ids: List[str]) -> None:
        for id in ids:
            if id not in self.__data:
                raise KeyError(f"Document with id {id} does not exist.")
            del self.__data[id]
        self.save_data()

    def add_documents(self, documents: List[Document], ids: Optional[List[str]] = None) -> None:
        for doc in documents:
            doc_id = ids.pop(0) if ids else str(uuid.uuid4())
            vector = self.__embedding.embed_documents([doc.page_content])[0]
            if isinstance(vector, np.ndarray):
                vector = vector.tolist()
            self.__data[doc_id] = {
                'id': doc_id,
                'page_content': doc.page_content,
                'metadata': doc.metadata,
                'vector': vector
            }
        self.save_data()

    def get_by_ids(self, ids: List[str]) -> List[Document]:
        documents = []
        for id in ids:
            if id in self.__data:
                doc_data = self.__data[id]
                documents.append(Document(
                    id=doc_data['id'],
                    page_content=doc_data['page_content'],
                    metadata=doc_data['metadata']
                ))
            else:
                raise KeyError(f"Document with id {id} does not exist.")
        return documents

    def get_all_documents(self) -> List[Document]:
        return [Document(
            id=doc_data['id'],
            page_content=doc_data['page_content'],
            metadata=doc_data['metadata']
        ) for doc_data in self.__data.values()]

    @classmethod
    def load(cls, path: str, embedding: Embeddings) -> "JSONVectorStore":
        vector_store = cls(path, embedding)
        vector_store.load_data()
        return vector_store

    def dump(self) -> None:
        self.save_data()
```
