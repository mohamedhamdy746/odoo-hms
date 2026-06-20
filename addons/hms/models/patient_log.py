from odoo import fields, models


class HmsPatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient Log History'
    _order = 'date desc'

    patient_id = fields.Many2one(
        comodel_name='hms.patient',
        string='Patient',
        ondelete='cascade',
        required=True,
    )
    created_by = fields.Many2one(
        comodel_name='res.users',
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True,
    )
    date = fields.Datetime(
        string='Date',
        default=fields.Datetime.now,
        readonly=True,
    )
    description = fields.Text(string='Description', required=True)
