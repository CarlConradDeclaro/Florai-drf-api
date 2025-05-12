import re

def strip_surrounding_stars(text):
    return re.sub(r'^\*+\s*|\s*\*+$', '', text).strip()
