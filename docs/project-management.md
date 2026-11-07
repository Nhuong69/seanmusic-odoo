# Quản lý mã nguồn, dữ liệu và thay đổi

## Git

Root là repository mã Sean Music; `odoo/` là submodule upstream. Commit gitlink pin
phiên bản Odoo, không đưa 1.3 GB checkout upstream thành mã riêng. Chưa có remote
Sean Music; người sở hữu chọn remote và quyết định commit/push.

```sh
git status --short
git submodule status
git -C odoo status --short
git check-ignore seanmusic.conf odoo.conf .venv/ .odoo-data/ .idea/
```

Sau khi kiểm tra secret, có thể stage các file mã/tài liệu được chọn và commit
cùng `.gitmodules`/gitlink `odoo`. Không `git add -f` cấu hình hoặc dữ liệu runtime.
Không tự chuyển upstream sang nhánh/commit khác để chữa lỗi module riêng.

## Backup và restore

Database và filestore phải tương ứng cùng thời điểm. Dừng Odoo hoặc dùng cửa sổ
backup có kiểm soát để tránh file và DB lệch nhau. Với cấu hình local hiện tại:

```sh
mkdir -p backups
pg_dump -h localhost -p 5432 -U YOUR_POSTGRES_ROLE -Fc db_seanmusic -f backups/seanmusic.dump
tar -czf backups/seanmusic-filestore.tar.gz -C .odoo-data/filestore db_seanmusic
```

Các tên file ví dụ cố định có thể ghi đè backup cũ: khi thực hiện, chọn tên timestamp
mới và xác nhận chưa tồn tại. `backups/` đã ignore, nhưng vẫn cần bản sao ở ổ/vị trí
riêng theo chính sách của chủ dự án. Không lưu mật khẩu trong lệnh hoặc đưa backup
lên remote mã nguồn. `pg_path` có thể cần chỉnh theo PostgreSQL trên từng máy.

Restore trước vào **DB mới** bằng `pg_restore`; filestore phải đặt dưới
`data_dir/filestore/<TÊN_DB_RESTORE>`. Trỏ cấu hình riêng tới DB restore, xác minh
đăng nhập/ảnh/tài khoản trước khi cân nhắc thay DB chính. Không chép đè hoặc xóa
`.odoo-data` của bản đang làm việc. PostgreSQL lưu DB ngoài cây source dự án.

## Phụ thuộc module

`sean_music_store` phụ thuộc `website_sale` và `sean_music_home` vì kế thừa template
login. `sean_music_home` chỉ cần `web` và `website`; module hoa hồng không còn là
phụ thuộc kéo theo của giao diện. Khi cần hoa hồng, cài `sean_music_collaborator`
tường minh. Không gỡ module hoa hồng khỏi DB hiện tại; thay manifest không xóa dữ liệu.

## Kiểm thử và giới hạn

- `tests/` ở root kiểm tra cấu hình, metadata, nguồn ảnh và đường dẫn mà không gọi DB.
- `custom_addons/*/tests/` là tests Odoo có fixtures riêng và rollback.
- Runner tạo DB test mới; DB chính không chạy `-i`, `-u`, seed hay test suite.
- HTTP smoke dựa trên fixture local. Mặc định không tạo giỏ; ghi chỉ khi opt-in.
- Các rủi ro homepage/pricelist và lịch sử hoa hồng trong project-risks vẫn tồn tại;
  đây không phải đợt sửa nghiệp vụ, không tuyên bố hoa hồng đã bất biến hay đủ kiểm toán.
