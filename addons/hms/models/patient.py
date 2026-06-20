from datetime import date

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Patient'
    _rec_name = 'first_name'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    birth_date = fields.Date(string='Birth Date')
    history = fields.Html(string='History')
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection(
        selection=[
            ('a+', 'A+'),
            ('a-', 'A-'),
            ('b+', 'B+'),
            ('b-', 'B-'),
            ('ab+', 'AB+'),
            ('ab-', 'AB-'),
            ('o+', 'O+'),
            ('o-', 'O-'),
        ],
        string='Blood Type',
    )
    pcr = fields.Boolean(string='PCR')
    image = fields.Image(string='Image')
    address = fields.Text(string='Address')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    email = fields.Char(string='Email')

    # Relational fields for Lab 2
    department_id = fields.Many2one(
        comodel_name='hms.department',
        string='Department',
    )
    doctor_ids = fields.Many2many(
        comodel_name='hms.doctors',
        string='Doctors',
    )
    department_capacity = fields.Integer(
        related='department_id.capacity',
        string='Department Capacity',
        readonly=True,
    )
    log_ids = fields.One2many(
        comodel_name='hms.patient.log',
        inverse_name='patient_id',
        string='History Logs',
    )
    state = fields.Selection(
        selection=[
            ('undetermined', 'Undetermined'),
            ('good', 'Good'),
            ('fair', 'Fair'),
            ('serious', 'Serious'),
        ],
        string='State',
        default='undetermined',
    )

    _sql_constraints = [
        ('unique_patient_email', 'UNIQUE(email)', 'The patient email must be unique!')
    ]


    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for patient in self:
            if patient.birth_date:
                patient.age = (
                    today.year
                    - patient.birth_date.year
                    - (
                        (today.month, today.day)
                        < (patient.birth_date.month, patient.birth_date.day)
                    )
                )
            else:
                patient.age = 0

    @api.constrains('department_id')
    def _check_department_is_opened(self):
        for record in self:
            if record.department_id and not record.department_id.is_opened:
                raise ValidationError("You cannot choose a closed department.")

    @api.constrains('email')
    def _check_valid_email(self):
        import re
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        for record in self:
            if record.email and not re.match(email_regex, record.email):
                raise ValidationError("Please enter a valid email address.")


    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'PCR Automatically Checked',
                    'message': 'PCR field has been automatically checked because the patient age is lower than 30.',
                }
            }

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            state_label = dict(self._fields['state'].selection).get(
                record.state, record.state
            )
            self.env['hms.patient.log'].create({
                'patient_id': record.id,
                'description': f"Patient created with state: {state_label}",
            })
        return records

    def write(self, vals):
        if 'state' in vals:
            for record in self:
                old_state = record.state
                new_state = vals['state']
                if old_state != new_state:
                    state_label = dict(self._fields['state'].selection).get(
                        new_state, new_state
                    )
                    self.env['hms.patient.log'].create({
                        'patient_id': record.id,
                        'description': f"State changed to {state_label}",
                    })
        return super().write(vals)
