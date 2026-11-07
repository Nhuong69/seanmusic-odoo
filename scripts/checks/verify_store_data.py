"""Local fixture check after checks/verify_store_local.py --allow-writes --submit-inquiry."""

assert env.cr.dbname == "db_seanmusic", "Only run against the local Sean Music database"
physical_products = env["product.template"].search([
    "|", "|", ("default_code", "=like", "GUITAR-%"),
    ("default_code", "=like", "DRUM-%"), ("default_code", "=like", "AMP-%"),
])
assert len(physical_products) == 31, len(physical_products)
missing_images = physical_products.filtered(lambda product: not product.image_1920)
assert not missing_images, missing_images.mapped("default_code")
print("PRODUCT_IMAGES_OK", len(physical_products))

public_inquiries = env["sean.music.inquiry"].with_user(env.ref("base.public_user"))
for operation in ("read", "create", "write", "unlink"):
    assert not public_inquiries.has_access(operation), operation
print("PUBLIC_INQUIRY_ACCESS_DENIED_OK")

inquiry = env["sean.music.inquiry"].search([
    ("email", "=", "kiem-thu@example.invalid"),
    ("name", "=", "Kiểm thử giao diện local"),
], order="id desc", limit=1)
assert inquiry and inquiry.state == "new", "The public form must not accept an arbitrary state"
assert inquiry.company_id == env["website"].browse(1).company_id
assert inquiry.website_id.id == 1
print("INQUIRY_PERSISTENCE_AND_ALLOWLIST_OK", inquiry.id)
print("STORE_DATA_VERIFIED")
