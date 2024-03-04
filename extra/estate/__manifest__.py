# -*- coding: utf-8 -*-
{
    'name': "Real Estate Property APP",

    'summary': "Real Estate Property APP___",

    'description': """
Real Estate Property APP
    """,

    'author': "My Company_Kiro",
    'website': "https://www.krio.com.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        "views/estate_property_offer_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        'views/estate_property_view.xml',
        "views/res_users_views.xml",
        "views/estate_menus.xml",

        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'sequence': 10,
    'application': True,
    'license': 'LGPL-3',

}

