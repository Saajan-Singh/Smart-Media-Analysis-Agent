"""
search_agent.py -- Semantic Text Retrieval Agent

Connects to the local ChromaDB vector store and performs semantic similarity
queries against indexed image data using the same all-MiniLM-L6-v2 model.
"""

import chromadb
from chromadb.utils import embedding_functions
from src import DB_DIR

# ---------------------------------------------------------------------------
# ChromaDB connection -- must mirror pipeline.py settings exactly
# ---------------------------------------------------------------------------

_COLLECTION_NAME = "image_text_analysis"
_MODEL_NAME = "all-MiniLM-L6-v2"

_chroma_client = chromadb.PersistentClient(path=DB_DIR)

_embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=_MODEL_NAME
)

_collection = _chroma_client.get_or_create_collection(
    name=_COLLECTION_NAME,
    embedding_function=_embedding_fn,
)


# ---------------------------------------------------------------------------
# Semantic search
# ---------------------------------------------------------------------------

def search_images(query: str, top_k: int = 1) -> list[dict]:
    """Query the vector database with a natural language string.

    Parameters
    ----------
    query : str
        Natural language search query.
    top_k : int
        Number of results to return (default 1).

    Returns
    -------
    list[dict]
        Each entry contains:
            - id:            document ID
            - source_file:   original image path
            - distance:      cosine distance (lower = more similar)
            - snippet:       first 500 chars of the matched document
    """
    if _collection.count() == 0:
        print("[search_agent] The vector database is empty. Run pipeline.py first.")
        return []

    results = _collection.query(
        query_texts=[query],
        n_results=min(top_k, _collection.count()),
    )

    matches: list[dict] = []
    for i in range(len(results["ids"][0])):
        doc_id = results["ids"][0][i]
        document = results["documents"][0][i] if results["documents"] else ""
        distance = results["distances"][0][i] if results["distances"] else None
        metadata = results["metadatas"][0][i] if results["metadatas"] else {}

        matches.append(
            {
                "id": doc_id,
                "source_file": metadata.get("source_file", "unknown"),
                "distance": distance,
                "snippet": document[:500],
            }
        )

    return matches


# ---------------------------------------------------------------------------
# Standalone interactive mode
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    doc_count = _collection.count()
    print(f"[search_agent] Connected to '{_COLLECTION_NAME}' -- {doc_count} document(s)\n")

    if doc_count == 0:
        print("No documents indexed yet. Run `python -m src.pipeline` first.")
        raise SystemExit(0)

    # Interactive query loop
    while True:
        try:
            query = input("Ask a question (or 'quit'): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not query or query.lower() in ("quit", "exit", "q"):
            print("Exiting.")
            break

        results = search_images(query, top_k=3)

        if not results:
            print("  No matches found.\n")
            continue

        for rank, match in enumerate(results, 1):
            print(f"\n--- Result #{rank} ---")
            print(f"  Source : {match['source_file']}")
            print(f"  Distance: {match['distance']:.4f}")
            print(f"  Content :\n{match['snippet']}")
        print()
