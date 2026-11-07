import time

from odoo import http
from odoo.fields import Domain
from odoo.http import request
from odoo.tools import email_normalize


class SeanMusicStore(http.Controller):
    @http.route("/sean-music", type="http", auth="public", website=True, sitemap=False)
    def home(self, **kwargs):
        products = request.env["product.template"].search(
            Domain.AND([
                request.env.website.sale_product_domain(),
                [("is_published", "=", True), ("default_code", "=like", "GUITAR-%")],
            ]),
            order="website_sequence, id",
            limit=8,
        )
        return request.render("sean_music_store.home", {"featured_products": products})

    @http.route(
        ["/huong-dan-chon-dan", "/ve-sean-music", "/lien-he", "/chinh-sach"],
        type="http", auth="public", website=True, sitemap=True,
    )
    def information(self, **kwargs):
        page = request.httprequest.path.strip("/").replace("-", "_")
        return request.render("sean_music_store." + page, {})

    @http.route(
        "/lien-he/gui", type="http", auth="public", website=True,
        methods=["POST"], csrf=True, sitemap=False,
    )
    def submit_inquiry(self, **post):
        if post.get("website_url"):
            return request.redirect("/lien-he?da_gui=1")
        values = {
            key: str(post.get(key, "")).strip()
            for key in ("name", "email", "phone", "message")
        }
        error = None
        if not 2 <= len(values["name"]) <= 150:
            error = "Vui lòng nhập họ và tên từ 2 đến 150 ký tự."
        elif not 10 <= len(values["message"]) <= 5000:
            error = "Vui lòng mô tả nhu cầu từ 10 đến 5.000 ký tự."
        elif not values["email"] and not values["phone"]:
            error = "Vui lòng để lại email hoặc số điện thoại để cửa hàng phản hồi."
        elif len(values["email"]) > 254 or (values["email"] and not email_normalize(values["email"])):
            error = "Địa chỉ email chưa hợp lệ."
        elif len(values["phone"]) > 30:
            error = "Số điện thoại không được quá 30 ký tự."
        elif request.session.get("sean_last_inquiry", 0) + 30 > time.time():
            error = "Bạn vừa gửi yêu cầu. Vui lòng chờ 30 giây trước khi gửi tiếp."
        if error:
            return request.render("sean_music_store.lien_he", {"form_error": error, "form_values": values})
        values.update({
            "company_id": request.env.website.company_id.id,
            "website_id": request.env.website.id,
        })
        # Public visitors may submit only these validated scalar fields. They
        # have no ACL to read or modify inquiries or choose another company.
        request.env["sean.music.inquiry"].sudo().create(values)
        request.session["sean_last_inquiry"] = time.time()
        return request.redirect("/lien-he?da_gui=1")
