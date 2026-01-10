# Census Records Guide

This guide explains how to add and manage census records on the Stanton-by-Dale History website.

## Overview

The census system allows you to:
- Store complete census data for multiple years
- Display census records in tables matching the original format
- Link census entries to resident pages (optional)
- Link households to building pages for cross-referencing
- Deep-link from resident pages to specific census entries
- Adapt to different census formats across years

## File Structure

Census files are stored in `/content/census/` with one file per year:
- `1861.md` - 1861 census data
- `1871.md` - 1871 census data
- etc.

All households for a given census year are in a single file.

## Data Format

Each census file has two main sections in the YAML frontmatter:

### 1. Fields Definition

Define the columns for that census year using short `key` names and full `label` names:

```yaml
fields:
  - key: "schedule"
    label: "Schedule Number"
  - key: "name"
    label: "Name and Surname"
  - key: "age"
    label: "Age"
  - key: "occupation"
    label: "Rank, Profession or Occupation"
    help: "Optional tooltip text"
```

**Why?** This allows easy data entry with short keys while displaying proper column headings.

### 2. Census Entries

Each household/schedule is an entry:

```yaml
entries:
  - schedule: 1
    street: "Stanhope Street"
    address: "Stanhope Arms"
    building: "building/stanhope-street/stanhope-arms"
    household:
      - name: "John Smith"
        resident: "resident/john-smith"
        relation: "Head"
        age: 45
        occupation: "Publican"
        # ... other fields
    notes: "Optional household notes"
```

## Key Features

### Shorthand Data Entry

Instead of typing `"Rank, Profession or Occupation"` for every person, just use the key `occupation`.

The layout template automatically maps `occupation` → "Rank, Profession or Occupation" based on your `fields` definition.

### Optional Resident Links

The `resident` field can be:
- A link: `resident: "resident/john-smith"` (if a resident page exists)
- Empty: `resident: ""` (if no resident page exists yet)

This is crucial because:
- Not everyone in the census needs a resident page (e.g., children)
- You can add census data before creating all resident pages
- Resident pages can be added later without restructuring the census

### Building Cross-References

Link households to buildings:
```yaml
building: "building/stanhope-street/stanhope-arms"
```

This creates bidirectional references:
- Building pages show which censuses mention them
- Census records link to building details

### Deep Linking

Each person gets an automatic anchor ID:
```
#schedule-N-person-M
```

Example: `#schedule-1-person-0` for the first person in schedule 1.

This allows resident pages to link directly to their census appearances.

### Responsive Table Layout

The census layout automatically:
- Renders data as a table matching the original census format
- Adds zebra striping for readability
- Makes tables responsive for mobile devices
- Links names to resident pages where available
- Highlights heads of household

## Different Census Years

Each census year has different fields. Configure the `fields` array for each year.

### 1841 Census Example

```yaml
fields:
  - key: "name"
    label: "Name"
  - key: "age"
    label: "Age"
    help: "Ages rounded to nearest 5 over age 15"
  - key: "occupation"
    label: "Profession, Trade, Employment"
  - key: "birthplace"
    label: "Where Born"
    help: "Y if born in same county, N if not, or country name"
```

### 1861 Census Example

```yaml
fields:
  - key: "name"
    label: "Name and Surname"
  - key: "relation"
    label: "Relation to Head of Family"
  - key: "condition"
    label: "Condition"
  - key: "age"
    label: "Age"
  - key: "gender"
    label: "Gender"
  - key: "occupation"
    label: "Rank, Profession or Occupation"
  - key: "birthplace"
    label: "Where Born"
  - key: "disability"
    label: "Whether Blind, Deaf or Dumb"
```

### 1911 Census Example

```yaml
fields:
  - key: "name"
    label: "Name and Surname"
  - key: "relation"
    label: "Relation to Head of Family"
  - key: "age"
    label: "Age"
  - key: "occupation"
    label: "Occupation"
  - key: "industry"
    label: "Industry or Service"
  - key: "employer"
    label: "Employer, Worker, or Own Account"
  - key: "birthplace"
    label: "Birthplace"
  - key: "nationality"
    label: "Nationality"
  - key: "marriage_years"
    label: "Years Married"
  - key: "children"
    label: "Children Born Alive"
```

## Adding Census Data

### Step 1: Create the File

Create `/content/census/YYYY.md` (e.g., `1861.md`)

### Step 2: Add Frontmatter

```yaml
---
title: "1861 Census"
date: 1861-04-07
census_year: 1861
census_date: "7 April 1861"
fields:
  # Define your fields here
entries:
  # Add your data here
---
```

### Step 3: Define Fields

Look at the original census form and define a field for each column:

```yaml
fields:
  - key: "schedule"
    label: "Schedule Number"
  - key: "name"
    label: "Name and Surname"
  # ... etc
```

Use short, simple keys for data entry (`name`, `age`, `occupation`).

### Step 4: Add Entries

For each household/schedule:

```yaml
entries:
  - schedule: 1
    street: "Stanhope Street"
    address: "The Red Lion"
    building: "building/stanhope-street/red-lion"
    household:
      - name: "John Smith"
        resident: "resident/john-smith"  # or "" if no page
        relation: "Head"
        condition: "Married"
        age: 45
        gender: "M"
        occupation: "Publican"
        birthplace: "Stanton, Derbyshire"
        disability: ""
```

**Tips:**
- Use `""` for empty fields
- Only link residents who have pages
- Add `notes` field to entries for additional context
- Group related households together with comments

### Step 5: Validate

Run validation to check for errors:

```bash
python3 validate-metadata.py
```

This checks:
- Required fields exist
- Field definitions are valid
- Resident links are correct
- Building links are correct
- YAML syntax is valid

### Step 6: View Locally

Build and serve the site locally:

```bash
hugo server
```

Navigate to `/census/YYYY/` to see your census.

## Tips and Best Practices

### Data Entry Efficiency

1. **Copy field definitions** from similar years
2. **Use text editor multi-cursor** for repetitive data
3. **Leave resident links blank initially** - add them later
4. **Use YAML comments** to organize schedules by street/area

### Handling Incomplete Data

- Use `""` for unknown fields rather than omitting them
- Add `notes` to explain gaps or uncertainties
- If a field doesn't exist in a census year, don't include it in `fields`

### Linking Strategy

**Link residents when:**
- They appear in multiple records
- They hold significant roles (publicans, clergy, officials)
- They're mentioned in newspaper articles

**Don't link residents when:**
- They only appear in census (children, temporary workers)
- You have no other information about them
- They're just passing through the village

### Building Links

Link buildings for:
- Named properties (pubs, farms, halls)
- Known addresses with building pages
- Properties mentioned in other records

Don't link for:
- Generic cottages without names
- Addresses without building pages
- Temporary or demolished buildings (unless documented)

## Troubleshooting

### YAML Syntax Errors

**Problem:** Validation fails with "No valid frontmatter found"

**Common causes:**
- Missing quotes around strings with special characters
- Double quotes in quoted strings (use single quotes inside)
- Incorrect indentation (must use spaces, not tabs)
- Unclosed brackets or quotes

**Fix:** Validate YAML syntax with an online YAML validator

### Missing Residents

**Problem:** Validation says `resident/john-smith.md does not exist`

**Solutions:**
1. Create the resident page
2. Change to `resident: ""` if page isn't needed
3. Check spelling and filename format

### Table Not Rendering

**Problem:** Census displays but table is blank

**Check:**
1. Fields array has correct keys
2. Household data uses the same keys as field definitions
3. No YAML syntax errors
4. Each person has required `name` field

## Advanced Features

### Household Notes

Add context to specific households:

```yaml
- schedule: 5
  household:
    # ... people
  notes: "This family moved to Ilkeston later in 1861"
```

### Multiple Addresses on Same Street

```yaml
- schedule: 1
  street: "Main Street"
  address: "The Hall"
  # ...

- schedule: 2
  street: "Main Street"
  address: "Hall Farm"
  # ...
```

### Cross-Referencing to Records

In historical records, reference census data:

```markdown
According to the 1861 census, John Smith was living at the Stanhope Arms
(see [1861 census](/census/1861/#schedule-1-person-0)).
```

## Summary

The census system provides:
- ✅ Flexible field definitions for different census years
- ✅ Easy data entry with shorthand keys
- ✅ Optional resident and building linking
- ✅ Accurate table rendering matching original format
- ✅ Deep linking for cross-references
- ✅ Validation to catch errors
- ✅ Responsive design for mobile

All census data is in structured YAML frontmatter, making it easy to:
- Search programmatically
- Export to other formats
- Generate statistics
- Create visualizations

For questions or issues, see the main project documentation or validation errors.
