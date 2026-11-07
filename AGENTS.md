# Sean Music — hướng dẫn làm việc với AI

## Bối cảnh và phạm vi

Website bán nhạc cụ tiếng Việt trên Odoo 20. Mã riêng ở `custom_addons/`;
gồm `sean_music_store`, `sean_music_collaborator` và `sean_music_home` (webclient/login).
`odoo/` là checkout upstream, không sửa core để xử lý yêu cầu của cửa hàng.
Giữ giỏ hàng, tài khoản và checkout gốc của Odoo. Không tự đổi sang React/Next.js.
Mở `custom_addons/sean_music_store/README.md` khi cần cách chạy hoặc hiểu giới hạn dữ liệu.

## Chọn skill theo việc đang làm

Đọc file tương ứng khi việc đó áp dụng, không nạp cả bộ cho mọi thay đổi:

| Công việc | Skill trong `.agents/skills/` |
| --- | --- |
| Tìm nguồn, Facebook/profile đào tạo AI, tham khảo cửa hàng | `sean-research/SKILL.md` |
| Chốt yêu cầu, hành trình mua hàng, trạng thái nghiệp vụ | `sean-product/SKILL.md` |
| QWeb/SCSS, bố cục, nội dung và bản sắc cửa hàng | `sean-design/SKILL.md` |
| ORM, controller, quyền, hoa hồng và tích hợp Odoo | `sean-odoo/SKILL.md` |
| Nghiệm thu một tính năng hoặc thay đổi giao diện đáng kể | `sean-acceptance/SKILL.md` |

Đây là bộ skill của dự án; ưu tiên quy trình có sẵn và chỉ bổ sung phần cần cho yêu cầu.

## Điều không được suy diễn từ dữ liệu

- `sean_condition=unknown` nghĩa là chưa xác nhận. Không tự gán “mới 99%”,
  đã kiểm định, còn hàng, bảo hành hoặc số khách hàng.
- Ảnh tham chiếu model không phải ảnh món hàng thực tế. Giữ thông tin nguồn ảnh.
- Giá hiển thị lấy theo website/pricelist của Odoo; không sửa tiền tệ kế toán để đổi ký hiệu.
- `sean_music_collaborator` tạo chứng từ hoa hồng khi xác nhận đơn nhưng còn đồng bộ
  lại sau sửa đơn; chưa bảo đảm snapshot bất biến, kể cả khi đã trả. Đọc rủi ro trong
  `.agents/skills/sean-odoo/references/project-risks.md` trước khi đổi hoặc khẳng định luồng hoa hồng.
- Không dùng các ERP connector khác để suy ra dữ liệu Sean Music.

## Điều phối subagent

Người dùng cho phép dùng subagent cho dự án này. Chỉ tách việc khi có các phần độc lập;
việc nhỏ làm trực tiếp. Các vai ở `.codex/agents/`:
`sean_researcher`, `sean_product_analyst`, `sean_frontend`, `sean_odoo_engineer`, `sean_reviewer`.
Mặc định chạy 1–2 vai cần thiết; trần cấu hình là 3 subagent đồng thời, không phải chỉ tiêu.

Mỗi giao việc ghi mục tiêu, dữ kiện đầu vào, file được sửa, đầu ra, cách kiểm chứng
và điểm dừng. Một file chỉ có một người sửa tại một thời điểm; đặc biệt
`views/store_templates.xml` phải có chủ sở hữu rõ ràng. Agent chính giữ việc đang
chặn tiến độ, tích hợp kết quả và xử lý xung đột; không làm lại phần đã giao.
Reviewer phải xem kết quả đã tích hợp. Các vai chỉ đọc là quy ước hành vi,
không phải sandbox riêng. Không tạo chat mới để thay cho subagent.

Nếu công cụ spawn hiện tại không có lựa chọn tên custom agent, đọc file TOML của vai
và truyền `developer_instructions` cùng nhiệm vụ vào prompt của subagent; không nói
rằng vai đã được nạp tự động khi chưa kiểm chứng.

## Kiểm chứng đúng phạm vi

Chỉ sửa hướng dẫn thì kiểm tra skill/TOML/link và tình huống mô phỏng; không cần cập nhật DB.
Thay đổi runtime: chọn kiểm tra theo `sean-acceptance`; không tự chạy toàn bộ seed/config.
`scripts/checks/verify_store_local.py` mặc định kiểm tra HTTP không tạo giỏ/inquiry.
`--allow-writes` cho phép tạo đơn nháp; `--submit-inquiry` cần cờ đó và còn tạo yêu
cầu tư vấn. Chỉ bật ghi với DB local dùng cho kiểm thử. Cấu hình chuẩn local là
`seanmusic.conf`, cổng `8079`; không commit cấu hình thật hay `.odoo-data`.
Nghiệm thu 9/10 cần bằng chứng, không tự chấm từ cảm giác hoặc từ số lượng file.

## Cách yêu cầu một tính năng

Ví dụ: “Dùng $sean-product và $sean-design cải thiện trang sản phẩm đàn cũ.
Giao sean_reviewer kiểm tra kết quả theo $sean-acceptance.
Ưu tiên ảnh/tình trạng thật, luồng hỏi tư vấn và trải nghiệm mobile.”

Các file mới được dùng trong phiên có discovery lại. Nếu chưa xuất hiện, mở lại
phiên ở thư mục này; trong phiên hiện tại có thể đọc trực tiếp đường dẫn skill/vai.
