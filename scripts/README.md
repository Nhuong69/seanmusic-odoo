# Công cụ dự án

Chạy từ root. Python dùng `.venv/bin/python`, cấu hình chuẩn `seanmusic.conf`.

| Nhóm | Tác dụng |
| --- | --- |
| `dev/init_local_config.py` | Tạo cấu hình local nếu chưa có; không gọi DB |
| `data/create_sample_data.py` | Tạo/cập nhật người dùng, sản phẩm và dữ liệu mẫu; cần `SAMPLE_PASSWORD` |
| `data/configure_vietnamese_store.py` | Cập nhật website, publish sản phẩm, giá và ảnh; có commit DB |
| `media/fetch_store_images.py` | Tải ảnh hãng/retailer, giữ URL nguồn trong manifest |
| `checks/verify_store_local.py` | HTTP read-only mặc định; `--allow-writes` tạo giỏ nháp, `--submit-inquiry` thêm inquiry |
| `checks/verify_store_data.py` | Đọc fixture local 31 nhạc cụ và inquiry kiểm thử đã tạo |
| `checks/run_odoo_tests.py` | Tạo DB test mới riêng và chạy tests addon |
| `docs/create_user_guide.js` | Công cụ xuất tài liệu tùy chọn; không thuộc runtime Odoo |

## Script dữ liệu: chỉ chạy khi chủ động muốn thay dữ liệu

Hai script `data/` giới hạn `db_seanmusic`, không được coi là migration production.
`configure_vietnamese_store.py` có các ID fixture cũ; phải rà soát trước khi dùng
với bộ dữ liệu khác. Không chạy nó chỉ để đổi port, kiểm tra website hoặc sửa IDE.
Odoo shell nhận script qua stdin nên root lấy từ working directory; nếu chạy
ở nơi khác, đặt biến `SEAN_MUSIC_ROOT` trỏ đúng checkout.

```sh
.venv/bin/python odoo/odoo-bin shell -c seanmusic.conf --no-http < scripts/data/configure_vietnamese_store.py
```

`SAMPLE_PASSWORD` là biến môi trường do người vận hành cung cấp cho script seed;
không ghi mật khẩu vào file hay câu lệnh sẽ commit. Seed có thể cập nhật mật khẩu
của user mẫu đã có. Luôn backup trước khi chạy script dữ liệu.

## Kiểm tra HTTP

```sh
.venv/bin/python scripts/checks/verify_store_local.py --base-url http://127.0.0.1:8079
```

Các kiểm tra dựa trên fixture cửa hàng đã Việt hóa; DB mới chỉ cài module chưa chắc
có Enya, VND hoặc 31 sản phẩm. Không seed để ép assertion xanh. Mặc định kiểm tra
trang, lọc giá, tìm kiếm, metadata giỏ và validation/CSRF; không tạo đơn/inquiry.
Chỉ với một server nối DB test disposable:

```sh
.venv/bin/python scripts/checks/verify_store_local.py --base-url http://127.0.0.1:18079 --allow-writes --submit-inquiry
```

Các file cũ trực tiếp dưới `scripts/` đã chuyển nhóm; dùng đường dẫn mới ở bảng.
Không có bước tự xóa đơn hay yêu cầu tư vấn sau kiểm thử.

## Xuất lại tài liệu (tùy chọn)

```sh
npm ci --prefix scripts/docs --ignore-scripts
npm run build --prefix scripts/docs
```

File xuất mới ở `artifacts/user-guide/`, không ghi đè bản tài liệu đã lưu trong
`docs/user-guide/`. Công cụ cần Node/npm và dependencies trong package lock.
