#!/bin/bash
cd /app/
# Lint and Autoformat the code in place
# Remove unused imports
autoflake --in-place --remove-all-unused-imports --ignore-init-module-imports -r ./scar_sim
# Perform all other steps
black --config pyproject.toml ./scar_sim
black --config pyproject.toml ./test
