from odoo import api, fields, models


class SeanMusicCommission(models.Model):
    _name = "sean.music.commission"
    _description = "Sean Music Commission"
    _order = "date desc, id desc"

    name = fields.Char(
        string="Reference", required=True, copy=False, readonly=True,
        default=lambda self: self.env["ir.sequence"].next_by_code("sean.music.commission") or "New",
    )
    collaborator_id = fields.Many2one(
        "sean.music.collaborator", required=True, ondelete="restrict", index=True
    )
    sale_order_id = fields.Many2one(
        "sale.order", string="Sales Order", required=True, ondelete="restrict", index=True
    )
    customer_id = fields.Many2one(related="sale_order_id.partner_id", store=True, readonly=True)
    date = fields.Datetime(related="sale_order_id.date_order", store=True, readonly=True)
    company_id = fields.Many2one(related="sale_order_id.company_id", store=True, readonly=True)
    currency_id = fields.Many2one(related="sale_order_id.currency_id", readonly=True)
    plan_id = fields.Many2one("sean.music.commission.plan", required=True, ondelete="restrict")
    state = fields.Selection(
        [("confirmed", "Confirmed"), ("paid", "Paid"), ("cancelled", "Cancelled")],
        default="confirmed", required=True, copy=False,
    )
    line_ids = fields.One2many("sean.music.commission.line", "commission_id", string="Commission Lines")
    base_amount = fields.Monetary(compute="_compute_amounts", store=True)
    commission_amount = fields.Monetary(compute="_compute_amounts", store=True)

    _order_unique = models.Constraint(
        "UNIQUE(sale_order_id, collaborator_id)",
        "A sales order can only have one commission for the same collaborator.",
    )

    @api.depends("line_ids.base_amount", "line_ids.amount")
    def _compute_amounts(self):
        for commission in self:
            commission.base_amount = sum(commission.line_ids.mapped("base_amount"))
            commission.commission_amount = sum(commission.line_ids.mapped("amount"))

    def action_mark_paid(self):
        self.filtered(lambda commission: commission.state == "confirmed").write({"state": "paid"})

    def action_mark_confirmed(self):
        self.filtered(lambda commission: commission.state == "paid").write({"state": "confirmed"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    @api.model
    def sync_from_order(self, order):
        if order.state != "sale" or not order.collaborator_id:
            return self.env["sean.music.commission"]
        commission = self.search(
            [("sale_order_id", "=", order.id), ("collaborator_id", "=", order.collaborator_id.id)],
            limit=1,
        )
        plan = order.collaborator_id.plan_id
        if not plan:
            return commission
        vals = {
            "collaborator_id": order.collaborator_id.id,
            "sale_order_id": order.id,
            "plan_id": plan.id,
            "state": "confirmed" if not commission or commission.state != "paid" else "paid",
        }
        if commission:
            commission.write(vals)
            commission.line_ids.unlink()
        else:
            commission = self.create(vals)
        line_values = []
        for sale_line in order.order_line.filtered(lambda line: line.product_id and not line.display_type):
            base_amount = sale_line.price_subtotal if plan.base_type == "untaxed" else sale_line.price_total
            rate = plan.get_rate(sale_line.product_id)
            line_values.append({
                "commission_id": commission.id,
                "sale_order_line_id": sale_line.id,
                "product_id": sale_line.product_id.id,
                "quantity": sale_line.product_uom_qty,
                "base_amount": base_amount,
                "rate": rate,
            })
        self.env["sean.music.commission.line"].create(line_values)
        return commission


class SeanMusicCommissionLine(models.Model):
    _name = "sean.music.commission.line"
    _description = "Sean Music Commission Line"
    _order = "commission_id, id"

    commission_id = fields.Many2one(
        "sean.music.commission", string="Commission Document", required=True, ondelete="cascade", index=True
    )
    sale_order_line_id = fields.Many2one("sale.order.line", required=True, ondelete="restrict")
    sale_order_id = fields.Many2one(related="commission_id.sale_order_id", store=True, readonly=True)
    collaborator_id = fields.Many2one(related="commission_id.collaborator_id", store=True, readonly=True)
    product_id = fields.Many2one("product.product", required=True, ondelete="restrict")
    quantity = fields.Float(required=True)
    currency_id = fields.Many2one(related="commission_id.currency_id", readonly=True)
    base_amount = fields.Monetary(string="Sales Base", required=True)
    rate = fields.Float(string="Rate (%)", required=True)
    amount = fields.Monetary(string="Commission", compute="_compute_amount", store=True)

    @api.depends("base_amount", "rate")
    def _compute_amount(self):
        for line in self:
            line.amount = line.base_amount * line.rate / 100
