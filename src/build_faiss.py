from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# =====================================
# LOAD KNOWLEDGE BASE
# =====================================

with open(
    "knowledge_base/phishing_knowledge.txt",
    "r",
    encoding="utf-8"
) as f:

    text = f.read()

documents = [
    line.strip()
    for line in text.split("\n")
    if line.strip()
]

print("Documents Loaded:", len(documents))

# =====================================
# EMBEDDING MODEL
# =====================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

embeddings = model.encode(
    documents
)

embeddings = np.array(
    embeddings
).astype("float32")

# =====================================
# FAISS INDEX
# =====================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(
    dimension
)

index.add(embeddings)

# =====================================
# SAVE
# =====================================

faiss.write_index(
    index,
    "models/faiss_index.bin"
)

with open(
    "models/faiss_docs.pkl",
    "wb"
) as f:
    pickle.dump(
        documents,
        f
    )

print("\nFAISS Index Saved")
print("Total Documents:", len(documents))