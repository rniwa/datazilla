"""
Tests for management command to update pushlogs.

"""

from django.core.management import call_command
from datazilla.model.base import PushLogModel



def call_update_pushlog(*args, **kwargs):
    call_command("update_pushlog", *args, **kwargs)


def test_no_args(capsys):
    """Shows need for a repo_host."""
    call_update_pushlog()

    exp = (
        "You must supply a host name for the repo pushlogs to store: --repo_host hostname\n",
        "",
        )

    assert capsys.readouterr() == exp


def test_no_numdays(capsys):
    """Shows need for numdays."""


    call_update_pushlog(repo_host="foo_host")

    exp = (
        "You must supply the number of days data.\n",
        "",
        )

    assert capsys.readouterr() == exp


def test_bad_numdays(capsys):
    """Shows numdays must be int."""


    call_update_pushlog(repo_host="foo_host", numdays="rats")

    exp = (
        "numdays must be an integer.\n",
        "",
        )

    assert capsys.readouterr() == exp


def test_successful_store(plm, capsys, monkeypatch):
    """Successful storage of pushlog data."""

    def mock_store_pushlogs(nothing, repo_host, numdays, enddate, branch):
        return {
            "branches": 1,
            "pushlogs_stored": 3,
            "changesets_stored": 7,
            "pushlogs_skipped": 0,
            "changesets_skipped": 0,
            }
    monkeypatch.setattr(PushLogModel, "store_pushlogs", mock_store_pushlogs)

    call_update_pushlog(repo_host="foo_host", numdays="1", project=plm.project)

    exp = (
        ("Branches: 1\nPushlogs stored: 3, skipped: 0\n" +
         "Changesets stored: 7, skipped: 0\n"),
        "",
        )

    assert capsys.readouterr() == exp
