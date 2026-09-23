"""
pipeline.py -- Text Ingestion & Local Vector Indexing

Orchestrates the extraction-to-index workflow:
  1. Runs image_analyzer.analyze_image() on a given image.
  2. Upserts the structured text + metadata into a local ChromaDB collection.
  3. Supports batch ingestion of all images inside the media/ directory.
"""

import os
import glob
from src.image_analyzer import analyze_image
from src import DB_DIR, MEDIA_DIR

import chromadb
from src.embedding import get_embedding_function

# ---------------------------------------------------------------------------
# ChromaDB setup -- persistent local storage
# ---------------------------------------------------------------------------

_COLLECTION_NAME = "image_text_analysis_azure"

_chroma_client = chromadb.PersistentClient(path=DB_DIR)

_embedding_fn = get_embedding_function()

_collection = _chroma_client.get_or_create_collection(
    name=_COLLECTION_NAME,
    embedding_function=_embedding_fn,
)


# ---------------------------------------------------------------------------
# Single-image indexing
# ---------------------------------------------------------------------------

def index_image(image_path: str, doc_id: str = None) -> dict:
    """Extract text from an image and upsert it into ChromaDB.

    Parameters
    ----------
    image_path : str
        Path to the image file.
    doc_id : str, optional
        Custom document ID.  Defaults to the filename stem.

    Returns
    -------
    dict
        The analysis result from image_analyzer.
    """
    data = analyze_image(image_path)
    unified_text = data["unified_text"]

    if doc_id is None:
        doc_id = os.path.splitext(os.path.basename(image_path))[0]

    _collection.upsert(
        ids=[doc_id],
        documents=[unified_text],
        metadatas=[
            {
                "source_file": data["source_file"],
                "media_type": "image",
                "character_count": len(unified_text),
            }
        ],
    )

    print(f"[pipeline] Indexed '{doc_id}' ({len(unified_text)} chars) -> {_COLLECTION_NAME}")
    return data

def delete_image_from_index(filename: str):
    """Delete an image's vector from ChromaDB based on its filename."""
    doc_id = os.path.splitext(os.path.basename(filename))[0]
    try:
        _collection.delete(ids=[doc_id])
        print(f"[pipeline] Deleted '{doc_id}' from '{_COLLECTION_NAME}'")
    except Exception as exc:
        print(f"[pipeline] Failed to delete '{doc_id}': {exc}")

# ---------------------------------------------------------------------------
# Batch ingestion -- process every image in media/ directory
# ---------------------------------------------------------------------------

_SUPPORTED_EXTENSIONS = (".png", ".jpg", ".jpeg")


def index_batch(directory: str = None) -> list[dict]:
    """Index all supported images found inside *directory*.

    Parameters
    ----------
    directory : str
        Folder to scan (defaults to ``media/``).

    Returns
    -------
    list[dict]
        Analysis results for every successfully indexed image.
    """
    if directory is None:
        directory = MEDIA_DIR

    if not os.path.isdir(directory):
        print(f"[pipeline] Directory '{directory}' not found -- skipping batch.")
        return []

    results: list[dict] = []
    for ext in _SUPPORTED_EXTENSIONS:
        for filepath in glob.glob(os.path.join(directory, f"*{ext}")):
            try:
                result = index_image(filepath)
                results.append(result)
            except Exception as exc:
                print(f"[pipeline] FAILED on {filepath}: {exc}")

    if not results:
        print(f"[pipeline] No images found in '{directory}'.")
    else:
        print(f"[pipeline] Batch complete -- {len(results)} image(s) indexed.")

    return results


# ---------------------------------------------------------------------------
# Standalone execution -- index test.png + batch from media/
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    # Single file from CLI arg, or default to media/test.png
    default_target = os.path.join(MEDIA_DIR, "test.png")
    target = sys.argv[1] if len(sys.argv) > 1 else default_target

    if os.path.isfile(target):
        print(f"=== Indexing single image: {target} ===\n")
        data = index_image(target)
        print()
        print("--- Extracted Content ---")
        print(data["unified_text"])
    else:
        print(f"[pipeline] File '{target}' not found.")

    # Also attempt batch ingest from media/
    if os.path.isdir(MEDIA_DIR):
        print(f"\n=== Batch indexing {MEDIA_DIR} directory ===\n")
        index_batch(MEDIA_DIR)

    # Show collection stats
    count = _collection.count()
    print(f"\n[pipeline] Total documents in '{_COLLECTION_NAME}': {count}")
