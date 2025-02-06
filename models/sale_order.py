from odoo.tools.safe_eval import safe_eval, time

import base64
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _process_attachments_for_template_post(self, mail_template):
        _logger.info('_process_attachments_for_template_post')
        result = super()._process_attachments_for_template_post(mail_template)
     
        for order in self:
            order_result = result.setdefault(order.id, {})
            docs = order.order_line.product_id.product_document_ids.filtered(lambda s: s.mail_attach_on_so == True)
            _logger.info("docs are %s", len(docs))
            order_result.setdefault('attachment_ids', [])
            attachments = order_result.setdefault('attachments', [])
            for doc in docs:
                 attachments.extend([( doc.ir_attachment_id.name,  doc.ir_attachment_id.datas)])

        return result