#!/usr/bin/env bash
set -euo pipefail

find . -type d -name "__pycache__" -prune -exec rm -rf {} +
find . -type f \( -name "*.pyc" -o -name "*.pyo" -o -name "*.pyd" \) -delete
find . -type d \( -name ".pytest_cache" -o -name ".mypy_cache" -o -name ".ruff_cache" \) -prune -exec rm -rf {} +

echo "Development artifacts removed."
