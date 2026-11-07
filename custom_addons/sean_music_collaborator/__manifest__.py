{
    "name": "Sean Music Collaborator Commissions",
    "version": "20.0.1.0.0",
    "category": "Sales/Commission",
    "summary": "Manage collaborators, sales attribution and commissions",
    "description": """
Sean Music collaborator management
==================================
Adds collaborator attribution to sales orders and calculates commissions from
confirmed sales without modifying Odoo core.
    """,
    "depends": ["sale", "contacts"],
    "data": [
        "security/sean_music_security.xml",
        "security/ir.access.csv",
        "data/commission_sequence.xml",
        "views/collaborator_views.xml",
        "views/commission_plan_views.xml",
        "views/commission_views.xml",
        "views/sale_order_views.xml",
        "views/menuitems.xml",
    ],
    "license": "LGPL-3",
    "author": "Sean Music",
    "installable": True,
    "application": True,
}
