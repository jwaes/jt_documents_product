import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = "product.product"


    def _get_documents_mail_attach_on_po(self):
        docs = self.product_document_ids.filtered(lambda s: s.mail_attach_on_po == True)
        docs = docs + self.product_tmpl_id.product_document_ids.filtered(lambda s: s.mail_attach_on_po == True)
        return docs