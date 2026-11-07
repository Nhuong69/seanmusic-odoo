import base64
import os
from pathlib import Path

from odoo import Command


if env.cr.dbname != "db_seanmusic":
    raise RuntimeError("Sample data is restricted to the local db_seanmusic database.")
ROOT = Path(os.environ.get("SEAN_MUSIC_ROOT", Path.cwd())).resolve()
ASSET_DIR = ROOT / "assets/products/services"
if not ASSET_DIR.is_dir():
    raise RuntimeError("Run Odoo shell from the project root or set SEAN_MUSIC_ROOT.")


def load_product_image(filename):
    return base64.b64encode((ASSET_DIR / filename).read_bytes()).decode("ascii")


def get_or_create(model, domain, values):
    record = env[model].search(domain, limit=1)
    if record:
        record.write(values)
        return record
    return env[model].create(values)


company = env.company
password = __import__("os").environ["SAMPLE_PASSWORD"]

# Sale user and linked contact.
sale_partner = get_or_create(
    "res.partner",
    [("email", "=", "nguyen.nhuong.em@seanmusic.local")],
    {
        "name": "Nguyễn Nhường Em",
        "email": "nguyen.nhuong.em@seanmusic.local",
        "company_id": company.id,
        "is_company": False,
    },
)
sale_user = env["res.users"].search(
    [("login", "=", "nguyen.nhuong.em")], limit=1
)
user_values = {
    "partner_id": sale_partner.id,
    "company_id": company.id,
    "company_ids": [Command.link(company.id)],
    "password": password,
    "group_ids": [
        Command.set(
            [
                env.ref("base.group_user").id,
                env.ref("sales_team.group_sale_salesman").id,
                env.ref("sean_music_collaborator.group_collaborator_user").id,
            ]
        )
    ],
}
if sale_user:
    sale_user.write(user_values)
else:
    user_values.update({"name": "Nguyễn Nhường Em", "login": "nguyen.nhuong.em"})
    sale_user = env["res.users"].create(user_values)

# Commission plan and collaborator record.
plan = get_or_create(
    "sean.music.commission.plan",
    [("name", "=", "Sean Music - CTV 10%")],
    {
        "name": "Sean Music - CTV 10%",
        "base_type": "untaxed",
        "default_rate": 10.0,
        "active": True,
    },
)
collaborator = get_or_create(
    "sean.music.collaborator",
    [("partner_id", "=", sale_partner.id), ("company_id", "=", company.id)],
    {
        "partner_id": sale_partner.id,
        "user_id": sale_user.id,
        "company_id": company.id,
        "plan_id": plan.id,
        "active": True,
    },
)

# Customer and sample products.
customer = get_or_create(
    "res.partner",
    [("email", "=", "customer.sample@seanmusic.local")],
    {
        "name": "Khách hàng mẫu Sean Music",
        "email": "customer.sample@seanmusic.local",
        "company_id": company.id,
        "customer_rank": 1,
    },
)
product_a = get_or_create(
    "product.product",
    [("default_code", "=", "SEAN-BEAT-001")],
    {
        "name": "Beat nhạc độc quyền - Gói Basic",
        "default_code": "SEAN-BEAT-001",
        "list_price": 500000.0,
        "sale_ok": True,
    },
)
product_a.product_tmpl_id.write({"image_1920": load_product_image("beat-basic-unsplash.jpeg")})
product_b = get_or_create(
    "product.product",
    [("default_code", "=", "SEAN-MIX-001")],
    {
        "name": "Dịch vụ mix & master - Gói Standard",
        "default_code": "SEAN-MIX-001",
        "list_price": 1200000.0,
        "sale_ok": True,
    },
)
product_b.product_tmpl_id.write({"image_1920": load_product_image("mix-master-unsplash.jpeg")})
product_donation = env["product.product"].search(
    ["|", ("name", "=", "Donation"), ("default_code", "=", "SEAN-DONATE-001")],
    limit=1,
)
if product_donation:
    product_donation.product_tmpl_id.write(
        {"image_1920": load_product_image("donation-unsplash.jpeg")}
    )

# A product-specific commission override demonstrates reusable rules.
rule = env["sean.music.commission.rule"].search(
    [("plan_id", "=", plan.id), ("product_id", "=", product_b.id)], limit=1
)
if rule:
    rule.write({"rate": 12.0, "sequence": 1})
else:
    env["sean.music.commission.rule"].create(
        {"plan_id": plan.id, "product_id": product_b.id, "rate": 12.0, "sequence": 1}
    )

# Confirmed sample order. Re-running the script updates the same order lines.
order = env["sale.order"].search(
    [("client_order_ref", "=", "SEAN-MUSIC-SAMPLE-001")], limit=1
)
order_values = {
    "partner_id": customer.id,
    "user_id": sale_user.id,
    "collaborator_id": collaborator.id,
    "company_id": company.id,
    "client_order_ref": "SEAN-MUSIC-SAMPLE-001",
    "order_line": [
        Command.create(
            {
                "product_id": product_a.id,
                "product_uom_qty": 2,
                "price_unit": product_a.list_price,
            }
        ),
        Command.create(
            {
                "product_id": product_b.id,
                "product_uom_qty": 1,
                "price_unit": product_b.list_price,
            }
        ),
    ],
}
if order:
    if order.state in ("draft", "sent"):
        order.write({"order_line": [Command.clear()]})
        order.write(order_values)
    order.write({"user_id": sale_user.id, "collaborator_id": collaborator.id})
else:
    order = env["sale.order"].create(order_values)
if order.state in ("draft", "sent"):
    order.action_confirm()

env.cr.commit()
print(
    "SAMPLE_DATA_READY",
    "user=", sale_user.login,
    "partner=", sale_partner.display_name,
    "order=", order.name,
    "state=", order.state,
    "untaxed=", order.amount_untaxed,
    "commission=", order.commission_amount,
)
