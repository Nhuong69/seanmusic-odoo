{
    "name": "Sean Music - Cửa hàng nhạc cụ tiếng Việt",
    "version": "20.0.1.0.0",
    "category": "Website/Theme",
    "summary": "Giao diện và thông tin nhạc cụ dành cho khách hàng Việt Nam",
    "depends": ["website_sale", "sean_music_home"],
    "data": [
        "security/ir.access.csv", "views/store_templates.xml",
        "views/product_views.xml", "views/inquiry_views.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "sean_music_store/static/src/scss/store.scss",
        ],
    },
    "license": "LGPL-3",
    "author": "Sean Music",
    "installable": True,
    "application": False,
}
