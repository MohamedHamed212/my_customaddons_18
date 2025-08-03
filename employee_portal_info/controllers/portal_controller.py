from odoo import http, fields
from odoo.http import request, route
from odoo.exceptions import AccessError, ValidationError
from odoo.addons.portal.controllers.portal import CustomerPortal


class EmployeePortal(CustomerPortal):

    def _get_employee(self):
        return request.env['hr.employee'].sudo().search([
            ('user_id', '=', request.env.user.id)
        ], limit=1)

    @http.route(['/my/employee'], type='http', auth='user', website=True)
    def portal_employee(self, **kwargs):
        employee = self._get_employee()
        contract = request.env['hr.contract'].sudo().search([
            ('employee_id', '=', employee.id),
            ('state', '=', 'open')
        ], limit=1) if employee else None

        if employee and contract and not employee.contract_id:
            employee.contract_id = contract

        payslips = request.env['hr.payslip'].sudo().search([
            ('employee_id', '=', employee.id)
        ], order="date_to desc") if employee else []

        return request.render("employee_portal_info.portal_employee_template", {
            'employee': employee,
            'payslips': payslips,
        })

    @http.route(['/my/employee/payslip/<int:payslip_id>'], type='http', auth='user', website=True)
    def portal_payslip_detail(self, payslip_id, **kwargs):
        employee = self._get_employee()
        payslip = request.env['hr.payslip'].sudo().search([
            ('id', '=', payslip_id),
            ('employee_id', '=', employee.id)
        ], limit=1)

        if not payslip:
            return request.render("website.404")

        return request.render("employee_portal_info.portal_payslip_detail", {
            'employee': employee,
            'payslip': payslip,
            'payslip_lines': payslip.line_ids,
        })

    @http.route(['/my/resignations'], type='http', auth='user', website=True)
    def portal_resignations(self, **kwargs):
        employee = self._get_employee()
        old_contracts = request.env['hr.contract'].sudo().search([
            ('employee_id', '=', employee.id),
            ('state', '!=', 'open')
        ]) if employee else []

        return request.render("employee_portal_info.portal_resignation_template", {
            'employee': employee,
            'old_contracts': old_contracts,
        })

    @http.route(['/my/resignations/<int:contract_id>'], type='http', auth='user', website=True)
    def portal_resignation_detail(self, contract_id, **kwargs):
        employee = self._get_employee()
        contract = request.env['hr.contract'].sudo().search([
            ('id', '=', contract_id),
            ('employee_id', '=', employee.id),
            ('state', '!=', 'open')
        ], limit=1)

        if not contract:
            return request.render("website.404")

        return request.render("employee_portal_info.portal_resignation_detail", {
            'contract': contract,
            'employee': employee,
        })

    @http.route(['/my/deductions'], type='http', auth='user', website=True)
    def portal_deductions(self, **kwargs):
        employee = self._get_employee()
        latest_payslip = request.env['hr.payslip'].sudo().search([
            ('employee_id', '=', employee.id),
            ('state', '=', 'done'),
        ], order="date_to desc", limit=1)

        deduction_lines = latest_payslip.line_ids.filtered(
            lambda line: line.category_id.code == 'DED'
        ) if latest_payslip else []

        return request.render("employee_portal_info.portal_deductions_template", {
            'deductions': deduction_lines,
        })

    @http.route(['/my/attendance'], type='http', auth='user', website=True)
    def portal_attendance(self, **kwargs):
        employee = self._get_employee()
        attendances = request.env['hr.attendance'].sudo().search([
            ('employee_id', '=', employee.id)
        ], order='check_in desc', limit=30) if employee else []

        return request.render("employee_portal_info.portal_attendance_template", {
            'employee': employee,
            'attendances': attendances,
        })

    @http.route(['/my/attendance/<int:attendance_id>'], type='http', auth='user', website=True)
    def portal_attendance_detail(self, attendance_id, **kwargs):
        employee = self._get_employee()
        attendance = request.env['hr.attendance'].sudo().browse(attendance_id)

        if not attendance.exists() or attendance.employee_id.id != employee.id:
            return request.redirect('/my/attendance')

        return request.render("employee_portal_info.portal_attendance_detail", {
            'attendance': attendance,
            'employee': employee,
        })

    @http.route(['/my/attendance/checkin'], type='http', auth='user', methods=['POST'], website=True, csrf=False)
    def portal_check_in(self, **kwargs):
        employee = self._get_employee()

        if not employee:
            request.session['portal_alert'] = {'message': 'Employee not found.', 'type': 'danger'}
            return request.redirect('/my/attendance')

        open_attendance = request.env['hr.attendance'].sudo().search([
            ('employee_id', '=', employee.id),
            ('check_out', '=', False)
        ], limit=1)

        if open_attendance:
            request.session['portal_alert'] = {
                'message': f'You are already checked in since {open_attendance.check_in}.',
                'type': 'warning'
            }
            return request.redirect('/my/attendance')

        request.env['hr.attendance'].sudo().create({
            'employee_id': employee.id,
            'check_in': fields.Datetime.now(),
        })

        request.session['portal_alert'] = {'message': 'Checked in successfully.', 'type': 'success'}
        return request.redirect('/my/attendance')

    @http.route(['/my/attendance/checkout'], type='http', auth='user', methods=['POST'], website=True, csrf=False)
    def portal_check_out(self, **kwargs):
        employee = self._get_employee()

        if not employee:
            request.session['portal_alert'] = {'message': 'Employee not found.', 'type': 'danger'}
            return request.redirect('/my/attendance')

        open_attendance = request.env['hr.attendance'].sudo().search([
            ('employee_id', '=', employee.id),
            ('check_out', '=', False)
        ], order="check_in desc", limit=1)

        if not open_attendance:
            request.session['portal_alert'] = {'message': 'No active Check In found to Check Out.', 'type': 'warning'}
            return request.redirect('/my/attendance')

        open_attendance.write({'check_out': fields.Datetime.now()})

        request.session['portal_alert'] = {'message': 'Checked out successfully.', 'type': 'success'}
        return request.redirect('/my/attendance')

    @http.route(['/my/leaves'], type='http', auth='user', website=True)
    def portal_leaves(self, **kwargs):
        employee = self._get_employee()
        leaves = request.env['hr.leave'].sudo().search([
            ('employee_id', '=', employee.id),
            ('state', 'in', ['confirm', 'validate1', 'validate', 'refuse', 'cancel'])
        ]) if employee else []

        return request.render("employee_portal_info.portal_leave_template", {
            'employee': employee,
            'leaves': leaves,
        })

    @http.route(['/my/leaves/<int:leave_id>'], type='http', auth='user', website=True)
    def portal_leave_detail(self, leave_id, **kwargs):
        leave = request.env['hr.leave'].sudo().browse(leave_id)

        if not leave.exists() or leave.employee_id.user_id.id != request.env.user.id:
            raise AccessError("You cannot access this leave request.")

        return request.render("employee_portal_info.portal_leave_detail_template", {
            'leave': leave,
        })

    @http.route(['/my/leaves/request'], type='http', auth='user', website=True)
    def portal_leave_request_form(self, **kwargs):
        domain = [
            '|',
            ('requires_allocation', '=', 'no'),
            '&',
            ('requires_allocation', '=', 'yes'),
            ('virtual_remaining_leaves', '>', 0),
        ]

        leave_types = request.env['hr.leave.type'].sudo().search(domain)
        return request.render("employee_portal_info.portal_leave_request_form", {
            'leave_types': leave_types
        })


    @http.route(['/my/leaves/request/submit'], type='http', auth='user', methods=['POST'], csrf=True, website=True)
    def portal_leave_submit(self, **post):
        employee = self._get_employee()
        if not employee:
            return request.redirect('/my/leaves')

        try:
            request.env['hr.leave'].sudo().create({
                'employee_id': employee.id,
                'holiday_status_id': int(post.get('leave_type_id')),
                'request_date_from': post.get('date_from'),
                'request_date_to': post.get('date_to'),
                'name': post.get('description', ''),
            })
        except Exception:
            request.session['leave_error'] = "There was an error submitting your leave request."
            return request.redirect('/my/leaves/request')

        return request.redirect('/my/leaves')
