# Nepali Number Display Feature

This feature automatically converts numbers to Nepali numerals when the user selects Nepali language in the application.

## How it Works

When a user switches the language to Nepali (नेपाली), all numbers in the application will be displayed using Nepali numerals:

- English: 1, 2, 3, 4, 5, 6, 7, 8, 9, 0
- Nepali: १, २, ३, ४, ५, ६, ७, ८, ९, ०

## Template Filters Available

### 1. `nepali_number`
Converts any number to Nepali numerals when language is Nepali.

**Usage:**
```django
{% load nepali_numbers %}
{{ 123|nepali_number }}  {# Shows: १२३ in Nepali, 123 in English #}
```

### 2. `nepali_percentage`
Converts percentage numbers to Nepali numerals with % symbol.

**Usage:**
```django
{% load nepali_numbers %}
{{ 45.67|nepali_percentage }}  {# Shows: ४५.६७% in Nepali, 45.67% in English #}
```

### 3. `nepali_count`
Converts count numbers to Nepali numerals.

**Usage:**
```django
{% load nepali_numbers %}
{{ user_count|nepali_count }}  {# Shows: १००० in Nepali, 1000 in English #}
```

## Where It's Applied

The Nepali number conversion is automatically applied to:

1. **Dashboard Statistics:**
   - Total Users count
   - Jobs Posted count
   - Jobs Filled count
   - Active Jobs count
   - Application Success Rate percentage
   - Profession distribution counts and percentages

2. **Forms List:**
   - Row numbers (S.N.)

3. **Job Details:**
   - Positions available count
   - Required personnel count

4. **Applications List:**
   - Application dates (if numbers are present)

## Language Switching

Users can switch between English and Nepali using the language dropdown in the navigation bar:

1. Click on the "Language" dropdown in the top navigation
2. Select "English" or "नेपाली"
3. The page will reload with the selected language
4. All numbers will automatically convert to the appropriate numeral system

## Technical Implementation

- **Template Filters:** Custom Django template filters in `app/templatetags/nepali_numbers.py`
- **Language Detection:** Uses Django's `get_language()` function
- **Automatic Conversion:** Only converts when language is Nepali (`ne-np`)
- **Fallback:** Returns original numbers for English language

## Adding to New Templates

To add Nepali number support to new templates:

1. Load the template tags:
```django
{% load nepali_numbers %}
```

2. Apply the appropriate filter:
```django
{{ number|nepali_number }}
{{ percentage|nepali_percentage }}
{{ count|nepali_count }}
```

## Examples

| English | Nepali | Filter Used |
|---------|--------|-------------|
| 123 | १२३ | `nepali_number` |
| 45.67% | ४५.६७% | `nepali_percentage` |
| 1000 | १००० | `nepali_count` |
| Hello 123 World | Hello १२३ World | `nepali_number` |

The feature is fully automatic and requires no additional configuration once implemented. 