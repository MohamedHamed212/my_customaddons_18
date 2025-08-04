from odoo import fields, models, api

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
        string="Tax Journal", config_parameter="account_reports.tax_journal_id", required=0
    )

    totals_below_sections = fields.Boolean(
        string="Totals Below Sections", config_parameter='account_reports.totals_below_sections'
    )

    account_reports_show_per_company_setting = fields.Boolean(
        string="Show per company setting", config_parameter='account_reports.show_per_company_setting'
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        journal_id = self.env['ir.config_parameter'].sudo().get_param('account_reports.tax_journal_id')
        res.update(
            account_tax_periodicity_journal_id=int(journal_id) if journal_id else False
        )
        return res

    def set_values(self):
        super().set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'account_reports.tax_journal_id',
            self.account_tax_periodicity_journal_id.id or ''
        )

class AccountMove(models.Model):
    _inherit = 'account.move'

    tax_closing_report_id = fields.Many2one(
        'account.report',
        string="Tax Closing Report"
    )
    tax_closing_alert = fields.Boolean(string="Tax Closing Alert")

