## Описание
Необходимо реализовать класс JSONVectorStore для хранения векторов. Сигнатура методов класса представлена ниже.


```Python
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document


class JSONVectorStore:
    def __init__(self, path: str, embedding: Embeddings) -> None:
        ...
    
    def delete(self, ids: list[str]) -> None:
        ...
    
    def add_documents(self, documents: list[Document], ids: Optional[list[str]] = None):
        ...
    
    def get_by_ids(self, ids: list[str]) -> list[Document]:
        ...
    
    def get_all_documents(self) -> list[Document]:
       ...
    
    @classmethod
    def load(cls, path: str, embedding: Embeddings) -> "JSONVectorStore":
        ...
    
    def dump(self) -> None:
        ...
```


### Критерии
1. После операции, меняющей состояние, должно происходить автосохранение
2. Перед сохранением вектора должно происходить его приведение в тип list, если вектор имеет тип numpy.ndarray
3. Идентификаторы для документов формируются исключительно уникальные, например, с помощью uuid или с помощью random
4. При удалении несуществующего документа по id должно выбрасываться исключение
5. Проверить, что при использовании объекта Document вызываются только существующие атрибуты:
   - id: Optional[str] - атрибут, выступающий идентификатором документа
   - page_content: str - атрибут, возвращающий текст документа
   - metadata: dict[str, str] - атрибут, возвращающий словарь с метаданным
6. Проверить, что при использовании объекта Embeddings вызываются только существующие атрибуты и методы:
   - embed_documents: (texts: list[str]) -> list[list[float]] - метод, возвращающий векторные представления переданных текстов
   - embed_query: (text: str) -> list[float] - метод, возвращающий векторное представление по переданному тексту
6. Перед сохранением объекта типа Document он должен корректно приводится к словарю
7. В методе load должна происходить создание Document на основе соответствующего словаря
8. Убедись, что реализованы все требуемые методы
9. Проверить, что поле с данными у JSONVectorStore является приватным и доступ к данным осуществляется только через методы

