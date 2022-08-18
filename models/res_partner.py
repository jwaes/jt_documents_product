from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    send_dropship_report_with_po = fields.Boolean(default=False, company_dependent=True, string="Attach DS report", help="Attach Dropship delivery slip to PO's for this partner")
    dropship_report = fields.Many2one('ir.actions.report', string='Dropship report')