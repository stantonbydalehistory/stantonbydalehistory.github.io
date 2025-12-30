# Metadata Validation Scripts

These scripts validate the metadata in all Hugo content articles to ensure that references to residents, buildings, and institutions are valid and point to existing files.

## Available Scripts

### Python Version (Recommended)
```bash
python3 validate-metadata.py
```

### Node.js Version
```bash
node validate-metadata.js
```
*Note: Requires `js-yaml` package. Install with: `npm install js-yaml`*

## What the Scripts Check

1. **Residents**: Validates that all paths in `residents:` field:
   - Start with `resident/`
   - Point to existing `.md` files in `content/resident/`

2. **Buildings**: Validates that all paths in `buildings:` field:
   - Start with `building/`
   - Point to existing `.md` files in `content/building/`

3. **Institutions**: Validates that all paths in `institutions:` field:
   - Start with `institution/`
   - Point to existing `.md` files in `content/institution/`

4. **Required Fields**: Checks that each article has:
   - `title` field
   - `date` field

5. **Recommended Fields**: Warns if missing:
   - `dateAdded` field (date the article was added to the repository)
   - `sources` or `source` field (at least one source should be documented)

6. **Deprecated Fields**: Warns about use of:
   - `people` field (should use `residents` instead)
   - `streets` field (should be removed, use tags or other fields instead)
   
7. **Conflicting Fields**: Warns if both `source` and `sources` are present (should consolidate to `sources`)

## Output

The scripts will display:
- ✅ Success message if all metadata is valid
- ❌ **Errors**: Critical issues that should be fixed (broken references, wrong formats)
- ⚠️  **Warnings**: Suggestions for improvements (deprecated fields)

## Example Output

```
🔍 Validating metadata in all articles...

Found 50 articles to validate

============================================================
VALIDATION RESULTS
============================================================

❌ ERRORS (2):
------------------------------------------------------------
  records/1923-07-05-funeral-c-j-w-radford.md: resident file 'resident/c-j-w-radford.md' does not exist
  records/1969-01-24-stapleford-news-horse-and-cart.md: institution file 'institution/wi.md' does not exist

⚠️  WARNINGS (1):
------------------------------------------------------------
  records/1920-03-19-joseph-wright-oldest-resident.md: Uses deprecated 'people' field, should use 'residents' instead

============================================================
Total: 2 error(s), 1 warning(s)
```

## Integration with Git

You can run this script as part of your pre-commit checks or CI/CD pipeline to ensure metadata quality.

### Pre-commit Hook Example

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python3 validate-metadata.py
if [ $? -ne 0 ]; then
    echo "Metadata validation failed. Fix errors before committing."
    exit 1
fi
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```
