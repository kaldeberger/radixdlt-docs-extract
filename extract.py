# scrape with: `wget -m -k -K -l 7 -t 6 -w 5 https://docs-babylon.radixdlt.com/main/index.html`

import os
import json
import argparse
from bs4 import BeautifulSoup

def extract_main_content(html_content):
    """Extract the text content inside the <main> tag from the given HTML."""
    soup = BeautifulSoup(html_content, 'lxml')
    main_tag = soup.find('main')
    
    if main_tag:
        return ' '.join(main_tag.stripped_strings)
    return None

def extract_title(html_content):
    """Extract the text content inside the <title> tag from the given HTML."""
    soup = BeautifulSoup(html_content, 'lxml')
    title_tag = soup.find('title')
    
    if title_tag:
        return title_tag.string.replace(" :: Radix Documentation", "").strip()
    return None

def clean_text(text):
    """Clean up text by replacing smart quotes and other problematic characters."""
    replacements = {
        '\u2018': "'",  # Left single quotation mark
        '\u2019': "'",  # Right single quotation mark
        '\u201C': '"',  # Left double quotation mark
        '\u201D': '"',  # Right double quotation mark
        '\u200b': '',   # Zero-width space
        '…': "...",     # Ellipsis
    }
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    return text

def find_html_files(folder_path):
    """Find all .html and .htm files in a folder (recursively) and return their absolute paths."""
    html_files = []

    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('.html') or filename.endswith('.htm'):
                full_path = os.path.join(dirpath, filename)
                html_files.append(full_path)

    return html_files

def read_file(file_path):
    """Read and return the content of a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract text from HTML files.")
    parser.add_argument('-i', type=str, required=True, help="Path to the folder containing HTML files.")
    parser.add_argument('-o', type=str, required=True, help="Path and filename for the output JSON file.")

    args = parser.parse_args()

    html_files = find_html_files(args.i)

    extracted_data = []

    for file_path in html_files:
        html_content = read_file(file_path)
        main_content = extract_main_content(html_content)
        page_title = extract_title(html_content)

        if main_content and page_title:
            data = {
                "page": clean_text(page_title),
                "content": clean_text(main_content)
            }
            extracted_data.append(data)

    # Save the list as a JSON file
    with open(args.o, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=4)
    
    print(f"Read {len(html_files)} files.")
    print(f"Extracted data from {len(extracted_data)} files and saved to {args.o}.")

