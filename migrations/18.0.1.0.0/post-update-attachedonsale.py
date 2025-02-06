import logging
from odoo.upgrade import util


_logger = logging.getLogger(__name__)


def migrate(cr, version):
            
    util.field.remove_field(cr, "product.document", "mail_attach_on_so")