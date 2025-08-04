from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    account_tax_periodicity = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
    ], string="Tax Periodicity")
    account_tax_periodicity_reminder_day = fields.Integer(string="Tax Reminder Day")
    account_tax_periodicity_journal_id = fields.Many2one(
        'account.journal',
        string="Tax Journal"
    )
    totals_below_sections = fields.Boolean(string="Totals Below Sections")