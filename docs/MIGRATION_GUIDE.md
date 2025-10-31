# User Migration Guide: From Geneweb to GenewebPy

**Version:** 1.0  
**Last Updated:** October 31, 2025  
**Status:** Active

> **For Administrators**: See [DEPLOYMENT.md](DEPLOYMENT.md) for server installation and deployment.  
> **For Developers**: See [OCAML_TO_PYTHON.md](OCAML_TO_PYTHON.md) for code translation reference.

## Table of Contents

1. [Introduction](#introduction)
2. [Before You Start](#before-you-start)
3. [Understanding the Migration](#understanding-the-migration)
4. [Step-by-Step Migration](#step-by-step-migration)
5. [Verifying Your Data](#verifying-your-data)
6. [What's Different](#whats-different)
7. [Getting Help](#getting-help)
8. [Frequently Asked Questions](#frequently-asked-questions)

---

## Introduction

Welcome! This guide will help you migrate your family tree data from the original Geneweb (OCaml version) to GenewebPy (Python version).

### What is GenewebPy?

GenewebPy is a modern reimplementation of Geneweb in Python. It offers:
- ✅ Same familiar interface and features
- ✅ Modern Python infrastructure
- ✅ Improved performance and maintainability
- ✅ Easy deployment with Docker
- ✅ Compatible with your existing Geneweb data

### Who Should Use This Guide?

This guide is for:
- **Family historians** managing their own Geneweb installation
- **Website administrators** hosting Geneweb for family/community use
- **Anyone** with existing Geneweb data who wants to migrate to GenewebPy

### What You'll Need

- Your existing Geneweb database
- Basic computer skills (following instructions, using command line)
- Backup of your data

### Important Note

**Your original Geneweb data will not be modified.** The migration creates a new database, leaving your original intact as a backup.

---

## Before You Start

### Check What You Have

First, let's understand your current Geneweb setup:

**Find your Geneweb installation:**
```bash
# On Linux/Mac, typically in:
~/geneweb/
# or
/usr/local/share/geneweb/

# On Windows:
C:\Program Files\Geneweb\
```

**Find your databases:**
```bash
# Look in the 'bases' directory
ls ~/geneweb/bases/
# You should see folders like: martin, family, smith, etc.
```

Each folder contains your family tree data in `.gwb` format.

---

## Understanding the Migration

### What Happens During Migration?

```
Your Geneweb Data (.gwb files)
         ↓
    Export to .gw format
         ↓
    Import to GenewebPy
         ↓
   New SQLite database
         ↓
    Ready to use!
```

### File Formats Explained

| Format | Used By | Description |
|--------|---------|-------------|
| `.gwb` | Old Geneweb (OCaml) | Binary database format |
| `.gw` | Both versions | Text format (human-readable) |
| `.db` (SQLite) | GenewebPy (Python) | New database format |

**The `.gw` format** is the bridge between old and new!

### What Gets Migrated?

✅ **Migrated**:
- All persons (names, dates, places)
- All families and relationships
- Birth, marriage, death events
- Additional events (baptism, burial, etc.)
- Sources and notes
- Witnesses
- Occupation information
- Titles

❌ **Not Migrated** (if you have custom modifications):
- Custom CSS themes (need to be reapplied)
- Custom plugins (may need updates)
- Server configuration (new config file)

---

## Step-by-Step Migration

### Option 1: Easy Migration with Docker (Recommended)

**Best for**: Users comfortable with Docker, want easiest setup

#### Step 1: Install Docker

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

**Mac:**
Download Docker Desktop from https://www.docker.com/products/docker-desktop

**Windows:**
Download Docker Desktop from https://www.docker.com/products/docker-desktop

#### Step 2: Get GenewebPy

```bash
# Download GenewebPy
git clone https://github.com/Lob-Corp/Legacy.git genewebpy
cd genewebpy

# Or download ZIP from GitHub and extract
```

#### Step 3: Export Your Data from Old Geneweb

**If you have `.gw` files already:**
```bash
# Just copy them to GenewebPy
cp ~/geneweb/bases/yourbase/yourbase.gw genewebpy/examples/mydata.gw
```

**If you only have `.gwb` files:**
Start gwsetup and follow instructions to export your database into a gw file

#### Step 4: Build and Start GenewebPy

```bash
cd genewebpy

# Build Docker image
./docker-manage.sh build

# Start the application
./docker-manage.sh start

# Check it's running
# Open browser to http://localhost:8080
```

#### Step 5: Import Your Data

```bash
# Import your family data
./docker-manage.sh gwsetup database gwc mybase examples/mydata.gw

# Or with more control:
./docker-manage.sh gwc examples/mydata.gw -o data/mybase.db -v -stats
```

**Watch for**:
- Progress messages showing persons being imported
- Final statistics (number of persons, families)
- Any error messages (note them for troubleshooting)

#### Step 6: Access Your Family Tree

Open your browser to:
```
http://localhost:8080/gwd
```

You should see your family tree data!

### Option 2: Manual Installation

**Best for**: Users who want more control, no Docker

#### Step 1: Install Python

**Check if you have Python 3.12+:**
```bash
python3 --version
# Should show: Python 3.12.x or higher
```

**Install if needed:**
- Linux: `sudo apt-get install python3.12`
- Mac: `brew install python@3.12`
- Windows: Download from https://www.python.org/

#### Step 2: Install GenewebPy

```bash
# Download
git clone https://github.com/Lob-Corp/Legacy.git genewebpy
cd genewebpy

# Create virtual environment
python3.12 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 3: Export Your Data

Same as Option 1, Step 3 above.

#### Step 4: Import Your Data

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Import data
python -m gwsetup.gwsetup database gwc mybase examples/mydata.gw

# Or with gwc directly:
python -m script.gwc examples/mydata.gw -o bases/mybase.db -v -stats
```

#### Step 5: Start the Application

```bash
# Set environment variables
export FLASK_APP=src.wserver
export DATABASE_PATH=bases/mybase.db

# Start server
flask run --host=0.0.0.0 --port=8080
```

Access at: http://localhost:8080/gwd

---

## Verifying Your Data

### Visual Inspection

1. **Search for a person** you know well
2. **Check their details**:
   - ✅ Name spelled correctly?
   - ✅ Birth date correct?
   - ✅ Birth place correct?
   - ✅ Parents listed?
   - ✅ Spouse(s) listed?
   - ✅ Children listed?

3. **Check a few families**:
   - ✅ Marriage dates correct?
   - ✅ All children present?
   - ✅ Events (baptism, death, etc.) there?

### Database Count Check

Compare person counts between old and new:

**Old Geneweb:**
```bash
# Count persons (approximate)
grep -c "^- " ~/geneweb/bases/yourbase/yourbase.gw
```

**New GenewebPy:**
```bash
# Using Docker
./docker-manage.sh shell
sqlite3 /app/bases/mybase.db "SELECT COUNT(*) FROM person;"

# Or manual installation
sqlite3 bases/mybase.db "SELECT COUNT(*) FROM person;"
```

**Numbers should match!** Small differences (1-2) might be due to dummy persons.

### Automated Tests

If you're comfortable with command line:

```bash
# Run verification tests (Docker)
./docker-manage.sh test

# Or manual
pytest tests/gwc_database_roundtrip/ -v
```

### What to Check For

Common issues:
- ❌ Missing persons → Check export file completeness
- ❌ Wrong dates → Check date format in .gw file
- ❌ Missing relationships → Check family blocks in .gw file
- ❌ Special characters broken → Check file encoding (should be UTF-8)

---

## What's Different

### Interface Changes

**Good news**: The web interface is nearly identical!

**Slight differences**:
- URLs might be slightly different (save new bookmarks)
- Some admin functions in new locations
- Enhanced search capabilities

### Features Available

| Feature | OCaml Geneweb | GenewebPy |
|---------|---------------|-----------|
| Basic genealogy | ✅ | ✅ |
| Search persons | ✅ | ✅ |
| Family trees | ✅ | ✅ |
| Add/Edit persons | ✅ | 🚧 In progress |
| Events | ✅ | ✅ |
| Sources | ✅ | ✅ |
| Export GEDCOM | ✅ | 🚧 In progress |
| Statistics | ✅ | ✅ |
| Relationship calculator | ✅ | 🚧 In progress |

**Key**: ✅ = Available, 🚧 = Coming soon, ❌ = Not available

### Database Access

**Old way** (OCaml Geneweb):
- Binary `.gwb` files
- Proprietary format
- Required Geneweb tools to access

**New way** (GenewebPy):
- SQLite `.db` files
- Standard SQL format
- Can use any SQLite tool to query!

**Benefit**: You can now use standard database tools:
```bash
# Example: Export all persons to CSV
sqlite3 -header -csv bases/mybase.db \
  "SELECT first_name, surname, birth_date FROM person;" \
  > persons.csv
```

### Backup Strategy

**Old Geneweb**: Backup entire `bases/` directory

**GenewebPy**: Just backup `.db` files!
```bash
# Simple backup
cp bases/mybase.db bases/mybase_backup_$(date +%Y%m%d).db

# Or automated
./docker-manage.sh shell
sqlite3 /app/bases/mybase.db ".backup '/app/bases/backup.db'"
```

---

## Getting Help

### Documentation

- **This guide**: User migration basics
- **[DOCKER.md](DOCKER.md)**: Docker deployment details
- **[DATABASE.md](DATABASE.md)**: Database structure reference
- **[GWC_IMPLEMENTATION.md](GWC_IMPLEMENTATION.md)**: Data import tool details

### Common Issues

#### "Import failed: syntax error"

**Problem**: Your .gw file has formatting issues

**Solution**:
```bash
# Check for common issues
grep "? .* +" examples/mydata.gw

# This pattern is invalid (death date between ? and +)
# Fix by removing the ? or moving death date
```

#### "Wrong number of persons imported"

**Problem**: Some persons might be duplicates or missing

**Solution**:
1. Check export file: `grep -c "^- " mydata.gw`
2. Check database: `sqlite3 mybase.db "SELECT COUNT(*) FROM person;"`
3. Look for warnings in import logs: `./docker-manage.sh gwc ... 2>&1 | grep WARNING`

#### "Special characters are broken (é, ñ, etc.)"

**Problem**: File encoding issue

**Solution**:
```bash
# Check file encoding
file -i mydata.gw

# Should be: text/plain; charset=utf-8
# If not, convert:
iconv -f ISO-8859-1 -t UTF-8 mydata.gw > mydata_utf8.gw
```

#### "Can't access the website"

**Check**:
1. Is Docker/Flask running? `./docker-manage.sh logs`
2. Is port 8080 available? `lsof -i :8080`
3. Firewall blocking? `sudo ufw allow 8080`

### Getting Support

1. **Check documentation** first (you're here!)
2. **Search GitHub issues**: https://github.com/Lob-Corp/Legacy/issues
3. **Ask the community**: Geneweb forums and mailing lists
4. **Open an issue**: Provide:
   - What you tried
   - Error messages (full text)
   - Your setup (OS, Docker/manual, database size)
   - Relevant log files

---

## Frequently Asked Questions

### Can I run both old and new Geneweb at the same time?

**Yes!** They use different ports and databases. Keep old Geneweb running while testing the new one.

### What if I want to go back to old Geneweb?

**No problem!** Your original data is unchanged. Just switch back to using the old server.

### Will my URLs change?

**Slightly**. Bookmark structure might differ, but search and navigation work the same way.

### Can I use my old database format directly?

**No**, but export to `.gw` format is quick and preserves all data.

### How do I export my data from GenewebPy?

```bash
# Export to .gw format
python -m script.gwexport bases/mybase.db > myexport.gw

# Or use SQLite directly for custom exports
sqlite3 bases/mybase.db -header -csv \
  "SELECT * FROM person;" > persons.csv
```

**After migration**: Use database tools to merge SQLite databases (advanced)

### How do I update/maintain my data?

Same as before:
- Use the web interface to add/edit persons
- Or export to `.gw`, edit, re-import
- Or use SQL updates directly (advanced users)

### Will my custom theme/CSS work?

Custom styling needs to be reapplied. Copy your CSS to the new templates directory and reference it in the configuration.

### Performance comparison?

GenewebPy typically performs **similar or better** than OCaml Geneweb, especially for:
- Large databases (> 10,000 persons)
- Complex searches
- Database queries

---

## Next Steps

Once migrated:

1. **Explore the interface** - Familiarize yourself with any changes
2. **Update bookmarks** - Save new URLs for favorite pages
3. **Test functionality** - Try adding a test person, editing, searching
4. **Set up backups** - Automate regular database backups
5. **Share with family** - Let others know about the migration
6. **Provide feedback** - Report any issues or suggestions

### Recommended: Set Up Regular Backups

**Daily backup script** (Linux/Mac):
```bash
#!/bin/bash
# save as: ~/backup-geneweb.sh

DATE=$(date +%Y%m%d)
SOURCE=/path/to/genewebpy/bases/mybase.db
DEST=~/geneweb_backups/mybase_$DATE.db

mkdir -p ~/geneweb_backups
cp $SOURCE $DEST

# Keep only last 30 days
find ~/geneweb_backups -name "*.db" -mtime +30 -delete

echo "Backup completed: $DEST"
```

Make executable and add to cron:
```bash
chmod +x ~/backup-geneweb.sh
crontab -e
# Add line: 0 2 * * * /home/youruser/backup-geneweb.sh
```

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-10-31 | Initial user migration guide |

---

**Questions or need help?** Open an issue on GitHub or contact the community!

**Happy genealogy research! 🌳**

---

**End of User Migration Guide**
