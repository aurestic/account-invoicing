# Copyright 2022 Aures TIC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from freezegun import freeze_time

from odoo.tests.common import SavepointCase


class TestInvoiceModeBiweekly(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.SaleOrder = cls.env["sale.order"]

    def test_late_invoicing_for_last_month(self):
        """Check that last month invoicing will be done if missed."""
        company = self.env.company
        company.invoicing_mode_biweekly_last_execution = "2022-05-31"
        self.assertTrue(self.env.company)
        with freeze_time("2022-06-03"):
            res = self.SaleOrder._company_biweekly_invoicing_today()
            self.assertFalse(res)
        with freeze_time("2022-06-15"):
            res = self.SaleOrder._company_biweekly_invoicing_today()
            self.assertTrue(res)

    def test_late_invoicing_for_last_biweekly(self):
        company = self.env.company
        company.invoicing_mode_biweekly_last_execution = "2022-05-15"
        self.assertTrue(self.env.company)
        with freeze_time("2022-05-20"):
            res = self.SaleOrder._company_biweekly_invoicing_today()
            self.assertFalse(res)
        with freeze_time("2022-05-31"):
            res = self.SaleOrder._company_biweekly_invoicing_today()
            self.assertTrue(res)

    def test_no_invoicing_done_yet(self):
        company = self.env.company
        company.invoicing_mode_biweekly_last_execution = None
        self.assertTrue(self.env.company)
        with freeze_time("2022-06-11"):
            res = self.SaleOrder._company_biweekly_invoicing_today()
            self.assertFalse(res)
        with freeze_time("2022-06-30"):
            res = self.SaleOrder._company_biweekly_invoicing_today()
            self.assertTrue(res)
