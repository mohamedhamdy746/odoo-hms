from odoo import fields, models


class HmsDepartment(models.Model):
    _name = 'hms.department'
    _description = 'Hospital Department'

    name = fields.Char(string='Name', required=True)
    capacity = fields.Integer(string='Capacity')
    is_opened = fields.Boolean(string='Is Opened', default=True)
    patient_ids = fields.One2many(
        comodel_name='hms.patient',
        inverse_name='department_id',
        string='Patients',
    )
