{
    "name": "Sean Music Home Theme",
    "version": "20.0.1.0.1",
    "category": "Hidden",
    "summary": "Sean Music branded login and application home screen",
    "description": "A Sean Music home screen inspired by the company's internal app launcher, implemented for Odoo 20.",
    "depends": ["web", "website"],
    "data": [
        "views/home_action.xml",
        "views/login_templates.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "sean_music_home/static/src/js/sean_music_home.js",
            "sean_music_home/static/src/xml/sean_music_home.xml",
            "sean_music_home/static/src/scss/sean_music_home.scss",
        ],
        "web.assets_frontend": [
            "sean_music_home/static/src/scss/sean_music_login.scss",
        ],
    },
    "license": "LGPL-3",
    "author": "Sean Music",
    "installable": True,
    "application": True,
}
