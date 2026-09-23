"""
memory_store.py -- Lightweight In-Memory Document Store

A minimal drop-in replacement for ChromaDB's Collection API, used when
the full chromadb package is unavailable (e.g., on Vercel with chromadb-client).

Data is ephemeral — it lives only for the duration of the process. This is
acceptable on Vercel where /tmp is wiped between cold starts anyway.
"""


class InMemoryCollection:
    """Mimics the subset of chromadb.Collection used by pipeline.py and search_agent.py."""

    def __init__(self, name: str = "in_memory"):
        self._name = name
        self._docs: dict[str, dict] = {}  # id -> {document, metadata}

    # ------------------------------------------------------------------
    def count(self) -> int:
        return len(self._docs)

    # ------------------------------------------------------------------
    def upsert(self, ids: list[str], documents: list[str], metadatas: list[dict] | None = None):
        for i, doc_id in enumerate(ids):
            self._docs[doc_id] = {
                "document": documents[i] if i < len(documents) else "",
                "metadata": metadatas[i] if metadatas and i < len(metadatas) else {},
            }

    # ------------------------------------------------------------------
    def get(self, where: dict | None = None, ids: list[str] | None = None) -> dict:
        """Retrieve documents, optionally filtered by metadata or ids."""
        results_ids = []
        results_docs = []
        results_meta = []

        for doc_id, entry in self._docs.items():
            if ids and doc_id not in ids:
                continue
            if where:
                match = all(entry["metadata"].get(k) == v for k, v in where.items())
                if not match:
                    continue
            results_ids.append(doc_id)
            results_docs.append(entry["document"])
            results_meta.append(entry["metadata"])

        return {
            "ids": results_ids,
            "documents": results_docs,
            "metadatas": results_meta,
        }

    # ------------------------------------------------------------------
    def query(
        self,
        query_texts: list[str],
        n_results: int = 1,
        where: dict | None = None,
    ) -> dict:
        """Return documents as 'matches'. No real vector similarity — returns
        all matching docs (filtered by metadata if provided), up to n_results.
        Results are wrapped in the nested list format ChromaDB uses."""
        matched_ids = []
        matched_docs = []
        matched_meta = []

        for doc_id, entry in self._docs.items():
            if where:
                match = all(entry["metadata"].get(k) == v for k, v in where.items())
                if not match:
                    continue
            matched_ids.append(doc_id)
            matched_docs.append(entry["document"])
            matched_meta.append(entry["metadata"])
            if len(matched_ids) >= n_results:
                break

        # ChromaDB returns nested lists (one per query text)
        distances = [[0.5] * len(matched_ids)]  # dummy distances
        return {
            "ids": [matched_ids],
            "documents": [matched_docs],
            "metadatas": [matched_meta],
            "distances": distances,
        }

    # ------------------------------------------------------------------
    def delete(self, ids: list[str]):
        for doc_id in ids:
            self._docs.pop(doc_id, None)
