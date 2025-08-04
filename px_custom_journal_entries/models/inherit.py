from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    account_tax_periodicity = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
    ], string="Tax Periodicity", config_parameter="account_reports.tax_periodicity")

    account_tax_periodicity_reminder_day = fields.Integer(
        string="Tax Reminder Day", config_parameter="account_reports.tax_reminder_day"
    )

    account_tax_periodicity_journal_id = fields.Many2one(
        'account.journal',
        string="Tax Journal", config_parameter="account_reports.tax_journal_id"
    )

    totals_below_sections = fields.Boolean(
        string="Totals Below Sections", config_parameter='account_reports.totals_below_sections'
    )

    account_reports_show_per_company_setting = fields.Boolean(
        string="Show per company setting", config_parameter='account_reports.show_per_company_setting'
    )
