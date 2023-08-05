import sys
from typing import Any, List

import click

from src.excel import write_xlsx


def main() -> None:
    sys.exit(cli())


@click.command()
@click.argument("template_xlsx", required=True, type=click.Path(exists=True))
@click.option(
    "--sheet_xy_csv",
    "-T",
    required=True,
    nargs=3,
    type=click.Tuple([int, str, click.Path(exists=True)]),
    multiple=True,
    help=("Sheet No and Address(ex: a1, aa12) and Input CSV file"),
)
@click.argument("output_xlsx", required=True, type=click.Path(writable=True))
@click.option("--delimiter", default=",", type=str, help="csv delimiter")
def cli(
    template_xlsx: str,
    sheet_xy_csv: List[Any],
    output_xlsx: str,
    delimiter: str,
) -> None:
    write_xlsx(template_xlsx, sheet_xy_csv, output_xlsx, delimiter)


if __name__ == "__main__":
    main()
