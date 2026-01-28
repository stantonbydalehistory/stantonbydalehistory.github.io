# Claude Instructions for Stanton-by-Dale History Site

## Project Overview
This is a Hugo static site documenting the history of Stanton-by-Dale village through historical records, residents, buildings, and institutions.

## Content Types and Metadata Standards

### 1. Records (Historical Articles)
Location: `content/records/`
Filename format: `YYYY-MM-DD-descriptive-title.md`

**Required Fields:**
```yaml
---
title: "Article Title"
date: YYYY-MM-DD  # Can be YYYY if only year is known
dateAdded: YYYY-MM-DD  # Date added to site
themes: ["theme1", "theme2"]  # e.g., "crime", "death", "business"
residents: []  # Array of resident/filename references
buildings: []  # Array of building/street/filename references
institutions: []  # Array of institution/filename references
sources:
  - type: "newspaper"  # or "document", "census", etc.
    title: "Newspaper Name"
    date: YYYY-MM-DD  # Can be YYYY if only year is known
    page: null  # or page number
---
```

**Date Format Note:** The `date` field can be:
- Full date: `YYYY-MM-DD` (e.g., `1883-11-23`)
- Year only: `YYYY` (e.g., `1839`) when exact date is unknown
- Filename should match: `YYYY-MM-DD-title.md` or `YYYY-title.md` for year-only dates

**Optional Fields:**
- `summary`: Brief description
- `tags`: Additional tags
- `street`: Street taxonomy
- `resident_role`: Role taxonomy
- `categories`: Alternative taxonomy
- `event_date_note`: Additional date context
- `record_type`: Set to `"announcement"` for birth/marriage/death announcements (excludes from homepage rotation)
- `announcement_type`: Type of announcement: `"birth"`, `"marriage"`, or `"death"` (only use with `record_type: "announcement"`)
- `person_building_links`: Dictionary mapping residents to buildings they're associated with
  ```yaml
  person_building_links:
    resident/firstname-lastname:
      - building/street-name/building-name
    resident/another-person:
      - building/street-name/another-building
  ```
  Use this when a person has a specific relationship to a building mentioned in the record (e.g., rector of a church, owner of a property, lived at a location) beyond just being mentioned in the same record.

- `person_institution_links`: Dictionary mapping residents to institutions they're associated with
  ```yaml
  person_institution_links:
    resident/firstname-lastname:
      - institution/institution-name
    resident/another-person:
      - institution/another-institution
  ```
  Use this when a person has a specific relationship to an institution (e.g., rector of a church, owner of a business, member of a club) beyond just being mentioned in the same record.

**Deprecated/Disallowed:**
- ❌ `businesses` (use `institutions` instead)
- ❌ `streets` (removed)
- ❌ `people` (use `residents` instead)

**Transcription Rules:**
- When given a screenshot of a historical newspaper article:
  - Transcribe text EXACTLY as it appears, including:
    - Original spelling errors (e.g., "secident" not "accident")
    - Original punctuation and capitalization
    - OCR errors in the source
  - Use markdown for formatting:
    - `**HEADLINE**` for bold headlines
    - Proper paragraph breaks
  - After frontmatter, include the transcribed text
  - Correct obvious OCR errors in your mind but flag them and note them.

### 2. Residents (People)
Location: `content/resident/`
Filename format: `firstname-lastname.md` or `title-firstname-lastname.md` (e.g., `rev-john-smith.md`)

**Required Fields:**
```yaml
---
title: "Full Name"
role: ["occupation"]  # or roles: ["role1", "role2"]
dates:
  birth: "YYYY" or "YYYY-MM-DD" or "" if unknown
  death: "YYYY" or "YYYY-MM-DD" or "" if unknown
---
```

**Optional Fields:**
- `aliases`: ["Alternative Name 1", "Alternative Name 2"]
- `draft`: true/false

**Disallowed Fields:**
- ❌ `notes` - Content must be in markdown body only, NOT in frontmatter
- ❌ `buildings` - Buildings are derived from records that mention the resident
- ❌ `institutions` - Institutions are derived from records that mention the resident
- ❌ `businesses` - Deprecated, and should be derived from records anyway

**Important:** Residents should NOT have direct links to buildings or institutions in metadata. These relationships are automatically derived from historical records that mention the resident.

### 3. Institutions (Businesses, Organizations, Churches, Clubs)
Location: `content/institution/`
Filename format: `descriptive-name.md`

**Required Fields:**
```yaml
---
title: "Institution Name"
institution_type: "business" | "social" | "religious" | "sports" | "governmental"  # Must be lowercase
---
```

**Valid Institution Types (lowercase only):**
- `business` - Pubs, shops, ironworks, smithy, etc.
- `social` - British Legion, Women's Institute, associations
- `religious` - Churches, chapels
- `sports` - Cricket club, sports clubs
- `governmental` - Police force, local government bodies

**Optional Fields:**
```yaml
buildings: []  # Array of building/street/filename where institution operates
residents: []  # Array of resident/filename associated with institution
operating_from: YYYY  # or null
operating_to: YYYY  # or null
dates:
  established: "YYYY"
  closed: "YYYY"
aliases: ["Alternative Name"]
location: "Place Name"
notes: "Brief description"
type: "Additional type info"
```

**Deprecated:**
- ⚠️ `premises` (use `buildings` instead)

### 4. Buildings
Location: `content/building/`
Filename format: `street-name/building-name.md`

**Standard Fields:**
```yaml
---
title: "Building Name or Address"
street: "Street Name"
number: "Number" (if applicable)
institutions: []  # Institutions that operated here
---
```

### 5. Census Records
Location: `content/census/`
Filename format: `YYYY.md` (e.g., `1861.md`)

**Required Fields:**
```yaml
---
title: "YYYY Census"
date: YYYY-MM-DD  # Census date
census_year: YYYY
census_date: "D Month YYYY"  # Human readable date
fields:  # Column definitions for this census year
  - key: "schedule"
    label: "Schedule Number"
  - key: "name"
    label: "Name and Surname"
  - key: "relation"
    label: "Relation to Head of Family"
  - key: "condition"
    label: "Condition"
    help: "Married, single, widowed"
  - key: "age"
    label: "Age"
  - key: "gender"
    label: "Gender"
    help: "M or F"
  - key: "occupation"
    label: "Rank, Profession or Occupation"
  - key: "birthplace"
    label: "Where Born"
  - key: "disability"
    label: "Whether Blind, Deaf or Dumb"
entries:  # Household entries
  - schedule: 1
    street: "Street Name"
    address: "Building Name"  # Optional
    building: "building/street/filename"  # Optional link
    household:
      - name: "John Smith"
        resident: "resident/john-smith"  # Optional - link if resident page exists
        relation: "Head"
        condition: "Married"
        age: 45
        gender: "M"
        occupation: "Publican"
        birthplace: "Stanton, Derbyshire"
        disability: ""
    notes: "Optional notes about this household"  # Optional
---

Content describing this census...
```

**Field Structure:**
- `fields`: Array of field definitions that define columns for this census year
  - `key`: Short field name used in household data (e.g., "name", "age", "occupation")
  - `label`: Full column heading as it appears on the census form
  - `help`: Optional tooltip text to explain the field

**Entry Structure:**
- `entries`: Array of households/schedules from the census
  - `schedule`: Schedule number from census form (required)
  - `street`: Street name (required)
  - `address`: Specific building name or address (optional)
  - `building`: Link to building page (optional, format: `building/street-name/filename`)
  - `household`: Array of people in this household (required)
    - Use short field names matching the `key` values in `fields`
    - `name`: Person's full name (required)
    - `resident`: Link to resident page (optional, format: `resident/filename`)
    - Other fields as defined in `fields` array
  - `notes`: Optional notes about this household

**Important Census Guidelines:**
1. **One census file per year** - All households for a year in one file
2. **Flexible fields** - Different census years have different fields, define them in `fields` array
3. **Optional resident links** - Only link to resident pages that exist; leave blank ("") for others (e.g., children who don't appear in other records)
4. **Use shorthand** - Field keys are short (name, age, occupation) while labels are full (Name and Surname, Rank Profession or Occupation)
5. **Building links** - Link households to building pages where applicable for cross-referencing
6. **Anchored links** - Each person gets an auto-generated anchor: `#schedule-N-person-M` for deep linking from resident pages
7. **Table layout** - The census layout automatically renders data as a table matching the original census format

**Different Census Years:**
Different census years have different fields. Always define the fields for that specific year:
- 1841: Fewer fields, no relationship to head, ages rounded
- 1851-1911: More detailed fields, exact ages, relationships
- Later censuses: Additional fields like rooms, employer status, etc.

Example fields for 1841 census:
```yaml
fields:
  - key: "schedule"
    label: "Schedule Number"
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

### 6. Photographs
Location: `content/photograph/`
Filename format: `descriptive-name.md`

**Required Fields:**
```yaml
---
title: "Photograph Title"
photo_date: "c. 1900"  # Can be approximate: "c. 1900", "Early 1930s", or specific: "1952"
image: "/images/photographs/filename.jpg"  # Path to image in static/images/photographs/
---
```

**Optional Fields:**
```yaml
photographer: "Unknown"  # Who took the photo
location: "High Street, Stanton by Dale"  # Where photo was taken
source: "Village Archive"  # Where photo came from
description: "A glimpse of village life"  # Short description for gallery view

# Linking to related entities (same as historical records)
buildings: []  # Array of building/street/filename references
institutions: []  # Array of institution/filename references
residents: []  # Array of resident/filename references
```

**Image Storage:**
- Place image files in `/static/images/photographs/`
- Supported formats: JPG, PNG
- Reference in frontmatter as `/images/photographs/filename.jpg` (note: no "static" prefix)

**Linking Behavior:**
- Photographs work the same as historical records for linking
- When you link a photograph to buildings/institutions/residents, it will appear on those entity pages
- Bidirectional: photographs show linked entities, and entities show linked photographs

### 7. Interviews
Location: `content/interview/`
Filename format: `YYYY-MM-DD-interviewee-name.md`

**Required Fields:**
```yaml
---
title: "Interview with [Name]"
date: YYYY-MM-DD  # Date of interview
dateAdded: YYYY-MM-DD  # Date added to site
interviewee: "Person Name"
interviewer: "Interviewer Name"
location: "Location"
---
```

**Optional Fields:**
```yaml
audio_file: "/path/to/audio.mp3"  # Path to audio recording
transcript_file: "/path/to/transcript.pdf"  # Path to transcript PDF
buildings: []  # Array of building references mentioned in interview
institutions: []  # Array of institution references
residents: []  # Array of resident references
```

### 8. Trade Directories
Location: `content/trade-directory/`
Filename format: `YYYY-directory-name.md`

**Required Fields:**
```yaml
---
title: "Directory Name, Year"
date: YYYY-MM-DD  # Publication date
dateAdded: YYYY-MM-DD  # Date added to site
directory_name: "Full Directory Name"
publisher: "Publisher Name"
sources:
  - type: "directory"
    title: "Full Directory Name"
    date: YYYY
    page: null  # or page number
---
```

**Optional Fields:**
```yaml
buildings: []  # Buildings mentioned in directory
institutions: []  # Institutions/businesses listed
residents: []  # People mentioned
```

## Validation
Run `python3 validate-metadata.py` to check all metadata conforms to standards after each edit.

## Path Reference Format
- Residents: `resident/filename` (without .md extension)
- Buildings: `building/street-name/filename`
- Institutions: `institution/filename`
- Census: `census/YYYY` (e.g., `census/1861`)
- Photographs: `photograph/filename`
- Interviews: `interview/filename`
- Trade Directories: `trade-directory/filename`

## Examples

### Example Census Entry
```yaml
---
title: "1861 Census"
date: 1861-04-07
census_year: 1861
census_date: "7 April 1861"
fields:
  - key: "schedule"
    label: "Schedule Number"
  - key: "street"
    label: "Street"
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
entries:
  - schedule: 1
    street: "Stanhope Street"
    address: "Stanhope Arms"
    building: "building/stanhope-street/stanhope-arms"
    household:
      - name: "John Smith"
        resident: "resident/john-smith"
        relation: "Head"
        condition: "Married"
        age: 45
        gender: "M"
        occupation: "Publican"
        birthplace: "Stanton, Derbyshire"
      - name: "Mary Smith"
        resident: ""
        relation: "Wife"
        condition: "Married"
        age: 42
        gender: "F"
        occupation: ""
        birthplace: "Sandiacre, Derbyshire"
---

This is the 1861 census for Stanton-by-Dale.
```

### Example Record
```yaml
---
title: "Dreadful Accident at Stanton-by-Dale"
date: 1883-11-23
dateAdded: 2025-12-30
themes: ["death", "accident", "inquest"]
buildings:
  - building/stanhope-street/stanhope-arms
institutions:
  - institution/stanhope-arms
  - institution/stanton-ironworks
residents:
  - resident/pc-newton
sources:
  - type: "newspaper"
    title: "Derbyshire Advertiser and Journal"
    date: 1883-11-23
    page: null
---

**DREADFUL ACCIDENT AT STANTON-BY-DALE.**

[Article text transcribed exactly as it appears...]
```

### Example Record with Person-Building Links
```yaml
---
title: "Church Service and Village Event"
date: 1937-05-14
dateAdded: 2025-12-30
themes: ["community", "religious"]
buildings:
  - building/main-street/the-hall
  - building/stanhope-street/st-michaels
institutions:
  - institution/st-michaels
residents:
  - resident/rev-a-b-roberts
  - resident/c-r-crompton
person_building_links:
  resident/rev-a-b-roberts:
    - building/stanhope-street/st-michaels  # Rector of this church
  resident/c-r-crompton:
    - building/main-street/the-hall  # Lives at The Hall
person_institution_links:
  resident/rev-a-b-roberts:
    - institution/st-michaels  # Rector of St Michael's
sources:
  - type: "newspaper"
    title: "Derby Daily Telegraph"
    date: 1937-05-14
    page: 4
---

A service in the Parish Church was conducted by the Rev. A. B. Roberts.
Mr. C. R. Crompton, of The Hall, Stanton-by-Dale donated medals to the children.
```

### Example Resident
```yaml
---
title: "P.C. Newton"
role: ["Police Constable"]
dates:
  birth: ""
  death: ""
---

Police Constable Newton was stationed at Stanton-by-Dale in 1883.

He discovered the body of George Course on the road after a fatal cart accident in November 1883.
```

### Example Institution
```yaml
---
title: "Stanton Ironworks"
institution_type: "business"
buildings: []
residents: []
operating_from: null
operating_to: null
aliases:
  - "Stanton Iron Works"
  - "The Stanton Ironworks"
---

The Stanton Ironworks was a major employer in the area...
```

### Example Photograph
```yaml
---
title: "The Chequers Inn, 1930s"
photo_date: "c. 1935"
image: "/images/photographs/chequers-1930s.jpg"
photographer: "Unknown"
location: "Dale Road, Stanton by Dale"
source: "Village Archive Collection"
description: "The Chequers Inn with licensee standing in doorway"
buildings:
  - building/dale-road/chequers-inn
institutions:
  - institution/chequers-inn
residents:
  - resident/john-smith
---

This photograph shows the Chequers Inn in the mid-1930s. The building features the characteristic stone construction typical of the area. Standing in the doorway is believed to be John Smith, the licensee at that time.

The pub served as a focal point for the community throughout this period.
```

## Common Patterns

### When creating a record from a newspaper screenshot:
1. Create filename: `YYYY-MM-DD-short-descriptive-title.md`
2. Extract date from filename if applicable, or prompt user if not visible.
3. Transcribe text EXACTLY including errors
4. Identify people, places, institutions mentioned
5. Create resident pages for any new people mentioned
6. Link to existing buildings/institutions
7. Format with proper markdown (bold headlines, paragraphs)

### When creating a resident:
1. Use format: `firstname-lastname.md` or `rev-firstname-lastname.md`
2. Use `role` or `roles` for occupation
3. DO NOT add `buildings` or `institutions` - let records define these
4. Content goes in markdown body, not `notes` field

### When creating an institution:
1. Use lowercase `institution_type`: business, social, religious, or sports
2. Link to buildings where it operates
3. Link to key residents (owners, officials)
4. Use `notes` for brief description

### When creating a census:
1. Use filename: `YYYY.md` (e.g., `1861.md`)
2. Define fields for that specific census year in `fields` array
3. Use shorthand keys in household data (name, age, occupation)
4. Only link to residents that have pages; leave others blank ("")
5. Link households to buildings where applicable
6. Add notes to individual households if needed
7. All households for a year go in one file

### When creating a photograph:
1. Use descriptive filename: `descriptive-name.md` (e.g., `chequers-inn-1930s.md`)
2. Place image file in `/static/images/photographs/`
3. Reference image as `/images/photographs/filename.jpg` (no "static" prefix)
4. Use approximate dates when exact date unknown: "c. 1935", "Early 1900s", "1950s"
5. Link to buildings, institutions, and residents visible or mentioned
6. Add descriptive content in markdown body with historical context
7. Use `description` field for short gallery caption

## Workflow
1. Create/edit content
2. Run validation: `python3 validate-metadata.py`
3. Fix any errors shown
4. Commit changes
5. Push to GitHub (site auto-deploys via GitHub Pages)
