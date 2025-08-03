# from odoo import models, api
#
# class HrEmployee(models.Model):
#     _inherit = 'hr.employee'
#
#     @api.model
#     def init(self):
#         print("__________________________________________________")
#         self.env.cr.execute("""
#             ALTER TABLE hr_employee DROP CONSTRAINT IF EXISTS hr_employee_user_uniq;
#         """)
