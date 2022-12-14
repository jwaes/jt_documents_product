# -*- coding: utf-8 -*-
{
    'name': "jt_documents_product",

    'summary': "Add extra fields to account",

    'description': "",

    'author': "jaco tech",
    'website': "https://jaco.tech",
    "license": "AGPL-3",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.4',

    # any module necessary for this one to work correctly
    'depends': ['base','documents', 'documents_product', 'sale_management', 'purchase', 'contacts'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/mail_template_views.xml',
        'data/fixdocs_action_data.xml',
        'report/purchase_order_templates.xml',        
        'views/document_views.xml',
        'views/mail_template_views.xml',
        'views/product_template_views.xml',
        'views/res_partner_views.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
