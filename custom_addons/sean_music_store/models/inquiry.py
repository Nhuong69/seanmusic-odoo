from odoo import fields, models


class SeanMusicInquiry(models.Model):
    _name = "sean.music.inquiry"
    _description = "Yêu cầu tư vấn Sean Music"
    _order = "create_date desc, id desc"

    name = fields.Char(string="Họ và tên", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Số điện thoại")
    message = fields.Text(string="Nhu cầu tư vấn", required=True)
    state = fields.Selection(
        [("new", "Chưa xử lý"), ("done", "Đã xử lý")],
        string="Trạng thái", default="new", required=True,
    )
    company_id = fields.Many2one(
        "res.company", string="Công ty", required=True,
        default=lambda self: self.env.company,
    )
    website_id = fields.Many2one("website", string="Website", ondelete="set null")
