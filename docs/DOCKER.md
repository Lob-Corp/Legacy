# Docker Deployment Guide

This guide explains how to run the GeneWeb Flask application and use `gwc` for database management in Docker.

## Quick Start

### 1. Configure Environment (Optional)

Copy the example environment file and customize if needed:

```bash
cp .env.example .env
# Edit .env to customize settings (DEBUG, PORT, SSL, etc.)
```

The application will use `.env` for configuration. If not present, defaults will be used.

### 2. Build the Docker Image

```bash
./docker-manage.sh build
```

Or manually:

```bash
docker-compose build
```

### 3. Start the Application

```bash
./docker-manage.sh start
```

The Flask application will be available at: **http://localhost:8080**
(or **https://localhost:8080** if SSL is enabled in `.env`)

### 4. Use gwc to Create/Update Database

```bash
# Create database from a .gw file
./docker-manage.sh gwc examples/test.gw -o data/test.db -v -stats

# Process minimal test file
./docker-manage.sh gwc test_assets/minimal.gw -o data/minimal.db -f

# Process with verbose output
./docker-manage.sh gwc test_assets/medium.gw -o data/medium.db -v -stats
```

## Docker Management Commands

### Application Management

```bash
# Start the application
./docker-manage.sh start

# Stop the application
./docker-manage.sh stop

# Restart the application
./docker-manage.sh restart

# View logs (follow mode)
./docker-manage.sh logs -f

# View last 100 lines
./docker-manage.sh logs --tail=100
```

### Database Operations with gwc

The `gwc` command processes `.gw` genealogy files and creates SQLite databases.

```bash
# Basic usage
./docker-manage.sh gwc <input.gw> -o <output.db>

# With verbose output and statistics
./docker-manage.sh gwc input.gw -o data/output.db -v -stats

# Force overwrite existing database
./docker-manage.sh gwc input.gw -o data/output.db -f

# Continue on errors
./docker-manage.sh gwc input.gw -o data/output.db -nofail
```

**gwc Options:**
- `-o, --output`: Output database path (required)
- `-v, --verbose`: Enable verbose output
- `-f, --force`: Force overwrite existing database
- `-stats`: Show statistics after processing
- `-nofail`: Continue processing on errors

### Development

```bash
# Open shell in the container
./docker-manage.sh shell

# Run tests
./docker-manage.sh test

# Inside the container shell, you can:
# - Run gwc: python -m script.gwc input.gw -o output.db
# - Run tests: pytest tests/
# - Access Python REPL: python
```

### Cleanup

```bash
# Stop and remove containers
./docker-manage.sh clean

# Remove everything including data volumes
./docker-manage.sh clean-all
```

## Directory Structure

```
.
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── docker-manage.sh        # Helper script for Docker operations
├── .dockerignore           # Files to exclude from Docker image
├── data/                   # Database files (persisted)
│   └── *.db                # SQLite databases created by gwc
├── logs/                   # Application logs (persisted)
├── examples/               # Example .gw files (mounted read-only)
└── test_assets/            # Test .gw files (mounted read-only)
```

## Volume Mounts

The Docker setup uses several volume mounts for data persistence and access:

| Host Path | Container Path | Purpose | Mode |
|-----------|----------------|---------|------|
| `./data` | `/app/data` | Database storage | Read-Write |
| `./logs` | `/app/logs` | Application logs | Read-Write |
| `./examples` | `/app/examples` | Example .gw files | Read-Only |
| `./test_assets` | `/app/test_assets` | Test .gw files | Read-Only |
| `./certs` | `/app/certs` | SSL certificates | Read-Only |

## Environment Variables

The application uses a `.env` file for configuration. Docker Compose automatically loads this file.

### Setup

1. **Copy the example configuration:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your settings:**
   ```bash
   # Flask Application Configuration
   DEBUG=false
   HOST=0.0.0.0
   PORT=8080
   
   # SSL Configuration
   SSL_ENABLED=false
   SSL_CERT_PATH=certs/cert.pem
   SSL_KEY_PATH=certs/key.pem
   ```

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `false` | Enable Flask debug mode |
| `HOST` | `0.0.0.0` | Flask server host (use `0.0.0.0` in Docker) |
| `PORT` | `8080` | Flask server port |
| `SSL_ENABLED` | `false` | Enable SSL/HTTPS |
| `SSL_CERT_PATH` | `certs/cert.pem` | Path to SSL certificate |
| `SSL_KEY_PATH` | `certs/key.pem` | Path to SSL private key |

### Using `.env` File

The `.env` file is automatically loaded by Docker Compose. Values defined in `.env` override the defaults in `docker-compose.yml`.

**Example `.env` for development:**
```bash
DEBUG=true
HOST=0.0.0.0
PORT=8080
SSL_ENABLED=false
```

**Example `.env` for production with SSL:**
```bash
DEBUG=false
HOST=0.0.0.0
PORT=8080
SSL_ENABLED=true
SSL_CERT_PATH=certs/cert.pem
SSL_KEY_PATH=certs/key.pem
```

> **Important Notes:**
> - Place your SSL certificate and key files in the `certs/` directory before enabling SSL
> - Use `HOST=0.0.0.0` in Docker to allow external connections (required)
> - Use `HOST=127.0.0.1` for local development outside Docker
> - The `.env` file is loaded automatically by Docker Compose - just restart: `./docker-manage.sh restart`

## Complete Workflow Example

### 1. Setup Environment (First Time)

```bash
# Copy example configuration
cp .env.example .env

# Edit if needed (optional - defaults work fine)
# nano .env
```

### 2. Build and Start

```bash
# Build the image
./docker-manage.sh build

# Start the application
./docker-manage.sh start
```

### 2. Create Database from .gw File

```bash
# Process a minimal genealogy file
./docker-manage.sh gwc test_assets/minimal.gw -o data/minimal.db -v -stats

# Expected output:
# Parsing file: test_assets/minimal.gw
# Found 2 persons, 1 families
# Creating database: data/minimal.db
# Saving 2 persons...
# Saving 1 families...
# Database created successfully!
```

### 3. Verify Database

```bash
# Open shell
./docker-manage.sh shell

# Inside container
sqlite3 /app/data/minimal.db

# SQL queries
SELECT COUNT(*) FROM person;
SELECT first_name, surname FROM person;
```

### 4. Access Flask Application

Open browser to **http://localhost:8080**

The Flask app can now query the SQLite database created by gwc.

### 5. Monitor Logs

```bash
# Follow logs in real-time
./docker-manage.sh logs -f

# View recent logs
./docker-manage.sh logs --tail=50
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
./docker-manage.sh logs

# Check container status
docker-compose ps

# Restart
./docker-manage.sh restart
```

### Permission Issues

```bash
# Ensure directories exist with proper permissions
mkdir -p data logs
chmod 755 data logs
```

### Database File Not Found

```bash
# Check if database was created
ls -la data/

# Verify mount points
docker-compose exec geneweb ls -la /app/data/
```

### gwc Command Fails

```bash
# Run gwc directly in container
docker-compose exec geneweb python -m script.gwc --help

# Check if input file is accessible
docker-compose exec geneweb ls -la /app/test_assets/
```

## Production Deployment

For production deployment, consider:

1. **Use environment-specific configuration:**
   ```bash
   cp docker-compose.yml docker-compose.prod.yml
   # Edit docker-compose.prod.yml
   docker-compose -f docker-compose.prod.yml up -d
   ```

2. **Enable SSL:**
   ```yaml
   environment:
     - SSL_ENABLED=true
     - SSL_CERT_PATH=/app/certs/cert.pem
     - SSL_KEY_PATH=/app/certs/key.pem
   volumes:
     - ./certs:/app/certs:ro
   ```

3. **Use a reverse proxy (nginx, traefik):**
   - Add nginx service to docker-compose.yml
   - Configure SSL termination at proxy level
   - Implement rate limiting and security headers

4. **Backup databases regularly:**
   ```bash
   # Backup script
   docker-compose exec geneweb sqlite3 /app/data/geneweb.db ".backup '/app/data/backup_$(date +%Y%m%d).db'"
   ```

5. **Monitor application:**
   - Use the built-in health check
   - Implement logging aggregation
   - Set up alerting

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Build and Test Docker Image

on: [push, pull_request]

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker-compose build
      
      - name: Start services
        run: docker-compose up -d
      
      - name: Wait for service
        run: sleep 10
      
      - name: Test gwc
        run: ./docker-manage.sh gwc test_assets/minimal.gw -o data/test.db -v
      
      - name: Run tests
        run: ./docker-manage.sh test
      
      - name: Stop services
        run: docker-compose down
```

## Advanced Usage

### Custom Python Commands

```bash
# Run any Python command in the container
docker-compose exec geneweb python -c "from database.sqlite_database_service import SQLiteDatabaseService; print('OK')"

# Run custom scripts
docker-compose exec geneweb python /app/tools/your_script.py
```

### Database Migrations

```bash
# Access database directly
docker-compose exec geneweb sqlite3 /app/data/geneweb.db

# Export database to SQL
docker-compose exec geneweb sqlite3 /app/data/geneweb.db .dump > backup.sql

# Import database from SQL
cat backup.sql | docker-compose exec -T geneweb sqlite3 /app/data/restored.db
```

## Support

For issues and questions:
- Check logs: `./docker-manage.sh logs`
- Review documentation in `docs/`
- Open an issue on GitHub
