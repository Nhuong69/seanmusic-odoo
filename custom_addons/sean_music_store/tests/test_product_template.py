from odoo.addons.base.tests.common import BaseCommon


class TestSeanProductTemplate(BaseCommon):
    _test_user_groups = ('product.group_product_manager',)

    def test_condition_defaults_to_unknown(self):
        product = self.env['product.template'].create({'name': 'Test guitar'})

        self.assertEqual(product.sean_condition, 'unknown')
        self.assertFalse(product.sean_condition_notes)
        self.assertEqual(product._sean_condition_label(), 'Cần xác nhận tình trạng')

    def test_instrument_condition_labels(self):
        product = self.env['product.template'].create({
            'name': 'Test guitar',
            'default_code': 'GUITAR-TEST',
        })
        labels = {
            'unknown': 'Cần xác nhận tình trạng',
            'new': 'Hàng mới',
            'like_new': 'Đã qua sử dụng - như mới',
            'good': 'Đã qua sử dụng - tốt',
            'fair': 'Đã qua sử dụng - có dấu vết',
        }
        for condition, label in labels.items():
            with self.subTest(condition=condition):
                product.sean_condition = condition
                self.assertEqual(product._sean_condition_label(), label)

    def test_service_code_label_preserves_condition(self):
        product = self.env['product.template'].create({
            'name': 'Test music lesson',
            'type': 'service',
            'default_code': 'SEAN-TEST',
        })

        self.assertEqual(product._sean_condition_label(), 'Dịch vụ âm nhạc')
        self.assertEqual(product.sean_condition, 'unknown')
        product.default_code = False
        self.assertEqual(product._sean_condition_label(), 'Cần xác nhận tình trạng')
