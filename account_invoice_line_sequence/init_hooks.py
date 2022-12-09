# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    """
    Fetches all invoice and resets the sequence of their invoice line
    """
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        invoice = env["account.move"].search([])
        invoice.read(["sequence"])
        invoice._reset_sequence()
