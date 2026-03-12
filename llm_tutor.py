import os
from google import genai

# Khởi tạo client. 
# Mẹo: Lúc demo hãy lấy API Key miễn phí từ Google AI Studio và gán vào biến môi trường GEMINI_API_KEY
client = genai.Client(api_key="AIzaSyAx8sL0SbPuLCNskfcoGmrs9JXiv9wFtEc")

def generate_context_aware_explanation(source_code, issue):
    """Gọi Gemini API để tạo lời giải thích theo ngữ cảnh."""
    line_number = issue['line']
    error_message = issue['message']
    basic_suggestion = issue['suggestion']
    
    # Lấy 5 dòng code xung quanh vị trí lỗi để Gemini hiểu bối cảnh
    lines = source_code.split('\n')
    start_line = max(0, line_number - 3)
    end_line = min(len(lines), line_number + 2)
    code_context = "\n".join(lines[start_line:end_line])

    prompt = f"""
    Bạn là một gia sư lập trình C++ kiên nhẫn. Sinh viên đang bị lỗi code.
    
    [CODE CỦA SINH VIÊN (quanh dòng {line_number})]
    ```cpp
    {code_context}
    ```
    
    [LỖI HỆ THỐNG PHÁT HIỆN]
    - Loại lỗi: {error_message}
    - Gợi ý thô: {basic_suggestion}
    
    [YÊU CẦU]
    Hãy viết 2-3 câu ngắn gọn bằng tiếng Việt:
    1. Giải thích dễ hiểu tại sao dòng {line_number} lại sai logic/cú pháp.
    2. Cung cấp đoạn code sửa lại cho đúng.
    Xưng "mình" và gọi "bạn". Không giải thích dông dài.
    """

    try:
        # Dùng model flash để phản hồi cực nhanh, phù hợp cho Web API
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text.strip()
    except Exception as e:
            print(f"🚨 Lỗi gọi API Gemini: {str(e)}") # In lỗi ra để bắt bệnh
            return f"(Hệ thống bận) {basic_suggestion}"