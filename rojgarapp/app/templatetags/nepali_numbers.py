from django import template
from django.utils.translation import get_language

register = template.Library()

# Nepali numeral mapping
NEPALI_NUMERALS = {
    '0': '०',
    '1': '१',
    '2': '२',
    '3': '३',
    '4': '४',
    '5': '५',
    '6': '६',
    '7': '७',
    '8': '८',
    '9': '९',
}

@register.filter
def nepali_number(value):
    """
    Convert numbers to Nepali numerals when language is Nepali
    Usage: {{ number|nepali_number }}
    """
    if value is None:
        return value
    
    # Check if current language is Nepali
    current_language = get_language()
    if not current_language.startswith('ne'):
        return value
    
    # Convert to string and replace each digit
    value_str = str(value)
    nepali_str = ''
    
    for char in value_str:
        if char in NEPALI_NUMERALS:
            nepali_str += NEPALI_NUMERALS[char]
        else:
            nepali_str += char
    
    return nepali_str

@register.filter
def nepali_percentage(value):
    """
    Convert percentage numbers to Nepali numerals
    Usage: {{ percentage|nepali_percentage }}
    """
    if value is None:
        return value
    
    # Check if current language is Nepali
    current_language = get_language()
    if not current_language.startswith('ne'):
        return f"{value}%"
    
    # Convert to string and replace each digit
    value_str = str(value)
    nepali_str = ''
    
    for char in value_str:
        if char in NEPALI_NUMERALS:
            nepali_str += NEPALI_NUMERALS[char]
        else:
            nepali_str += char
    
    return f"{nepali_str}%"

@register.filter
def nepali_count(value):
    """
    Convert count numbers to Nepali numerals
    Usage: {{ count|nepali_count }}
    """
    if value is None:
        return value
    
    # Check if current language is Nepali
    current_language = get_language()
    if not current_language.startswith('ne'):
        return value
    
    # Convert to string and replace each digit
    value_str = str(value)
    nepali_str = ''
    
    for char in value_str:
        if char in NEPALI_NUMERALS:
            nepali_str += NEPALI_NUMERALS[char]
        else:
            nepali_str += char
    
    return nepali_str 