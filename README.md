# GenewebPy

GenewebPy is a reimplementation of Geneweb - originally written in OCaml - in Python.

## Requirement
The app has made with Python 3.12.11. Any version compatibility erro are on the user's responsability.

## 🐳 Docker Quick Start

Run the Flask application and use `gwc` in Docker:

```bash
# Optional: Configure environment variables
cp .env.example .env
# Edit .env to customize PORT, SSL, etc.

# Build and start the application
./docker-manage.sh build
./docker-manage.sh start

# Create database from .gw file using gwc
./docker-manage.sh gwc test_assets/minimal.gw -o data/minimal.db -v -stats

# Or use gwsetup for database management
./docker-manage.sh gwsetup database create mybase
./docker-manage.sh gwsetup database gwc mybase test_assets/minimal.gw
./docker-manage.sh gwsetup database delete mybase

# Access application at http://localhost:8080/gwd
```

**See [docs/DOCKER.md](docs/DOCKER.md) for complete Docker deployment guide.**

## 🚀 Ansible Deployment

Deploy to remote servers with Ansible:

```bash
cd ansible

# Configure your server in inventory.yml
# Then deploy:
ansible-playbook -i inventory.yml deploy.yml --limit production

# Or using Make
make deploy-prod
```

**See [docs/ANSIBLE.md](docs/ANSIBLE.md) for Ansible deployment guide.**

## Documentation

### 📘 Main Documentation
- **[GWC Implementation Guide](docs/GWC_IMPLEMENTATION.md)** - Complete guide to the Python `gwc` (GeneWeb Compiler) implementation
  - Architecture and processing pipeline
  - Command-line usage and options
  - Parser implementation and fixes
  - Dummy person system (OCaml-compatible)
  - Converter API reference with examples
  - Implementation status and roadmap

### 📚 Additional Documentation
- **[Documentation Index](docs/README.md)** - Complete documentation navigation guide
- **[Database Architecture](docs/DATABASE.md)** - Complete database documentation (SQLAlchemy models, relationships, and usage)
- **[Testing Policy](docs/TESTING_POLICY.md)** - Comprehensive testing guidelines, requirements, and best practices
- **[Quality Insurance](docs/QUALITY_INSURANCE.md)** - Branch organization, merging rules, and development workflow
- **[Golden Master Testing](docs/GOLDEN_MASTER.md)** - Testing approach and scenarios
- **[OCaml to Python Translation](docs/OCAML_TO_PYTHON.md)** - Reference for OCaml-to-Python differences

## Quick Start

### Creating a Database from .gw Files

The `gwc` (GeneWeb Compiler) tool converts GeneWeb `.gw` files into SQLite databases:

```bash
# Basic usage
python -m script.gwc -v -f -o family.db input.gw

# Multiple files
python -m script.gwc -v -f -o database.db file1.gw file2.gw file3.gw

# With statistics
python -m script.gwc -v -stats -f -o data.db genealogy.gw
```

**Options**:
- `-v`: Verbose output with progress
- `-f`: Force overwrite existing database
- `-o <file>`: Output database file
- `-stats`: Show compilation statistics
- `-nofail`: Continue on errors

**See**: [GWC Implementation Guide](docs/GWC_IMPLEMENTATION.md) for complete documentation.

### Database Management with gwsetup

The `gwsetup` CLI provides a convenient interface for managing GeneWeb databases:

```bash
# Create an empty database
python -m gwsetup.gwsetup database create mybase

# Create database from .gw file
python -m gwsetup.gwsetup database gwc mybase input.gw

# Delete a database
python -m gwsetup.gwsetup database delete mybase
```

**Docker usage**:
```bash
# Use gwsetup through docker-manage.sh
./docker-manage.sh gwsetup database create mybase
./docker-manage.sh gwsetup database gwc mybase test_assets/minimal.gw
./docker-manage.sh gwsetup database delete mybase
```

All databases are created in the `bases/` directory with a `.db` extension.

### Working with the Database

```python
from database.sqlite_database_service import SQLiteDatabaseService
from repositories.person_repository import PersonRepository

# Connect to database
db_service = SQLiteDatabaseService("family.db")
db_service.connect()

# Use repositories
person_repo = PersonRepository(db_service)
all_persons = person_repo.get_all_persons()

for person in all_persons:
    print(f"{person.first_name} {person.surname}")
```

**See**: [Database Architecture](docs/DATABASE.md) for complete database documentation.

## Quality Insurance

To see the documentation of branches organisation and tests, [see Quality Insurance](docs/QUALITY_INSURANCE.md)

