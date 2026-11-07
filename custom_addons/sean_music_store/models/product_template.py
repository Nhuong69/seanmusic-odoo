from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    sean_condition = fields.Selection(
        [
            ("unknown", "Cần xác nhận tình trạng"),
            ("new", "Hàng mới"),
            ("like_new", "Đã qua sử dụng - như mới"),
            ("good", "Đã qua sử dụng - tốt"),
            ("fair", "Đã qua sử dụng - có dấu vết"),
        ],
        string="Tình trạng nhạc cụ", default="unknown", required=True,
    )
    sean_condition_notes = fields.Text(string="Ngoại hình và lưu ý")
    sean_image_source = fields.Char(string="Nguồn ảnh sản phẩm")

    def _sean_condition_label(self):
        self.ensure_one()
        if (self.default_code or "").startswith("SEAN-"):
            return "Dịch vụ âm nhạc"
        return dict(self._fields["sean_condition"]._description_selection(self.env))[
            self.sean_condition
        ]
