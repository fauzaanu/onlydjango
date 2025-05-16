
```bash
sudo docker rm -f $(sudo docker ps -aq) && sudo docker compose -f dev_helpers/dev.docker-compose.yml up -d
```

```bash
uv run python manage.py migrate
```

```bash
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', '123')"
```

```bash
npx tailwindcss -i onlydjango/input.css -o Project/static/css/style.css
```