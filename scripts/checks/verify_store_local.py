"""Read-only storefront checks by default. --allow-writes also creates a draft cart.

--submit-inquiry also creates one clearly labelled local verification inquiry.
No payment or order confirmation is submitted.
"""
import argparse
import re
from urllib.parse import urljoin, urlparse

import requests
from lxml import html


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--base-url", default="http://127.0.0.1:8079")
parser.add_argument("--allow-writes", action="store_true", help="Allow a draft cart on a disposable local test database")
parser.add_argument("--submit-inquiry", action="store_true")
args = parser.parse_args()
base = args.base_url.rstrip("/")
if urlparse(base).hostname not in ("127.0.0.1", "localhost", "::1") or urlparse(base).scheme != "http":
    parser.error("Only local HTTP test servers are allowed.")
if args.submit_inquiry and not args.allow_writes:
    parser.error("--submit-inquiry requires --allow-writes and a disposable local database.")
session = requests.Session()


def get(path):
    response = session.get(urljoin(base, path), timeout=30)
    assert response.status_code == 200, (path, response.status_code)
    return html.fromstring(response.content)


for path in ["/", "/shop", "/huong-dan-chon-dan", "/ve-sean-music", "/lien-he", "/chinh-sach", "/web/login"]:
    tree = get(path)
    assert tree.get("lang", "").startswith("vi"), (path, tree.get("lang"))
    print("PAGE_OK", path)

tree = get("/shop?max_price=5000000")
prices = tree.xpath('//div[contains(@class,"product_price")]//span[contains(@class,"oe_currency_value")]/text()')
assert prices, "No price filter results"
assert all(int(re.sub(r"\D", "", price)) <= 5000000 for price in prices), prices
print("PRICE_FILTER_OK", len(prices))

tree = get("/shop?search=Enya")
titles = tree.xpath('//h6[contains(@class,"o_wsale_products_item_title")]/a//span/text()')
assert titles and all("Enya" in title for title in titles), titles
print("SEARCH_OK", titles)

tree = get("/shop")
detail = tree.xpath('//h6[contains(@class,"o_wsale_products_item_title")]/a/@href')[0]
tree = get(detail)
assert "Cần xác nhận tình trạng" in tree.text_content()
template_id = tree.xpath('//button[@name="add_to_cart"]/@data-product-template-id')
product_id = tree.xpath('//button[@name="add_to_cart"]/@data-product-id')
assert template_id and product_id, "Missing native cart product metadata"
if args.allow_writes:
    response = session.post(base + "/shop/cart/add", json={
    "jsonrpc": "2.0", "method": "call", "id": 1,
    "params": {"product_template_id": int(template_id[0]), "product_id": int(product_id[0]), "quantity": 1},
    }, timeout=30)
    payload = response.json()
    assert "error" not in payload, payload
    cart = get("/shop/cart")
    assert cart.xpath('//*[@id="cart_products"]'), "Cart item missing"
    assert "₫" in cart.text_content()
    print("CART_OK")
else:
    print("CART_NOT_RUN (use --allow-writes on a disposable local database)")

contact = get("/lien-he")
token = contact.xpath('//form[@action="/lien-he/gui"]/input[@name="csrf_token"]/@value')[0]
response = session.post(base + "/lien-he/gui", data={"name": "Kiểm thử local"}, timeout=30)
assert response.status_code == 400, response.status_code
print("CSRF_OK")
response = session.post(base + "/lien-he/gui", data={
    "csrf_token": token, "name": "Kiểm thử local", "email": "invalid", "message": "Kiểm tra thông tin đầu vào của biểu mẫu.",
}, timeout=30)
assert response.status_code == 200 and "Địa chỉ email chưa hợp lệ" in response.text
print("FORM_VALIDATION_OK")

if args.submit_inquiry:
    response = session.post(base + "/lien-he/gui", data={
        "csrf_token": token, "name": "Kiểm thử giao diện local",
        "email": "kiem-thu@example.invalid",
        "message": "Yêu cầu kiểm thử tự động trên local, không phải khách hàng thật.",
        "state": "done", "company_id": "99999",
    }, timeout=30)
    assert response.status_code == 200 and "Sean Music đã nhận yêu cầu" in response.text
    print("INQUIRY_SAVED_OK")
print("STOREFRONT_VERIFIED")
