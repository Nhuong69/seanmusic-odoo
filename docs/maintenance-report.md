# Báo cáo tổ chức dự án - 07/11/2026

## Phạm vi đã xử lý

- Khởi tạo Git root, khai báo checkout `odoo/` hiện có làm submodule từ
  `https://github.com/odoo/odoo.git`, pin commit
  `678c9654d85d921da058a87aa13cf9cf93d6a1ed`. Không sửa core, không pull/push.
- Ignore cấu hình thật, venv, filestore/runtime, backup, cache, log và IDE cá nhân.
  Hai cấu hình thật có mode 0600, giữ nguyên thông tin truy cập.
- `seanmusic.conf` là cấu hình local chuẩn port 8079/loopback; PyCharm `.run/`
  và VS Code trỏ cùng file. File `odoo.conf` cũ được giữ tương thích, port cũng 8079.
- Thêm mẫu config không có secret và generator tạo file độc quyền, không ghi đè.
- Thêm hướng dẫn dựng môi trường, requirements Python/dev, dependencies và lockfile
  cho công cụ Node xuất tài liệu (tùy chọn, không thuộc runtime cửa hàng).
- Chuyển script vào `data/`, `media/`, `checks/`, `dev/`, `docs/`; bỏ hardcode
  thư mục máy cá nhân trong script dữ liệu. Sửa hàm seed ảnh trả chuỗi base64 phù
  hợp Odoo 20; không chạy seed để kiểm chứng đợt này.
- Chuyển `Sale/` thành `assets/products/originals/`; ảnh tham chiếu và manifest
  vào `assets/products/references/`; URL nguồn giữ nguyên, chỉ cập nhật file path.
  Ảnh dịch vụ ở `assets/products/services/`, logo ở `assets/branding/`.
- Tài liệu DOCX và hình minh họa được giữ tại `docs/user-guide/`. Baseline screenshot
  chuyển sang `artifacts/redesign-preview/`, không coi đó là ảnh hiện trạng.
- Bỏ phụ thuộc hoa hồng không được tham chiếu khỏi manifest `sean_music_home`.
  Store vẫn phụ thuộc Home vì kế thừa login. Không uninstall module đã có hoặc
  cập nhật registry của database làm việc.
- Bổ sung test addon cho nhãn tình trạng, inquiry ACL/công ty, luật/tính hoa hồng.
  HTTP smoke mặc định không tạo giỏ/inquiry; ghi cần opt-in `--allow-writes`.
- Cập nhật README và hướng dẫn AI để không dùng lại đường dẫn/port cũ.

## Bằng chứng kiểm chứng

| Kiểm tra | Kết quả |
| --- | --- |
| `python -m unittest discover -s tests -v` | PASS: 7 tests cấu trúc/config/ảnh/IDE/DB guard |
| `python -m compileall -q scripts tests custom_addons` | PASS |
| `node --check scripts/docs/create_user_guide.js` | PASS cú pháp |
| `npm install --package-lock-only --ignore-scripts ...` | PASS resolution docx/sharp, không chạy lifecycle scripts |
| Odoo parser đọc `seanmusic.conf` | PASS port 8079, loopback, các addons path tồn tại |
| `python -m pip check` | PASS, không có dependency conflict |
| Skill quick_validate cho acceptance/design/odoo | PASS |
| HTTP `verify_store_local.py --base-url http://127.0.0.1:8079` | PASS 7 trang, lọc giá, Enya search, metadata giỏ, CSRF và invalid email |
| Giỏ/inquiry ghi mới trên DB làm việc | NOT RUN; không bật `--allow-writes` |
| Suite Odoo DB riêng | PASS: `0 failed, 0 error(s) of 20 tests`; gồm 18 test custom và 2 web probes tự thêm bởi framework |

Suite chạy với `scripts/checks/run_odoo_tests.py --create-test-db`; DB mới được
giữ là `db_seanmusic_test_20261107_040903`. Log và filestore test nằm ở
`artifacts/tests/db_seanmusic_test_20261107_040903/`. Các test record rollback;
module/schema/test DB vẫn tồn tại để truy vết. Không seed, `-i`, `-u` hoặc chạy
test suite trên `db_seanmusic`.

## Giới hạn

- Không kiểm thử lại toàn bộ layout bằng browser vì không đổi layout; HTTP pass
  không phải bằng chứng nghiệm thu thiết kế 9/10.
- Không xuất lại hoặc render tài liệu DOCX; bản cũ chỉ được di chuyển nguyên vẹn.
- Không kiểm thử dựng venv từ máy sạch hay restore backup trong đợt này.
- Không xử lý các thay đổi chính sách giá/hoa hồng đã ghi trong project-risks.
  Test tính hoa hồng không chứng minh lịch sử paid bất biến hoặc đủ mọi role.
- Không chọn remote, tạo commit hay push thay chủ dự án. Mã được chuẩn bị cho
  initial commit; kiểm tra `git status` trước khi chủ dự án commit.
