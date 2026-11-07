# Sean Music

Website nhạc cụ tiếng Việt trên **Odoo 20**, với mã riêng trong `custom_addons/`.
Giữ giỏ hàng, tài khoản và checkout gốc; không sửa upstream để làm nghiệp vụ riêng.

## Chạy local

1. Clone repository cùng submodule: `git clone --recurse-submodules <URL_REPOSITORY>`.
   Với bản clone đã có: `git submodule update --init --recursive`.
   Gitlink `odoo` pin chính xác commit upstream; không tự `git pull` trong đó.
2. Cài Python >= 3.12 và PostgreSQL 16. Môi trường đã chạy trên máy hiện tại là
   Python 3.14.4; Python 3.10 của dự án `besco` không dùng cho dự án này.
3. Tạo môi trường và cài dependencies:

   ```sh
   python3.14 -m venv .venv
   .venv/bin/python -m pip install -r requirements-dev.txt
   .venv/bin/python scripts/dev/init_local_config.py --db-user YOUR_POSTGRES_ROLE
   ```

   Role PostgreSQL phải tồn tại, có quyền với DB hiện tại; chỉ cần CREATEDB nếu cài DB mới
   hoặc chạy suite test riêng. Script config không tạo role, không đổi mật khẩu DB,
   không ghi đè file đã có. Sửa `db_password` trong file local nếu PostgreSQL yêu cầu.
   Trên macOS cần công cụ biên dịch/libpq khi dependency chưa có wheel tương ứng;
   xem yêu cầu hệ thống trong checkout Odoo nếu pip báo thiếu thư viện hệ điều hành.
4. Với DB **đã có**, chỉ chạy:

   ```sh
   .venv/bin/python odoo/odoo-bin -c seanmusic.conf
   ```

   Mở [website](http://127.0.0.1:8079/) hoặc [quản trị](http://127.0.0.1:8079/web).
   Không chạy seed hay `-i` cho mỗi lần khởi động.

5. Chỉ với DB local **mới**, cài module trước:

   ```sh
   .venv/bin/python odoo/odoo-bin -c seanmusic.conf -i sean_music_store,sean_music_collaborator --without-demo --stop-after-init --no-http
   ```

   Cài module không tự cung cấp danh mục hàng thật hay biến tình trạng thành đã kiểm định.
   Script trong `scripts/data/` là công cụ thay dữ liệu local có chủ đích, không phải
   bước chạy thường ngày hay migration sản xuất. Đọc [hướng dẫn script](scripts/README.md).

## PyCharm và VS Code

PyCharm có cấu hình chia sẻ `.run/Sean Music local.run.xml`. Chọn:

| Mục | Giá trị tính từ thư mục dự án |
| --- | --- |
| Interpreter | `.venv/bin/python` |
| Script | `odoo/odoo-bin` |
| Parameters | `-c /DUONG_DAN_DU_AN/seanmusic.conf` |
| Working directory | Root dự án |

VS Code dùng `.vscode/launch.json` với cùng file `seanmusic.conf` và port `8079`.
Dừng server cũ trước khi Run để tránh trùng cổng. `.conf` không thay được interpreter.
`odoo.conf` cũ vẫn được giữ local để tương thích, cũng dùng port 8079; **không chạy
hai cấu hình cùng lúc**. `seanmusic.conf` là cấu hình chuẩn cho tài liệu và IDE mới.
Cron tắt trong cấu hình debug; không dùng nguyên cấu hình này cho production.

## Cấu trúc

```text
config/                  Cấu hình mẫu không chứa secret
odoo/                    Git submodule upstream, pin commit
custom_addons/           Storefront, home/login, hoa hồng
scripts/{dev,data,media,checks,docs}/
assets/branding/         Logo nguồn
assets/products/originals/  Ảnh dự án cung cấp
assets/products/references/  Ảnh hãng/retailer + sources.json
assets/products/services/   Ảnh dịch vụ
docs/user-guide/         Tài liệu và hình minh họa đã có
artifacts/              Ảnh nghiệm thu, test logs, file xuất (không commit)
tests/                  Kiểm tra cấu trúc, không cần DB
.agents/, .codex/       Hướng dẫn AI và phân vai
.run/, .vscode/         Cấu hình chạy chia sẻ
.venv/, .odoo-data/     Môi trường và dữ liệu local (không commit)
```

Ảnh dùng trực tiếp trên website nằm trong `custom_addons/*/static/`, không phải các
thư mục nguồn ở `assets/`. Không xóa chúng vì thấy ảnh nguồn trùng nội dung.

## Kiểm tra

```sh
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/checks/verify_store_local.py --base-url http://127.0.0.1:8079
```

Kiểm tra HTTP mặc định không gửi giỏ/inquiry. Muốn kiểm tra ghi phải chủ động
thêm `--allow-writes` và dùng server nối DB local **dành cho kiểm thử**. Suite addon:

```sh
.venv/bin/python scripts/checks/run_odoo_tests.py --create-test-db
```

Runner chỉ chấp nhận DB mới có tiền tố `db_seanmusic_test_`, không dùng DB làm việc
`db_seanmusic`. Test data rollback theo Odoo; DB và filestore test vẫn được giữ
để xem lại, không tự xóa. Xem [quản lý dự án](docs/project-management.md).

## Dữ liệu và bảo mật

- Không commit `seanmusic.conf`, `odoo.conf`, `.odoo-data`, `.venv`, backup, log hay
  file IDE cá nhân. Mẫu config không có mật khẩu thật. Không có remote Sean Music
  nào được tự thiết lập hay đẩy lên trong quá trình tổ chức dự án.
- `unknown` là chưa xác nhận; ảnh tham chiếu không chứng minh tình trạng món hàng.
- Backup Odoo phải có **database và filestore tương ứng**. `.odoo-data` không phải
  cache để xóa. Hướng dẫn backup/restore ở [quản lý dự án](docs/project-management.md).
- Các rủi ro giá/hoa hồng đã biết được giữ riêng trong
  `.agents/skills/sean-odoo/references/project-risks.md`; đợt tổ chức thư mục không
  tự thay đổi chính sách nghiệp vụ đó.
