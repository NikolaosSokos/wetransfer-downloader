from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from wetransfer_downloader.downloader import WeTransferDownloader

app = FastAPI()
downloader = WeTransferDownloader(headless=True)

API_KEY = None  # replace later or use environment variable

class DownloadRequest(BaseModel):
    url: str

def verify_api_key(key: str | None):
    if API_KEY and key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")

@app.post("/download")
def download_endpoint(payload: DownloadRequest, x_api_key: str | None = Header(None)):
    verify_api_key(x_api_key)

    try:
        out = downloader.download(payload.url)
        return {"saved_file": str(out)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
