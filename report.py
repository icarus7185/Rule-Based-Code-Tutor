import re
import json
import html
import markdown # Thêm thư viện này

class ReportMaker:
    def __init__(self, source_code, issues):
        self.source_code = source_code
        self.issues = issues

    def generate_html_report(self, output_filename="report.html"):
        """Tạo file HTML hiển thị code và các lỗi được tô màu"""
        
        # 1. Chuẩn bị CSS (Đã nâng cấp style cho Markdown)
        css_style = """
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f9; margin: 20px; }
            .container { background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; text-align: center; border-bottom: 2px solid #eee; padding-bottom: 10px; }
            .guide-section { margin-bottom: 30px; }
            .step-title { font-weight: bold; margin-top: 20px; padding: 8px 12px; color: white; border-radius: 4px; letter-spacing: 0.5px; }
            .step-p1 { background-color: #e74c3c; } /* Red */
            .step-p2 { background-color: #f39c12; } /* Orange */
            .step-p3 { background-color: #3498db; } /* Blue */
            
            /* Box chứa từng lỗi */
            .issue-item { margin-top: 15px; padding: 15px 20px; border-left: 5px solid #ddd; background-color: #fafafa; border-radius: 0 8px 8px 0; }
            
            /* --- CSS DÀNH RIÊNG CHO AI SUGGESTION (MARKDOWN) --- */
            .suggestion { margin-top: 12px; color: #34495e; font-size: 15px; line-height: 1.6; }
            .suggestion p { margin: 8px 0; }
            /* Inline code (ví dụ: `int a`) */
            .suggestion code { background-color: #fce4ec; color: #d81b60; padding: 2px 6px; border-radius: 4px; font-family: 'Courier New', Courier, monospace; font-size: 0.95em; }
            /* Khối code bự (Block code) */
            .suggestion pre { background-color: #282c34; color: #abb2bf; padding: 15px; border-radius: 6px; overflow-x: auto; font-family: 'Courier New', Courier, monospace; margin: 12px 0; border: 1px solid #1e2227; }
            .suggestion pre code { background-color: transparent; color: inherit; padding: 0; }
            
            .code-viewer { font-family: 'Courier New', monospace; background: #282c34; color: #abb2bf; padding: 15px; border-radius: 6px; overflow-x: auto; }
            .code-line { display: block; white-space: pre; padding: 2px 0; }
            .line-number { color: #5c6370; margin-right: 15px; user-select: none; }
            .highlight-p1 { background-color: rgba(231, 76, 60, 0.3); } 
            .highlight-p2 { background-color: rgba(243, 156, 18, 0.3); } 
            .highlight-p3 { background-color: rgba(52, 152, 219, 0.3); } 
        </style>
        """

        # 2. Tạo nội dung phần Hướng dẫn
        guide_html = '<div class="guide-section"><h2>📋 Hướng dẫn sửa lỗi từng bước</h2>'
        if not self.issues:
            guide_html += "<p>✅ Tuyệt vời! Không phát hiện lỗi nào.</p>"
        else:
            current_priority = -1
            titles = {1: "BƯỚC 1: SỬA LỖI CẤU TRÚC & CÚ PHÁP (BẮT BUỘC)", 2: "BƯỚC 2: KIỂM TRA LOGIC", 3: "BƯỚC 3: GỢI Ý PHONG CÁCH"}
            for issue in self.issues:
                if issue['priority'] != current_priority:
                    current_priority = issue['priority']
                    guide_html += f'<div class="step-title step-p{current_priority}">{titles.get(current_priority, "KHÁC")}</div>'
                
                loc = f"Dòng {issue['line']}" if issue['line'] > 0 else "Toàn cục"
                
                # --- SỬ DỤNG MARKDOWN Ở ĐÂY ---
                raw_suggestion = issue["suggestion"]
                # Convert sang HTML và hỗ trợ dịch các khối code ```
                html_suggestion = markdown.markdown(raw_suggestion, extensions=['fenced_code'])
                
                guide_html += f'<div class="issue-item"><strong>[{loc}] {html.escape(issue["message"])}</strong><br>'
                guide_html += f'<div class="suggestion">💡 <strong>Gợi ý từ AI:</strong><br>{html_suggestion}</div></div>'
        guide_html += '</div>'

        # 3. Tạo nội dung phần Xem Code 
        line_issue_map = {}
        for issue in self.issues:
            if issue['line'] > 0:
                current_p = line_issue_map.get(issue['line'], 100)
                line_issue_map[issue['line']] = min(current_p, issue['priority'])

        code_lines = self.source_code.split('\n')
        code_viewer_html = '<div class="code-viewer-container"><h2>💻 Mã nguồn của bạn</h2><div class="code-viewer">'
        for i, line in enumerate(code_lines, 1):
            escaped_line = html.escape(line)
            priority = line_issue_map.get(i)
            highlight_class = f"highlight-p{priority}" if priority else ""
            code_viewer_html += f'<span class="code-line {highlight_class}"><span class="line-number">{i:3} |</span>{escaped_line}</span>'
        code_viewer_html += '</div></div>'

        # 4. Ghép lại thành file HTML hoàn chỉnh
        full_html = f"""
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <title>Báo cáo phân tích mã nguồn</title>
            {css_style}
        </head>
        <body>
            <div class="container">
                <h1>Báo cáo phân tích mã nguồn</h1>
                {guide_html}
                <hr>
                {code_viewer_html}
            </div>
        </body>
        </html>
        """

        # 5. Ghi ra file
        try:
            with open(output_filename, "w", encoding="utf-8") as f:
                f.write(full_html)
            print(f"\n✅ Đã tạo báo cáo HTML thành công: {output_filename}")
        except Exception as e:
            print(f"\n❌ Lỗi khi ghi file HTML: {e}")