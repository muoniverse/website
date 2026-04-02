#!/usr/bin/env python3
"""
Script to convert muoniverse job openings Excel file to HTML table code.

Usage: python3 excel_to_html.py [input.xlsx]
"""

import datetime
from html import escape
import os
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

    def safe_text(value):
        if pd.isna(value):
            return ""
        return escape(str(value), quote=True)

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
            html.append(f'                        <td class="role">{safe_text(row["Role"])}</td>')
            html.append(f'                        <td class="location">{safe_text(row["Location"])}</td>')
            html.append(f'                        <td class="location">{safe_text(row["Responsible PI"])}</td>')
            html.append(f'                        <td class="position">{safe_text(row["Position"])}</td>')
            if pd.isna(row["Link"]):
                html.append('                        <td><a class="apply-link-disabled">Opening soon</a></td>')
            else:
                html.append(f'                        <td><a href="{safe_text(row["Link"])}" target="_blank" class="apply-link">Info &amp; apply</a></td>')

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
    except FileNotFoundError:
        print(f"Error: File '{excel_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Get the "index.html" file in the parent folder of this script
    html_file = os.path.join(os.path.dirname(__file__), "..", "index.html")
    # Search for the markers in the HTML file and replace the content between them with the generated HTML
    with open(html_file, "r") as f:
        html_content = f.read()
    start_marker = "<!-- start-job-table -->"
    end_marker = "<!-- end-job-table -->"
    start_index = html_content.find(start_marker)
    end_index = html_content.find(end_marker)
    if start_index == -1 or end_index == -1:
        print("Error: Markers not found in HTML file.", file=sys.stderr)
        sys.exit(1)

    # Check that there are no duplicate markers
    if html_content.count(start_marker) > 1 or html_content.count(end_marker) > 1:
        print("Error: Duplicate markers found in HTML file.", file=sys.stderr)
        sys.exit(1)
    new_html_content = html_content[:start_index + len(start_marker)] + "\n"
    new_html_content += html_output + "\n"
    new_html_content += html_content[end_index:]
    with open(html_file, "w") as f:
        f.write(new_html_content)
    # print(html_output)

    print("HTML table generated and inserted into index.html successfully.", file=sys.stderr)
    print("Run   python -m http.server   in the parent folder to serve the website locally, then open http://localhost:8000 in your browser.", file=sys.stderr)
