import os
import xml.etree.ElementTree as ET

# Mẫu tên file (sẽ format với số Chương)
file_templates = [
    "XMLdata/hanh_vi_to_chuc/questions-VAA-C{}K1L1.xml",
    "XMLdata/hanh_vi_to_chuc/questions-VAA-C{}K2L2.xml",
    "XMLdata/hanh_vi_to_chuc/questions-VAA-C{}K3L3.xml",
    # thêm hoặc bỏ comment các template khác nếu cần
]

for C in range(1, 10):  # Chạy từ Chương 1 tới Chương 9
    Cstr = str(C)
    files = [t.format(Cstr) for t in file_templates]

    # Chỉ lấy những file tồn tại
    existing_files = [f for f in files if os.path.exists(f)]
    if not existing_files:
        print(f"⚠️ Chương {C}: không tìm thấy file nguồn, bỏ qua.")
        continue

    try:
        # Parse file đầu tiên làm gốc
        tree = ET.parse(existing_files[0])
        root = tree.getroot()

        # Duyệt các file còn lại và thêm nội dung vào root
        for f in existing_files[1:]:
            tree_tmp = ET.parse(f)
            root_tmp = tree_tmp.getroot()
            for question in root_tmp.findall('question'):
                root.append(question)

        # Ghi kết quả ra file mới
        output_file = f"XMLdata/questions-VAA-C{C}.xml"
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        print(f"Chương {C}: đã hợp nhất xong, file kết quả: {output_file}")

    except ET.ParseError as e:
        print(f"❌ Chương {C}: lỗi khi parse XML: {e}")
    except Exception as e:
        print(f"❌ Chương {C}: lỗi không mong muốn: {e}")
