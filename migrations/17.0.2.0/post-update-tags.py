import logging
from odoo.upgrade import util


_logger = logging.getLogger(__name__)


def migrate(cr, version):
    
    ProductDocument = util.env(cr)['product.document']
    DocumentsDocument = util.env(cr)['documents.document']

    po_tag = util.env(cr).user.company_id.product_document_tag_po
    _logger.info("PO tag is %s ", po_tag.name)
    attach_ids = DocumentsDocument.search([['tag_ids', 'in', po_tag.id]]).attachment_id.ids
    ids = ProductDocument.search([['ir_attachment_id', 'in', attach_ids ]]).ids



    for record in util.iter_browse(ProductDocument, ids):
        _logger.info("Product document PO %s", record.name)
        record.mail_attach_on_po = True


    so_tag = util.env(cr).user.company_id.product_document_tag_so
    _logger.info("SO tag is %s ", so_tag.name)    
    attach_ids = DocumentsDocument.search([['tag_ids', 'in', so_tag.id]]).attachment_id.ids
    ids = ProductDocument.search([['ir_attachment_id', 'in', attach_ids ]]).ids

    for record in util.iter_browse(ProductDocument, ids):
        _logger.info("Product document SO %s", record.name)
        record.mail_attach_on_so = True
        record.attached_on = 'quotation'

