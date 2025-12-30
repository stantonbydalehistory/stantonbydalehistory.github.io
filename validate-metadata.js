#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const contentDir = path.join(__dirname, 'content');
const errors = [];
const warnings = [];

// Helper to check if a file exists
function fileExists(filePath) {
  const fullPath = path.join(contentDir, filePath + '.md');
  return fs.existsSync(fullPath);
}

// Helper to extract frontmatter from markdown file
function extractFrontmatter(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;
  
  try {
    return yaml.load(match[1]);
  } catch (e) {
    return null;
  }
}

// Get all markdown files in a directory recursively
function getMarkdownFiles(dir, fileList = []) {
  const files = fs.readdirSync(dir);
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      getMarkdownFiles(filePath, fileList);
    } else if (file.endsWith('.md')) {
      fileList.push(filePath);
    }
  });
  
  return fileList;
}

// Validate a single article
function validateArticle(filePath) {
  const relativePath = path.relative(contentDir, filePath);
  const frontmatter = extractFrontmatter(filePath);
  
  if (!frontmatter) {
    errors.push(`${relativePath}: No valid frontmatter found`);
    return;
  }
  
  // Check residents
  if (frontmatter.residents) {
    if (!Array.isArray(frontmatter.residents)) {
      errors.push(`${relativePath}: 'residents' should be an array`);
    } else {
      frontmatter.residents.forEach(resident => {
        if (!resident.startsWith('resident/')) {
          errors.push(`${relativePath}: resident path '${resident}' should start with 'resident/'`);
        } else if (!fileExists(resident)) {
          errors.push(`${relativePath}: resident file '${resident}.md' does not exist`);
        }
      });
    }
  }
  
  // Check buildings
  if (frontmatter.buildings) {
    if (!Array.isArray(frontmatter.buildings)) {
      errors.push(`${relativePath}: 'buildings' should be an array`);
    } else {
      frontmatter.buildings.forEach(building => {
        if (!building.startsWith('building/')) {
          errors.push(`${relativePath}: building path '${building}' should start with 'building/'`);
        } else if (!fileExists(building)) {
          errors.push(`${relativePath}: building file '${building}.md' does not exist`);
        }
      });
    }
  }
  
  // Check institutions
  if (frontmatter.institutions) {
    if (!Array.isArray(frontmatter.institutions)) {
      errors.push(`${relativePath}: 'institutions' should be an array`);
    } else {
      frontmatter.institutions.forEach(institution => {
        if (!institution.startsWith('institution/')) {
          errors.push(`${relativePath}: institution path '${institution}' should start with 'institution/'`);
        } else if (!fileExists(institution)) {
          errors.push(`${relativePath}: institution file '${institution}.md' does not exist`);
        }
      });
    }
  }
  
  // Check for old 'people' field
  if (frontmatter.people) {
    warnings.push(`${relativePath}: Uses deprecated 'people' field, should use 'residents' instead`);
  }
  
  // Check required fields
  if (!frontmatter.title) {
    errors.push(`${relativePath}: Missing 'title' field`);
  }
  if (!frontmatter.date) {
    errors.push(`${relativePath}: Missing 'date' field`);
  }
}

// Main validation
console.log('🔍 Validating metadata in all articles...\n');

const recordsDir = path.join(contentDir, 'records');
if (!fs.existsSync(recordsDir)) {
  console.error('❌ Records directory not found:', recordsDir);
  process.exit(1);
}

const articleFiles = getMarkdownFiles(recordsDir);
console.log(`Found ${articleFiles.length} articles to validate\n`);

articleFiles.forEach(validateArticle);

// Report results
console.log('═'.repeat(60));
console.log('VALIDATION RESULTS');
console.log('═'.repeat(60));

if (errors.length === 0 && warnings.length === 0) {
  console.log('✅ All metadata is valid!');
} else {
  if (errors.length > 0) {
    console.log(`\n❌ ERRORS (${errors.length}):`);
    console.log('─'.repeat(60));
    errors.forEach(error => console.log(`  ${error}`));
  }
  
  if (warnings.length > 0) {
    console.log(`\n⚠️  WARNINGS (${warnings.length}):`);
    console.log('─'.repeat(60));
    warnings.forEach(warning => console.log(`  ${warning}`));
  }
  
  console.log('\n' + '═'.repeat(60));
  console.log(`Total: ${errors.length} error(s), ${warnings.length} warning(s)`);
  
  if (errors.length > 0) {
    process.exit(1);
  }
}
