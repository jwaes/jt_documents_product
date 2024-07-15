import logging
from odoo.upgrade import util


_logger = logging.getLogger(__name__)


def migrate(cr, version):
    
    po_tag = util.env(cr).user.company_id.product_document_tag_po
    _logger.info("PO tag is %s ", po_tag.name)
    so_tag = util.env(cr).user.company_id.product_document_tag_so
    _logger.info("SO tag is %s ", so_tag.name)    

    attach_ids = util.env(cr)['documents.document'].search([['tag_ids', 'in', [po_tag.id, so_tag.id]]]).attachment_id.ids

    ids = util.env(cr)['product.document'].search([['ir_attachment_id', 'in', attach_ids ]]).ids

    ProductDocument = util.env(cr)['product.document']
    for record in util.iter_browse(ProductDocument, ids):
        _logger.info("Product document %s", record.name)
        if po_tag in record.tag_ids:
            _logger.info("PO tag")
            record.mail_attach_on_po = True
        if so_tag in record.tag_ids:
            record.mail_attach_on_so = True
            record.attached_on = 'quotation'
            _logger.info("SO tag")
