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
        # for move in self.filtered('edi_document_ids'):
        #     move_result = result.setdefault(move.id, {})
        #     for edi_doc in move.edi_document_ids:
        #         edi_attachments = edi_doc._filter_edi_attachments_for_mailing()
        #         move_result.setdefault('attachment_ids', []).extend(edi_attachments.get('attachment_ids', []))
        #         move_result.setdefault('attachments', []).extend(edi_attachments.get('attachments', []))


    #         if tmpl.is_so and so_tag:
    #             sos = self.env[tmpl.model].search([('id', '=', active_id)])
    #             for so in sos:
    #                 for line in so.order_line:
    #                     product = line.product_id
    #                     for attach in product.product_tmpl_id.tmpl_attachment_so_ids:
    #                         tmpl.attachment_ids = tmpl.attachment_ids | attach.copy()                         
    #                     for attach in product.product_attachment_so_ids:
    #                         tmpl.attachment_ids = tmpl.attachment_ids | attach.copy()
    #         
        for order in self:
            order_result = result.setdefault(order.id, {})
            docs = order.order_line.product_id.product_document_ids.filtered(lambda s: s.mail_attach_on_so == True)
            _logger.info("docs are %s", len(docs))
            order_result.setdefault('attachment_ids', [])
            attachments = order_result.setdefault('attachments', [])
            for doc in docs:
                 attachments.extend([( doc.ir_attachment_id.name,  doc.ir_attachment_id.datas)])

            # order_result['attachments'] = attachments
            # return {'attachments': [( dosc.ir_attachment_id.name,  docs.ir_attachment_id.datas)]}
            # for doc in docs:          
            #     order_result.append({ doc.ir_attachment_id.name : doc.ir_attachment_id.datas })        


        return result