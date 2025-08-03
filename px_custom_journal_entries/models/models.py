from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    payment_type = fields.Selection([
        ('cash', 'Cash'),
        ('wallet', 'Wallet'),
        ('on line', 'On Line')
    ], string="Payment Type")
