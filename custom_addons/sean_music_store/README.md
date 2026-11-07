# Sean Music - giao diện cửa hàng tiếng Việt

Module Odoo 20 cho website Sean Music: trang chủ, danh mục, thông tin sản phẩm,
hướng dẫn chọn đàn, liên hệ và chính sách mua hàng. Sử dụng giỏ hàng, tài khoản,
bộ lọc và quy trình thanh toán sẵn có của Odoo.

## Chạy local

Từ root dự án; xem `README.md` ở root để tạo venv/config và cài dependencies.
DB đã có chỉ cần:

```sh
.venv/bin/python odoo/odoo-bin -c seanmusic.conf
```

Mở http://127.0.0.1:8079/. Chỉ cài mới với `-i sean_music_store` trên DB mới;
chỉ dùng `-u sean_music_store` khi thay module cần update. Không tự chạy script
dữ liệu mỗi lần khởi động. Các script đó chuyển sang `scripts/data/`, chỉ hỗ trợ
fixture local `db_seanmusic`; xem `scripts/README.md` trước khi sử dụng.

## Kiểm chứng local

```sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/checks/verify_store_local.py --base-url http://127.0.0.1:8079
```

HTTP mặc định không tạo giỏ/inquiry. Chỉ trên DB test disposable, bật
`--allow-writes --submit-inquiry` để kiểm tra ghi (tạo giỏ nháp và yêu cầu có nhãn
**Kiểm thử giao diện local**, không thanh toán/xác nhận đơn). Kiểm tra fixture DB
bằng Odoo shell với `scripts/checks/verify_store_data.py` sau khi tạo inquiry mẫu.
Suite addon độc lập: `scripts/checks/run_odoo_tests.py --create-test-db`.
Ảnh chụp lịch sử chuyển sang `artifacts/redesign-preview/`.

## Dữ liệu và những thông tin cần hoàn thiện

- Danh mục được sắp theo guitar điện, guitar mộc, bass, trống và ampli.
- Bảng giá VND dùng các mức giá số hiện có trong dữ liệu, có các quy tắc giá cố
  định cho từng sản phẩm. Không thay đổi tiền tệ kế toán của công ty.
- Không tự xác nhận hàng mới/cũ, tỷ lệ ngoại hình, kiểm định, tồn kho hoặc bảo hành.
  Cập nhật các trường ở tab **Thông tin đàn cũ** trong biểu mẫu sản phẩm.
- Các sản phẩm có mã GUITAR-/DRUM-/AMP-/SEAN- được hiển thị trên bản local.
- Thông tin liên hệ đọc từ hồ sơ công ty. Không hiển thị email và điện thoại mẫu.
- Chưa cấu hình hay thử giao dịch thanh toán thực tế.
- Biểu mẫu tại `/lien-he` lưu yêu cầu trong Odoo; xem tại ứng dụng Trang web >
  Tư vấn Sean Music. Có kiểm tra đầu vào, CSRF và giới hạn gửi theo phiên.
  Khách công khai không được đọc hay sửa các yêu cầu.
- Sao lưu database trước khi triển khai: `/private/tmp/seanmusic-before-redesign-20261106.dump`.

## Tham khảo thiết kế

- https://reverb.com/gear/used-guitars: tìm kiếm, nhóm nhạc cụ và lựa chọn theo giá.
- https://www.guitarcenter.com/Used/: cấu trúc danh mục thiết bị đã qua sử dụng.
- https://2handland.com/nhac-cu-cu: thông tin ngoại hình và cách trình bày giá VND.

Giao diện được thiết kế riêng; không sao chép mã nguồn hoặc thương hiệu của các trang tham khảo.

## Nguồn ảnh

- Ảnh đầu trang: https://unsplash.com/photos/assorted-color-electric-guitars-aW2ELKtnbRU
- Ảnh phòng thu: https://unsplash.com/photos/people-playing-musical-instruments-inside-room-1RKH1_JasMw
- Ảnh danh mục điện, bass, trống, ampli: thư mục `assets/products/originals/` (Sale cũ).
- Ảnh danh mục guitar mộc: https://us.donnermusic.com/products/donner-hush-c-guitar
- Ảnh tham chiếu model và URL nguồn chi tiết: `assets/products/references/sources.json`.
  Script tải ảnh: `scripts/media/fetch_store_images.py`.

Ảnh tham chiếu nhà sản xuất/nhà bán lẻ chỉ minh họa model, không chứng minh tình
trạng hoặc các phụ kiện của món hàng cụ thể. Ghi chú này hiển thị trên trang sản
phẩm. Cần xác nhận quyền sử dụng ảnh sản phẩm bên thứ ba trước khi đưa lên website
công khai; thay bằng ảnh thực tế của cửa hàng khi có thể.
