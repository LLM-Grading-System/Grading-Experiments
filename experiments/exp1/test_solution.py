import random

import pytest
import os
import tempfile
from langchain_core.embeddings import FakeEmbeddings
from langchain_core.documents import Document
from experiments.exp1.solution import JSONVectorStore


@pytest.fixture(scope="function")
def vector_store():
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    embedding = FakeEmbeddings(size=100)
    vector_store = JSONVectorStore(temp_file.name, embedding)
    yield vector_store
    temp_file.close()
    os.remove(temp_file.name)


def test_add_documents(vector_store):
    doc1 = Document(id=None, page_content="Test document 1", metadata={"author": "Author 1"})
    doc2 = Document(id=None, page_content="Test document 2", metadata={"author": "Author 2"})

    vector_store.add_documents([doc1, doc2])

    documents = vector_store.get_all_documents()
    assert len(documents) == 2
    assert documents[0].id != documents[1].id


def test_get_by_ids(vector_store):
    doc1_content = "Test document 1"
    doc1_metadata = {"author": "Author 1"}
    doc1 = Document(id=None, page_content=doc1_content, metadata=doc1_metadata)
    doc1_id = hex(random.randint(1, 100))
    vector_store.add_documents([doc1], [doc1_id])

    retrieved_docs = vector_store.get_by_ids([doc1_id])
    assert len(retrieved_docs) == 1
    assert retrieved_docs[0].page_content == doc1_content
    assert retrieved_docs[0].metadata == doc1_metadata


def test_get_by_ids_non_existent(vector_store):
    with pytest.raises(BaseException):
        vector_store.get_by_ids(["non_existent_id"])


def test_delete_documents(vector_store):
    doc1 = Document(id=None, page_content="Test document 1", metadata={"author": "Author 1"})
    doc1_id = hex(random.randint(1, 100))
    vector_store.add_documents([doc1], [doc1_id])

    vector_store.delete([doc1_id])
    assert len(vector_store.get_all_documents()) == 0


def test_dump_load():
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    embedding = FakeEmbeddings(size=100)

    vector_store_1 = JSONVectorStore(temp_file.name, embedding)
    doc1_content = "Test document 1"
    doc1_metadata = {"author": "Author 1"}
    doc1 = Document(id=None, page_content=doc1_content, metadata=doc1_metadata)
    vector_store_1.add_documents([doc1])
    vector_store_1.dump()

    vector_store_2 = JSONVectorStore.load(temp_file.name, embedding)
    documents = vector_store_2.get_all_documents()
    assert len(documents) == 1
    assert documents[0].page_content == doc1_content
    assert documents[0].metadata == doc1_metadata

    temp_file.close()
    os.remove(temp_file.name)