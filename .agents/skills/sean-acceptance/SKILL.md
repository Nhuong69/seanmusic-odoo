---
name: sean-acceptance
description: Verify substantial Sean Music storefront or business flow changes using observable browser, data and access evidence and an explicit 9/10 acceptance rubric.
---

# Nghiệm thu bằng hành vi và bằng chứng

Chọn kiểm tra tương xứng với diff. Sửa tài liệu/config thì kiểm tra cấu trúc, link,
discovery nếu có và mô phỏng quyết định; không gọi đó là nghiệm thu website.
Đổi giao diện/logic thì kiểm tra hành trình liên quan và ít nhất một trạng thái lỗi.

## Kiểm tra đang có và tác dụng phụ

Chạy từ root dự án. Đọc script trước nếu nó đã đổi.

```sh
# Server local mặc định http://127.0.0.1:8079; không tạo giỏ/inquiry.
.venv/bin/python scripts/checks/verify_store_local.py

# Ngoài giỏ, tạo inquiry có nhãn kiểm thử.
.venv/bin/python scripts/checks/verify_store_local.py --allow-writes --submit-inquiry

# Cần inquiry mẫu từ lệnh trên; script có assertion DB db_seanmusic.
.venv/bin/python odoo/odoo-bin shell -c seanmusic.conf --no-http < scripts/checks/verify_store_data.py
```

Các lệnh này không xác nhận đơn/thanh toán thật. Chỉ bật `--allow-writes` với DB
local disposable; có thể đổi server bằng `--base-url`. Script HTTP kiểm tra ngôn ngữ,
lọc giá, search, giỏ, CSRF và validation; không kiểm tra layout bằng screenshot.
Script data giả định fixture 31 sản phẩm và website ID 1: khi fixture đổi, kiểm tra
nguyên nhân thay vì ép dữ liệu khớp assertion. Không xóa đơn/inquiry của người khác
để dọn test; ghi nhận record test do mình tạo khi cần truy vết.

Nếu server chưa chạy, xác định DB/port đang dùng trước khi bật. Khi cần update:
`.venv/bin/python odoo/odoo-bin -c seanmusic.conf -u sean_music_store --stop-after-init --no-http`
chỉ dùng với DB local được xác nhận cho công việc. Dùng `-i` khi cài mới theo README.
Không thay seed/currency để làm test xanh.

Kiểm tra tổ chức dự án không cần DB: `.venv/bin/python -m unittest discover -s tests -v`.
Suite addon riêng: `scripts/checks/run_odoo_tests.py --create-test-db`; runner chỉ tạo
DB mới có tiền tố `db_seanmusic_test_`, không xóa DB sau test và không đụng DB làm việc.

## Bằng chứng kết thúc

Ghi kết quả pass/fail/not run, lệnh hoặc bước tái hiện, ảnh hiện tại khi có đổi bố
cục, trạng thái dữ liệu sau thao tác và giới hạn còn lại. Ảnh cũ không thay kiểm tra mới.
Thay quyền/hoa hồng cần test theo role và transition tương ứng, không chỉ smoke test UI.

Đọc [scorecard](references/scorecard.md) khi đánh giá mục tiêu 9/10. Mục chưa kiểm tra
ghi chưa đánh giá; không cho điểm giả. Lỗi nghiêm trọng về giá, dữ liệu, quyền hoặc
luồng mua chính chặn nghiệm thu dù điểm hình thức cao.
