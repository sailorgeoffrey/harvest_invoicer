import calendar
import csv
import locale
from datetime import timedelta, datetime

from jinja2 import Template
from markdown_it import MarkdownIt
from markdown_pdf import MarkdownPdf, Section

import config

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def generate_markdown(start_date, end_date, invoice_rows, total):
    formatted_invoice = {
        "date": (end_date + timedelta(days=1)).strftime("%d %b %Y"),
        "start_date": start_date.strftime("%d %b %Y"),
        "end_date": end_date.strftime("%d %b %Y"),
        "rate": locale.currency(config.rate),
        "terms": config.terms,
        "due": config.due_fn(end_date).strftime("%d %b %Y"),
        "total": locale.currency(total)
    }

    # render the template
    with open('template.md', 'r') as template_file:
        template = Template(template_file.read(), trim_blocks=True)
    return template.render(invoice=formatted_invoice, items=invoice_rows)


def convert_md_to_html(markdown):
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
    pdf = MarkdownPdf()
    pdf.add_section(
        Section(markdown),
        user_css=open("style.css").read()
    )
    return pdf


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    invoices = {}
    totals = {}
    with open("input.csv", 'r') as file:
        csvreader = csv.reader(file, delimiter=';')
        header = next(csvreader)
        for row in csvreader:
            key = row[0] + row[1]
            line_total = config.rate * int(row[3])
            item = {
                "client": row[2] or config.defaults.get("client"),
                "hours": int(row[3]),
                "description": row[4] or config.defaults.get("description"),
                "total": locale.currency(line_total),
            }
            if key not in invoices:
                invoices[key] = [item]
                totals[key] = line_total
            else:
                invoices[key].append(item)
                totals[key] += line_total

    for key in invoices.keys():
        invoice = invoices[key]
        year = int(key[:4])
        month = int(key[-2:])
        start = datetime(year, month, 1)
        end = datetime(year, month, calendar.monthrange(year, month)[1])
        md = generate_markdown(start, end, invoice, totals[key])

        convert_markdown_to_pdf(md).save(end.strftime("%Y%m") + "_invoice.pdf")

        # output_file = codecs.open(end.strftime("%Y%m") + "_invoice.html", "w", "utf-8")
        # output_file.write(convert_md_to_html(md))
        # output_file.close()
