import logging
from odoo.upgrade import util


_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = util.env(cr)

    for record in env['product.document'].browse(ids):
        
        if record.mail_attach_on_so:
            record.attached_on_sale = 'quotation'
