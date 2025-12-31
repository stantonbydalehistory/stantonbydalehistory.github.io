#!/usr/bin/env python3
"""
Validate metadata in all Hugo content articles.
Checks that residents, buildings, and institutions paths are valid.
"""

import os
import sys
import re
from pathlib import Path
import yaml

# Colors for terminal output
class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def extract_frontmatter(file_path):
    """Extract YAML frontmatter from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return None
        
        return yaml.safe_load(match.group(1))
    except Exception as e:
        print(f"{Colors.RED}Error reading {file_path}: {e}{Colors.RESET}")
        return None

def file_exists(content_dir, relative_path):
    """Check if a referenced file exists."""
    full_path = content_dir / f"{relative_path}.md"
    return full_path.exists()

# Expected fields for records/articles
EXPECTED_ARTICLE_FIELDS = {
    'title', 'date', 'dateAdded', 'sources', 'source', 'summary',
    'residents', 'buildings', 'institutions', 
    'person_building_links',  # maps residents to buildings they're associated with (any relationship type)
    'person_institution_links',  # maps residents to institutions they're associated with (any relationship type)
    'tags', 'themes', 'street', 'resident_role',
    'type', 'draft', 'layout',
    'businesses',  # deprecated, should be 'institutions'
    'categories',  # deprecated or alternative taxonomy
    'event_date_note'  # additional context for dates
}

# Expected fields for institutions
EXPECTED_INSTITUTION_FIELDS = {
    'title', 'institution_type', 'type', 'location', 'dates',
    'buildings', 'residents', 'notes', 'draft',
    'operating_from', 'operating_to',  # date range fields
    'aliases',  # alternative names
    'premises'  # deprecated, should be 'buildings'
}

# Expected fields for residents
EXPECTED_RESIDENT_FIELDS = {
    'title', 'role', 'roles', 'dates', 'birth', 'death',
    'aliases', 'draft',
    'buildings',  # deprecated, should be derived from records
    'institutions',  # deprecated, should be derived from records
    'businesses',  # deprecated, was renamed to institutions
    'notes'  # deprecated, content should be in markdown body only
}

# Valid institution types (enum)
VALID_INSTITUTION_TYPES = {
    'business',
    'social',
    'religious',
    'sports',
    'governmental'
}

def validate_article(file_path, content_dir, errors, warnings):
    """Validate a single article's metadata."""
    relative_path = file_path.relative_to(content_dir)
    frontmatter = extract_frontmatter(file_path)
    
    if not frontmatter:
        errors.append(f"{relative_path}: No valid frontmatter found")
        return
    
    # Check for unexpected fields
    for field in frontmatter.keys():
        if field not in EXPECTED_ARTICLE_FIELDS:
            errors.append(f"{relative_path}: Unexpected field '{field}'")
    
    # Check residents
    if 'residents' in frontmatter:
        residents = frontmatter['residents']
        if not isinstance(residents, list):
            errors.append(f"{relative_path}: 'residents' should be an array")
        else:
            for resident in residents:
                if not resident.startswith('resident/'):
                    errors.append(
                        f"{relative_path}: resident path '{resident}' should start with 'resident/'"
                    )
                elif not file_exists(content_dir, resident):
                    errors.append(
                        f"{relative_path}: resident file '{resident}.md' does not exist"
                    )
    
    # Check buildings
    if 'buildings' in frontmatter:
        buildings = frontmatter['buildings']
        if not isinstance(buildings, list):
            errors.append(f"{relative_path}: 'buildings' should be an array")
        else:
            for building in buildings:
                if not building.startswith('building/'):
                    errors.append(
                        f"{relative_path}: building path '{building}' should start with 'building/'"
                    )
                elif not file_exists(content_dir, building):
                    errors.append(
                        f"{relative_path}: building file '{building}.md' does not exist"
                    )
    
    # Check institutions
    if 'institutions' in frontmatter:
        institutions = frontmatter['institutions']
        if not isinstance(institutions, list):
            errors.append(f"{relative_path}: 'institutions' should be an array")
        else:
            for institution in institutions:
                if not institution.startswith('institution/'):
                    errors.append(
                        f"{relative_path}: institution path '{institution}' should start with 'institution/'"
                    )
                elif not file_exists(content_dir, institution):
                    errors.append(
                        f"{relative_path}: institution file '{institution}.md' does not exist"
                    )
    
    # Check person_building_links (maps residents to buildings they're associated with)
    if 'person_building_links' in frontmatter:
        person_building_links = frontmatter['person_building_links']
        if not isinstance(person_building_links, dict):
            errors.append(f"{relative_path}: 'person_building_links' should be a dictionary/object")
        else:
            for resident, building_list in person_building_links.items():
                # Check resident path
                if not resident.startswith('resident/'):
                    errors.append(
                        f"{relative_path}: person_building_links key '{resident}' should start with 'resident/'"
                    )
                elif not file_exists(content_dir, resident):
                    errors.append(
                        f"{relative_path}: person_building_links resident '{resident}.md' does not exist"
                    )
                
                # Check building list
                if not isinstance(building_list, list):
                    errors.append(
                        f"{relative_path}: person_building_links['{resident}'] should be an array of building paths"
                    )
                else:
                    for building in building_list:
                        if not building.startswith('building/'):
                            errors.append(
                                f"{relative_path}: person_building_links building '{building}' should start with 'building/'"
                            )
                        elif not file_exists(content_dir, building):
                            errors.append(
                                f"{relative_path}: person_building_links building '{building}.md' does not exist"
                            )
    
    # Check person_institution_links (maps residents to institutions they're associated with)
    if 'person_institution_links' in frontmatter:
        person_institution_links = frontmatter['person_institution_links']
        if not isinstance(person_institution_links, dict):
            errors.append(f"{relative_path}: 'person_institution_links' should be a dictionary/object")
        else:
            for resident, institution_list in person_institution_links.items():
                # Check resident path
                if not resident.startswith('resident/'):
                    errors.append(
                        f"{relative_path}: person_institution_links key '{resident}' should start with 'resident/'"
                    )
                elif not file_exists(content_dir, resident):
                    errors.append(
                        f"{relative_path}: person_institution_links resident '{resident}.md' does not exist"
                    )
                
                # Check institution list
                if not isinstance(institution_list, list):
                    errors.append(
                        f"{relative_path}: person_institution_links['{resident}'] should be an array of institution paths"
                    )
                else:
                    for institution in institution_list:
                        if not institution.startswith('institution/'):
                            errors.append(
                                f"{relative_path}: person_institution_links institution '{institution}' should start with 'institution/'"
                            )
                        elif not file_exists(content_dir, institution):
                            errors.append(
                                f"{relative_path}: person_institution_links institution '{institution}.md' does not exist"
                            )

    
    # Check for deprecated 'streets' field
    if 'streets' in frontmatter:
        warnings.append(
            f"{relative_path}: Uses deprecated 'streets' field, should be removed"
        )
    
    # Check for deprecated 'people' field
    if 'people' in frontmatter:
        warnings.append(
            f"{relative_path}: Uses deprecated 'people' field, should use 'residents' instead"
        )
    
    # Check for deprecated 'businesses' field
    if 'businesses' in frontmatter:
        warnings.append(
            f"{relative_path}: Uses deprecated 'businesses' field, should use 'institutions' instead"
        )
    
    # Check required fields
    if 'title' not in frontmatter:
        errors.append(f"{relative_path}: Missing 'title' field")
    if 'date' not in frontmatter:
        errors.append(f"{relative_path}: Missing 'date' field")
    if 'dateAdded' not in frontmatter:
        warnings.append(f"{relative_path}: Missing 'dateAdded' field")
    
    # Check for sources
    if 'sources' not in frontmatter and 'source' not in frontmatter:
        warnings.append(f"{relative_path}: Missing 'sources' or 'source' field")
    elif 'sources' in frontmatter:
        sources = frontmatter['sources']
        if not isinstance(sources, list):
            errors.append(f"{relative_path}: 'sources' should be an array")
        elif len(sources) == 0:
            warnings.append(f"{relative_path}: 'sources' field is empty, should have at least one source")
    
    # Check for both source and sources
    if 'source' in frontmatter and 'sources' in frontmatter:
        warnings.append(
            f"{relative_path}: Has both 'source' and 'sources' fields, consolidate to 'sources'"
        )

def validate_institution(file_path, content_dir, errors, warnings):
    """Validate a single institution's metadata."""
    relative_path = file_path.relative_to(content_dir)
    frontmatter = extract_frontmatter(file_path)
    
    if not frontmatter:
        errors.append(f"{relative_path}: No valid frontmatter found")
        return
    
    # Check for unexpected fields
    for field in frontmatter.keys():
        if field not in EXPECTED_INSTITUTION_FIELDS:
            errors.append(f"{relative_path}: Unexpected field '{field}'")
    
    # Check institution_type is set
    if 'institution_type' not in frontmatter:
        errors.append(f"{relative_path}: Missing 'institution_type' field")
    elif not frontmatter['institution_type']:
        errors.append(f"{relative_path}: 'institution_type' field is empty")
    else:
        # Check institution_type is a valid value
        institution_type = frontmatter['institution_type'].lower()
        if institution_type not in VALID_INSTITUTION_TYPES:
            valid_types = ', '.join(sorted([t.capitalize() for t in VALID_INSTITUTION_TYPES]))
            errors.append(
                f"{relative_path}: Invalid institution_type '{frontmatter['institution_type']}'. "
                f"Must be one of: {valid_types}"
            )
    
    # Check for deprecated 'premises' field
    if 'premises' in frontmatter:
        warnings.append(
            f"{relative_path}: Uses deprecated 'premises' field, should use 'buildings' instead"
        )

def validate_resident(file_path, content_dir, errors, warnings):
    """Validate a single resident's metadata."""
    relative_path = file_path.relative_to(content_dir)
    frontmatter = extract_frontmatter(file_path)
    
    if not frontmatter:
        errors.append(f"{relative_path}: No valid frontmatter found")
        return
    
    # Check for unexpected fields
    for field in frontmatter.keys():
        if field not in EXPECTED_RESIDENT_FIELDS:
            errors.append(f"{relative_path}: Unexpected field '{field}'")
    
    # Check for deprecated 'notes' field
    if 'notes' in frontmatter:
        errors.append(
            f"{relative_path}: Uses 'notes' field. Content should be in markdown body only, not in frontmatter"
        )
    
    # Check for deprecated 'businesses' field
    if 'businesses' in frontmatter:
        warnings.append(
            f"{relative_path}: Uses deprecated 'businesses' field, should use 'institutions' instead"
        )
    
    # Check for deprecated 'buildings' field
    if 'buildings' in frontmatter:
        warnings.append(
            f"{relative_path}: Resident should not have 'buildings' field. Buildings are derived from records"
        )
    
    # Check for deprecated 'institutions' field
    if 'institutions' in frontmatter:
        warnings.append(
            f"{relative_path}: Resident should not have 'institutions' field. Institutions are derived from records"
        )

def get_file_context(file_path, content_dir):
    """Get the frontmatter context of a file for LLM fixing."""
    frontmatter = extract_frontmatter(file_path)
    if not frontmatter:
        return "No frontmatter found"
    
    relative_path = file_path.relative_to(content_dir)
    return yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)

def main():
    """Main validation routine."""
    # Get content directory
    script_dir = Path(__file__).parent
    content_dir = script_dir / 'content'
    records_dir = content_dir / 'records'
    institution_dir = content_dir / 'institution'
    resident_dir = content_dir / 'resident'
    
    if not records_dir.exists():
        print(f"{Colors.RED}❌ Records directory not found: {records_dir}{Colors.RESET}")
        sys.exit(1)
    
    print(f"{Colors.BLUE}🔍 Validating metadata in all articles, institutions, and residents...{Colors.RESET}\n")
    
    # Get all markdown files
    article_files = list(records_dir.rglob('*.md'))
    print(f"Found {len(article_files)} articles to validate")
    
    institution_files = []
    if institution_dir.exists():
        institution_files = list(institution_dir.glob('*.md'))
        print(f"Found {len(institution_files)} institutions to validate")
    
    resident_files = []
    if resident_dir.exists():
        resident_files = list(resident_dir.glob('*.md'))
        print(f"Found {len(resident_files)} residents to validate")
    print()
    
    errors = []
    warnings = []
    error_contexts = {}  # Store file contexts for errors
    
    # Validate each article
    for article_file in article_files:
        validate_article(article_file, content_dir, errors, warnings)
    
    # Validate each institution
    for institution_file in institution_files:
        validate_institution(institution_file, content_dir, errors, warnings)
    
    # Validate each resident
    for resident_file in resident_files:
        validate_resident(resident_file, content_dir, errors, warnings)
    
    # Collect context for files with errors
    for error in errors:
        file_match = re.match(r'^(.*?):', error)
        if file_match:
            relative_path = file_match.group(1)
            full_path = content_dir / relative_path
            if full_path.exists() and relative_path not in error_contexts:
                error_contexts[relative_path] = get_file_context(full_path, content_dir)
    
    # Report results
    print("=" * 60)
    print(f"{Colors.BOLD}VALIDATION RESULTS{Colors.RESET}")
    print("=" * 60)
    
    if not errors and not warnings:
        print(f"{Colors.GREEN}✅ All metadata is valid!{Colors.RESET}")
    else:
        if errors:
            print(f"\n{Colors.RED}❌ ERRORS ({len(errors)}):{Colors.RESET}")
            print("-" * 60)
            for error in errors:
                print(f"  {error}")
        
        if warnings:
            print(f"\n{Colors.YELLOW}⚠️  WARNINGS ({len(warnings)}):{Colors.RESET}")
            print("-" * 60)
            for warning in warnings:
                print(f"  {warning}")
        
        print("\n" + "=" * 60)
        print(f"Total: {Colors.RED}{len(errors)} error(s){Colors.RESET}, "
              f"{Colors.YELLOW}{len(warnings)} warning(s){Colors.RESET}")
        
        # Generate LLM-friendly output
        if errors:
            print("\n" + "=" * 60)
            print(f"{Colors.BOLD}LLM CONTEXT (Copy this to fix errors):{Colors.RESET}")
            print("=" * 60)
            print("\n```")
            print("TASK: Fix the following metadata validation errors in Hugo content files.")
            print(f"Repository: stantonbydalehistory.github.io")
            print(f"Content directory: {content_dir}")
            print()
            print("ERRORS TO FIX:")
            for i, error in enumerate(errors, 1):
                print(f"{i}. {error}")
            
            print("\n" + "-" * 60)
            print("FILE CONTEXTS (Current frontmatter of files with errors):")
            print("-" * 60)
            
            for file_path, context in sorted(error_contexts.items()):
                print(f"\nFile: {file_path}")
                print("---")
                print(context)
                print("---")
            
            print("\n" + "-" * 60)
            print("AVAILABLE REFERENCE FILES:")
            print("-" * 60)
            
            # List available residents
            resident_dir = content_dir / 'resident'
            if resident_dir.exists():
                residents = sorted([f.stem for f in resident_dir.glob('*.md')])
                print(f"\nResidents ({len(residents)}):")
                for r in residents[:20]:  # Show first 20
                    print(f"  - resident/{r}")
                if len(residents) > 20:
                    print(f"  ... and {len(residents) - 20} more")
            
            # List available buildings
            building_dir = content_dir / 'building'
            if building_dir.exists():
                buildings = sorted([str(f.relative_to(building_dir).with_suffix('')) 
                                  for f in building_dir.rglob('*.md')])
                print(f"\nBuildings ({len(buildings)}):")
                for b in buildings[:20]:  # Show first 20
                    print(f"  - building/{b}")
                if len(buildings) > 20:
                    print(f"  ... and {len(buildings) - 20} more")
            
            # List available institutions
            institution_dir = content_dir / 'institution'
            if institution_dir.exists():
                institutions = sorted([f.stem for f in institution_dir.glob('*.md')])
                print(f"\nInstitutions ({len(institutions)}):")
                for inst in institutions:
                    print(f"  - institution/{inst}")
            
            print("\n" + "-" * 60)
            print("INSTRUCTIONS:")
            print("-" * 60)
            print("1. Fix incorrect path formats (e.g., 'institution//stanhope-arms' → 'building/stanhope-street/stanhope-arms')")
            print("2. Create missing resident/building/institution files if they should exist")
            print("3. Remove references to non-existent files if they're not needed")
            print("4. Ensure all paths use the correct prefix (resident/, building/, institution/)")
            print("5. Update the frontmatter in the affected files using replace_string_in_file tool")
            print("```")
            
            sys.exit(1)

if __name__ == '__main__':
    main()
