import xml.etree.ElementTree as ET

file_path = "Pháp Luật Đại Cương_8_450_Admin_10-18 16-35/C4.xml"
tree = ET.parse(file_path)
root = tree.getroot()

count_multichoice = sum(1 for q in root.findall("question") if q.get("type") == "multichoice")

print(f"Tổng số câu hỏi trắc nghiệm trong '{file_path}': {count_multichoice}")
