from pathlib import Path
import shutil

from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


BASE_DIR = Path(__file__).resolve().parent

DOCUMENT_PATH = BASE_DIR / "documents" / "medical_guidelines.txt"
VECTOR_STORE_PATH = BASE_DIR / "vector_store"


def build_vector_store():
    print("=" * 60)
    print("Building Medical Knowledge Base")
    print("=" * 60)

    # -----------------------------
    # Check if the knowledge base exists
    # -----------------------------
    if not DOCUMENT_PATH.exists():
        raise FileNotFoundError(
            f"Knowledge base not found:\n{DOCUMENT_PATH}"
        )

    print(f"Loading knowledge base from:\n{DOCUMENT_PATH}\n")

    # -----------------------------
    # Load the medical guidelines
    # -----------------------------
    loader = TextLoader(
        str(DOCUMENT_PATH),
        encoding="utf-8"
    )

    documents = loader.load()

    text = documents[0].page_content

    # -----------------------------
    # Split on separator
    # -----------------------------
    sections = [
        section.strip()
        for section in text.split("------------------------------------------------")
        if section.strip()
    ]

    docs = [
        Document(page_content=section)
        for section in sections
    ]

    print(f"Loaded {len(docs)} guideline chunks.")

    # -----------------------------
    # Delete previous FAISS index
    # -----------------------------
    if VECTOR_STORE_PATH.exists():
        print("\nDeleting old vector store...")
        shutil.rmtree(VECTOR_STORE_PATH)

    VECTOR_STORE_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    # -----------------------------
    # Create embedding model
    # -----------------------------
    print("\nLoading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # -----------------------------
    # Build FAISS database
    # -----------------------------
    print("Creating FAISS index...")

    vector_db = FAISS.from_documents(
        docs,
        embeddings
    )

    # -----------------------------
    # Save vector store
    # -----------------------------
    vector_db.save_local(
        str(VECTOR_STORE_PATH)
    )

    print("\nVector store created successfully!")

    print(f"Saved to:\n{VECTOR_STORE_PATH}")

    print("=" * 60)


if __name__ == "__main__":
    build_vector_store()