from odoo.tools.safe_eval import safe_eval, time

import base64
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class MailTemplate(models.Model):
    _inherit = "mail.template"

    def _folder_id(self):
        foldr = self.env.company.product_folder_id
        return [('folder_id', '=', foldr.id)]

    send_dropship_documents = fields.Boolean(default=False, string="Send dropship documents")

