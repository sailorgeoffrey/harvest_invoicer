import calendar
import configparser
import json
import locale
import sys
from datetime import timedelta, datetime

import keyring
import os
import requests

from jinja2 import Template
from markdown_it import MarkdownIt
from markdown_pdf import MarkdownPdf, Section

DEFAULT_SERVICE_DESCRIPTION = "Development and consulting services."

CONFIG_FILE = '.invoicer_config.ini'

config = configparser.ConfigParser()
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def convert_md_to_html(markdown):
    """Takes Markdown text and converts it to an HTML document.
    Use this to preview the rendered Markdown and adjust CSS.
    There is code commented at the bottom to use this instead of PDF.
    """
    body = (
        MarkdownIt('commonmark', {'breaks': True, 'html': True})
        .enable('table')
    ).render(markdown)
    output = """<!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="utf-8">
        <style type="text/css">
    """

    output += open("style.css").read()

    output += """
        </style>
    </head>

    <body>
    """
    output += body

    output += """</body>

    </html>
    """
    return output


def convert_markdown_to_pdf(markdown):
    """Takes Markdown text and converts it to a PDF document.
    """
    pdf = MarkdownPdf()
    pdf.add_section(
        Section(markdown),
        user_css=open("style.css").read()
    )
    return pdf


# The main method optionally takes an argument for the month to invoice.
if __name__ == '__main__':

    input_month = sys.argv[-1]
    if len(input_month) != 6 or not input_month.isdigit():
        input_month = input("Enter invoice month (YYYYMM): ")

    if os.path.isfile(".invoicer_config.ini"):
        config.read(CONFIG_FILE)
    else:
        account_id = input("Please enter your Harvest account ID.\n")
        config['Harvest'] = {'account_id': account_id}
        rate_str = input("Please enter your hourly rate.\n")
        config['Billing'] = {'rate': rate_str}
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)

    key = keyring.get_password("invoicer", "harvest_key")
    if key is None:
        key = input("Please enter your Harvest API key.\n")
        keyring.set_password("invoicer", "harvest_key", key)

    year = int(input_month[:4])
    month = int(input_month[-2:])
    start = datetime(year, month, 1)
    end_exclusive = (start + timedelta(days=32)).replace(day=1)
    end_inclusive = datetime(year, month, calendar.monthrange(year, month)[1])
    rate: int = int(config.get('Billing', 'rate'))
    resp = requests.get(
        url="https://api.harvestapp.com/v2/reports/time/clients",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Harvest-Account-Id": config.get('Harvest', 'account_id'),
            "User-Agent": "Invoicer (geoffc@gmail.com)",
            "Authorization": "Bearer " + key,
        },
        params={
            "from": start.strftime("%Y%m%d"),
            "to": end_exclusive.strftime("%Y%m%d"),
        }
    )
    if resp.status_code != 200:
        print(resp.text)
        exit(1)

    # Loop through each client for the month and create line items and a running total for the invoice.
    invoice_total = 0
    items = []
    for client in json.loads(resp.text)["results"]:
        client_key = client['client_name'].replace(" ", "_").lower()
        try:
            description = config.get("Descriptions", client_key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            description = (input(
                f"Please enter a description for your work at {client['client_name']}. Press enter for \"{DEFAULT_SERVICE_DESCRIPTION}\": ").strip()
                           or DEFAULT_SERVICE_DESCRIPTION)
            if input(
                    f"Would you like to save this description and not ask for {client['client_name']} in the future? (y/n) ") == "y":
                config['Descriptions'] = {client_key: description}
                with open(CONFIG_FILE, 'w') as configfile:
                    config.write(configfile)
        line_total = rate * int(client['total_hours'])
        items.append({
            "client": client['client_name'],
            "hours": client['total_hours'],
            "description": description,
            "total": locale.currency(line_total),
        })
        invoice_total = invoice_total + line_total

    # Create the invoice headers and common elements.
    due_fn = lambda date: date + +timedelta(days=45)
    invoice = {
        "date": (end_inclusive + timedelta(days=1)).strftime("%d %b %Y"),
        "start_date": start.strftime("%d %b %Y"),
        "end_date": end_inclusive.strftime("%d %b %Y"),
        "rate": locale.currency(rate),
        "terms": "Net 45",
        "due": due_fn(end_inclusive).strftime("%d %b %Y"),
        "total": locale.currency(invoice_total)
    }

    # render the template
    with open('template.md', 'r') as template_file:
        template = Template(template_file.read(), trim_blocks=True)
    md = template.render(invoice=invoice, items=items)

    convert_markdown_to_pdf(md).save(input_month + "_invoice.pdf")

    # output_file = codecs.open(input_month + "_invoice.html", "w", "utf-8")
    # output_file.write(convert_md_to_html(md))
    # output_file.close()
