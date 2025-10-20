import re
import xml.etree.ElementTree as ET

# Dữ liệu đầu vào dạng văn bản (dán toàn bộ nội dung đề từ file txt hoặc chuỗi)
raw_text = """
Câu 1. Ai lấy cái nỏ thần của An Dương Vương? (cấp độ 1)
A. Tôi
B. Bạn
C. Không ai cả
D. Không xác định
Đáp án: D
"""

# Khởi tạo root XML
questions_el = ET.Element("questions")

code = "C1K1L1"

# Tách từng câu hỏi
pattern = re.compile(r'Câu (\d+).\s*(.*?)\s*\(cấp độ (\d)\)(.*?)Đáp án: ([A-D])', re.DOTALL)
matches = pattern.findall(raw_text)

for num, text, level, options_block, answer in matches:
    q_id = f"{code}Q{num}"
    q_el = ET.SubElement(questions_el, "question", id=q_id)

    ET.SubElement(q_el, "text").text = text.strip()
    ET.SubElement(q_el, "level").text = level.strip()

    opts_el = ET.SubElement(q_el, "options")
    opt_pattern = re.findall(r'([A-D])\.\s*(.*?)\n', options_block + "\n")
    for label, opt_text in opt_pattern:
        ET.SubElement(opts_el, "option").text = f"{label}. {opt_text.strip()}"

    ET.SubElement(q_el, "answer").text = answer.strip()

# Ghi ra file XML
tree = ET.ElementTree(questions_el)
ET.indent(tree, space="  ", level=0)
tree.write(f"{code}_raw.xml", encoding="utf-8", xml_declaration=True)

print(f"Đã chuyển đổi thành công sang XML và lưu vào: {code}_raw.xml")
