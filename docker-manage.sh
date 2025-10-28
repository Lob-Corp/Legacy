#!/bin/bash
# Docker helper script for managing GeneWeb application

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_usage() {
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  build              Build the Docker image"
    echo "  start              Start the application"
    echo "  stop               Stop the application"
    echo "  restart            Restart the application"
    echo "  logs               Show application logs"
    echo "  shell              Open a shell in the container"
    echo "  gwc <args>         Run gwc command (e.g., gwc input.gw -o data/output.db)"
    echo "  test               Run tests inside container"
    echo "  clean              Stop and remove containers, networks"
    echo "  clean-all          Clean everything including volumes"
    echo ""
    echo "Examples:"
    echo "  $0 build                                  # Build the image"
    echo "  $0 start                                  # Start the app"
    echo "  $0 gwc examples/test.gw -o data/test.db   # Create database from .gw file"
    echo "  $0 gwc test_assets/minimal.gw -o data/minimal.db -v -stats"
    echo "  $0 logs -f                                # Follow logs"
    echo "  $0 shell                                  # Access container shell"
}

ensure_dirs() {
    mkdir -p data logs
}

build_image() {
    echo -e "${GREEN}Building Docker image...${NC}"
    docker-compose build
    echo -e "${GREEN}Build complete!${NC}"
}

start_app() {
    ensure_dirs
    echo -e "${GREEN}Starting GeneWeb application...${NC}"
    docker-compose up -d
    echo -e "${GREEN}Application started on https://localhost:8080${NC}"
    echo -e "${YELLOW}Use '$0 logs -f' to follow logs${NC}"
}

stop_app() {
    echo -e "${YELLOW}Stopping GeneWeb application...${NC}"
    docker-compose down
    echo -e "${GREEN}Application stopped${NC}"
}

restart_app() {
    echo -e "${YELLOW}Restarting GeneWeb application...${NC}"
    docker-compose restart
    echo -e "${GREEN}Application restarted${NC}"
}

show_logs() {
    docker-compose logs "$@"
}

open_shell() {
    echo -e "${GREEN}Opening shell in container...${NC}"
    docker-compose exec geneweb /bin/bash
}

run_gwc() {
    ensure_dirs
    echo -e "${GREEN}Running gwc with arguments: $@${NC}"

    if ! docker-compose ps | grep -q "geneweb-app.*Up"; then
        echo -e "${YELLOW}Container not running. Starting it first...${NC}"
        docker-compose up -d
        sleep 2
    fi

    docker-compose exec geneweb python -m script.gwc "$@"
}

run_tests() {
    echo -e "${GREEN}Running tests inside container...${NC}"
    docker-compose exec geneweb pytest tests/
}

clean() {
    echo -e "${YELLOW}Cleaning up containers and networks...${NC}"
    docker-compose down
    echo -e "${GREEN}Cleanup complete${NC}"
}

clean_all() {
    echo -e "${RED}Cleaning up everything (including volumes)...${NC}"
    read -p "This will delete all data volumes. Continue? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose down -v
        echo -e "${GREEN}Complete cleanup done${NC}"
    else
        echo -e "${YELLOW}Cleanup cancelled${NC}"
    fi
}

# Main command dispatcher
case "${1:-}" in
    build)
        build_image
    ;;
    start)
        start_app
    ;;
    stop)
        stop_app
    ;;
    restart)
        restart_app
    ;;
    logs)
        shift
        show_logs "$@"
    ;;
    shell)
        open_shell
    ;;
    gwc)
        shift
        run_gwc "$@"
    ;;
    test)
        run_tests
    ;;
    clean)
        clean
    ;;
    clean-all)
        clean_all
    ;;
    help|--help|-h)
        print_usage
    ;;
    *)
        echo -e "${RED}Unknown command: ${1:-}${NC}"
        echo ""
        print_usage
        exit 1
    ;;
esac
