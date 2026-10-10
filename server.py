import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class DownloadRequest(BaseModel):
    url: str

@app.post("/get-download-link")
def get_download_link(req: DownloadRequest):
    try:
        cobalt_url = "https://api.cobalt.tools/api/json"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "url": req.url,
            "vCodec": "h264",
            "videoQuality": "720"
        }
        
        response = requests.post(cobalt_url, json=payload, headers=headers, timeout=15)
        data = response.json()
        
        # Direkten Link aus der API-Antwort fischen
        if "url" in data:
            return {"status": "success", "url": data["url"]}
        elif "picker" in data and len(data["picker"]) > 0:
            return {"status": "success", "url": data["picker"][0]["url"]}
        else:
            return {"status": "error", "message": "Konnte keinen Link über die API generieren."}
            
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
