from django.db.backends.sqlite3.base import DatabaseWrapper as SQLiteDatabaseWrapper


class DatabaseWrapper(SQLiteDatabaseWrapper):
    def create_cursor(self, name=None):
        cursor = super().create_cursor(name)
        self._set_pragma(cursor)
        return cursor

    def _set_pragma(self, cursor):
        cursor.execute("PRAGMA journal_mode=DELETE;")
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("PRAGMA synchronous = FULL;")
