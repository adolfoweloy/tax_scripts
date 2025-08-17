
import re

def continental_to_english(number: str) -> str:
    """
    Convert numeric strings from Brazilian format to US
    e.g. "1.234,56 to 1,234.56
    """
    number = number.strip()
    if re.fullmatch(r'[\d\.\,]+', number):
        return number.replace('.', '').replace(',', '.')
    return number