import csv
import sys
from io import StringIO
from typing import Any, List

import click

from src.excel import read_xlsx, write_xlsx


def main() -> None:
    sys.exit(cli())


@click.group(help="openpyxl wrappert cli")
def cli() -> None:
    pass


@cli.command()
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
def write(
    template_xlsx: str,
    sheet_xy_csv: List[Any],
    output_xlsx: str,
    delimiter: str,
) -> None:
    write_xlsx(template_xlsx, sheet_xy_csv, output_xlsx, delimiter)


@cli.command()
@click.option(
    "--input_xlsx", "-I", required=True, type=click.Path(readable=True)
)
@click.option("--sheet_no", default=1, type=int, help="sheet no")
@click.option(
    "--output", type=click.Path(writable=True), help="output file name",
)
@click.option("--delimiter", default=",", type=str, help="csv delimiter")
def read(input_xlsx: str, sheet_no: int, output: str, delimiter=str) -> None:
    rows = read_xlsx(input_xlsx, sheet_no)

    buffer = StringIO()
    writer = csv.writer(buffer, delimiter=delimiter)
    writer.writerows(rows)
    message = buffer.getvalue()
    buffer.close()

    if output:
        with open(output, "w", newline="", encoding="UTF-8") as csvfile:
            click.echo(message, file=csvfile, nl=False)
    else:
        click.echo(message, nl=False)


cli.add_command(write)
cli.add_command(read)


if __name__ == "__main__":
    main()
