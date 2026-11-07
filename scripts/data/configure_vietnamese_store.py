"""Run with Odoo shell against the local db_seanmusic database."""
import json
import os
from pathlib import Path

from odoo import Command
from odoo.tools import BinaryBytes


if env.cr.dbname != "db_seanmusic":
    raise RuntimeError("This configuration is restricted to db_seanmusic.")

website = env["website"].browse(1)
vietnamese = env["res.lang"].search([("code", "=", "vi_VN")], limit=1)
vnd = env.ref("base.VND")
vnd.active = True
website.write({
    "name": "Sean Music",
    "default_lang_id": vietnamese.id,
    "language_ids": [Command.set(vietnamese.ids)],
    "homepage_url": "/sean-music",
    "shop_ppg": 24,
    "shop_ppr": 4,
    "shop_gap": "22px",
    "show_category_title": True,
    "shop_opt_products_design_classes": (
        "o_wsale_products_opt_layout_catalog o_wsale_products_opt_design_thumbs "
        "o_wsale_products_opt_name_color_regular o_wsale_products_opt_rounded_1 "
        "o_wsale_products_opt_thumb_contain o_wsale_products_opt_cc1"
    ),
})
website.user_id.partner_id.lang = "vi_VN"

pricelist = env["product.pricelist"].search([
    ("website_id", "=", website.id), ("currency_id", "=", vnd.id),
], limit=1)
if not pricelist:
    pricelist = env["product.pricelist"].create({
        "name": "Sean Music - Giá bán VND",
        "currency_id": vnd.id, "website_id": website.id,
        "company_id": website.company_id.id, "selectable": True,
        "sequence": 1, "tax_display": "tax_excluded",
    })
website.user_id.partner_id.specific_property_product_pricelist = pricelist

base = Path(os.environ.get("SEAN_MUSIC_ROOT", Path.cwd())).resolve()
if not (base / "custom_addons/sean_music_store").is_dir():
    raise RuntimeError("Run Odoo shell from the project root or set SEAN_MUSIC_ROOT.")
image_manifest = base / "assets/products/references/sources.json"
image_sources = json.loads(image_manifest.read_text()) if image_manifest.exists() else {}
local_images = {
    "AMP-NUX-DA30BT": "assets/products/originals/Amp/Amplifier Nux DA-30BT",
    "AMP-NUX-MB50BT": "assets/products/originals/Amp/Amplifier Nux Mighty Bass 50BT",
    "GUITAR-BASS-XANH": "assets/products/originals/Guitar/Bass Xanh",
    "GUITAR-ENYA-XMARI": "assets/products/originals/Guitar/Enya Xmari",
    "DRUM-NUX-DM210": "assets/products/originals/Drum/NUX DM210",
}
for folder in (base / "assets/products/originals/Drum").iterdir():
    for model in ["DM110", "DM310", "DM7X", "DM8", "DP2000"]:
        if model in folder.name:
            local_images["DRUM-NUX-" + model] = str(folder.relative_to(base))

products = env["product.template"].search([
    ("sale_ok", "=", True), ("default_code", "!=", False),
])
for product in products:
    code = product.default_code
    if not code.startswith(("GUITAR-", "DRUM-", "AMP-", "SEAN-")):
        continue
    if code.startswith("GUITAR-"):
        if code == "GUITAR-BASS-XANH":
            category = "bass"
        elif code in ("GUITAR-DONNER-HUSHC", "GUITAR-DONNER-HUSHIPRO"):
            category = "acoustic"
        else:
            category = "electric"
    elif code.startswith("DRUM-"):
        category = "drum"
    elif code.startswith("AMP-"):
        category = "amp"
    else:
        category = "service"
    product.write({
        "public_categ_ids": [Command.set(env.ref("sean_music_store.category_" + category).ids)],
        "is_published": True,
        "website_sequence": {
            "electric": 10000, "acoustic": 20000, "bass": 30000,
            "drum": 40000, "amp": 50000, "service": 60000,
        }[category] + product.id,
    })
    if code.startswith("SEAN-"):
        product.sean_condition_notes = "Dịch vụ âm nhạc. Trao đổi nội dung, thời hạn và quyền sử dụng trước khi đặt hàng."
        service_images = {
            "SEAN-BEAT-001": "beat-basic-unsplash.jpeg",
            "SEAN-MIX-001": "mix-master-unsplash.jpeg",
        }
        if code in service_images and not product.image_128:
            product.image_1920 = BinaryBytes(
                (base / "assets/products/services" / service_images[code]).read_bytes()
            )
    if code in local_images and not product.image_128:
        candidates = sorted((base / local_images[code]).glob("*.jpg"))
        if candidates:
            product.image_1920 = BinaryBytes(candidates[0].read_bytes())
    if code in image_sources and not product.image_128:
        source = image_sources[code]
        product.write({
            "image_1920": BinaryBytes((base / source["file"]).read_bytes()),
            "sean_image_source": source["page"],
            "sean_condition_notes": "Ảnh minh họa model từ nhà sản xuất/nhà bán lẻ. Cần xác nhận ảnh thực tế, ngoại hình, màu sắc và phụ kiện của món hàng trước khi mua.",
        })
    item = env["product.pricelist.item"].search([
        ("pricelist_id", "=", pricelist.id), ("product_tmpl_id", "=", product.id),
    ], limit=1)
    values = {
        "pricelist_id": pricelist.id, "product_tmpl_id": product.id,
        "applied_on": "1_product", "compute_price": "fixed",
        "fixed_price": product.list_price,
    }
    if item:
        item.write(values)
    else:
        env["product.pricelist.item"].create(values)

for code, name in {
    "GUITAR-ENYA-XMARI": "Guitar điện Enya X-Mari",
    "GUITAR-BASS-XANH": "Guitar bass màu xanh",
    "AMP-NUX-DA30BT": "Ampli NUX DA-30BT",
    "AMP-NUX-MB50BT": "Ampli bass NUX Mighty Bass 50BT",
    "GUITAR-NS2NA": "Guitar điện Tanglewood Northstar NS2NA",
    "GUITAR-NS1MC": "Guitar điện Tanglewood Northstar NS1MC",
    "GUITAR-NS1BL": "Guitar điện Tanglewood Northstar NS1BL",
    "GUITAR-FENDER-PLAYER2": "Guitar điện Fender Player II Stratocaster HSS",
}.items():
    product = products.filtered(lambda p: p.default_code == code)
    product.with_context(lang="en_US").write({"name": name})
    product.with_context(lang="vi_VN").write({"name": name})

donation = env["product.template"].search([("id", "=", 5)])
if donation:
    donation.with_context(lang="vi_VN").name = "Ủng hộ hoạt động âm nhạc"
    donation.write({
        "website_sequence": 99999,
        "public_categ_ids": [Command.set(env.ref("sean_music_store.category_service").ids)],
    })

for old_id, name in {
    1: "Nhạc cụ", 2: "Đĩa nhạc", 3: "Phụ kiện", 4: "Bản nhạc",
    5: "Đồ lưu niệm", 6: "Thiết bị âm thanh", 7: "Khóa học", 8: "Bộ sản phẩm",
}.items():
    old_category = env["product.public.category"].browse(old_id).exists()
    if old_category:
        old_category.with_context(lang="vi_VN").write({"name": name, "not_in_shop": True})

for tax in env["account.tax"].search([("company_id", "=", website.company_id.id)]):
    label = tax.with_context(lang="en_US").invoice_label or ""
    if label.startswith("Tax "):
        tax.with_context(lang="vi_VN").invoice_label = label.replace("Tax ", "Thuế ", 1)

for code, name in {
    "SEAN-BEAT-001": "Beat nhạc độc quyền - Gói cơ bản",
    "SEAN-MIX-001": "Dịch vụ mix và master - Gói tiêu chuẩn",
}.items():
    products.filtered(lambda p: p.default_code == code).with_context(lang="vi_VN").name = name

for xmlid, active in [
    ("website_sale.products_categories", True),
    ("website_sale.products_categories_top", False),
    ("website_sale.products_attributes", True),
    ("website_sale.filter_products_price", True),
]:
    view = env.ref(xmlid, raise_if_not_found=False)
    if view:
        view.active = active

env["ir.module.module"]._load_module_terms(
    ["web", "website", "website_sale", "portal", "auth_signup", "auth_passkey_portal", "payment", "website_sale_stock"],
    ["vi_VN"], overwrite=False,
)
env.cr.commit()
print("VIETNAMESE_STORE_READY", len(products), "products; pricelist", pricelist.id)
