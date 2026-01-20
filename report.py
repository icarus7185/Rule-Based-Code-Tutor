import re
import json
import html

class ReportMaker:
    def __init__(self, source_code, issues):
        self.source_code = source_code
        self.issues = issues

    def generate_html_report(self, output_filename="report.html"):
        """Tạo file HTML hiển thị code và các lỗi được tô màu"""
        
        # 1. Chuẩn bị CSS
        css_style = """
        <style>
            body { font-family: sans-serif; background-color: #f4f4f9; margin: 20px; }
            .container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .guide-section { margin-bottom: 30px; }
            .step-title { font-weight: bold; margin-top: 15px; padding: 5px; color: white; border-radius: 4px;}
            .step-p1 { background-color: #d9534f; } /* Red for Syntax */
            .step-p2 { background-color: #f0ad4e; } /* Orange for Logic */
            .step-p3 { background-color: #5bc0de; } /* Blue for Info/Warning */
            .issue-item { margin-left: 20px; padding: 5px; border-left: 3px solid #ddd; margin-bottom: 5px; }
            .suggestion { font-style: italic; color: #555; }
            
            .code-viewer { font-family: 'Courier New', monospace; background: #2d2d2d; color: #f8f8f2; padding: 10px; border-radius: 5px; overflow-x: auto; }
            .code-line { display: block; white-space: pre; padding: 2px 0; }
            .line-number { color: #75715e; margin-right: 15px; user-select: none; }
            /* Highlighting classes for code lines */
            .highlight-p1 { background-color: rgba(217, 83, 79, 0.4); } /* Red tint */
            .highlight-p2 { background-color: rgba(240, 173, 78, 0.4); } /* Orange tint */
            .highlight-p3 { background-color: rgba(91, 192, 222, 0.4); } /* Blue tint */
        </style>
        """

        # 2. Tạo nội dung phần Hướng dẫn (Guide Section)
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
                guide_html += f'<div class="issue-item"><strong>[{loc}] {html.escape(issue["message"])}</strong><br>'
                guide_html += f'<span class="suggestion">💡 Gợi ý: {html.escape(issue["suggestion"])}</span></div>'
        guide_html += '</div>'

        # 3. Tạo nội dung phần Xem Code (Code Viewer Section)
        # Tạo map để biết dòng nào bị lỗi gì: line_no -> priority thấp nhất (nghiêm trọng nhất)
        line_issue_map = {}
        for issue in self.issues:
            if issue['line'] > 0:
                current_p = line_issue_map.get(issue['line'], 100)
                line_issue_map[issue['line']] = min(current_p, issue['priority'])

        code_lines = self.source_code.split('\n')
        code_viewer_html = '<div class="code-viewer-container"><h2>💻 Mã nguồn của bạn</h2><div class="code-viewer">'
        for i, line in enumerate(code_lines, 1):
            # Escape các ký tự đặc biệt C++ như <iostream> -> &lt;iostream&gt;
            escaped_line = html.escape(line)
            
            # Xác định class CSS để tô màu dựa trên priority
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
                <h1>Hệ thống Hỗ trợ Lập trình C++</h1>
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
            print("👉 Hãy mở file này bằng trình duyệt web để xem kết quả trực quan.")
        except Exception as e:
            print(f"\n❌ Lỗi khi ghi file HTML: {e}")