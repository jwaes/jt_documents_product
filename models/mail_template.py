from odoo.tools.safe_eval import safe_eval, time

import base64
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class MailTemplate(models.Model):
    _inherit = "mail.template"

    def _folder_id(self):
        foldr = self.env.company.product_folder
        return [('folder_id', '=', foldr.id)]

    send_dropship_documents = fields.Boolean(default=False, string="Send dropship documents")

    attachment_ids = fields.Many2many(
        'ir.attachment', compute='_compute_attachment_ids', string='attachment_ids')

    fixed_attachment_ids = fields.Many2many('ir.attachment', 'email_template_attachment_rel', 'email_template_id',
                                      'attachment_id', 'Fixed Attachments',
                                      help="You may attach files to this template, to be added to all "
                                           "emails created from this template")

    # product_document_tag_so = fields.Many2one('documents.tag', string="Product document SO tag", domain=_folder_id,
    #                                  default=lambda self: self.env.ref('product_document_tag_so',
    #                                                                    raise_if_not_found=False))
    is_so = fields.Boolean(compute='_compute_is_so', string='Is So')

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
            po_tag = self.env.user.company_id.product_document_tag_po
            if tmpl.is_po and po_tag:
                pos = self.env[tmpl.model].search([('id', '=', active_id)])
                for po in pos:
                    for line in po.order_line:
                        product = line.product_id
                        for attach in product.product_tmpl_id.tmpl_attachment_po_ids:
                            tmpl.attachment_ids = tmpl.attachment_ids | attach
                        for attach in product.product_attachment_po_ids:
                            tmpl.attachment_ids = tmpl.attachment_ids | attach
                    if tmpl.send_dropship_documents:
                        company = po.partner_id
                        if not company.is_company:
                            company = po.partner_id.company_id
                        if company.partner_id.send_dropship_report_with_po and company.dropship_report:
                            for dropship in po.picking_ids.filtered(lambda p: p.is_dropship):
                                report_data = self._generate_dropship_report(company.dropship_report, dropship, po)
                                if report_data:
                                    Attachment = self.env['ir.attachment']
                                    tmpl.write({'attachment_ids':[(4,Attachment.create(report_data).id,_)]})

            so_tag = self.env.user.company_id.product_document_tag_so
            if tmpl.is_so and so_tag:
                sos = self.env[tmpl.model].search([('id', '=', active_id)])
                for so in sos:
                    for line in so.order_line:
                        product = line.product_id
                        for attach in product.product_tmpl_id.tmpl_attachment_so_ids:
                            tmpl.attachment_ids = tmpl.attachment_ids | attach                          
                        for attach in product.product_attachment_so_ids:
                            tmpl.attachment_ids = tmpl.attachment_ids | attach
            
    def _generate_dropship_report(self, report, dropship, po):
        if dropship:
            if report.report_type in ['qweb-html', 'qweb-pdf']:
                result, format = report._render_qweb_pdf([dropship.id])
            else:
                res = report._render([dropship])
                if not res:
                    raise UserError(_('Unsupported report type %s found.', report.report_type))
                result, format = res
            
            if not report.attachment:
                raise UserError(_('The report should have the \'Save as Attachment Prefix\' field filled in'))

            attachment_name = safe_eval(report.attachment, {'object': dropship, 'time': time})
            result = base64.b64encode(result)

            attachment_data = {
                'name': attachment_name,
                'datas': result,
                'type': 'binary',
            }            
            return attachment_data



    def generate_email(self, res_ids, fields):
        res = super().generate_email(res_ids, fields)

        return res