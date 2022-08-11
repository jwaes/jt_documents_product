import logging
from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _folder_id(self):
        foldr = self._get_document_folder()
        return [('folder_id', '=', foldr.id)]

    # attachment_ids = fields.One2many('ir.attachment', string='Attachments', compute='_compute_attachment_ids', readonly=True)    
    document_ids = fields.One2many('documents.document', string='Documents', compute='_compute_document_ids')


    attachment_po_ids = fields.Many2many('ir.attachment','attachment_product_tmpl_po_rel','product_tmpl_id','attach_id', string='PO Attachments',) 
    attachment_so_ids = fields.Many2many('ir.attachment','attachment_product_tmpl_so_rel','product_tmpl_id','attach_id', string='SO Attachments',) 

    document_count = fields.Integer('Document Count', compute='_compute_document_count')


    product_attachment_tag_po = fields.Many2one('documents.tag', string="Product document PO tag", domain=_folder_id,
                                    default=lambda self: self.env.ref('product_document_tag_po',
                                                                    raise_if_not_found=False))

    

    @api.onchange('attachment_po_ids')
    def _onchange_attachment_po_ids(self):
        self.ensure_one()

        for new_attach in self.attachment_po_ids:
            if new_attach.id.origin not in self._origin.attachment_po_ids.ids:
                document = self.env['documents.document'].search([('attachment_id','=', new_attach.id.origin)])
                document.add_po_tag()

        for original_attach in self._origin.attachment_po_ids:
            attach_found = False
            for new_attach in self.attachment_po_ids:
                if original_attach.id == new_attach.id.origin:
                    attach_found= True
            if not attach_found:
                document = self.env['documents.document'].search([('attachment_id','=',original_attach.id)])
                _logger.info("removed an attachment")
                document.remove_po_tag()

    # def sync_tagged_documents(self):
    #     self._sync_tagged_documents()

    # def _sync_tagged_documents(self):
    #     fee = 1
    #     po_tag = self.env.user.company_id.product_document_tag_po
    #     documents = self.env['documents.document'].search([('res_model', '=', self._name), ('res_id', '=', self.id), ('type', '=', 'binary')])
    #     for document in documents:
    #         _logger.info("document : %s", document.name)
    #         #attachments if there is a tag and not included
    #         for tag in document.tag_ids:
    #             if tag.id == po_tag.id:
    #                 if document.attachment_id in self.attachment_po_ids:
    #                     self._add_po_tag(document)
    #         if document.attachment_id not in self.attachment_po_ids:
    #             # not deleting in sync ... only adding
    #             # self._remove_po_tag(document)
    #             fee = 3
    #         else:
    #             document.add_po_tag()

    def add_po_document(self, document):
        _logger.info("linking PO document to product.template because a po_tag was added to the document")
        self.write({'attachment_po_ids':[(4,document.attachment_id.id,_)]})

    def remove_po_document(self, document):
        self.write({'attachment_po_ids':[(3,document.attachment_id.id,_)]})

    # def write(self, vals):
    #     write_result = super(ProductTemplate, self).write(vals)
    #     # self._sync_tagged_documents()
    #     return write_result

    def _compute_document_count(self):
        for record in self:
            record.document_count = len(self.document_ids)        


    # def _compute_attachment_ids(self):
    #     attachments = self.env['ir.attachment'].search([('res_model', '=', self._name), ('res_id', '=', self.id), ('type', '=', 'binary'), ])
    #     # ('type', 'in', ('binary', 'url'))
    #     self.attachment_ids = attachments

    @api.depends('attachment_po_ids')
    def _compute_document_ids(self):
        documents = self.env['documents.document'].search([('res_model', '=', self._name), ('res_id', '=', self.id), ('type', '=', 'binary'), ])
        self.document_ids = documents

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


