# WeTransfer Downloader

A simple Python tool and API for automatically downloading files from **WeTransfer links**, including shortlinks like `https://we.tl/t-XXXXX`.

This project uses **Playwright + Chromium** to open the link, handle cookie/consent dialogs, click the “Download” button, and save the file locally.  
Perfect for automations such as **n8n**, personal scripts, and home server workflows.

---

## ⭐ Purpose

WeTransfer links cannot be downloaded directly with `requests`.  
They require:

- Redirect handling  
- JavaScript rendering  
- Cookie banners  
- “Download” button clicks  

This tool solves that by using an automated browser and exposing a simple API endpoint.

---

## 📦 Installation (uv)

Install dependencies:

```bash
uv sync
```

Install Chromium for Playwright:

```bash
playwright install chromium
```

---

## ▶️ Run the API

Start the FastAPI server:

```bash
uv run uvicorn api.main:app --host 0.0.0.0 --port 8000
```

API available at:

```
http://localhost:8000
```

Interactive docs:

```
http://localhost:8000/docs
```

Downloaded files saved in:

```
downloads/
```

---

## 📡 API Usage

### POST `/download`

**JSON Body:**

```json
{
  "url": "https://we.tl/t-XXXXXXX"
}
```

**Example request:**

```bash
curl -X POST http://localhost:8000/download   -H "Content-Type: application/json"   -d '{"url": "https://we.tl/t-XXXXXXX"}'
```

**Example response:**

```json
{
  "saved_file": "downloads/MyFile.mp4"
}
```

---

## 🧠 How It Works

1. Launches a headless Chromium browser  
2. Opens the WeTransfer link  
3. Accepts cookie banner (if present)  
4. Clicks the correct “Download” button  
5. Waits for the download to complete  
6. Saves the file into `downloads/`  
7. Returns the filename via the API  

---

## ✔ Recommended Use Case

This project is ideal for:

- n8n automations  
- Email-to-download workflows  
- Personal servers  
- Home automation  
- Self-hosted systems  

It is **not** intended for public commercial API reselling or large-scale cloud usage.

---

## 📜 License

MIT License — free to modify and self-host.
