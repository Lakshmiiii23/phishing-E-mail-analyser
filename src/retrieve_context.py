import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import faiss
import numpy as np
import pickle

_sentence_transformers_available = False
_sentence_transformers_error = None
SentenceTransformer = None

try:
    from sentence_transformers import SentenceTransformer
    _sentence_transformers_available = True
except Exception as exc:
    _sentence_transformers_error = exc

# Load FAISS Index and Documents robustly
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))

index_path = os.path.join(project_root, "models", "faiss_index.bin")
index = faiss.read_index(index_path)

# Load Documents
docs_path = os.path.join(project_root, "models", "faiss_docs.pkl")
with open(docs_path, "rb") as f:
    documents = pickle.load(f)

model = None
if _sentence_transformers_available:
    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )


def retrieve_context(
    email_text,
    top_k=3
):
    if model is None:
        raise RuntimeError(
            "Semantic retrieval is unavailable because sentence-transformers failed to load. "
            f"Original error: {_sentence_transformers_error}"
        )

    query_embedding = model.encode(
        [email_text]
    )

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for idx in indices[0]:
        results.append(
            documents[idx]
        )

    return results


if __name__ == "__main__":

    sample_email = """
    URGENT!

    Verify your account immediately.

    Click now to avoid suspension.

    """

    results = retrieve_context(
        sample_email
    )

    print("\nRetrieved Context:\n")

    for item in results:
        print("-", item)