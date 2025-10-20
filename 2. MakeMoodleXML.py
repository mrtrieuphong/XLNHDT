import xml.etree.ElementTree as ET
from xml.dom import minidom
import re
import os

def parse_new_questions(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        questions_data = []
        
        for q_elem in root.findall('question'):
            options = []
            options_elem = q_elem.find('options')
            if options_elem is not None:
                for opt_elem in options_elem.findall('option'):
                    raw = (opt_elem.text or "").strip()

                    # 1) Ưu tiên lấy từ thuộc tính label (XML của bạn có)
                    label_attr = (opt_elem.get('label') or "").strip()
                    if label_attr:
                        letter = label_attr.upper()
                        text = raw
                    else:
                        # 2) Fallback: hỗ trợ "A. ..." / "A) ..." / "A ... "
                        m = re.match(r'\s*([A-D])[\.\)]?\s*(.*)$', raw, re.DOTALL | re.IGNORECASE)
                        if m:
                            letter = m.group(1).upper()
                            text = m.group(2).strip()
                        else:
                            # 3) Cuối cùng: gán tuần tự A, B, C, D nếu không nhận diện được
                            letter = chr(ord('A') + len(options))
                            text = raw

                    options.append({'letter': letter, 'text': text})

            question_info = {
                'id': q_elem.get('id'),
                'text': (q_elem.find('text').text or "").strip(),
                'level': (q_elem.find('level').text or "").strip(),
                'correct_answer_letter': (q_elem.find('answer').text or "").strip().upper(),
                'options': options
            }
            questions_data.append(question_info)
            
        return questions_data
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy tệp '{file_path}'")
        return None
    except ET.ParseError:
        print(f"Lỗi: Không thể phân tích tệp XML '{file_path}'")
        return None

def create_moodle_xml(questions):
    """
    Tạo nội dung tệp Moodle XML từ dữ liệu câu hỏi đã được phân tích.
    """
    if not questions:
        return ""

    # Tự động xác định mã danh mục từ ID câu hỏi đầu tiên (ví dụ: C1K3L4Q24)
    first_id = questions[0]['id']
    match = re.match(r"(C\d+)(K\d+)(L\d+)", first_id)
    if not match:
        print("Lỗi: Không thể xác định mã danh mục từ ID câu hỏi.")
        return ""
        
    cat_c, cat_k, cat_l = match.groups()
    chapter_num = cat_c[1:]
    k_num = cat_k[1:]
    level_num = cat_l[1:]

    # Bắt đầu xây dựng chuỗi XML
    xml_output_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<quiz>'
    ]

    # --- Thêm các câu hỏi danh mục ---
    category_template = """
  <question type="category">
    <category>
      <text>{path}</text>
    </category>
    <info format="html">
      <text><![CDATA[<p>{name}</p>]]></text>
    </info>
    <idnumber>{id}</idnumber>
  </question>"""
    
    xml_output_lines.append(category_template.format(path=f"$module$/top/{cat_c}", name=f"Chương {chapter_num}", id=cat_c))
    xml_output_lines.append(category_template.format(path=f"$module$/top/{cat_c}/{cat_k}", name=f"Chuẩn đầu ra K{k_num}", id=f"{cat_c}{cat_k}"))
    xml_output_lines.append(category_template.format(path=f"$module$/top/{cat_c}/{cat_k}/{cat_l}", name=f"Cấp độ {level_num}", id=f"{cat_c}{cat_k}{cat_l}"))

    # --- Thêm các câu hỏi trắc nghiệm ---
    question_template = """
  <question type="multichoice">
    <name>
      <text>Câu {q_num}:</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p>{q_text}</p>]]></text>
    </questiontext>
    <generalfeedback format="html"><text/></generalfeedback>
    <defaultgrade>1.0000000</defaultgrade>
    <penalty>0.3333333</penalty>
    <hidden>0</hidden>
    <idnumber>{q_id}</idnumber>
    <single>true</single>
    <shuffleanswers>true</shuffleanswers>
    <answernumbering>ABCD</answernumbering>
    <showstandardinstruction>0</showstandardinstruction>
    <correctfeedback format="html">
      <text><![CDATA[<p>Your answer is correct.</p>]]></text>
    </correctfeedback>
    <partiallycorrectfeedback format="html">
      <text><![CDATA[<p>Your answer is partially correct.</p>]]></text>
    </partiallycorrectfeedback>
    <incorrectfeedback format="html">
      <text><![CDATA[<p>Your answer is incorrect.</p>]]></text>
    </incorrectfeedback>
    <shownumcorrect/>{answers_block}
  </question>"""

    answer_template = """
    <answer fraction="{fraction}" format="html">
      <text><![CDATA[<p>{ans_text}</p>]]></text>
      <feedback format="html"><text/></feedback>
    </answer>"""

    for q in questions:
        q_num_match = re.search(r'Q(\d+)$', q['id'])
        q_num = q_num_match.group(1) if q_num_match else ""
        
        answers_block = ""
        for option in q['options']:
            fraction = "100" if option['letter'] == q['correct_answer_letter'] else "0"
            answers_block += answer_template.format(fraction=fraction, ans_text=option['text'])
        
        xml_output_lines.append(
            question_template.format(
                q_num=q_num,
                q_text=q['text'],
                q_id=q['id'],
                answers_block=answers_block
            )
        )

    xml_output_lines.append('</quiz>')
    
    # Kết hợp các dòng thành một chuỗi duy nhất và định dạng lại
    # Sử dụng minidom để làm đẹp XML, giúp dễ đọc hơn
    rough_string = "".join(xml_output_lines)
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ", encoding="UTF-8").decode()

    return pretty_xml

# --- Chương trình chính ---
if __name__ == "__main__":
    import os, re
    from glob import glob

    input_dir = "hanh_vi_to_chuc"
    output_dir = os.path.join("XMLdata", "hanh_vi_to_chuc")
    os.makedirs(output_dir, exist_ok=True)

    input_files = sorted(glob(os.path.join(input_dir, "*_raw.xml")))
    if not input_files:
        print(f"⚠️ Không tìm thấy file *_raw.xml trong thư mục '{input_dir}'.")
        raise SystemExit(0)

    total_questions = 0

    for input_file in input_files:
        base = os.path.basename(input_file)
        code = re.sub(r'_raw\.xml$', '', base)  # ví dụ: C1K1L1_raw.xml -> C1K1L1
        output_file = os.path.join(output_dir, f"questions-VAA-{code}.xml")

        # 1) Đọc và phân tích các câu hỏi mới
        new_questions = parse_new_questions(input_file)
        if not new_questions:
            print(f"⚠️ Bỏ qua '{base}' (không đọc được câu hỏi).")
            continue

        # 2) Tạo nội dung XML theo cấu trúc Moodle
        moodle_xml_content = create_moodle_xml(new_questions)
        if not moodle_xml_content:
            print(f"⚠️ Bỏ qua '{base}' (không tạo được Moodle XML).")
            continue

        # 3) Ghi ra tệp đích
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(moodle_xml_content)
            print(f"✅ {base} → {output_file} ({len(new_questions)} câu hỏi)")

            # In dải QID để đối chiếu nhanh
            try:
                start_id = int(new_questions[0]['id'].split('Q')[-1])
                end_id = int(new_questions[-1]['id'].split('Q')[-1])
                count_range = end_id - start_id + 1
                print(f"   Dải ID: {new_questions[0]['id']} → {new_questions[-1]['id']} (~{count_range} vị trí, {len(new_questions)} câu hợp lệ)")
            except Exception:
                pass

            total_questions += len(new_questions)
        except IOError:
            print(f"❌ Lỗi: Không thể ghi vào tệp '{output_file}'")

    print(f"\nHoàn tất. Tổng số câu hỏi đã xuất: {total_questions}")