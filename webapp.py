from fastapi import FastAPI, Response, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
import io
from pydantic import BaseModel
import re
import json
from engine import GenericRuleEngine
from report import ReportMaker
import report
from llm_tutor import generate_context_aware_explanation
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
async def process_prompt(ai_mode: str = "", input_source_code: str = ""):
    rules = json.load(open('rules.json', encoding='utf-8'))
    tutor = GenericRuleEngine(rules)
    
    # 1. Quét code bằng Rule-based cũ
    issues = tutor.analyze(input_source_code)

    # 2. Dùng Gemini nâng cấp lời giải thích
    for issue in issues:
        # Chỉ gọi API cho lỗi ưu tiên cao (SYNTAX và LOGIC) để tránh lạm dụng API
        if issue['priority'] <= 2: 
            ai_explanation = generate_context_aware_explanation(ai_mode, input_source_code, issue)
            issue['suggestion'] = ai_explanation # Ghi đè gợi ý cũ kỹ bằng văn hay chữ tốt của Gemini

    # 3. Xuất HTML như bình thường
    report_obj = ReportMaker(input_source_code, issues)
    report_obj.generate_html_report("ket_qua_phan_tich.html")

    with open('ket_qua_phan_tich.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    return HTMLResponse(content=html_content)

# --- API 2: Upload file .cpp và trả về HTML report ---
@app.post("/api/upload-cpp")
async def upload_cpp_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        file_content = content.decode('utf-8')
        
        # Phân tích code
        rules = json.load(open('rules.json', encoding='utf-8'))
        tutor = GenericRuleEngine(rules)
        print("--- Đang phân tích file .cpp... ---")
        # print(file_content)
        issues = tutor.analyze(file_content)

        # 2. Dùng Gemini nâng cấp lời giải thích
        for issue in issues:
            # Chỉ gọi API cho lỗi ưu tiên cao (SYNTAX và LOGIC) để tránh lạm dụng API
            if issue['priority'] <= 2: 
                ai_explanation = generate_context_aware_explanation("genai", file_content, issue)
                issue['suggestion'] = ai_explanation # Ghi đè gợi ý cũ kỹ bằng văn hay chữ tốt của Gemini
        
        # TẠO BÁO CÁO HTML
        report_obj = ReportMaker(file_content, issues)
        report_obj.generate_html_report("ket_qua_phan_tich.html")
        
        with open('ket_qua_phan_tich.html', 'r', encoding='utf-8') as html_file:
            html_content = html_file.read()
        
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Lỗi: {str(e)}</h1>")

# --- API 2: Upload file .cpp và trả về HTML report ---
@app.post("/api/upload-cpp/local")
async def upload_cpp_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        file_content = content.decode('utf-8')
        
        # Phân tích code
        rules = json.load(open('rules.json', encoding='utf-8'))
        tutor = GenericRuleEngine(rules)
        print("--- Đang phân tích file .cpp... ---")
        # print(file_content)
        issues = tutor.analyze(file_content)

        # 2. Dùng Gemini nâng cấp lời giải thích
        for issue in issues:
            # Chỉ gọi API cho lỗi ưu tiên cao (SYNTAX và LOGIC) để tránh lạm dụng API
            if issue['priority'] <= 2: 
                ai_explanation = generate_context_aware_explanation("ollama", file_content, issue)
                issue['suggestion'] = ai_explanation # Ghi đè gợi ý cũ kỹ bằng văn hay chữ tốt của Gemini
        
        # TẠO BÁO CÁO HTML
        report_obj = ReportMaker(file_content, issues)
        report_obj.generate_html_report("ket_qua_phan_tich.html")
        
        with open('ket_qua_phan_tich.html', 'r', encoding='utf-8') as html_file:
            html_content = html_file.read()
        
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Lỗi: {str(e)}</h1>")
