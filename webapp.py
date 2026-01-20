from fastapi import FastAPI, Response, UploadFile, File
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

# --- API 2: Upload file .cpp và trả về HTML report ---
@app.post("/api/upload-cpp")
async def upload_cpp_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        file_content = content.decode('utf-8')
        
        # Phân tích code
        rules = json.load(open('rules.json'))
        tutor = GenericRuleEngine(rules)
        print("--- Đang phân tích file .cpp... ---")
        issues = tutor.analyze(file_content)
        
        # TẠO BÁO CÁO HTML
        report_obj = ReportMaker(file_content, issues)
        report_obj.generate_html_report("ket_qua_phan_tich.html")
        
        with open('ket_qua_phan_tich.html', 'r', encoding='utf-8') as html_file:
            html_content = html_file.read()
        
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Lỗi: {str(e)}</h1>")
