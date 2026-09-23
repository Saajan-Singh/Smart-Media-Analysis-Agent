"""
search_agent.py -- Semantic Text Retrieval Agent

Connects to the local ChromaDB vector store and performs semantic similarity
queries against indexed image data using the same all-MiniLM-L6-v2 model.
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from src import DB_DIR, ENV_PATH, MEDIA_DIR

try:
    import chromadb
    from src.embedding import get_embedding_function
except ImportError:
    chromadb = None

load_dotenv(dotenv_path=ENV_PATH)

# ---------------------------------------------------------------------------
# LLM Initialization
# ---------------------------------------------------------------------------

USE_AZURE = bool(os.getenv("AZURE_OPENAI_ENDPOINT"))

if USE_AZURE:
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
    api_key = os.getenv("AZURE_OPENAI_API_KEY", "")
    
    llm_client = OpenAI(
        base_url=f"{endpoint}/openai/v1/",
        api_key=api_key
    )
    llm_model = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
elif os.getenv("OPENAI_API_KEY"):
    llm_client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    llm_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
else:
    llm_client = None
    llm_model = None

# ---------------------------------------------------------------------------
# ChromaDB connection (with in-memory fallback)
# ---------------------------------------------------------------------------

_COLLECTION_NAME = "image_text_analysis_azure"
_collection = None

try:
    if chromadb:
        _chroma_client = chromadb.PersistentClient(path=DB_DIR)
        _embedding_fn = get_embedding_function()
        _collection = _chroma_client.get_or_create_collection(
            name=_COLLECTION_NAME,
            embedding_function=_embedding_fn,
        )
        print(f"[search_agent] Using ChromaDB PersistentClient at {DB_DIR}")
except Exception as e:
    print(f"[search_agent] ChromaDB PersistentClient unavailable ({e})")

if _collection is None:
    from src.memory_store import InMemoryCollection
    _collection = InMemoryCollection(name=_COLLECTION_NAME)
    print(f"[search_agent] Using InMemoryCollection fallback")


# ---------------------------------------------------------------------------
# Semantic search
# ---------------------------------------------------------------------------

def search_images(query: str, top_k: int = 1, source_filter: str = None) -> list[dict]:
    """Query the vector database with a natural language string.

    Parameters
    ----------
    query : str
        Natural language search query.
    top_k : int
        Number of results to return (default 1).
    source_filter : str, optional
        If provided, only return results whose source_file metadata
        ends with this filename (e.g. 'test.png').

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

    query_kwargs = {
        "query_texts": [query],
        "n_results": min(top_k, _collection.count()),
    }

    if source_filter:
        full_path = os.path.join(MEDIA_DIR, source_filter)
        query_kwargs["where"] = {"source_file": full_path}

    results = _collection.query(**query_kwargs)

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
# Generative LLM Response
# ---------------------------------------------------------------------------

def generate_answer(query: str, search_results: list[dict]) -> str:
    """Generate a conversational answer using the LLM based on retrieved context."""
    if not USE_AZURE and not llm_client:
        return "LLM client not configured. Please set AZURE_OPENAI_API_KEY or OPENAI_API_KEY in .env"
    
    if not search_results:
        return "I couldn't find any relevant information to answer your question."

    # Construct the context from the best matches
    context = ""
    for rank, match in enumerate(search_results, 1):
        context += f"--- Source {rank}: {match['source_file']} ---\n"
        context += f"{match['snippet']}\n\n"

    system_prompt = "You are a Smart Media Analysis Agent. Answer the user's question using ONLY the provided OCR text and visual tags. Do NOT append the source file name, file path, or 'Source:' citations to your response. Provide ONLY the direct, natural answer to the user's question."

    user_prompt = f"Context:\n{context}\n\nUser Question:\n{query}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        response = llm_client.chat.completions.create(
            model=llm_model,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating answer: {e}"

# ---------------------------------------------------------------------------
# Full RAG Pipeline 
# ---------------------------------------------------------------------------

def generate_moderation_report_direct(document: str) -> dict:
    """Generate a content moderation report for a specific image using the LLM directly from text."""
    if not USE_AZURE and not llm_client:
        return {"categories": ["Media Analysis Error"], "risk_score": 0, "reasoning": "LLM client not configured."}
    
    if not document:
         return {"categories": ["General Media"], "risk_score": 0, "reasoning": "No OCR data found for this image."}

    system_prompt = """You are a strict, literal, deterministic content moderation engine. You must evaluate the provided image captions exactly as they are written. DO NOT invent backstories, assume context, or be creative. If the captions describe aggressive actions (yelling, pointing, hitting), you must classify it as violence or conflict. Never assume close proximity means affection unless explicitly stated by the captions.

You are an automated Content Moderation API. 
Analyze the provided OCR text and visual descriptions.
You MUST respond with ONLY a valid JSON object matching this schema:
{
  "categories": ["tag1", "tag2"],
  "risk_score": integer between 0 and 100,
  "reasoning": "A brief explanation of why this risk score was given."
}

For the 'categories' field, provide a single, meaningful, descriptive noun that represents the actual visual content or theme of the image (e.g., 'Transportation', 'Architecture', 'Meme', 'Dashboard', 'Nature', 'Document'). STRICTLY DO NOT use moderation-related terms, risk statuses, or adjectives like 'Benign', 'Safe', 'Harmless', 'Warning', or 'Clear' as the category name.

Carefully analyze the visual captions for signs of aggressive body language (e.g., yelling, shouting, pointing fingers, angry expressions). Do not assume close-proximity interactions are affectionate. If the captions indicate arguing, hostility, or fighting, strictly categorize this as 'Conflict' or 'Aggression' and elevate the risk score accordingly based on the severity of the depicted hostility."""

    user_prompt = f"Image Data:\n{document}"
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        response = llm_client.chat.completions.create(
            model=llm_model,
            messages=messages,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content.strip()
        # Remove any markdown JSON formatting if present
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        
        return json.loads(content.strip())
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"categories": ["Media Analysis Error"], "risk_score": 0, "reasoning": f"Backend API Error: {str(e)}"}

def generate_moderation_report(filename: str) -> dict:
    """Generate a content moderation report for a specific image using the LLM via ChromaDB lookup."""
    # Fetch the document from ChromaDB directly
    full_path = os.path.join(MEDIA_DIR, filename)
    try:
        results = _collection.get(where={"source_file": full_path})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"categories": ["Media Analysis Error"], "risk_score": 0, "reasoning": f"DB Error: {str(e)}"}
        
    if not results or not results.get("documents") or len(results["documents"]) == 0:
        return {"categories": ["General Media"], "risk_score": 0, "reasoning": "No OCR data found for this image. It may not be indexed yet."}
        
    document = results["documents"][0]
    return generate_moderation_report_direct(document)

def query_pipeline(user_query: str, target_filename: str = None) -> dict:
    """Executes the full RAG pipeline (search + generation) and returns a structured response."""
    results = search_images(user_query, top_k=3, source_filter=target_filename)
    
    if not results:
        return {
            "answer": "I couldn't find any relevant information to answer your question.",
            "source": "None",
            "distance": None,
            "ocr_context": "No documents matched the query."
        }
    
    answer = generate_answer(user_query, results)
    
    ocr_context = ""
    for rank, match in enumerate(results, 1):
        ocr_context += f"--- Source {rank}: {match['source_file']} ---\n{match['snippet']}\n\n"
        
    return {
        "answer": answer,
        "source": results[0]['source_file'],
        "distance": round(results[0]['distance'], 4) if results[0].get('distance') is not None else None,
        "ocr_context": ocr_context.strip()
    }

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

        print("\n[search_agent] Generating answer...")
        answer = generate_answer(query, results)
        
        print("\n=========================================")
        print("Answer:")
        print("=========================================")
        print(answer)
        print("\n--- Retrieved Sources ---")
        for rank, match in enumerate(results, 1):
            print(f"  #{rank}: {match['source_file']} (Distance: {match['distance']:.4f})")
        print("=========================================\n")
