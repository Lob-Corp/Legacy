# Docker Quick Reference

## Essential Commands

```bash
# Setup (first time only)
cp .env.example .env         # Copy environment config
# Edit .env as needed

# Build & Start
./docker-manage.sh build    # Build image
./docker-manage.sh start    # Start application

# Database Operations
./docker-manage.sh gwc input.gw -o data/output.db -v -stats
./docker-manage.sh gwsetup database create mybase
./docker-manage.sh gwsetup database gwc mybase input.gw

# Management
./docker-manage.sh stop     # Stop application
./docker-manage.sh restart  # Restart application
./docker-manage.sh logs -f  # Follow logs
./docker-manage.sh shell    # Open container shell

# Cleanup
./docker-manage.sh clean     # Remove containers
./docker-manage.sh clean-all # Remove everything including data
```

## Tool Options

### gwc (GeneWeb Compiler)
```bash
-o, --output FILE    # Output database path (required)
-v, --verbose        # Verbose output
-f, --force          # Force overwrite existing database
-stats               # Show statistics
-nofail              # Continue on errors
```

### gwsetup (Database Manager)
```bash
database create <name>        # Create empty database
database gwc <name> <file>    # Create database from .gw file
database delete <name>        # Delete database
```

## Common Workflows

### Create Database from .gw File

```bash
# Using gwc (manual path)
./docker-manage.sh gwc test_assets/minimal.gw -o data/test.db -v -stats

# Using gwsetup (automatic paths in bases/)
./docker-manage.sh gwsetup database gwc mybase test_assets/minimal.gw
```

### Update Existing Database

```bash
./docker-manage.sh gwc updated_data.gw -o data/test.db -f -v
```

### Manage Multiple Databases

```bash
# Create databases
./docker-manage.sh gwsetup database create family1
./docker-manage.sh gwsetup database create family2

# Populate databases
./docker-manage.sh gwsetup database gwc family1 data1.gw
./docker-manage.sh gwsetup database gwc family2 data2.gw

# Delete database
./docker-manage.sh gwsetup database delete family1
```

### Process Multiple Files

```bash
./docker-manage.sh shell
# Inside container:
python -m script.gwc file1.gw file2.gw -o /app/data/combined.db -v
```

### Access Database

```bash
./docker-manage.sh shell
sqlite3 /app/data/test.db
# SQL: SELECT * FROM person;
```

## Troubleshooting

```bash
# View logs
./docker-manage.sh logs --tail=100

# Check container status
docker-compose ps

# Rebuild from scratch
./docker-manage.sh stop
./docker-manage.sh clean
./docker-manage.sh build
./docker-manage.sh start

# Check disk usage
docker system df

# Remove unused images
docker image prune
```

## File Locations

| Purpose | Host Path | Container Path |
|---------|-----------|----------------|
| gwsetup databases | `./bases/` | `/app/bases/` |
| gwc databases | `./data/` | `/app/data/` |
| Logs | `./logs/` | `/app/logs/` |
| Input files | `./examples/` | `/app/examples/` |
| Test files | `./test_assets/` | `/app/test_assets/` |

## URLs

- Flask App: http://localhost:8080/gwd (or https if SSL enabled)
- Health Check: http://localhost:8080 (GET)

## Environment Configuration

The application reads configuration from `.env` file:

```bash
# Copy example and edit
cp .env.example .env

# Available variables:
DEBUG=false                          # Enable debug mode
HOST=0.0.0.0                        # Server host
PORT=8080                           # Server port
SSL_ENABLED=false                   # Enable HTTPS
SSL_CERT_PATH=certs/cert.pem       # SSL certificate path
SSL_KEY_PATH=certs/key.pem         # SSL key path
```

> Docker Compose automatically loads `.env` - no restart needed after editing.
