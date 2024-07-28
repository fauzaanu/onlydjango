from django.db.backends.signals import connection_created
from django.dispatch import receiver


# @receiver(connection_created)
# def apply_pragma_on_connection(sender, connection, **kwargs):
#     """
#     sqlite3 optimization, Django 5.1 however allows this to be set in settings.py
#     """
#     if connection.vendor == "sqlite":
#         with connection.cursor() as cursor:
#             cursor.execute("PRAGMA journal_mode=WAL;")

    # https://blog.pecar.me/django-sqlite-benchmark
    # Django 5.1 made it possible (PR, Ticket#24018) to configure PRAGMA commands when a new connection is established with the init_command option. You can use this to enable WAL mode in the settings file:
    # DATABASES = {
    #     "default": {
    #         "ENGINE": "django.db.backends.sqlite3",
    #         "NAME": BASE_DIR / "db.sqlite3",
    #         "OPTIONS": {
    #             "init_command": "PRAGMA journal_mode=WAL;",  # <- Only works in Django 5.1+
    #         },
    #     }
    # }
