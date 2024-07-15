# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductDocument(models.Model):
    _inherit = 'product.document'

    mail_attach_on_so = fields.Boolean(string="Attach Sales Order")
    mail_attach_on_po = fields.Boolean(string="Attach Purchase Order")

    def action_goto_documents(self):
        self.ensure_one()
        folder_id = self.env['product.product']._get_document_folder()
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
