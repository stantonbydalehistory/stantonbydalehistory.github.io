# Metadata Validation Scripts

These scripts validate the metadata in all Hugo content articles to ensure that references to residents, buildings, and institutions are valid and point to existing files.

## Available Scripts

### Python Version (Recommended)
```bash
python3 validate-metadata.py
```

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