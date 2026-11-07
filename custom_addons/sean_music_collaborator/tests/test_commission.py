from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestSeanCommission(BaseCommon):
    # A business manager is not the superuser. The user role cannot create
    # commission documents/lines, so confirmation under that role is out of scope.
    _test_user_groups = ('sean_music_collaborator.group_collaborator_manager',)

    @classmethod
    def setup_independent_company(cls):
        return cls.env['res.company'].create({
            'name': 'Sean commission test company',
            'country_id': cls.env.ref('base.us').id,
            'currency_id': cls.env.ref('base.USD').id,
        })

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.parent_category = cls.env['product.category'].create({
            'name': 'Test instruments',
        })
        cls.child_category = cls.env['product.category'].create({
            'name': 'Test guitars',
            'parent_id': cls.parent_category.id,
        })
        cls.unrelated_category = cls.env['product.category'].create({
            'name': 'Test unrelated category',
        })
        cls.product, cls.other_product = cls.env['product.product'].create([
            {
                'name': 'Test guitar service',
                'type': 'service',
                'categ_id': cls.child_category.id,
                'taxes_id': [Command.clear()],
                'supplier_taxes_id': [Command.clear()],
                'company_id': cls.company.id,
            }, {
                'name': 'Test other service',
                'type': 'service',
                'categ_id': cls.unrelated_category.id,
                'taxes_id': [Command.clear()],
                'supplier_taxes_id': [Command.clear()],
                'company_id': cls.company.id,
            },
        ])
        cls.plan = cls.env['sean.music.commission.plan'].create({
            'name': 'Test commission plan',
            'base_type': 'untaxed',
            'default_rate': 5.0,
        })
        cls.collaborator = cls.env['sean.music.collaborator'].create({
            'partner_id': cls.env['res.partner'].create({'name': 'Test collaborator'}).id,
            'plan_id': cls.plan.id,
            'company_id': cls.company.id,
        })
        cls.pricelist = cls.env['product.pricelist'].create({
            'name': 'Test commission pricelist',
            'currency_id': cls.currency.id,
            'company_id': cls.company.id,
        })
        tax_group = cls.env['account.tax.group'].create({
            'name': 'Test sales tax group',
            'company_id': cls.company.id,
        })
        cls.tax = cls.env['account.tax'].create({
            'name': 'Test sales tax 10%',
            'amount_type': 'percent',
            'amount': 10.0,
            'type_tax_use': 'sale',
            'price_include_override': 'tax_excluded',
            'company_id': cls.company.id,
            'tax_group_id': tax_group.id,
        })

    def _create_rule(self, **values):
        return self.env['sean.music.commission.rule'].create({
            'plan_id': self.plan.id,
            **values,
        })

    def test_unmatched_rules_use_default_rate(self):
        self.assertEqual(self.plan.get_rate(self.product), 5.0)
        self._create_rule(product_id=self.other_product.id, rate=20.0)
        self._create_rule(product_category_id=self.unrelated_category.id, rate=30.0)

        self.assertEqual(self.plan.get_rate(self.product), 5.0)

    def test_product_rule_precedes_category_regardless_of_sequence(self):
        self._create_rule(product_category_id=self.parent_category.id, sequence=1, rate=20.0)
        self._create_rule(product_id=self.product.id, sequence=99, rate=7.0)

        self.assertEqual(self.plan.get_rate(self.product), 7.0)

    def test_product_rules_use_sequence_then_id(self):
        first = self._create_rule(product_id=self.product.id, sequence=20, rate=8.0)
        second = self._create_rule(product_id=self.product.id, sequence=10, rate=9.0)
        self.assertEqual(self.plan.get_rate(self.product), 9.0)

        first.sequence = second.sequence
        self.assertLess(first.id, second.id)
        self.assertEqual(self.plan.get_rate(self.product), 8.0)

    def test_category_rule_applies_to_descendant(self):
        self._create_rule(product_category_id=self.parent_category.id, rate=12.0)

        self.assertEqual(self.plan.get_rate(self.product), 12.0)
        self.assertEqual(self.plan.get_rate(self.other_product), 5.0)

    def test_category_rules_use_sequence_then_id(self):
        # Current policy orders matching categories by sequence/id, not depth.
        first = self._create_rule(
            product_category_id=self.parent_category.id, sequence=20, rate=8.0,
        )
        second = self._create_rule(
            product_category_id=self.child_category.id, sequence=10, rate=9.0,
        )
        self.assertEqual(self.plan.get_rate(self.product), 9.0)

        first.sequence = 1
        self.assertEqual(self.plan.get_rate(self.product), 8.0)
        first.sequence = second.sequence
        self.assertLess(first.id, second.id)
        self.assertEqual(self.plan.get_rate(self.product), 8.0)

    def test_zero_product_rate_does_not_fall_back(self):
        self._create_rule(product_category_id=self.parent_category.id, rate=20.0)
        self._create_rule(product_id=self.product.id, rate=0.0)

        self.assertEqual(self.plan.get_rate(self.product), 0.0)

    def test_zero_category_rate_does_not_fall_back(self):
        self._create_rule(product_category_id=self.parent_category.id, rate=0.0)

        self.assertEqual(self.plan.get_rate(self.product), 0.0)

    def _create_order(self):
        self.assertFalse(self.env.su)
        self._create_rule(product_id=self.product.id, rate=10.0)
        return self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'company_id': self.company.id,
            'user_id': self.env.uid,
            'pricelist_id': self.pricelist.id,
            'fiscal_position_id': False,
            'document_tax_mode': 'tax_excluded',
            'collaborator_id': self.collaborator.id,
            'order_line': [
                Command.create({'display_type': 'line_section', 'name': 'Test section'}),
                Command.create({
                    'product_id': self.product.id,
                    'product_uom_qty': 2.0,
                    'price_unit': 100.0,
                    'discount': 10.0,
                    'tax_ids': [Command.set(self.tax.ids)],
                }),
                Command.create({
                    'product_id': self.other_product.id,
                    'product_uom_qty': 3.0,
                    'price_unit': 50.0,
                    'discount': 0.0,
                    'tax_ids': [Command.set(self.tax.ids)],
                }),
                Command.create({'display_type': 'line_note', 'name': 'Test note'}),
            ],
        })

    def _assert_commission_amounts(self, base_type, bases, amounts):
        self.plan.base_type = base_type
        order = self._create_order()
        sale_lines = order.order_line.filtered(lambda line: not line.display_type)
        guitar_line = sale_lines.filtered(lambda line: line.product_id == self.product)
        other_line = sale_lines - guitar_line
        self.assertAlmostEqual(guitar_line.price_subtotal, 180.0)
        self.assertAlmostEqual(guitar_line.price_total, 198.0)
        self.assertAlmostEqual(other_line.price_subtotal, 150.0)
        self.assertAlmostEqual(other_line.price_total, 165.0)
        self.assertFalse(order.commission_ids)

        # Exercise the real confirmation hook as a regular commission manager.
        order.action_confirm()
        self.assertEqual(order.state, 'sale')
        commission = order.commission_ids
        self.assertEqual(len(commission), 1)
        self.assertEqual(commission.collaborator_id, self.collaborator)
        self.assertEqual(commission.plan_id, self.plan)
        self.assertEqual(commission.state, 'confirmed')
        self.assertEqual(commission.currency_id, order.currency_id)
        self.assertEqual(len(commission.line_ids), 2)
        self.assertCountEqual(commission.line_ids.sale_order_line_id.ids, sale_lines.ids)
        for product, sale_line, quantity, rate, base, amount in (
            (self.product, guitar_line, 2.0, 10.0, bases[0], amounts[0]),
            (self.other_product, other_line, 3.0, 5.0, bases[1], amounts[1]),
        ):
            with self.subTest(product=product.name):
                line = commission.line_ids.filtered(lambda item: item.product_id == product)
                self.assertEqual(len(line), 1)
                self.assertEqual(line.sale_order_line_id, sale_line)
                self.assertEqual(line.quantity, quantity)
                self.assertEqual(line.rate, rate)
                self.assertAlmostEqual(line.base_amount, base)
                self.assertAlmostEqual(line.amount, amount)
        self.assertAlmostEqual(commission.base_amount, sum(bases))
        self.assertAlmostEqual(commission.commission_amount, sum(amounts))
        self.assertAlmostEqual(order.commission_amount, sum(amounts))

    def test_untaxed_commission_uses_discounted_subtotals(self):
        self._assert_commission_amounts('untaxed', (180.0, 150.0), (18.0, 7.5))

    def test_total_commission_includes_tax_after_discount(self):
        self._assert_commission_amounts('total', (198.0, 165.0), (19.8, 8.25))

    def test_zero_default_rate_produces_zero_amount(self):
        self.assertFalse(self.env.su)
        self.plan.default_rate = 0.0
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'company_id': self.company.id,
            'user_id': self.env.uid,
            'pricelist_id': self.pricelist.id,
            'collaborator_id': self.collaborator.id,
            'order_line': [Command.create({
                'product_id': self.product.id,
                'product_uom_qty': 2.0,
                'price_unit': 100.0,
                'discount': 0.0,
                'tax_ids': [Command.clear()],
            })],
        })
        order.action_confirm()
        commission = order.commission_ids

        self.assertEqual(len(commission), 1)
        self.assertEqual(len(commission.line_ids), 1)
        self.assertAlmostEqual(commission.base_amount, 200.0)
        self.assertEqual(commission.line_ids.rate, 0.0)
        self.assertEqual(commission.line_ids.amount, 0.0)
        self.assertEqual(commission.commission_amount, 0.0)
