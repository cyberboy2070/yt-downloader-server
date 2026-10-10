import os
import subprocess
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
DOWNLOAD_DIR = "/tmp/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

class DownloadRequest(BaseModel):
    url: str

@app.post("/download")
def download_video(req: DownloadRequest):
    output_template = os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s")
    
    command = [
        "yt-dlp",
        "-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / b",
        "--merge-output-format", "mp4",
        "-o", output_template,
        req.url
    ]
    
    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
        files = os.listdir(DOWNLOAD_DIR)
        if not files:
            return {"status": "error", "message": "Keine Datei gefunden"}
            
        latest_file = max([os.path.join(DOWNLOAD_DIR, f) for f in files], key=os.path.getctime)
        return {"status": "success", "filename": os.path.basename(latest_file)}
    
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr}

@app.get("/file/{filename}")
def get_file(filename: str):
    from fastapi.responses import FileResponse
    file_path = os.path.join(DOWNLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="video/mp4", filename=filename)
    return {"error": "Datei nicht gefunden"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
