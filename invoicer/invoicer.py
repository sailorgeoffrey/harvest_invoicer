import argparse
import calendar
import locale
import os
import sys
from datetime import timedelta, date

from jinja2 import Template

from .config import Config
from .doc_generator import generate_pdf
from .harvest_client import HarvestClient
from .models import Invoice, LineItem, DateRange

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILE = os.path.join(PACKAGE_DIR, 'template.md')
CONFIG_FILE = '.invoicer_config.ini'


def get_date_range(month_str=None):
    """
    Parse date range from month string (YYYYMM) or use last month if not provided
    """
    if not month_str or len(month_str) != 6 or not month_str.isdigit():
        start = date.today().replace(day=1, month=date.today().month - 1)
    else:
        start = date(int(month_str[:4]), int(month_str[-2:]), 1)
    end = date(start.year, start.month, calendar.monthrange(start.year, start.month)[1])
    return DateRange(start, end)


def render_template(invoice):
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as template_file:
        template = Template(template_file.read(), trim_blocks=True)
    return template.render(invoice=invoice, items=invoice.line_items)


class Invoicer:
    def __init__(self, _date_range, _config, _client):
        self.config = _config
        self.start_date = _date_range.start
        self.end_date = _date_range.end
        self.client = _client

    def run(self, document_generator):
        harvest_report = self.client.fetch_report(self.start_date, self.end_date)
        invoicer_model = self.generate_model(harvest_report)
        rendered_template = render_template(invoicer_model)
        file_prefix = self.start_date.strftime("%Y%m") + "_invoice"
        output_file = document_generator(rendered_template, file_prefix)
        return output_file

    def generate_model(self, harvest_report):
        invoice_total = 0
        line_items = []
        # Loop through each client for the month and create line items and a running total for the invoice.
        for client in harvest_report:
            client_name = client['client_name']
            line_total = self.config.rate * int(client['total_hours'])
            line_items.append(LineItem(
                client=client_name,
                hours=client['total_hours'],
                description=self.config.get_description(client_name),
                total=locale.currency(line_total)
            ))
            invoice_total = invoice_total + line_total
        # Create the invoice headers and common elements.
        due_fn = lambda end_date: end_date + timedelta(days=45)
        return Invoice(
            date=(self.end_date + timedelta(days=1)).strftime("%d %b %Y"),
            start_date=self.start_date.strftime("%d %b %Y"),
            end_date=self.end_date.strftime("%d %b %Y"),
            rate=locale.currency(self.config.rate),
            terms="Net 45",
            due=due_fn(self.end_date).strftime("%d %b %Y"),
            total=locale.currency(invoice_total),
            line_items=line_items
        )


def main():
    parser = argparse.ArgumentParser(
        description='Generate invoices from Harvest time tracking data'
    )
    parser.add_argument(
        'month',
        nargs='?',
        help='Month to generate invoice for (format: YYYYMM, e.g., 202504). Defaults to previous month'
    )
    parser.add_argument(
        '--config',
        default=CONFIG_FILE,
        help=f'Path to config file (default: {CONFIG_FILE})'
    )
    parser.add_argument(
        '--preview',
        action='store_true',
        help='Generate markdown preview instead of PDF'
    )

    args = parser.parse_args()

    try:
        config = Config(args.config)
        date_range = get_date_range(args.month)

        invoicer = Invoicer(
            date_range,
            config,
            HarvestClient(config.account_id, config.api_key)
        )

        generator = lambda content, filename: print(content) if args.preview else generate_pdf(content, filename)
        output_file = invoicer.run(generator)

        if not args.preview:
            print(f"Invoice generated successfully: {output_file}")

    except FileNotFoundError as e:
        print(f"Error: Could not find file - {e.filename}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
