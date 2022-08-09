import logging
from odoo import api, fields, models, _


_logger = logging.getLogger(__name__)

class MailTemplate(models.Model):
    _inherit = "mail.template"

    def _folder_id(self):
        foldr = self.env.company.product_folder
        return [('folder_id', '=', foldr.id)]

    attachment_ids = fields.Many2many('ir.attachment', compute='_compute_attachment_ids', string='attachment_ids'  )

    fixed_attachment_ids = fields.Many2many('ir.attachment', 'email_template_attachment_rel', 'email_template_id',
                                      'attachment_id', 'Fixed Attachments',
                                      help="You may attach files to this template, to be added to all "
                                           "emails created from this template")

    product_document_tag_so = fields.Many2one('documents.tag', string="Product document SO tag", domain=_folder_id,
                                     default=lambda self: self.env.ref('product_document_tag_so',
                                                                       raise_if_not_found=False))
    is_so = fields.Boolean(compute='_compute_is_so', string='Is So')


    product_document_tag_po = fields.Many2one('documents.tag', string="Product document PO tag", domain=_folder_id,
                                     default=lambda self: self.env.ref('product_document_tag_po',
                                                                       raise_if_not_found=False))
    is_po = fields.Boolean(compute='_compute_is_po', string='Is Po')
    

    @api.depends('model')
    def _compute_is_so(self):
        for tmpl in self:
            tmpl.is_so = tmpl.model == 'sale.order'

    @api.depends('model')
    def _compute_is_po(self):
        for tmpl in self: 
            tmpl.is_po = tmpl.model == 'purchase.order'

    @api.depends('fixed_attachment_ids')
    def _compute_attachment_ids(self):
        active_id = self.env.context.get('active_id')
        for tmpl in self:
            tmpl.attachment_ids = tmpl.fixed_attachment_ids

            if tmpl.is_po and tmpl.product_document_tag_po:
                pos = self.env[tmpl.model].search([('id', '=', active_id)])
                for po in pos:
                    for line in po.order_line:
                        product = line.product_id
                        for document in product.document_ids:
                            for tag in document.tag_ids:
                                if tag.id == tmpl.product_document_tag_po.id:
                                    tmpl.attachment_ids = tmpl.attachment_ids | document.attachment_id

            if tmpl.is_so and tmpl.product_document_tag_so:
                sos = self.env[tmpl.model].search([('id', '=', active_id)])
                for so in sos:
                    for line in so.order_line:
                        product = line.product_id
                        for document in product.document_ids:
                            for tag in document.tag_ids:
                                if tag.id == tmpl.product_document_tag_so.id:
                                    tmpl.attachment_ids = tmpl.attachment_ids | document.attachment_id
    

    def generate_email(self, res_ids, fields):
        res = super().generate_email(res_ids, fields)

        return res