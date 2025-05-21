import codecs
import os

from markdown_it import MarkdownIt
from markdown_pdf import MarkdownPdf, Section

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
STYLE_FILE = os.path.join(PACKAGE_DIR, 'style.css')


def generate_pdf(markdown, file_prefix):
    """Takes Markdown text and converts it to a PDF document.
    """
    pdf = MarkdownPdf()
    pdf.add_section(
        Section(markdown),
        user_css=open(STYLE_FILE).read()
    )
    output_filename = file_prefix + ".pdf"
    pdf.save(output_filename)
    return output_filename


def generate_html(markdown, file_prefix):
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
    output_filename = file_prefix + ".html"
    output_file = codecs.open(output_filename, "w", "utf-8")
    output_file.write(output)
    output_file.close()
