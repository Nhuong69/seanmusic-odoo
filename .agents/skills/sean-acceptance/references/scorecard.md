# Thang nghiệm thu Sean Music

Đây là tiêu chí dự án đề xuất ngày 06/11/2026, không phải chứng nhận bên ngoài.
Chỉ chấm các hạng mục đã có bằng chứng. Khi thiếu hạng mục, báo tỷ lệ đã đánh giá
và điểm trên phần đó, không gọi là đạt 9/10 tổng thể.

Chọn phạm vi trước khi chấm: storefront gồm UI/hành trình khách; backend thuần
nghiệp vụ không đổi UI. Với backend, hai mục hình ảnh/mobile là không áp dụng (N/A),
khác với hạng mục có áp dụng nhưng chưa kiểm tra. Không bỏ mục sau khi thấy kết quả xấu.

| Hạng mục | Storefront | Backend | Bằng chứng cần có cho mức tốt |
| --- | ---: | ---: | --- |
| Nghiệp vụ sát thực tế | 25 | 35 | Dữ liệu có nguồn; trạng thái chưa biết; ai xử lý sau khi gửi; luồng lỗi |
| Chức năng xuyên suốt | 25 | 30 | Storefront: tìm/lọc → chi tiết → giỏ/tư vấn → dữ liệu lưu. Backend: transition → dữ liệu/chứng từ → báo cáo; hồi quy liên quan |
| Bản sắc và nội dung | 20 | N/A | Screenshot mới; ảnh đúng ngữ cảnh; tiếng Việt cụ thể; phân cấp rõ; không bịa cam kết |
| Mobile và khả năng tiếp cận | 15 | N/A | Luồng ở 390px; không tràn ở 320px khi liên quan; keyboard/focus/label/contrast |
| Độ tin cậy và khả năng bảo trì | 15 | 35 | Role/ACL/CSRF khi liên quan; giữ native Odoo; lịch sử/tiền tệ khi liên quan; test có thể lặp |

Chấm mỗi hạng mục 0–10; tổng = tổng(điểm × trọng số)/100.
Mốc: 0–3 hỏng/không có; 4–6 hoạt động một phần; 7–8 luồng chính và lỗi cơ bản tốt;
9–10 có bằng chứng cả trạng thái biên quan trọng và reviewer độc lập không còn lỗi lớn.

Điều kiện đạt: tổng ≥9.0, không hạng mục áp dụng nào dưới 8, không còn lỗi chặn bên dưới.
Không tự suy ra điểm từ việc một script chạy thành công.
Ghi rõ “9/10 phạm vi backend” khi dùng cột backend, không gọi đó là điểm website.
Chỉnh sửa nhỏ chỉ báo tiêu chí liên quan đạt/chưa đạt; không cố cho điểm cả website.

Lỗi chặn: lộ dữ liệu khách; sai giá/tổng tiền; bịa tồn kho/kiểm định/bảo hành;
CTA chính không hoạt động; gửi form không lưu nhưng báo thành công; mất dữ liệu;
luồng chính không dùng được trên mobile/keyboard. Chưa kiểm thử live payment thì
báo riêng, không xác nhận phần đó đã đạt yêu cầu vận hành.

Mẫu kết luận: phạm vi; bằng chứng; bảng điểm; lỗi còn lại; chưa kiểm tra; quyết định
đạt/chưa đạt. Việc tạo bộ skill chỉ chứng minh cấu hình/hướng dẫn, không chứng minh
website hay trải nghiệm người dùng đã đạt 9/10.
