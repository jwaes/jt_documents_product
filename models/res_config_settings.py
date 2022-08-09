from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    product_document_tag_so = fields.Many2one('documents.tag', related='company_id.product_document_tag_so', readonly=False,
                                     string="Product document SO tag")

    product_document_tag_po = fields.Many2one('documents.tag', related='company_id.product_document_tag_po', readonly=False,
                                     string="Product document PO tag")

