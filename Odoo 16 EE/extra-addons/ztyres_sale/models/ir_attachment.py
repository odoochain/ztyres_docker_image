from odoo import models, fields, api, _

class PaymentReceiptAttachment(models.Model):
    _inherit = 'ir.attachment'

    doc_attach_rel = fields.Many2many('hr.employee.', 'doc_attachment_id', 'attach_id3', 'doc_id',
                                      string="Attachment", invisible=1)