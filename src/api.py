import os
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from src.search_agent import query_pipeline, generate_moderation_report
from src.pipeline import index_image
from src import PROJECT_ROOT, MEDIA_DIR

app = FastAPI(title="Smart Media Analysis API")

design_dir = os.path.join(PROJECT_ROOT, "Design")

class QueryRequest(BaseModel):
    query: str
    filename: str | None = None

@app.post("/api/chat")
def chat_endpoint(req: QueryRequest):
    return query_pipeline(req.query, req.filename)

@app.get("/api/moderation_report/{filename}")
def moderation_report_endpoint(filename: str):
    return generate_moderation_report(filename)

@app.post("/api/upload")
async def upload_endpoint(file: UploadFile = File(...)):
    """Save an uploaded media file to media/ and run the ingestion pipeline on it."""
    os.makedirs(MEDIA_DIR, exist_ok=True)
    save_path = os.path.join(MEDIA_DIR, file.filename)

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        # Assume it's an image
        index_image(save_path)
        category = "Uncategorized"
        try:
            report = generate_moderation_report(file.filename)
            if report and report.get("categories"):
                category = report["categories"][0].strip().title()
        except Exception as e:
            print(f"Error determining category: {e}")
            
        return {
            "filename": file.filename,
            "primary_category": category
        }
    except Exception as e:
        return {"filename": file.filename, "primary_category": "Error"}

app.mount("/static", StaticFiles(directory=design_dir), name="static")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(design_dir, "code.html"))
