import click
from .works import Works

@click.command(help='Show outputs either RIS or bibtex for a DOI.')
@click.option("--ris", is_flag=True, default=False, help="Show ris")
@click.option("--bibtex", is_flag=True, default=False, help="Show bibtex")
@click.argument('doi', nargs=1)
def main(doi, ris, bibtex):
    w = Works(doi)
    if ris:
        print(w._ris())
    if bibtex:
        print(w._bibtex())
