import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class Document(models.Model):
    _inherit = 'documents.document'


    def write(self, vals):
        write_result = super(Document, self).write(vals)
        _logger.info("write document")
        self._sync_tags()
        return write_result

    def _sync_tags(self):
        _logger.info('syncing tags')
        if self.res_model == 'product.template':
            po_tag = self.env.user.company_id.product_document_tag_po
            product_template = self.env[self.res_model].browse(self.res_id)
            if po_tag in self.tag_ids:                
                if self.attachment_id not in product_template.attachment_po_ids:
                    product_template.add_po_document(self)
            else:
                if self.attachment_id in product_template.attachment_po_ids:
                    product_template.remove_po_document(self)            

    check_if_added_to_model = fields.Char('model check')

    @api.onchange('tag_ids')
    def _onchange_tag_ids(self):
        _logger.info("tag_ids onchange triggered")

    @api.onchange('active')
    def _onchange_locked(self):
        _logger.info("active onchange triggered")

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        _logger.info("partner_id onchange triggered")

    @api.onchange('name')
    def _onchange_name(self):
        _logger.info("name onchange triggered")

    def add_po_tag(self):
        po_tag = self.env.user.company_id.product_document_tag_po
        for document in self:
            if po_tag not in document.tag_ids:
                _logger.info("adding po tag")
                document.write({'tag_ids':[(4,po_tag.id,_)]})

    def remove_po_tag(self):
        po_tag = self.env.user.company_id.product_document_tag_po
        for document in self:
            if po_tag in document.tag_ids:
                _logger.info("removing po tag")
                document.write({'tag_ids':[(3,po_tag.id,_)]})               
