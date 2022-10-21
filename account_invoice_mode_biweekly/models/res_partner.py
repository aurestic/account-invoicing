# Copyright 2022 Aures TIC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    invoicing_mode = fields.Selection(
        selection_add=[("biweekly", "Biweekly")],
        ondelete={"biweekly": "set default"},
    )
