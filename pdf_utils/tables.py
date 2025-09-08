from pdfplumber.page import Page
from typing import TypeAlias, Tuple
import re

## type definitions
PageIndex: TypeAlias = int
TopPosition: TypeAlias = int
LabelLocation: TypeAlias = Tuple[PageIndex, TopPosition]

## Returns the page and top position where a label is found
## The label is represented as a list of strings
def find_label_locations(query_tokens: list[str], pages: list[Page]) -> list[LabelLocation]:
    locations = []
    for page_index, page in enumerate(pages):
        words = page.extract_words()    
        words_to_match = len(query_tokens)
        for i in range(len(words)):
            count = 0
            for j in range(words_to_match):
                word = words[i + j]
                if query_tokens[j] in word['text']:
                    count += 1
                else:
                    break
            if count == words_to_match:
                locations.append((page_index, words[i]['top']))
                break
    return locations


## Extracts the first matching pattern value from a PDF page
## Example usage:
##     pattern = re.compile(r"Saldo Atual em (\d{2}/\d{2}/\d{4})")
##     balance_date = extract_pattern_value(page, pattern)
def extract_pattern_value(page: Page, pattern: re.Pattern[str]) -> str | None:
    text = page.extract_text()
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None


def extract_data_table_after_location(label_locations: list[LabelLocation], pages: list[Page]) -> list[list[str]]:
    table_data = []
    header_added = False

    for label_location in label_locations:
        page_index, balance_y_position = label_location
        page = pages[page_index]

        # Get table objects with their positions
        table_objects = page.find_tables()
        target_table = None
        tables_below = []

        # Find all tables below the balance text
        for table_obj in table_objects:
            table_top = table_obj.bbox[1]  # top y-coordinate of table
            # Check if table is below the balance text (higher y-value means below in this coordinate system)
            if table_top > balance_y_position:
                tables_below.append((table_top, table_obj))

        if len(tables_below) > 0:
            target_table = tables_below[0][1]  # If only one table, use it
        
        if target_table:
            if not header_added:
                table_data.extend(target_table.extract())
                header_added = True
            else:
                table_data.extend(target_table.extract()[1:])

    return table_data
