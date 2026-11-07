from odoo import Command
from odoo.exceptions import AccessError
from odoo.tests.common import new_test_user
from odoo.tools import mute_logger

from odoo.addons.base.tests.common import BaseCommon


class TestSeanInquiryAccess(BaseCommon):
    _test_user_groups = ('sales_team.group_sale_salesman',)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.other_company = cls.env['res.company'].create({
            'name': 'Inquiry other company',
        })
        cls.public_user = new_test_user(
            cls.env, login='sean_inquiry_public', groups='base.group_public',
            company_id=cls.company.id,
            company_ids=[Command.set(cls.company.ids)],
        )
        cls.portal_user = new_test_user(
            cls.env, login='sean_inquiry_portal', groups='base.group_portal',
            company_id=cls.company.id,
            company_ids=[Command.set(cls.company.ids)],
        )
        cls.website_user = new_test_user(
            cls.env, login='sean_inquiry_designer',
            groups='website.group_website_designer',
            company_id=cls.company.id,
            company_ids=[Command.set(cls.company.ids)],
        )
        cls.own_inquiry, cls.other_inquiry = cls.env['sean.music.inquiry'].create([
            {
                'name': 'Own company inquiry',
                'message': 'Test guitar advice',
                'company_id': cls.company.id,
            }, {
                'name': 'Other company inquiry',
                'message': 'Private advice request',
                'company_id': cls.other_company.id,
            },
        ])

    def _inquiries_as(self, user):
        inquiries = self.env['sean.music.inquiry'].with_user(user).with_context(
            allowed_company_ids=self.company.ids,
        )
        self.assertFalse(inquiries.env.su)
        return inquiries

    def _assert_crud_denied(self, user):
        inquiries = self._inquiries_as(user)
        record = inquiries.browse(self.own_inquiry.id)
        operations = {
            'create': lambda: inquiries.create({
                'name': 'Unauthorized inquiry',
                'message': 'Direct ORM creation must be denied',
                'company_id': self.company.id,
            }),
            'read': lambda: record.read(['message']),
            'write': lambda: record.write({'message': 'Unauthorized change'}),
            'unlink': record.unlink,
        }
        for operation, call in operations.items():
            with self.subTest(operation=operation), mute_logger(
                'odoo.addons.base.models.ir_access', 'odoo.orm.models',
            ), self.assertRaises(AccessError):
                call()

    def test_public_cannot_crud_inquiries(self):
        self._assert_crud_denied(self.public_user)

    def test_portal_cannot_crud_inquiries(self):
        self._assert_crud_denied(self.portal_user)

    def test_staff_can_create_read_and_update_own_company(self):
        for user in (self.env.user, self.website_user):
            with self.subTest(user=user.login):
                inquiries = self._inquiries_as(user)
                record = inquiries.create({
                    'name': 'Staff inquiry',
                    'message': 'Test advice request',
                })
                self.assertEqual(record.company_id, self.company)
                self.assertEqual(record.state, 'new')
                self.assertEqual(record.read(['message'])[0]['message'], 'Test advice request')
                record.write({'state': 'done'})
                self.assertEqual(record.state, 'done')

    def test_staff_search_is_restricted_to_allowed_company(self):
        for user in (self.env.user, self.website_user):
            with self.subTest(user=user.login):
                inquiries = self._inquiries_as(user)
                visible = inquiries.search([
                    ('id', 'in', (self.own_inquiry | self.other_inquiry).ids),
                ])
                self.assertEqual(visible.ids, self.own_inquiry.ids)

    def test_staff_cannot_read_other_company_by_id(self):
        for user in (self.env.user, self.website_user):
            with self.subTest(user=user.login):
                inquiries = self._inquiries_as(user)
                # Prove read permission exists before checking the company restriction.
                self.assertEqual(
                    inquiries.browse(self.own_inquiry.id).read(['message'])[0]['message'],
                    'Test guitar advice',
                )
                with (
                    mute_logger('odoo.addons.base.models.ir_access'),
                    self.assertRaises(AccessError),
                ):
                    inquiries.browse(self.other_inquiry.id).read(['message'])
