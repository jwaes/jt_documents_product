import logging
from odoo.upgrade import util


_logger = logging.getLogger(__name__)


def migrate(cr, version):

    env = util.env(cr)

    documents = env["product.document"].search([])

    for doc in documents:
        if doc.mail_attach_on_so:
            doc.attached_on_sale = 'quotation'

            
    util.field.remove_field(cr, "product.document", "mail_attach_on_so")