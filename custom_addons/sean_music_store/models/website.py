from odoo import models


class Website(models.Model):
    _inherit = "website"

    def _get_product_sort_mapping(self):
        return [
            ("website_sequence asc", "Gợi ý cho bạn"),
            ("publish_date desc", "Mới đăng gần đây"),
            ("name asc", "Tên từ A đến Z"),
            ("list_price asc", "Giá từ thấp đến cao"),
            ("list_price desc", "Giá từ cao đến thấp"),
        ]
