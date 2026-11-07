from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SeanMusicCommissionPlan(models.Model):
    _name = "sean.music.commission.plan"
    _description = "Sean Music Commission Plan"
    _order = "name"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    base_type = fields.Selection(
        [("untaxed", "Untaxed Sales"), ("total", "Sales Including Tax")],
        default="untaxed",
        required=True,
        help="The amount used as the base for commission calculation.",
    )
    default_rate = fields.Float(string="Default Rate (%)", default=5.0, required=True)
    rule_ids = fields.One2many("sean.music.commission.rule", "plan_id", string="Product Rules")
    collaborator_ids = fields.One2many("sean.music.collaborator", "plan_id")

    @api.constrains("default_rate")
    def _check_default_rate(self):
        for plan in self:
            if not 0 <= plan.default_rate <= 100:
                raise ValidationError("The default commission rate must be between 0 and 100%.")

    def get_rate(self, product):
        self.ensure_one()
        product_rule = self.rule_ids.filtered(lambda rule: rule.product_id == product).sorted(
            key=lambda rule: (rule.sequence, rule.id)
        )[:1]
        if product_rule:
            return product_rule.rate
        category_rules = self.rule_ids.filtered(
            lambda rule: rule.product_category_id
            and product.categ_id in rule.product_category_id.search(
                [("id", "child_of", rule.product_category_id.ids)]
            )
        ).sorted(key=lambda rule: (rule.sequence, rule.id))
        return category_rules[:1].rate if category_rules else self.default_rate


class SeanMusicCommissionRule(models.Model):
    _name = "sean.music.commission.rule"
    _description = "Sean Music Commission Rule"
    _order = "sequence, id"

    plan_id = fields.Many2one("sean.music.commission.plan", required=True, ondelete="cascade")
    sequence = fields.Integer(default=10)
    product_id = fields.Many2one("product.product", string="Product", ondelete="restrict")
    product_category_id = fields.Many2one(
        "product.category", string="Product Category", ondelete="restrict"
    )
    rate = fields.Float(string="Rate (%)", required=True, default=5.0)

    @api.constrains("product_id", "product_category_id", "rate")
    def _check_rule(self):
        for rule in self:
            if rule.product_id and rule.product_category_id:
                raise ValidationError("A commission rule must target a product or a category, not both.")
            if not 0 <= rule.rate <= 100:
                raise ValidationError("The commission rate must be between 0 and 100%.")
