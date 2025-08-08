from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import SimpleTestCase


class CollectStaticIfNeededTests(SimpleTestCase):
    def test_runs_when_static_changed(self):
        with patch(
            "onlydjango.management.commands.collectstatic_if_needed.call_command"
        ) as mock_call:
            with patch(
                "onlydjango.management.commands.collectstatic_if_needed.Command._get_changed_files",
                return_value=["onlydjango/static/js/app.js"],
            ):
                call_command("collectstatic_if_needed", stdout=StringIO())
                mock_call.assert_called_once_with("collectstatic", "--noinput")

    def test_skips_when_no_static_changes(self):
        with patch(
            "onlydjango.management.commands.collectstatic_if_needed.call_command"
        ) as mock_call:
            with patch(
                "onlydjango.management.commands.collectstatic_if_needed.Command._get_changed_files",
                return_value=["README.md"],
            ):
                call_command("collectstatic_if_needed", stdout=StringIO())
                mock_call.assert_not_called()

    def test_force_flag_runs(self):
        with patch(
            "onlydjango.management.commands.collectstatic_if_needed.call_command"
        ) as mock_call:
            with patch(
                "onlydjango.management.commands.collectstatic_if_needed.Command._get_changed_files",
                return_value=["README.md"],
            ):
                call_command("collectstatic_if_needed", "--force", stdout=StringIO())
                mock_call.assert_called_once_with("collectstatic", "--noinput")
