# Excel to HTML Table Converter

This script reads the job openings Excel file, generates the HTML table, and inserts it into the job table section of the parent [index.html](../index.html) file.

## Requirements

```shell
pip install -r requirements.txt
```

## Usage

### Basic usage

```shell
python3 excel_to_html.py
```

This uses the default input file name muoniverse-job-openings.xlsx.

### Use a custom Excel file

```shell
python3 excel_to_html.py input.xlsx
```

The script updates the content between the markers below in the parent [index.html](../index.html):

- <!-- start-job-table -->
- <!-- end-job-table -->

## Notes

- If `Comments` is exactly `Closed` (case-insensitive), the row is hidden even if Deadline is in the future.
- Rows are shown if Deadline is empty or in the future.
- Rows are hidden if Deadline is in the past.
- Missing Link shows disabled text: Opening soon.
- Example-row filtering is currently disabled in code and can be enabled by uncommenting the relevant lines.
