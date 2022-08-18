from odoo import api, fields, models, api, _


class ResCompany(models.Model):
    _inherit = "res.company"

    def _folder_id(self):
        foldr = self.env.company.product_folder
        return [('folder_id', '=', foldr.id)]

    product_document_tag_so = fields.Many2one('documents.tag', string="Product document SO tag", domain=_folder_id,
                                     default=lambda self: self.env.ref('product_document_tag_so',
                                                                       raise_if_not_found=False))

    product_document_tag_po = fields.Many2one('documents.tag', string="Product document PO tag", domain=_folder_id,
                                     default=lambda self: self.env.ref('product_document_tag_po',
                                                                       raise_if_not_found=False))                                                                 

