---
name: sean-product
description: Turn Sean Music feature requests into realistic Vietnamese instrument retail flows, data requirements and observable acceptance criteria before implementation.
---

# Tính năng sát vận hành cửa hàng

Đọc model/controller/template liên quan. Tách “đã có trong code”, “đã kiểm thử” và
“đề xuất”. Không coi nút bấm hoặc trang mẫu là một nghiệp vụ hoàn chỉnh.

Với tính năng đáng kể, chốt ngắn gọn: ai sử dụng, họ cần quyết định gì, dữ liệu từ
đâu, ai cập nhật, kết quả được lưu ở đâu, trạng thái lỗi và tiêu chí thành công.
Nếu thiếu dữ kiện không chặn triển khai, ghi giả định có thể sửa và tiếp tục.

Áp dụng các tình huống thực của dự án:

- Khách mới tìm đàn theo ngân sách/loại nhạc cụ; lọc, bỏ lọc, không có kết quả,
  quay lại danh sách phải dễ hiểu. Không tự thêm chatbot để thay bộ lọc.
- Khách mua đàn cũ cần tình trạng từng món, ảnh thật, phụ kiện và điều kiện mua.
  Hiện model mới có `sean_condition`, `sean_condition_notes`, `sean_image_source`;
  thông tin bảo hành/kiểm định/tồn kho chưa có chứng cứ thì ghi cần xác nhận.
- Giá, số lượng và tổng giỏ phải đi qua logic Odoo. Chưa thử thanh toán thật thì
  nghiệm thu đến bước được phép và nói rõ giới hạn đó.
- Tư vấn: `/lien-he/gui` lưu `sean.music.inquiry`; cần kiểm tra thông tin sai,
  gửi lại, nội dung quá dài, thành công và nhân viên thấy được yêu cầu.
  “Đã nhận” không đồng nghĩa đã gọi lại hoặc đã gửi email.
- Hoa hồng: phân biệt ước tính, chứng từ lúc xác nhận và khoản thực tế đã chi.
  Chứng từ hiện còn có thể bị tính lại sau khi đã trả, chưa là snapshot bất biến.
  Đọc [rủi ro lịch sử và quyền](../sean-odoo/references/project-risks.md) trước khi
  chốt task hoa hồng; tách người hưởng doanh số, người đã nhận tiền và nghĩa vụ còn lại.

Viết tiêu chí theo Given/When/Then hoặc bảng trạng thái, gắn bằng chứng có thể quan sát.
Ví dụ: tình trạng `unknown` → hiện “Cần xác nhận tình trạng”; không thêm badge kiểm định.
Ưu tiên luồng chính hoạt động xuyên suốt; không biến mọi ý tưởng thành tính năng bắt buộc.

Handoff cho người làm: mục tiêu, dữ liệu thật/thiếu, trạng thái, file dự kiến,
tiêu chí kiểm chứng. Với thay đổi lớn, dùng scorecard trong `sean-acceptance`.
