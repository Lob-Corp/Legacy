#!/bin/bash

set -e  # exit on error

show_usage() {
  echo "Usage: $0 {build|clean|run {gwsetup|gwd}}"
  exit 1
}

case "$1" in
  build)
    echo "🔨 Building project..."
    cd ./legacy
    ocaml ./configure.ml
    make clean distrib
    cd ..
    ;;

  clean)
    echo "🧹 Cleaning project..."
    cd ./legacy
    make clean
    cd ..
    ;;

  run)
    case "$2" in
      gwsetup)
        echo "🚀 Running GW Setup..."
        ./legacy/distribution/gwsetup.sh
        ;;
      gwd)
        echo "🚀 Running GWD..."
        ./legacy/distribution/gwd.sh
        ;;
      *)
        echo "❌ Invalid run option. Use 'gwsetup' or 'gwd'."
        show_usage
        ;;
    esac
    ;;

  *)
    echo "❌ Invalid option."
    show_usage
    ;;
esac
