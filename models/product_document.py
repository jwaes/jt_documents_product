# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class ProductDocument(models.Model):
    _inherit = 'product.document'

    # mail_attach_on_so = fields.Boolean(string="Attach Sales Order")
    mail_attach_on_po = fields.Boolean(string="Attach Purchase Order")



    def action_goto_documents(self):
        
        company = self.company_id or self.env.company
        folder_id = company.product_folder

        _logger.info("folder is %s", folder_id.name)
        return {
            'name': self.env._('Documents'),
            'res_model': 'documents.document',
            'type': 'ir.actions.act_window',
            'views': [(False, 'list')],
            'view_mode': 'list',
            'context': {
                "searchpanel_default_folder_id": folder_id,
            },
            'domain': [
                ['res_model', '=', self.ir_attachment_id.res_model],
                ['res_id', '=', self.ir_attachment_id.res_id],
            ],
        }      
    