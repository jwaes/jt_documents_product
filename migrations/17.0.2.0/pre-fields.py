import logging
from odoo.upgrade import util


_logger = logging.getLogger(__name__)


def migrate(cr, version):

    util.remove_view(cr, xml_id='jt_documents_product.email_template_form_inherit_mail')
    util.remove_view(cr, xml_id='jt_documents_product.res_config_settings_view_form')
    