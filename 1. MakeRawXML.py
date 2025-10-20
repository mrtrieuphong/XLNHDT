import re
import xml.etree.ElementTree as ET

# Dữ liệu đầu vào dạng văn bản (dán toàn bộ nội dung đề từ file txt hoặc chuỗi)
raw_text = """
Câu 291: Văn hóa sẽ được hình thành trong tất cả các trường hợp dưới đây, ngoại trừ…. (cấp độ 3)
A. Các nhà sáng lập chỉ thuê mướn và giữ lại những nhân viên nào có suy nghĩ và cảm nhận giống họ.
B. Các nhà sáng lập khắc vào trí não nhân viên và xã hội hóa họ theo cách họ suy nghĩ và cảm nhận.
C. Các nhà sáng lập giữ kín viễn cảnh, chiến lược đối với tất cả nhân viên của tổ chức.
D. Hành vi và hành động của các nhà sáng lập là những khuôn mẫu khuyến khích nhân viên trở nên giống họ và qua đó nhân viên cũng thấm nhuần những niềm tin của họ.
Đáp án: C
Câu 292: Bạn là tư vấn văn hóa tổ chức cho một công ty khởi nghiệp trong ngành dịch vụ. Ban lãnh đạo muốn xây dựng một môi trường làm việc cởi mở, khuyến khích chia sẻ và giảm tính hình thức. Họ đưa ra ví dụ về AirAsia, nơi nhân viên không bị yêu cầu mặc đồng phục nghiêm ngặt, thường xuyên tổ chức tiệc, thảo luận thoải mái và không có nhiều cấp bậc trong quản lý. Dựa trên kiến thức về hành vi tổ chức, bạn sẽ phân tích mô hình văn hóa nào phù hợp nhất với định hướng này? (cấp độ 3)
A. Chủ nghĩa cá nhân và kiểm soát nghiêm ngặt
B. Tư tưởng phân cấp quyền lực rõ ràng
C. Chủ nghĩa tập thể và khoảng cách quyền lực thấp
D. Nền văn hóa né tránh rủi ro cao
Đáp án: C
Câu 293: Bạn được mời đến tư vấn cho một công ty đang gặp khó khăn trong việc duy trì văn hóa tổ chức tích cực sau khi thay đổi lãnh đạo. Người tiền nhiệm thường xuyên tương tác, lan tỏa giá trị cởi mở, trao quyền cho nhân viên. Tuy nhiên, lãnh đạo mới lại áp dụng phong cách kiểm soát chặt chẽ, ít chia sẻ thông tin. Dựa trên kiến thức hành vi tổ chức, bạn sẽ phân tích vai trò nào của lãnh đạo là quan trọng nhất trong việc duy trì hoặc thay đổi văn hóa tổ chức? (cấp độ 3)
A. Lãnh đạo không liên quan đến sự hình thành văn hóa
B. Lãnh đạo chỉ đảm bảo quy trình, không tác động đến giá trị tổ chức
C. Lãnh đạo truyền bá, củng cố hoặc thay đổi các giá trị văn hóa cốt lõi thông qua hành vi, quyết định và tương tác
D. Nhân viên là yếu tố duy nhất quyết định toàn bộ văn hóa tổ chức
Đáp án: C
Câu 294: Trong một tổ chức, nhân viên thường làm việc độc lập, ít chia sẻ thông tin với nhau. Tuy nhiên, các quản lý lại linh hoạt trong việc phân công nhiệm vụ để thích nghi với từng tình huống. Loại văn hóa tổ chức nào phản ánh đúng đặc điểm trên? (cấp độ 3)
A. Văn hóa mạng lưới
B. Văn hóa cộng đồng
C. Văn hóa phân tán
D. Văn hóa vụ lợi
Đáp án: C
Câu 295: Một tổ chức muốn xây dựng văn hóa “lấy khách hàng làm trung tâm”, nhưng hiện tại hệ thống đánh giá nhân viên chỉ tập trung vào năng suất nội bộ (ví dụ: số lượng sản phẩm hoàn thành). Là nhà quản lý, bạn nên làm gì để điều chỉnh hệ thống quản lý nhằm định hướng lại văn hóa tổ chức? (cấp độ 3)
A. Tăng lương cho nhân viên hoàn thành công việc đúng thời hạn
B. Tổ chức hội thảo về tầm quan trọng của khách hàng nhưng giữ nguyên hệ thống đánh giá hiện tại
C. Cập nhật tiêu chí đánh giá nhân viên, bổ sung các chỉ số về mức độ hài lòng của khách hàng và kỹ năng phục vụ
D. Đưa ra khẩu hiệu “Khách hàng là thượng đế” nhưng không thay đổi hệ thống khen thưởng
Đáp án: C
Câu 296: Một công ty đang gặp khó khăn trong việc thúc đẩy tinh thần hợp tác và chia sẻ thông tin giữa các phòng ban. Nhân viên có xu hướng làm việc độc lập, theo chức năng chuyên môn riêng biệt. Là nhà quản lý, bạn nên áp dụng giải pháp nào sau đây để thay đổi văn hóa theo hướng hợp tác và cởi mở hơn? (cấp độ 3)
A. Tăng cường giám sát và yêu cầu nhân viên báo cáo chéo giữa các bộ phận
B. Thay đổi cơ cấu từ mô hình chức năng sang mô hình làm việc theo nhóm dự án
C. Bổ sung thêm quy định xử phạt các hành vi thiếu hợp tác
D. Tổ chức nhiều hoạt động gắn kết ngoài giờ như du lịch, dã ngoại
Đáp án: B
Câu 297: Một doanh nghiệp muốn chuyển từ văn hóa làm việc bảo thủ sang văn hóa sáng tạo và linh hoạt. Tuy nhiên, do đặc thù ngành, họ không thể nhanh chóng thay đổi đội ngũ hiện tại. Dựa trên phương pháp thay đổi văn hóa tổ chức, giải pháp nào sau đây là phù hợp nhất trong hoàn cảnh này? (cấp độ 3)
A. Giữ nguyên nhân sự và chờ thế hệ lãnh đạo tiếp theo tự điều chỉnh
B. Sa thải hàng loạt nhân viên cũ để tuyển mới hoàn toàn
C. Tập trung tổ chức các chương trình đào tạo nhằm thay đổi nhận thức và hành vi của nhân viên
D. Áp đặt các quy định mới buộc nhân viên phải tuân theo
Đáp án: C
Câu 298: Một doanh nghiệp khởi nghiệp đang phát triển nhóm sản phẩm mới. Quá trình làm việc cần nhiều sự trao đổi, hỗ trợ và tinh thần học hỏi giữa các thành viên. Nhà quản lý nên lựa chọn duy trì loại văn hóa nào để phù hợp nhất với đặc điểm này? (cấp độ 3)
A. Văn hóa vụ lợi
B. Văn hóa mạng lưới
C. Văn hóa phân tán
D. Văn hóa cộng đồng
Đáp án: B
Câu 299: Bạn là quản lý tuyển dụng cho một công ty có văn hóa vụ lợi mạnh. Để nhân viên gắn bó và phát huy tốt trong môi trường này, bạn nên ưu tiên chọn ứng viên có đặc điểm nào sau đây? (cấp độ 3)
A. Ưa làm việc nhóm, không đề cao thành tích cá nhân
B. Có mục tiêu cá nhân rõ ràng và khả năng cạnh tranh cao
C. Thoải mái với việc hỗ trợ đồng nghiệp dù không có lợi ích trực tiếp
D. Không quan tâm đến lương thưởng, chỉ cần môi trường ổn định
Đáp án: B
Câu 300: Một tổ chức có mục tiêu nâng cao sự gắn kết, tinh thần học hỏi và làm việc nhóm giữa các nhân viên. Tuy nhiên, họ gặp khó khăn trong việc duy trì những giá trị này trong thời gian dài. Tổ chức đó khả năng cao đang theo đuổi loại hình văn hoá nào? (cấp độ 3)
A. Văn hóa vụ lợi
B. Văn hóa mạng lưới
C. Văn hóa phân tán
D. Văn hóa cộng đồng
Đáp án: D 
"""

code = "C9K3L3"
# Chương ,Chuẩn đầu ra, Cấp độ 

# Lấy cấp độ từ chữ L trong code (ví dụ C1K4L4 -> level = "4")
mL = re.search(r'L\s*(\d+)', code, flags=re.IGNORECASE)
level_from_code = mL.group(1) if mL else "1"

# Regex: (Cấp độ X) là tùy chọn; options là các dòng bắt đầu bằng A/B/C/D
pattern = re.compile(
    r'Câu\s*(?P<num>\d+)\s*[:\.]?\s*'                              # số câu
    r'(?P<text>.*?)'                                                # nội dung câu hỏi (non-greedy)
    r'(?:\(\s*Cấp\s*độ\s*(?P<level>\d+)\s*\))?\s*'                 # (Cấp độ X) tùy chọn (không dùng nữa)
    r'(?P<options>(?:^[A-D][\.\)]\s*.*?(?:\n|$))+?)'                # block phương án
    r'\s*Đáp\s*án\s*:\s*(?P<answer>[A-D])',                         # đáp án
    re.DOTALL | re.IGNORECASE | re.MULTILINE
)

opt_splitter = re.compile(
    r'([A-D])[\.\)]\s*(.*?)(?=\n[A-D][\.\)]|\Z)', re.DOTALL
)

matches = list(pattern.finditer(raw_text))

questions_el = ET.Element("questions")

if not matches:
    print("⚠️ Không tìm thấy câu hỏi nào. Kiểm tra xem văn bản có đúng định dạng không (đặc biệt là cụm '(Cấp độ X)' hiện đã là TÙY CHỌN).")

for m in matches:
    num = m.group('num')
    text = m.group('text').strip()
    # dùng level lấy từ code
    level = level_from_code
    options_block = m.group('options')
    answer = m.group('answer').upper().strip()

    q_id = f"{code}Q{num}"
    q_el = ET.SubElement(questions_el, "question", id=q_id)
    ET.SubElement(q_el, "text").text = text
    ET.SubElement(q_el, "level").text = level

    opts_el = ET.SubElement(q_el, "options")
    for label, opt_text in opt_splitter.findall(options_block):
        ET.SubElement(opts_el, "option", label=label).text = opt_text.strip()

    ET.SubElement(q_el, "answer").text = answer

# Ghi ra file XML + in ra màn hình để bạn kiểm tra nhanh
tree = ET.ElementTree(questions_el)
ET.indent(tree, space="  ", level=0)
out_path = f"{code}_raw.xml"
tree.write(out_path, encoding="utf-8", xml_declaration=True)

print(f"✅ Đã trích xuất {len(matches)} câu hỏi.")
print(f"Đã lưu XML: {out_path}\n")