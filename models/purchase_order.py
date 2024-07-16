from odoo.tools.safe_eval import safe_eval, time

import base64
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _process_attachments_for_template_post(self, mail_template):
        result = super()._process_attachments_for_template_post(mail_template)
     
        for order in self:
            order_result = result.setdefault(order.id, {})
            docs = order.order_line.product_id.product_document_ids.filtered(lambda s: s.mail_attach_on_po == True)
            order_result.setdefault('attachment_ids', [])
            attachments = order_result.setdefault('attachments', [])
            for doc in docs:
                 attachments.extend([( doc.ir_attachment_id.name,  doc.ir_attachment_id.datas)])

            if mail_template.send_dropship_documents:
                partner = order.partner_id
                send_dropship_report = False
                company = None
                if partner.is_company:
                    company = partner
                    send_dropship_report = company.send_dropship_report_with_po
                    company = partner
                elif partner.parent_id:
                    company = partner.parent_id
                    send_dropship_report = company.send_dropship_report_with_po
                if send_dropship_report and company.dropship_report:
                    for dropship in order.picking_ids.filtered(lambda p: p.is_dropship):
                        report_data = order._generate_dropship_report(company.dropship_report, dropship)
                        if report_data:
                            Attachment = self.env['ir.attachment']
                            delivery_slip = Attachment.create(report_data)
                            attachments.extend([( delivery_slip.name, delivery_slip.datas)])

        return result


    def _generate_dropship_report(self, report, dropship, lang='en'):
        if dropship:
            if report.report_type in ['qweb-html', 'qweb-pdf']:
                result, format = report.with_context(lang=lang)._render_qweb_pdf(dropship.id)
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