from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse, JSONResponse
import io
from pydantic import BaseModel

app = FastAPI()

class PromptRequest(BaseModel):
    content: str

# --- 1. API Trả về giao diện HTML ---
@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Read HTML content from a file
    with open('clientUI.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    return html_content

# --- API 1: Xử lý Prompt (Text -> Text) ---
@app.get("/api/analyze")
async def process_prompt(text: str = ""):
    with open('clientUI.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    return html_content

@app.post("/api/analyze")
async def generate_image1(promptData: PromptRequest):
    print(promptData.content)
    with open('ket_qua_phan_tich.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    return html_content
