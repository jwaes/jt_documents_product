import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _folder_id(self):
        foldr = self._get_document_folder()
        return [('folder_id', '=', foldr.id)]

    tmpl_document_ids = fields.One2many('documents.document', string='Template documents', compute='_compute_tmpl_document_ids')
    tmpl_document_count = fields.Integer('Document Count', compute='_compute_tmpl_document_count')

    tmpl_attachment_po_ids = fields.Many2many('ir.attachment','attachment_product_tmpl_po_rel','product_tmpl_id','attach_id', string='PO Attachments',) 
    tmpl_attachment_so_ids = fields.Many2many('ir.attachment','attachment_product_tmpl_so_rel','product_tmpl_id','attach_id', string='SO Attachments',) 


    product_attachment_tag_po = fields.Many2one('documents.tag', string="Product document PO tag", domain=_folder_id,
                                    default=lambda self: self.env.ref('product_document_tag_po',
                                                                    raise_if_not_found=False))
    product_attachment_tag_so = fields.Many2one('documents.tag', string="Product document SO tag", domain=_folder_id,
                                    default=lambda self: self.env.ref('product_document_tag_so',
                                                                    raise_if_not_found=False))                                                                    
    

    @api.onchange('tmpl_attachment_po_ids')
    def _onchange_tmpl_attachment_po_ids(self):
        self.ensure_one()

        for new_attach in self.tmpl_attachment_po_ids:
            if new_attach.id.origin not in self._origin.tmpl_attachment_po_ids.ids:
                document = self.env['documents.document'].search([('attachment_id','=', new_attach.id.origin)])
                document.add_po_tag()

        for original_attach in self._origin.tmpl_attachment_po_ids:
            attach_found = False
            for new_attach in self.tmpl_attachment_po_ids:
                if original_attach.id == new_attach.id.origin:
                    attach_found= True
            if not attach_found:
                document = self.env['documents.document'].search([('attachment_id','=',original_attach.id)])
                _logger.info("removed an attachment")
                document.remove_po_tag()

    @api.onchange('tmpl_attachment_so_ids')
    def _onchange_tmpl_attachment_so_ids(self):
        self.ensure_one()

        for new_attach in self.tmpl_attachment_so_ids:
            if new_attach.id.origin not in self._origin.tmpl_attachment_so_ids.ids:
                document = self.env['documents.document'].search([('attachment_id','=', new_attach.id.origin)])
                document.add_so_tag()

        for original_attach in self._origin.tmpl_attachment_so_ids:
            attach_found = False
            for new_attach in self.tmpl_attachment_so_ids:
                if original_attach.id == new_attach.id.origin:
                    attach_found= True
            if not attach_found:
                document = self.env['documents.document'].search([('attachment_id','=',original_attach.id)])
                _logger.info("removed an attachment")
                document.remove_so_tag()                

    def add_po_document(self, document):
        self.write({'tmpl_attachment_po_ids':[(4,document.attachment_id.id,_)]})

    def remove_po_document(self, document):
        self.write({'tmpl_attachment_po_ids':[(3,document.attachment_id.id,_)]})

    def add_so_document(self, document):
        self.write({'tmpl_attachment_so_ids':[(4,document.attachment_id.id,_)]})

    def remove_so_document(self, document):
        self.write({'tmpl_attachment_so_ids':[(3,document.attachment_id.id,_)]})

    def _compute_tmpl_document_count(self):
        for record in self:
            record.tmpl_document_count = len(self.tmpl_document_ids)        

    @api.depends('tmpl_attachment_po_ids')
    def _compute_tmpl_document_ids(self):
        documents = self.env['documents.document'].search([('res_model', '=', self._name), ('res_id', '=', self.id), ('type', '=', 'binary'), ])
        self.tmpl_document_ids = documents

    def action_see_tmpl_documents(self):
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
            _logger.info("Product template: %s", record.name)
            for po_a in record.tmpl_attachment_po_ids:
                if po_a.res_model != record._name:
                    _logger.info("PO model does not match")
                    po_a.res_model = record._name
                    po_a.res_id = record.id
                else:
                    _logger.info("PO model matches")
            for so_a in record.tmpl_attachment_so_ids:
                if so_a.res_model != record._name:
                    _logger.info("SO model does not match")
                    so_a.res_model = record._name
                    so_a.res_id = record.id
                else:
                    _logger.info("SO model matches")                    
            for product in record.product_variant_ids:
                product.fix_document_models()


