set -euo pipefail

coverage run -m --source=. pytest -v
coverage report -m
coverage html
