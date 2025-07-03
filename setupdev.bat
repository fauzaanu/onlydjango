for /f %%i in ('docker ps -q') do docker rm -f %%i
docker compose -f dev_helpers/dev.docker-compose.yml up -d
uv run python manage.py makemigrations
uv run python manage.py migrate
