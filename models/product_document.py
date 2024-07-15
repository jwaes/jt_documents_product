# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductDocument(models.Model):
    _inherit = 'product.document'

    mail_attach_on_so = fields.Boolean(string="Attach on Quotation / Sales Order")
    mail_attach_on_po = fields.Boolean(string="Attach on RFQ / Purchase Order")
