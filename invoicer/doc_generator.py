import codecs
from datetime import date

from markdown_it import MarkdownIt
from markdown_pdf import MarkdownPdf, Section

STYLE_FILE = 'style.css'


def generate_pdf(markdown, prefix=date.today().strftime("%Y%m")):
    """Takes Markdown text and converts it to a PDF document.
    """
    pdf = MarkdownPdf()
    pdf.add_section(
        Section(markdown),
        user_css=open(STYLE_FILE).read()
    )
    pdf.save(prefix + "_invoice.pdf")


def generate_html(markdown, prefix=date.today().strftime("%Y%m")):
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

    output += open(STYLE_FILE).read()

    output += """
        </style>
    </head>

    <body>
    """
    output += body

    output += """</body>

    </html>
    """

    output_file = codecs.open(prefix + "_invoice.html", "w", "utf-8")
    output_file.write(output)
    output_file.close()
