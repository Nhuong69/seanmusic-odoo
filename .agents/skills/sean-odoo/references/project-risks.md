# Rủi ro từ kiểm toán code ngày 06/11/2026

Kiểm toán chỉ đọc; chưa chạy Odoo/DB, chưa tái hiện bằng user thường. Đây là đầu vào
cho task sau, không phải yêu cầu tự sửa mọi vấn đề khi chỉ đổi giao diện.
Đường dẫn dưới đây tính từ root dự án; kiểm tra lại line khi code thay đổi.

| Quan sát và rủi ro | Bằng chứng | Kiểm chứng khi triển khai thay đổi liên quan |
| --- | --- | --- |
| Homepage dùng `list_price`; shop/giỏ dùng cơ chế giá website, có thể lệch khi đổi pricelist | `custom_addons/sean_music_store/views/store_templates.xml:39`; `scripts/data/configure_vietnamese_store.py` | Cùng sản phẩm/khách/pricelist: homepage, shop, chi tiết, giỏ; cả giảm giá/thuế |
| Đồng bộ xóa dòng và tạo lại, không loại chứng từ `paid`; lịch sử có thể bị sửa | `custom_addons/sean_music_collaborator/models/commission.py:53`; `models/sale_order.py:30` trong cùng module | Sửa dòng đơn sau confirmed/paid; so chứng từ trước/sau; cần chính sách khóa/điều chỉnh |
| Đổi hoặc bỏ cộng tác viên có thể để khoản người cũ tồn tại | `custom_addons/sean_music_collaborator/models/commission.py:54` | A → B → bỏ trống → hủy; kiểm chứng từ và tổng từng người |
| User hoa hồng có read/update chứng từ nhưng thiếu quyền create dòng; xác nhận có thể AccessError | `custom_addons/sean_music_collaborator/security/ir.access.csv:8`; `models/commission.py:69` trong cùng module | Xác nhận bằng user đúng nhóm bán hàng, không dùng superuser để kết luận |
| Tổng hoa hồng cộng số tiền đơn rồi hiển thị tiền công ty, chưa thấy quy đổi | `custom_addons/sean_music_collaborator/models/collaborator.py:30` | Đơn hai tiền tệ, tỷ giá/ngày tính và báo cáo theo chính sách |
| Quyền nhiều công ty và đổi trạng thái cần kiểm chứng phía server | `custom_addons/sean_music_collaborator/security/ir.access.csv:2`; `models/commission.py:43` trong cùng module | Ma trận role/company, gọi phương thức trực tiếp; không chỉ domain trên form |
| Tình trạng trên template, chưa theo serial/món riêng; ảnh không chứng minh món bán | `custom_addons/sean_music_store/models/product_template.py:7` | Hai món cùng model nhưng khác tình trạng/ảnh; ghi thiếu dữ liệu, không tự nhận đã có quản lý serial |
| Field nguồn ảnh chưa render riêng; cảnh báo ảnh tham chiếu phụ thuộc ghi chú cấu hình có thể bị xóa | `custom_addons/sean_music_store/views/store_templates.xml:52`; `scripts/data/configure_vietnamese_store.py` | Ghi chú trống/được thay: cảnh báo ảnh hãng còn đúng và hiện rõ; không suy ra field nguồn đã được hiển thị |
| `sean_music_home` patch WebClient/NavBar và điều hướng `/odoo` → `/web` | `custom_addons/sean_music_home/static/src/js/sean_music_home.js:11`; `controllers/web_client.py:8` cùng module | Login, điều hướng ứng dụng, quyền, desktop/mobile nếu sửa home/assets |

Giới hạn tại thời điểm kiểm toán 06/11: chưa có tests riêng cho custom addons. Đợt
tổ chức dự án bổ sung tests; xem kết quả mới trong docs/maintenance-report.md. Không
suy ra các rủi ro trên đã được sửa chỉ vì thêm tests. Smoke scripts không bao
phủ hoa hồng, nhiều công ty, nhiều tiền tệ, concurrency hoặc hoàn trả.
Publish sản phẩm không chứng minh tồn khả dụng. Stock core chỉ tham gia khi module,
loại sản phẩm và cấu hình phù hợp; không đồng nhất xác nhận đơn với giao thành công.

Ưu tiên đề xuất: kiểm chứng lệch giá và quyền xác nhận trước; rồi lịch sử hoa hồng,
đổi người hưởng và đa tiền tệ. Mỗi sửa đổi cần scope riêng và bằng chứng tái hiện.
