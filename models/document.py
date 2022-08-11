import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class Document(models.Model):
    _inherit = 'documents.document'


    def write(self, vals):
        write_result = super(Document, self).write(vals)
        self._sync_tags()
        return write_result

    def _sync_tags(self):
        _logger.info('syncing tags')
        if self.res_model == 'product.template':
            po_tag = self.env.user.company_id.product_document_tag_po
            product_template = self.env[self.res_model].browse(self.res_id)
            if po_tag in self.tag_ids:                
                if self.attachment_id not in product_template.tmpl_attachment_po_ids:
                    product_template.add_po_document(self)
            else:
                if self.attachment_id in product_template.tmpl_attachment_po_ids:
                    product_template.remove_po_document(self)

            so_tag = self.env.user.company_id.product_document_tag_so
            if so_tag in self.tag_ids:                
                if self.attachment_id not in product_template.tmpl_attachment_so_ids:
                    product_template.add_so_document(self)
            else:
                if self.attachment_id in product_template.tmpl_attachment_so_ids:
                    product_template.remove_so_document(self)

        if self.res_model == 'product.product':
            po_tag = self.env.user.company_id.product_document_tag_po
            product = self.env[self.res_model].browse(self.res_id)
            if po_tag in self.tag_ids:                
                if self.attachment_id not in product.product_attachment_po_ids:
                    product.add_po_document(self)
            else:
                if self.attachment_id in product.product_attachment_po_ids:
                    product.remove_po_document(self)

            so_tag = self.env.user.company_id.product_document_tag_so
            if so_tag in self.tag_ids:                
                if self.attachment_id not in product.product_attachment_so_ids:
                    product.add_so_document(self)
            else:
                if self.attachment_id in product.product_attachment_so_ids:
                    product.remove_so_document(self)                      


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

    def add_so_tag(self):
        so_tag = self.env.user.company_id.product_document_tag_so
        for document in self:
            if so_tag not in document.tag_ids:
                _logger.info("adding so tag")
                document.write({'tag_ids':[(4,so_tag.id,_)]})

    def remove_so_tag(self):
        so_tag = self.env.user.company_id.product_document_tag_so
        for document in self:
            if so_tag in document.tag_ids:
                _logger.info("removing so tag")
                document.write({'tag_ids':[(3,so_tag.id,_)]})                           
