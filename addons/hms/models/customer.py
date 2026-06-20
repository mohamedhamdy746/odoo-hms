from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one(
        comodel_name='hms.patient',
        string='Related Patient',
    )

    @api.constrains('related_patient_id')
    def _check_related_patient_email(self):
        for partner in self:
            if partner.related_patient_id and partner.related_patient_id.email:
                domain = [
                    ('email', '=', partner.related_patient_id.email),
                    ('id', '!=', partner.id),
                ]
                other_partner = self.search(domain, limit=1)
                if other_partner:
                    raise ValidationError(
                        f"Cannot link customer to patient '{partner.related_patient_id.first_name}'. "
                        f"The patient's email '{partner.related_patient_id.email}' is already "
                        f"assigned to another customer '{other_partner.name}'."
                    )

    def unlink(self):
        for record in self:
            if record.related_patient_id:
                raise ValidationError(
                    "You cannot delete a customer that is linked to a patient."
                )
        return super().unlink()
