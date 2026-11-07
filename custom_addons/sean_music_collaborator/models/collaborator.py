from odoo import fields, models


class SeanMusicCollaborator(models.Model):
    _name = "sean.music.collaborator"
    _description = "Sean Music Collaborator"
    _order = "name"

    name = fields.Char(related="partner_id.name", store=True, readonly=True)
    partner_id = fields.Many2one(
        "res.partner", string="Contact", required=True, ondelete="restrict", index=True
    )
    user_id = fields.Many2one(
        "res.users", string="Odoo User", help="Optional internal user linked to this collaborator."
    )
    plan_id = fields.Many2one(
        "sean.music.commission.plan", string="Commission Plan", ondelete="restrict"
    )
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, required=True, index=True
    )
    sale_order_ids = fields.One2many(
        "sale.order", "collaborator_id", string="Sales Orders", readonly=True
    )
    commission_ids = fields.One2many(
        "sean.music.commission", "collaborator_id", string="Commissions", readonly=True
    )
    sale_count = fields.Integer(compute="_compute_totals")
    commission_total = fields.Monetary(compute="_compute_totals", currency_field="currency_id")
    currency_id = fields.Many2one(related="company_id.currency_id", readonly=True)

    _partner_unique = models.Constraint(
        "UNIQUE(partner_id, company_id)",
        "A contact can only be registered once as a collaborator per company.",
    )

    def _compute_totals(self):
        for collaborator in self:
            commissions = collaborator.commission_ids.filtered(lambda c: c.state != "cancelled")
            collaborator.sale_count = len(collaborator.sale_order_ids.filtered(lambda o: o.state == "sale"))
            collaborator.commission_total = sum(commissions.mapped("commission_amount"))

    def action_view_sales(self):
        self.ensure_one()
        action = self.env.ref("sale.action_orders").read()[0]
        action["domain"] = [("collaborator_id", "=", self.id)]
        return action

    def action_view_commissions(self):
        self.ensure_one()
        action = self.env.ref("sean_music_collaborator.action_commission").read()[0]
        action["domain"] = [("collaborator_id", "=", self.id)]
        return action
