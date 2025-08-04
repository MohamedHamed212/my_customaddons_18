from odoo import fields, models

class WorkLocation(models.Model):
    _inherit = 'hr.work.location'

    longitude = fields.Float(string="Longitude")
    latitude = fields.Float(string="Latitude")
    range = fields.Float(string="Range (meters)")
