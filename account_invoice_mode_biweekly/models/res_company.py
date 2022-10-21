# Copyright 2022 Aures TIC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    invoicing_mode_biweekly_last_execution = fields.Datetime(
        string="Last execution",
        help="Last execution of weekly invoicing.",
        readonly=True,
    )
