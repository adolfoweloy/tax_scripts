from pdfplumber.page import Page
import re

## TODO: this function has a bad smell. 
# It extracts balance data  
# balance data is not used within this function
# And this makes it hard to refactor in order to make this function more generic
def extract_current_balance_data(pages: list[Page]):
    for first_page in pages:
        # Extract the text from the first page
        text = first_page.extract_text()
        match = re.search(r"Saldo Atual em (\d{2}/\d{2}/\d{4})", text)
        if match:
            balance_at = match.group(1)
            words = first_page.extract_words()

            # Find the position of the balance date
            balance_y_position = None
            for i in range(len(words)):
                word = words[i]
                if "Saldo" in word['text']:
                    if ("Atual" in words[i+1]['text']):
                        balance_y_position = word['top']  # Use top instead of bottom
                        break

            if balance_y_position:
                # Get table objects with their positions
                table_objects = first_page.find_tables()
                
                target_table = None
                tables_below = []

                # Find all tables below the balance text
                for table_obj in table_objects:
                    table_top = table_obj.bbox[1]  # top y-coordinate of table
                    # Check if table is below the balance text (higher y-value means below in this coordinate system)
                    if table_top > balance_y_position:
                        tables_below.append((table_top, table_obj))
                
                # Sort tables by y-position and get the second one (index 1)
                if len(tables_below) >= 2:
                    tables_below.sort(key=lambda x: x[0])  # Sort by y-position
                    target_table = tables_below[1][1]  # Get the second table
                elif len(tables_below) == 1:
                    target_table = tables_below[0][1]  # If only one table, use it
                
                if target_table:
                    table_data = target_table.extract()
                    return (balance_at, table_data)
                else:
                    raise ValueError("No table found after current balance text")

    return None
