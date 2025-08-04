from odoo import http
from odoo.http import request
from odoo.addons.hr_attendance.controllers.main import HrAttendance
from odoo.exceptions import UserError
import math

class HrAttendanceGeofence(HrAttendance):
    
    @http.route('/hr_attendance/manual_selection', type="json", auth="public")
    def manual_selection_with_geolocation(self, token, employee_id, pin_code, latitude=False, longitude=False):
        def haversine(lat1, lon1, lat2, lon2):
            R = 6371000
            phi1 = math.radians(lat1)
            phi2 = math.radians(lat2)
            delta_phi = math.radians(lat2 - lat1)
            delta_lambda = math.radians(lon2 - lon1)
            a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            return R * c

        company = self._get_company(token)
        if company:
            employee = request.env['hr.employee'].sudo().browse(employee_id)
            if employee.company_id == company and ((not company.attendance_kiosk_use_pin) or (employee.pin == pin_code)):
                work_location = employee.work_location_id
                if work_location and work_location.latitude and work_location.longitude and work_location.range:
                    user_lat = float(latitude)
                    user_lon = float(longitude)
                    wl_lat = float(work_location.latitude)
                    wl_lon = float(work_location.longitude)
                    wl_range = float(work_location.range)
                    distance = haversine(user_lat, user_lon, wl_lat, wl_lon)
                    if distance > wl_range:
                        raise UserError('You must be within the accepted range to check in/out.')
                employee.sudo()._attendance_action_change(self._get_geoip_response('kiosk', latitude=latitude, longitude=longitude))
                return self._get_employee_info_response(employee)
        return {}
