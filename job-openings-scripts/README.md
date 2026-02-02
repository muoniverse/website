# Excel to HTML Table Converter

This script converts the job openings Excel file into the correct HTML table code.

## Requirements

```bash
pip install pandas openpyxl
```

## Usage

### Basic usage (output to file):
```bash
python3 excel_to_html.py > table_output.html
```
Then replace the corresponding section in the `index.html`.


## Notes

- Empty rows are automatically skipped, as well as rows with missing information
- Check the code to enable/hide example columns
- In the future, add filter to automatically hide job offerings with deadline in the past
