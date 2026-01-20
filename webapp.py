from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse, JSONResponse
import io
from pydantic import BaseModel
import re
import json
from engine import GenericRuleEngine
from report import ReportMaker
import report

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
async def process_prompt(input_source_code: str = ""):

    rules = json.load(open('rules.json'))

    tutor = GenericRuleEngine(rules)
    print("--- Đang phân tích mã nguồn... ---")
    issues = tutor.analyze(input_source_code)

    short_messege = [item['message'] for item in issues]

    print(short_messege)

    # TẠO BÁO CÁO HTML
    report = ReportMaker(input_source_code, issues)
    report.generate_html_report("ket_qua_phan_tich.html")

    with open('ket_qua_phan_tich.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
        
    print(html_content)
    return html_content

@app.post("/api/analyze")
async def generate_image1(promptData: PromptRequest):
    print(promptData.content)
    with open('ket_qua_phan_tich.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    return html_content
