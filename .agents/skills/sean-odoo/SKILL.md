---
name: sean-odoo
description: Implement Sean Music Odoo 20 custom models, controllers, access rules and commission logic while preserving native website_sale and historical business data.
---

# Phát triển Odoo đúng đường thực thi

Tìm entrypoint → controller/model → quyền → template hoặc action, chỉ đọc phần
liên quan. Dùng extension của custom module, không vá `odoo/`.
Đọc `odoo/skills/odoo-guidelines/SKILL.md` cùng guideline đúng loại file;
đụng quyền/route công khai thì đọc thêm `odoo/skills/odoo-security/SKILL.md`.
Các skill upstream tham chiếu lẫn nhau: mở đường dẫn gốc và reference cần thiết,
không copy một `SKILL.md` lẻ làm mất dependencies.

## Invariant riêng dự án

- Website: tái dùng `website_sale`, domain sản phẩm của website, pricelist,
  cart và checkout; không tạo hệ giá hoặc giỏ song song trong JavaScript.
- Inquiry: public không có ACL trực tiếp. `sudo().create()` chỉ nhận field scalar
  allowlist đã validate; company/website lấy từ request, không từ POST.
  Giữ CSRF, honeypot và hạn gửi; hạn theo session không phải chống spam toàn hệ thống.
- Đàn cũ: giữ `unknown` mặc định; không đổi nghĩa field hoặc tự backfill tình trạng.
- Hoa hồng: đọc `sean_music_collaborator/models/sale_order.py`, `commission.py`
  và `commission_plan.py`. Chứng từ được tạo khi xác nhận nhưng có thể bị tính lại,
  kể cả đã trả; không gọi đó là snapshot bất biến. Khi sửa luồng này, chốt chính sách
  lịch sử/đổi người hưởng và test quyền user thường; không sửa bằng `sudo()` rộng.
- Giá: homepage hiện dùng `list_price`, chưa đồng nhất chắc chắn với pricelist ở
  shop/giỏ. Phân biệt invariant mong muốn và implementation hiện tại.
- Quyền Odoo 20: kiểm tra ACL hợp nhất `ir.access` trong checkout; không suy luận
  ý nghĩa dòng không có group theo thói quen phiên bản cũ.
- Python/controller/XML phải dùng API đúng checkout Odoo 20; không áp ví dụ phiên
  bản cũ mà chưa xem implementation. Escape nội dung người dùng trong QWeb.

Khi thay model/ACL/manifest, xác định có cần update module và dữ liệu migration.
Không chạy `create_sample_data.py` hoặc `configure_vietnamese_store.py` như test:
chúng thay dữ liệu. Không in secret từ `odoo.conf` hay sửa currency kế toán.

Chọn kiểm thử theo rủi ro: ORM/access/route cho logic và quyền, browser cho trạng
thái người dùng. Dùng DB test/local được xác nhận; lệnh update module là mutation.
Xem cách chạy và giới hạn ở `custom_addons/sean_music_store/README.md` và
`sean-acceptance/SKILL.md`. Báo file đã sửa, hành vi thay đổi và kiểm thử thực tế.

Đọc [các rủi ro đã quan sát](references/project-risks.md) khi đụng giá, hoa hồng,
quyền nhiều công ty hoặc webclient; đây là nhận định tĩnh, chưa phải bug đã tái hiện.
