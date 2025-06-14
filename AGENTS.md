1. Install docker ( curl -fsSL https://get.docker.com -o get-docker.sh | sh )
2. docker compose -f dev_helpers/dev.docker-compose.yml up -d
4. Install UV ( curl -LsSf https://astral.sh/uv/install.sh | sh )
5. Run `uv sync`
6. `uv run python manage.py migrate`
8. Instead of `python manage.py` always use `uv run python manage.py`
9. Instead of `python manage.py test` it should be `uv run python manage.py test`
