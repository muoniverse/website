#!/usr/bin/env python3
"""
Script to convert muoniverse job openings Excel file to HTML table code.

Usage: python3 excel_to_html.py input.xlsx > output.html
"""

import datetime
import pandas as pd
import sys

def generate_html_table(excel_file):
    """
    Read Excel file and generate HTML table code.
    
    Args:
        excel_file: Path to the Excel file
    
    Returns:
        HTML table string
    """
    # Read the Excel file
    df = pd.read_excel(excel_file)
    
    # Note: If you want to filter out example rows, uncomment the following lines:
    # if 'is an example' in df.columns:
    #     df = df[df['is an example'] != True]
    
    # Keep only the columns we need
    COLUMNS = ['Role', 'Location', 'Responsible PI', 'Position', 'Link', 'Deadline']
    
    df = df[COLUMNS]
    ## Drop rows where essential fields are missing
    ##df = df.dropna(subset=COLUMNS)
    
    # Start building the HTML
    html = []
    html.append('            <table>')
    html.append('                <thead>')
    html.append('                    <tr>')
    html.append('                        <th>Role</th>')
    html.append('                        <th>Location</th>')
    html.append('                        <th>Main PI(s)</th>')
    html.append('                        <th>Position</th>')
    html.append('                        <th></th>')
    html.append('                    </tr>')
    html.append('                </thead>')
    html.append('                <tbody>')
    
    # Add each row
    for _, row in df.iterrows():
        has_deadline = not pd.isna(row['Deadline'])
        if not has_deadline or row['Deadline'] > datetime.datetime.now():
            html.append('                    <tr>')
            html.append(f'                        <td class="role">{row["Role"]}</td>')
            html.append(f'                        <td class="location">{row["Location"]}</td>')
            html.append(f'                        <td class="location">{row["Responsible PI"]}</td>')
            html.append(f'                        <td>{row["Position"]}</td>')
            if pd.isna(row["Link"]):
                html.append(f'                        <td><a href="#" class="apply-link-disabled">Opening soon</a></td>')
            else:
                html.append(f'                        <td><a href="{row["Link"]}" target="_blank" class="apply-link">Info &amp; apply</a></td>')
                
            html.append('                    </tr>')
        else:
            print(f"# Skipping {row['Role']} at {row['Location']} ({row['Position']})", file=sys.stderr)

    html.append('                </tbody>')
    html.append('            </table>')
    
    return '\n'.join(html)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        excel_file = sys.argv[1]
    else:
        excel_file = "muoniverse-job-openings.xlsx"
    
    try:
        html_output = generate_html_table(excel_file)
        print(html_output)
    except FileNotFoundError:
        print(f"Error: File '{excel_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
