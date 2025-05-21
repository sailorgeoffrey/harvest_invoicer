import calendar
import unittest
from datetime import date

from invoicer.invoicer import get_date_range, render_template
from invoicer.models import Invoice, LineItem


class TestInvoicer(unittest.TestCase):

    def test_get_date_range_with_arg(self):
        args = ["script", "202504"]
        dates = get_date_range(args)
        self.assertEqual(
            dates.start,
            date(2025, 4, 1),
        )
        self.assertEqual(
            dates.end,
            date(2025, 4, 30),
        )

    def test_get_date_range_without_arg(self):
        args = ["script"]
        dates = get_date_range(args)
        self.assertEqual(
            dates.start,
            date.today().replace(day=1, month=date.today().month - 1),
        )
        self.assertEqual(
            dates.end,
            date(dates.start.year, dates.start.month, calendar.monthrange(dates.start.year, dates.start.month)[1]),
        )

    def test_render_template(self):
        md = render_template(Invoice(
            date="1st May 2025",
            start_date="1st April 2025",
            end_date="30th April 2025",
            rate="$100",
            terms="Net 45",
            due="45th April 2025",
            total="$1,000",
            line_items=[
                LineItem(client="Client A", hours=10, description="Work", total="$1,000"),
            ]
        ))
        self.assertTrue(md.__contains__("Client A"))
