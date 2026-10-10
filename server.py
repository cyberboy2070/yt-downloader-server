import subprocess
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class DownloadRequest(BaseModel):
    url: str

@app.post("/get-download-link")
def get_download_link(req: DownloadRequest):
    # Wir fragen yt-dlp nur nach der direkten MP4-Download-URL von YouTube
    command = [
        "yt-dlp",
        "--js-runtimes", "node",
        "--extractor-args", "youtube:player_client=ios,android",
        "--get-url",
        "-f", "b[ext=mp4]/best", # Holt ein fertiges Video inkl. Ton (kein manuelles FFmpeg-Mergen auf dem Server nötig!)
        req.url
    ]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        direct_url = result.stdout.strip()
        
        if not direct_url:
            return {"status": "error", "message": "Konnte keinen Link generieren"}
            
        return {"status": "success", "url": direct_url}
        
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
