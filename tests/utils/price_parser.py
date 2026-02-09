import re

def parse_price(text: str) -> float:
    """Extract numeric value from price strings like 'ILS 49.60', '$49.60', '49.60'."""
    if not text:
        raise ValueError("empty price text")
    m = re.search(r"[\d,]+(?:\.\d+)?", text)
    if not m:
        raise ValueError(f"no numeric price in '{text}'")
    num = m.group(0).replace(",", "")
    return float(num)