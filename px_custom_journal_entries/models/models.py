from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    payment_type = fields.Selection([
        ('cash', 'Cash'),
        ('wallet', 'Wallet'),
        ('on line', 'On Line')
    ], string="Payment Type")
    exclude_bank_lines = fields.Boolean(
        string="Exclude Bank Lines from Reports",
        help="Exclude bank journal lines from being considered in tax reports or financial closing."
    )
