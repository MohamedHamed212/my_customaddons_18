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
        string="Tax Journal", config_parameter="account_reports.tax_journal_id", required=False
    )

    totals_below_sections = fields.Boolean(
        string="Totals Below Sections", config_parameter='account_reports.totals_below_sections'
    )

    account_reports_show_per_company_setting = fields.Boolean(
        string="Show per company setting", config_parameter='account_reports.show_per_company_setting'
    )

class AccountMove(models.Model):
    _inherit = 'account.move'

    tax_closing_report_id = fields.Many2one(
        'account.report',
        string="Tax Closing Report"
    )
    tax_closing_alert = fields.Boolean(string="Tax Closing Alert")


class ResCompany(models.Model):
    _inherit = 'res.company'

    account_display_representative_field = fields.Boolean(
        string="Display Account Representative",
        default=False
    )

