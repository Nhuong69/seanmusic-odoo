---
name: sean-design
description: Design and refine Sean Music QWeb/SCSS storefront pages with distinct instrument retail identity, truthful Vietnamese content and usable mobile flows.
---

# Thiết kế Sean Music có chủ đích

Trước khi sửa giao diện, xem template/SCSS hiện tại và ảnh giao diện nếu có.
`artifacts/redesign-preview/` là ảnh baseline đã lưu, không chứng minh website hiện tại.
Xác định nhiệm vụ của trang và một hướng mỹ thuật bằng 2–3 câu; không cần tạo tài
liệu riêng cho chỉnh sửa nhỏ.

## Bản sắc đang có

- Tên Sean Music; xanh đậm `--sean-ink`, điểm nhấn cam `--sean-orange`, nền sáng
  `--sean-paper`, hình nhạc cụ. Token nằm trong
  `custom_addons/sean_music_store/static/src/scss/store.scss`.
- Giữ ngôn ngữ hình ảnh hiện có trừ khi yêu cầu đổi thương hiệu. Bản sắc đến từ
  ảnh, nhịp bố cục và nội dung nhạc cụ; không phải từ việc đổi font tùy tiện.
- Kiểm tra dấu tiếng Việt và khả năng đọc trước khi thêm font; font hệ thống hiện
  tại hợp lệ. Không biến lời khuyên “tránh font phổ biến” thành lệnh cấm tuyệt đối.

## Quyết định theo nhiệm vụ

- Trang chủ: một trọng tâm thị giác, lối vào danh mục/ngân sách rõ, ít CTA cạnh tranh.
- Danh mục: scan nhanh ảnh, tên model, giá, tình trạng; giữ grid sản phẩm vì đây là
  cấu trúc mua sắm hữu ích. Bộ lọc phải có trạng thái chọn/bỏ chọn/không kết quả.
- Chi tiết: ảnh lớn, thông tin quyết định mua và hành động gần nhau. Đặt ghi chú
  ảnh tham chiếu/tình trạng chưa xác nhận nơi khách nhìn thấy trước khi quyết định.
- Biểu mẫu: nhãn rõ, lỗi sát trường, giữ dữ liệu sau lỗi; không dùng toast thay
  cho việc lưu thật. Chỉ thêm Zalo/điện thoại khi có thông tin đã xác nhận.
- Viết tiếng Việt như nhân viên tư vấn: nói loại đàn, nhu cầu, điều kiện cụ thể.
  Tránh lời hứa “đỉnh cao”, “số 1”, review/số liệu khống và giảm giá giả.

Tránh bố cục quảng cáo SaaS lặp lại, nền gradient/trang trí vô cớ, quá nhiều badge
và animation cản mua hàng. Card, gradient hay animation được dùng khi có lý do
phù hợp; không có danh sách cấm theo mốt. Không tạo ảnh chứng minh tình trạng hàng bằng AI.

## Triển khai và kiểm tra

Dùng QWeb kế thừa và SCSS giới hạn scope `.o_sean_music_store`; xem hướng dẫn
SCSS/assets tại `odoo/skills/odoo-web-guidelines/SKILL.md` khi liên quan.
Không phá selector/data-attribute của giỏ/checkout Odoo.

Với thay đổi bố cục, xem trang chạy thật ở khoảng 390px và 1440px, kiểm tra thêm
320px hoặc zoom khi có nguy cơ tràn. Đi qua tìm → lọc → chi tiết → giỏ/tư vấn.
Kiểm tra bàn phím, focus, label, tương phản và giảm chuyển động nếu có animation.
Báo ảnh/luồng đã xem và lỗi còn lại; nếu không có browser, không tự nhận đã kiểm tra hình ảnh.
