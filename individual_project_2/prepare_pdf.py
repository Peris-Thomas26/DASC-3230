#!/usr/bin/env python3
"""Prepare exported notebook HTML for printing as an A4 PDF.

Usage:
    python3 prepare_pdf.py individual_project_2.html
    python3 prepare_pdf.py individual_project_2.html --output executed.html

Open the resulting HTML in a browser and print/save as PDF: A4, 100% scale,
headers and footers off. Save the PDF as executed.pdf. This script only adds
print CSS; it does not run code, replace answers, or generate a PDF itself.
"""

import argparse
from html.parser import HTMLParser
from pathlib import Path


STYLE_ID = "individual-project-a4-print-style"
PRINT_CSS = """@page {
  size: A4 portrait;
  margin: 12mm;
}

@media print {
  html, body {
    width: auto !important;
    min-width: 0 !important;
    max-width: none !important;
    height: auto !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: visible !important;
  }

  main, #notebook, #notebook-container, .container, .jp-Notebook {
    width: auto !important;
    min-width: 0 !important;
    max-width: 100% !important;
    height: auto !important;
    max-height: none !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: visible !important;
    box-shadow: none !important;
  }

  /* JupyterLab and classic exports: release fixed-width and scrolling boxes. */
  .jp-Cell, .jp-Cell-inputWrapper, .jp-Cell-outputWrapper,
  .jp-InputArea, .jp-InputArea-editor, .jp-OutputArea,
  .jp-OutputArea-child, .jp-OutputArea-output,
  .jp-RenderedHTMLCommon, .jp-RenderedText,
  .cell, .inner_cell, .input, .input_area,
  .output_wrapper, .output, .output_area, .output_subarea,
  .text_cell_render, .rendered_html,
  .CodeMirror, .CodeMirror-scroll, .cm-editor, .cm-scroller,
  .cm-content, .highlight {
    box-sizing: border-box !important;
    width: auto !important;
    min-width: 0 !important;
    max-width: 100% !important;
    height: auto !important;
    max-height: none !important;
    overflow: visible !important;
  }

  /* Block flow permits wrapping and page breaks through long code cells. */
  .jp-Cell-inputWrapper, .jp-Cell-outputWrapper,
  .jp-InputArea, .jp-InputArea-editor,
  .jp-OutputArea-child, .jp-OutputArea-output,
  .cell, .input, .output_area, .output_subarea, .cm-editor {
    display: block !important;
  }

  .jp-InputPrompt, .jp-OutputPrompt, .prompt {
    display: block !important;
    width: auto !important;
    min-width: 0 !important;
    text-align: left !important;
    white-space: normal !important;
  }

  pre, code, .CodeMirror-line, .cm-line {
    white-space: pre-wrap !important;
    overflow-wrap: anywhere !important;
    word-break: normal !important;
    hyphens: none !important;
  }

  pre {
    width: auto !important;
    min-width: 0 !important;
    max-width: 100% !important;
    height: auto !important;
    max-height: none !important;
    overflow: visible !important;
    box-sizing: border-box !important;
  }

  .output_scroll, .jp-CodeCell.jp-mod-outputsScrolled .jp-Cell-outputArea {
    height: auto !important;
    max-height: none !important;
    overflow: visible !important;
    resize: none !important;
    box-shadow: none !important;
  }

  .jp-CodeCell.jp-mod-outputsScrolled .jp-Cell-outputArea::after {
    display: none !important;
    content: none !important;
  }

  .jp-Cell, .cell, .jp-InputArea, .jp-InputArea-editor,
  .jp-OutputArea, .jp-OutputArea-child, .jp-OutputArea-output,
  .input, .input_area, .output, .output_area, .output_subarea, pre {
    break-inside: auto !important;
    page-break-inside: auto !important;
  }

  img, .jp-RenderedSVG > svg, .output_svg > svg,
  .jp-OutputArea-output > svg, .output_subarea > svg {
    max-width: 100% !important;
    height: auto !important;
    break-inside: avoid !important;
    page-break-inside: avoid !important;
  }

  table {
    width: auto !important;
    max-width: 100% !important;
    table-layout: auto !important;
  }

  th, td {
    white-space: normal !important;
    overflow-wrap: anywhere !important;
    word-break: normal !important;
  }
}
"""


class StyleLocations(HTMLParser):
    """Locate our style and the closing head without rewriting any HTML."""

    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.line_offsets = [0]
        for index, character in enumerate(source):
            if character == "\n":
                self.line_offsets.append(index + 1)
        self.head_end = None
        self.in_head = False
        self.style_start = None
        self.styles = []

    def absolute_offset(self):
        line, column = self.getpos()
        return self.line_offsets[line - 1] + column

    def handle_starttag(self, tag, attrs):
        if tag == "head":
            self.in_head = True
        if tag == "style" and dict(attrs).get("id") == STYLE_ID:
            if not self.in_head:
                raise ValueError("The existing print style must be inside the HTML head.")
            self.style_start = self.absolute_offset()

    def handle_endtag(self, tag):
        if tag == "style" and self.style_start is not None:
            end = self.source.find(">", self.absolute_offset())
            if end < 0:
                raise ValueError("The existing print style has no closing tag.")
            self.styles.append((self.style_start, end + 1))
            self.style_start = None
        if tag == "head":
            self.head_end = self.absolute_offset()
            self.in_head = False


def prepare_html(source):
    locations = StyleLocations(source)
    locations.feed(source)
    locations.close()
    if locations.head_end is None:
        raise ValueError("No closing </head> found. Use the complete HTML exported from Jupyter.")
    if locations.style_start is not None:
        raise ValueError("The existing print style has no closing tag.")
    if len(locations.styles) > 1:
        raise ValueError("More than one matching print-style ID was found in the HTML.")
    newline = "\r\n" if "\r\n" in source else "\n"
    style = f'<style id="{STYLE_ID}" type="text/css">\n{PRINT_CSS}</style>'
    style = style.replace("\n", newline)
    if locations.styles:
        start, end = locations.styles[0]
        return source[:start] + style + source[end:]
    position = locations.head_end
    return source[:position] + style + newline + source[position:]


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("html", type=Path, help="HTML exported from Jupyter")
    parser.add_argument("--output", type=Path,
                        help="Output HTML; default: executed.html beside the input")
    args = parser.parse_args()
    source_path = args.html.expanduser().resolve()
    output_path = (args.output.expanduser().resolve() if args.output else
                   source_path.with_name("executed.html"))
    try:
        if source_path == output_path or (output_path.exists() and
                                         output_path.samefile(source_path)):
            parser.error("The output must differ from the input; the original HTML is never overwritten.")
        source = source_path.read_bytes().decode("utf-8")
        result = prepare_html(source)
        output_path.write_bytes(result.encode("utf-8"))
    except (OSError, UnicodeError, ValueError) as error:
        parser.error(str(error))
    print(f"Prepared: {output_path}")
    print("Open this HTML in your browser; print/save as PDF with A4 paper, 100% scale,")
    print("and headers/footers off. Save the PDF as executed.pdf.")


if __name__ == "__main__":
    main()
