from odoo import api, fields, models


class HmsDoctor(models.Model):
    _name = 'hms.doctors'
    _description = 'Hospital Doctor'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    image = fields.Image(string='Image')
    name = fields.Char(string='Name', compute='_compute_name', store=True)

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for doctor in self:
            doctor.name = f"{doctor.first_name or ''} {doctor.last_name or ''}".strip()
