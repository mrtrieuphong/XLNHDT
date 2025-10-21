import os
import xml.etree.ElementTree as ET
from glob import glob

# Patterns (dùng glob để khớp cả trường hợp có hoặc không có segment "S<number>" giữa K và L)
file_patterns = [
    "XMLdata/hanh_vi_to_chuc/questions-VAA-C{}K1*L1.xml",
    "XMLdata/hanh_vi_to_chuc/questions-VAA-C{}K2*L2.xml",
    "XMLdata/hanh_vi_to_chuc/questions-VAA-C{}K3*L3.xml",
    # thêm hoặc bỏ comment các pattern khác nếu cần
]

def merge_chapter_files(chapter_number: int):
    Cstr = str(chapter_number)
    files = []
    for p in file_patterns:
        files.extend(sorted(glob(p.format(Cstr))))

    # Lọc những file thật sự tồn tại và loại trùng, giữ thứ tự
    existing_files = sorted(dict.fromkeys(f for f in files if os.path.exists(f)))
    if not existing_files:
        print(f"⚠️ Chương {chapter_number}: không tìm thấy file nguồn, bỏ qua.")
        return

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
        output_file = f"XMLdata/questions-VAA-C{chapter_number}.xml"
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        print(f"Chương {chapter_number}: đã hợp nhất xong, file kết quả: {output_file}")

    except ET.ParseError as e:
        print(f"❌ Chương {chapter_number}: lỗi khi parse XML: {e}")
    except Exception as e:
        print(f"❌ Chương {chapter_number}: lỗi không mong muốn: {e}")


if __name__ == '__main__':
    # Chạy từ Chương 1 tới Chương 9 (nếu cần tới 10 đổi range thành (1, 11))
    for C in range(1, 10):
        merge_chapter_files(C)
