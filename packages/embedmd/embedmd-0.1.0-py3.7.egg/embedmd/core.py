"""
topo2geo/core.py
"""

import re
import markdown
from pathlib import Path
import click
from . import version as VERSION

CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help']
}


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('html_file')
# @click.argument('output_file')
def main(html_file: str):
    """
    Embed markdown files into html files
    """
    if not Path(html_file).exists():
        print(f'Error: file {html_file} does not exist')
        return

    with open(html_file, 'r') as f:
        html = f.read()

    markdown_files = re.findall(r'#INCLUDE (.*).md', html)
    for filename in markdown_files:
        try:
            with open(f'{filename}.md', 'r') as f:
                md = f.read()
        except IOError:
            ...
            continue

        md_html = markdown.markdown(md, extensions=['md_in_html'])

        html.replace(f"'#INCLUDE {filename}.md'", md_html)
