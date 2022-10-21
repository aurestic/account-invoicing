# Copyright 2022 Aures TIC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def cron_generate_biweekly_invoices(self):
        """Cron called daily to check if biweekly invoicing needs to be done."""
        from pudb.remote import set_trace

        set_trace(term_size=(190, 50))
        companies = self._company_biweekly_invoicing_today()
        if companies:
            self.generate_biweekly_invoices(companies)

    @api.model
    def generate_biweekly_invoices(self, companies=None):
        """Generate biweekly invoices for customers who require that mode.

        Invoices will be generated by other jobs split for different customer
        and different payment term.
        """
        if not companies:
            companies = self.company_id
        saleorder_groups = self.read_group(
            [
                ("invoicing_mode", "=", "biweekly"),
                ("invoice_status", "=", "to invoice"),
                ("company_id", "in", companies.ids),
            ],
            ["partner_invoice_id"],
            groupby=self._get_groupby_fields_for_biweekly_invoicing(),
            lazy=False,
        )
        for saleorder_group in saleorder_groups:
            saleorder_ids = self.search(saleorder_group["__domain"]).ids
            self.with_delay()._generate_invoices_by_partner(saleorder_ids)
        companies.write(
            {
                "invoicing_mode_biweekly_last_execution": fields.Datetime.now(),
            }
        )
        return saleorder_groups

    @api.model
    def _get_groupby_fields_for_biweekly_invoicing(self):
        """Returns the sale order fields used to group them into jobs."""
        return ["partner_invoice_id", "payment_term_id"]

    def _generate_invoices_by_partner(self, saleorder_ids, invoicing_mode="biweekly"):
        """Generate invoices for a group of sale order belonging to a customer."""
        sales = (
            self.browse(saleorder_ids)
            .exists()
            .filtered(lambda r: r.invoice_status == "to invoice")
        )
        if not sales:
            return "No sale order found to invoice ?"
        invoices = sales._create_invoices(
            grouped=sales[:1].partner_invoice_id.one_invoice_per_order, final=True
        )
        for invoice in invoices:
            invoice.with_delay()._validate_invoice()
        return invoices

    @api.model
    def _company_biweekly_invoicing_today(self):
        """Get company ids for which today is biweekly invoicing day."""
        companies = self.env["res.company"]
        now = fields.Datetime.now()
        last_day_of_this_month = fields.Datetime.add(now, day=31).day
        if now.day in (last_day_of_this_month, 15):
            companies = companies.search(
                [
                    "|",
                    ("invoicing_mode_biweekly_last_execution", "<", now),
                    ("invoicing_mode_biweekly_last_execution", "=", False),
                ]
            )
        return companies
