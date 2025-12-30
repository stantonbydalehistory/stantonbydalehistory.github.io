# GitHub Copilot Instructions for Stanton-by-Dale History Site

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
date: YYYY-MM-DD
dateAdded: YYYY-MM-DD  # Date added to site
themes: ["theme1", "theme2"]  # e.g., "crime", "death", "business"
residents: []  # Array of resident/filename references
buildings: []  # Array of building/street/filename references
institutions: []  # Array of institution/filename references
sources:
  - type: "newspaper"  # or "document", "census", etc.
    title: "Newspaper Name"
    date: YYYY-MM-DD
    page: null  # or page number
---
```

**Optional Fields:**
- `summary`: Brief description
- `tags`: Additional tags
- `street`: Street taxonomy
- `resident_role`: Role taxonomy
- `categories`: Alternative taxonomy
- `event_date_note`: Additional date context
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
institution_type: "business" | "social" | "religious" | "sports"  # Must be lowercase
---
```

**Valid Institution Types (lowercase only):**
- `business` - Pubs, shops, ironworks, smithy, etc.
- `social` - British Legion, Women's Institute, associations
- `religious` - Churches, chapels
- `sports` - Cricket club, sports clubs

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

## Validation
Run `python3 validate-metadata.py` to check all metadata conforms to standards after each edit.

## Path Reference Format
- Residents: `resident/filename` (without .md extension)
- Buildings: `building/street-name/filename`
- Institutions: `institution/filename`

## Examples

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

## Workflow
1. Create/edit content
2. Run validation: `python3 validate-metadata.py`
3. Fix any errors shown
4. Commit changes
5. Push to GitHub (site auto-deploys via GitHub Pages)
