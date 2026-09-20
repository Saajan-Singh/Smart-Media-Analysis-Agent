# Smart Media Analysis Agent: Project Overview

## 1. Project Objective
The Smart Media Analysis Agent is a Retrieval-Augmented Generation (RAG) pipeline designed to extract meaningful insights from multimedia files (images/video) and make them searchable via semantic queries. By leveraging cloud-based AI vision and local vector embeddings, the agent can "understand" media and retrieve specific files based on natural language questions.

## 2. Architecture & Tech Stack
* **Cloud AI Extraction:** Azure AI Vision (Image Analysis 4.0) for dense image captioning and Optical Character Recognition (OCR).
* **Local Vector Database:** ChromaDB (Persistent Local Client).
* **Embedding Model:** `sentence-transformers` (`all-MiniLM-L6-v2`) to convert text into high-dimensional mathematical vectors.
* **Environment Management:** `python-dotenv` for secure API credential handling.
* **Version Control:** Git and GitHub.

## 3. The Local Fallback Strategy (MFA Workaround)
Originally, this architecture was designed to use **Azure AI Search** for vector storage and retrieval. However, due to institutional Multi-Factor Authentication (MFA) enforcement blocking cloud search deployment, the project successfully pivoted to a **hybrid-local architecture**.

Instead of relying on Azure for vector indexing, the pipeline uses **ChromaDB** to host the vector space entirely locally on the machine. This ensures the project remains functional and searchable without being bottlenecked by cloud authentication barriers.

## 4. Project Structure

```
Smart-Media-Analysis-Agent/
|-- .env                        # Azure API credentials (git-ignored)
|-- .gitignore                  # Protects secrets and generated data
|-- requirements.txt            # Python dependencies
|-- PROJECT_WORKFLOW.md         # This file
|-- README.md                   # Repository readme
|-- media_db/                   # ChromaDB persistent vector store (git-ignored)
|-- media/                      # Raw image/video assets
|   |-- test.png
|-- src/                        # Core Python package
    |-- __init__.py             # Package init with project path constants
    |-- image_analyzer.py       # Azure Vision extraction engine
    |-- pipeline.py             # Extraction-to-ChromaDB ingestion bridge
    |-- search_agent.py         # Semantic similarity search agent
    |-- vision_test.py          # Standalone Azure API integration test
```

## 5. Pipeline Component Breakdown

### A. `src/vision_test.py` (The Proving Ground) - [x] Completed
This script acts as the initial integration test. It securely loads the Azure endpoints from the `.env` file, sends a local test image to the Azure AI Vision endpoint, and prints the generated tags and extracted OCR text to the terminal to verify API functionality.

### B. `src/image_analyzer.py` (Image to Text Extraction Engine) - [x] Completed
The core extraction module. Authenticates to Azure AI Vision and implements `analyze_image()` which:
- Reads a local image file in binary format.
- Requests `VisualFeatures.TAGS` and `VisualFeatures.READ` (OCR) with graceful `CAPTION` fallback for region compatibility.
- Parses the response into a structured dictionary and a unified Markdown string for downstream indexing.

### C. `src/pipeline.py` (Text Ingestion & Local Vector Indexing) - [x] Completed
The automated ingestion engine. Bridges extraction into ChromaDB by:
1. Running `image_analyzer.analyze_image()` on a given image.
2. Upserting the structured text into a local ChromaDB collection (`image_text_analysis`) with metadata (`source_file`, `media_type`, `character_count`).
3. Supporting batch ingestion of all `.png`, `.jpg`, `.jpeg` images inside the `media/` directory.

### D. `src/search_agent.py` (Semantic Text Retrieval) - [x] Completed
The user-facing retrieval agent. When a user asks a natural language question:
1. Embeds the query into a vector using the same `all-MiniLM-L6-v2` model.
2. Calculates cosine distance against records stored in ChromaDB.
3. Returns the most semantically relevant image path, distance score, and matched content snippet.

## 6. Execution Instructions

**1. Install Dependencies**
```bash
pip install -r requirements.txt
```

**2. Configure Environment**
Create a `.env` file in the root directory:
```env
AZURE_VISION_ENDPOINT="<your-endpoint-url>"
AZURE_VISION_KEY="<your-api-key>"
```

**3. Test Azure Vision Independently**
```bash
python -m src.vision_test
```

**4. Run the Full Extraction-to-Index Pipeline**
```bash
python -m src.pipeline
```

**5. Query the Semantic Search Agent**
```bash
python -m src.search_agent
```

## 7. Future Development Scope
* **OpenCV Integration:** Expanding the ingestion pipeline to process `.mp4` video files by extracting frames at specific intervals and routing them through the Azure Vision logic.
* **Generative LLM Synthesis:** Upgrading `search_agent.py` to pass the retrieved ChromaDB context into a Local or Cloud LLM to generate conversational, human-like answers rather than just returning the raw data match.
* **Cloud Re-Migration:** Swapping ChromaDB back to Azure AI Search once MFA tenant restrictions are resolved.
