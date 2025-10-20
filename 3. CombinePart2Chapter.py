import xml.etree.ElementTree as ET

# Danh sách các file cần hợp nhất
C = "5"
files = [
    "XMLdata/questions-VAA-C{}K1L1.xml".format(C),
    "XMLdata/questions-VAA-C{}K2L2.xml".format(C),
    "XMLdata/questions-VAA-C{}K3L3.xml".format(C),
    "XMLdata/questions-VAA-C{}K4L4.xml".format(C),
]

# Parse file đầu tiên làm gốc
tree = ET.parse(files[0])
root = tree.getroot()

# Duyệt các file còn lại và thêm nội dung vào root
for f in files[1:]:
    tree_tmp = ET.parse(f)
    root_tmp = tree_tmp.getroot()
    for question in root_tmp.findall('question'):
        root.append(question)

# Ghi kết quả ra file mới
output_file = "XMLdata/questions-VAA-C{}.xml".format(C)
tree.write(output_file, encoding='utf-8', xml_declaration=True)

print(f"Đã hợp nhất xong, file kết quả: {output_file}")
