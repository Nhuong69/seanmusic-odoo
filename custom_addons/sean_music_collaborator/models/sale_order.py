from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    collaborator_id = fields.Many2one(
        "sean.music.collaborator",
        string="Collaborator",
        ondelete="restrict",
        tracking=True,
        domain="[('company_id', '=', company_id), ('active', '=', True)]",
        help="The collaborator credited for this sale.",
    )
    commission_ids = fields.One2many(
        "sean.music.commission", "sale_order_id", string="Commissions", readonly=True
    )
    commission_amount = fields.Monetary(
        string="Commission", compute="_compute_commission_amount", currency_field="currency_id"
    )

    def _compute_commission_amount(self):
        for order in self:
            order.commission_amount = sum(
                order.commission_ids.filtered(lambda commission: commission.state != "cancelled").mapped(
                    "commission_amount"
                )
            )

    def action_confirm(self):
        result = super().action_confirm()
        for order in self:
            self.env["sean.music.commission"].sync_from_order(order)
        return result

    def action_cancel(self):
        result = super().action_cancel()
        self.mapped("commission_ids").action_cancel()
        return result

    def write(self, vals):
        result = super().write(vals)
        if {"order_line", "collaborator_id"} & set(vals):
            for order in self.filtered(lambda order: order.state == "sale"):
                self.env["sean.music.commission"].sync_from_order(order)
        return result
