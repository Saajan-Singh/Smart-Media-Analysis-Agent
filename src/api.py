import os
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from src.search_agent import query_pipeline, generate_moderation_report
from src.pipeline import index_image, delete_image_from_index
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

@app.delete("/api/media/{filename}")
def delete_media_endpoint(filename: str):
    """Delete a media file from the filesystem and its vector from the database."""
    file_path = os.path.join(MEDIA_DIR, filename)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        delete_image_from_index(filename)
        return {"status": "success", "message": f"Deleted {filename}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/media/{filename}")
def serve_media_file(filename: str):
    """Serve an uploaded media file by name."""
    file_path = os.path.join(MEDIA_DIR, filename)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}, 404

@app.get("/api/health")
def health_check():
    """Diagnostic endpoint to verify the function is alive and env vars are set."""
    return {
        "status": "ok",
        "AZURE_VISION_ENDPOINT": bool(os.getenv("AZURE_VISION_ENDPOINT")),
        "AZURE_OPENAI_ENDPOINT": bool(os.getenv("AZURE_OPENAI_ENDPOINT")),
        "AZURE_OPENAI_API_KEY": bool(os.getenv("AZURE_OPENAI_API_KEY")),
        "AZURE_VISION_KEY": bool(os.getenv("AZURE_VISION_KEY")),
        "VERCEL": bool(os.environ.get("VERCEL")),
        "MEDIA_DIR": MEDIA_DIR,
    }

os.makedirs(MEDIA_DIR, exist_ok=True)

# Static file mounts — only for local dev; Vercel uses routes in vercel.json
try:
    if os.path.isdir(design_dir):
        app.mount("/static", StaticFiles(directory=design_dir), name="static")
except Exception:
    pass

@app.get("/")
def serve_index():
    index_path = os.path.join(design_dir, "code.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    return {"message": "Smart Media Analysis API is running."}

