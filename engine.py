import re
import json
import html  # Thư viện để escape ký tự HTML đặc biệt

class GenericRuleEngine:
    def __init__(self, rules_json):
        self.rules = rules_json

    # --- CÁC HÀM XỬ LÝ PHÂN TÍCH (GIỮ NGUYÊN NHƯ CŨ) ---
    def _preprocess_code(self, code):
        """Loại bỏ comment và nội dung trong string để tránh bắt lỗi nhầm"""
        code = re.sub(r'/\*[\s\S]*?\*/', '', code) # Multi-line comment
        code = re.sub(r'//.*', '', code)           # Single-line comment
        # Thay nội dung trong ngoặc kép bằng ""
        code = re.sub(r'"[^"\\\\]*(?:\\\\.[^"\\\\]*)*"', '""', code)
        return code

    def _check_brackets(self, source_code):
        """Sử dụng Stack để kiểm tra sự cân bằng của các dấu ngoặc {}, [], ()"""
        stack = []
        bracket_map = {')': '(', '}': '{', ']': '['}
        issues = []
        
        lines = source_code.split('\n')
        for row, line in enumerate(lines, 1):
            for col, char in enumerate(line, 1):
                if char in bracket_map.values(): # Dấu mở
                    stack.append({'char': char, 'row': row, 'col': col})
                elif char in bracket_map.keys(): # Dấu đóng
                    if not stack:
                        issues.append({'line': row, 'priority': 1, 'type': 'SYNTAX', 'message': f"Dư dấu đóng '{char}'", 'suggestion': f"Xóa dấu '{char}' thừa."})
                    else:
                        top = stack.pop()
                        if top['char'] != bracket_map[char]:
                            issues.append({'line': row, 'priority': 1, 'type': 'SYNTAX', 'message': f"Dấu đóng '{char}' không khớp với dấu mở '{top['char']}' tại dòng {top['row']}", 'suggestion': "Kiểm tra lại cặp dấu đóng/mở."})
        
        while stack:
            unclosed = stack.pop()
            issues.append({'line': unclosed['row'], 'priority': 1, 'type': 'SYNTAX', 'message': f"Dấu mở '{unclosed['char']}' chưa được đóng.", 'suggestion': f"Thêm dấu đóng tương ứng cho '{unclosed['char']}'."})
        return issues

    def analyze(self, source_code):
        clean_code = self._preprocess_code(source_code)
        lines = clean_code.split('\n')
        all_issues = []

        # 1. Kiểm tra cấu trúc ngoặc (Stack)
        all_issues.extend(self._check_brackets(clean_code))

        # 2. Kiểm tra các luật Regex (JSON)
        for rule in self.rules:
            if rule.get('scope') == 'LINE':
                for i, line in enumerate(lines):
                    if not line.strip(): continue
                    if re.search(rule['pattern'], line):
                        all_issues.append({'line': i + 1, 'priority': rule['priority'], 'type': rule['type'], 'message': rule['message'], 'suggestion': rule['suggestion']})
            elif rule.get('scope') == 'FILE':
                if re.search(rule['trigger_pattern'], clean_code) and not re.search(rule['required_pattern'], clean_code):
                    all_issues.append({'line': 0, 'priority': rule['priority'], 'type': rule['type'], 'message': rule['message'], 'suggestion': rule['suggestion']})

        # Sắp xếp theo độ ưu tiên (nhỏ trước) và số dòng
        all_issues.sort(key=lambda x: (x['priority'], x['line']))
        return all_issues

