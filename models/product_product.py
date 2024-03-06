import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_document_ids = fields.One2many('documents.document', string='Variant documents', compute='_compute_product_document_ids')
    product_document_count = fields.Integer('Variant Document Count', compute='_compute_product_document_count')

    product_attachment_po_ids = fields.Many2many('ir.attachment','attachment_product_po_rel','product_id','attach_id', string='Variant PO Attachments',) 
    product_attachment_so_ids = fields.Many2many('ir.attachment','attachment_product_so_rel','product_id','attach_id', string='Variant SO Attachments',)     

    product_calculated_attachment_po_ids = fields.Many2many('ir.attachment',compute='_compute_product_calculated_attachment_po_ids') 

    @api.depends('product_attachment_po_ids')
    def _compute_product_calculated_attachment_po_ids(self):
        for prd in self:
            prd.product_calculated_attachment_po_ids = prd.product_attachment_po_ids | prd.product_tmpl_id.tmpl_attachment_po_ids
            blah = 1


    @api.onchange('product_attachment_po_ids')
    def _onchange_product_attachment_po_ids(self):
        self.ensure_one()

        for new_attach in self.product_attachment_po_ids:
            if new_attach.id.origin not in self._origin.product_attachment_po_ids.ids:
                document = self.env['documents.document'].search([('attachment_id','=', new_attach.id.origin)])
                document.add_po_tag()

        for original_attach in self._origin.product_attachment_po_ids:
            attach_found = False
            for new_attach in self.product_attachment_po_ids:
                if original_attach.id == new_attach.id.origin:
                    attach_found= True
            if not attach_found:
                document = self.env['documents.document'].search([('attachment_id','=',original_attach.id)])
                _logger.info("removed an attachment")
                document.remove_po_tag()

    @api.onchange('product_attachment_so_ids')
    def _onchange_product_attachment_so_ids(self):
        self.ensure_one()

        for new_attach in self.product_attachment_so_ids:
            if new_attach.id.origin not in self._origin.product_attachment_so_ids.ids:
                document = self.env['documents.document'].search([('attachment_id','=', new_attach.id.origin)])
                document.add_so_tag()

        for original_attach in self._origin.product_attachment_so_ids:
            attach_found = False
            for new_attach in self.product_attachment_so_ids:
                if original_attach.id == new_attach.id.origin:
                    attach_found= True
            if not attach_found:
                document = self.env['documents.document'].search([('attachment_id','=',original_attach.id)])
                _logger.info("removed an attachment")
                document.remove_so_tag()   

    def _compute_product_document_count(self):
        for record in self:
            record.product_document_count = len(self.product_document_ids)        

    @api.depends('product_attachment_po_ids')
    def _compute_product_document_ids(self):
        documents = self.env['documents.document'].search([('res_model', '=', self._name), ('res_id', '=', self.id), ('type', '=', 'binary'), ])
        self.product_document_ids = documents


    def add_po_document(self, document):
        self.write({'product_attachment_po_ids':[(4,document.attachment_id.id,_)]})

    def remove_po_document(self, document):
        self.write({'product_attachment_po_ids':[(3,document.attachment_id.id,_)]})

    def add_so_document(self, document):
        self.write({'product_attachment_so_ids':[(4,document.attachment_id.id,_)]})

    def remove_so_document(self, document):
        self.write({'product_attachment_so_ids':[(3,document.attachment_id.id,_)]})


    def action_see_documents(self):
        self.ensure_one()
        folder_id = self._get_document_folder()
        return {
            'name': _('Documents'),
            'res_model': 'documents.document',
            'type': 'ir.actions.act_window',
            'views': [(False, 'list')],
            'view_mode': 'list',
            'context': {
                "searchpanel_default_folder_id": folder_id,
            },
            'domain': [
                ['res_model', '=', self._name],
                ['res_id', '=', self.id],
            ],
        }    

    def fix_document_models(self):
        for record in self:
            _logger.info("Product variant: %s", record.name)
            for po_a in record.product_attachment_po_ids:
                if po_a.res_model != record._name:
                    _logger.info("PO model does not match")
                    po_a.res_model = record._name
                    po_a.res_id = record.id
                else:
                    _logger.info("PO model matches")
            for so_a in record.product_attachment_so_ids:
                if so_a.res_model != record._name:
                    _logger.info("SO model does not match")
                    so_a.res_model = record._name
                    so_a.res_id = record.id
                else:
                    _logger.info("SO model matches")                       