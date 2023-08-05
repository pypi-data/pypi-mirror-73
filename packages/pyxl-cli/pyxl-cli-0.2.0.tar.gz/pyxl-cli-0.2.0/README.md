# pyxl-cli

opeypyxl wrapper for cli use.

## install

```sh
pip install pyxl-cli
```

## usage

### read
output stdout CSV format

```sh
pyxl read \
    --input_xlsx input.xlsx
```

output file TSV format

```sh
pyxl read \
    --input_xlsx input.xlsx \
    --output /tmp/output.tsv \
    --delimiter='\t'
```

### write
for CSV file

```sh
pyxl write \
    --sheet_xy_csv 1 A1 input.csv \
    template.xlsx output.xlsx
```

for 2 TSV files

```sh
pyxl write \
    --sheet_xy_csv 1 A1 input_a.tsv \
    --sheet_xy_csv 1 F12 input_b.tsv \
    --delimiter="\t" \
    template.xlsx output.xlsx
```