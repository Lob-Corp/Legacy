import os
from pathlib import Path

import pytest
from click.testing import CliRunner

from gwsetup import gwsetup


def test_create_database_invalid_name_empty():
    ok, msg = gwsetup.create_database("")
    assert not ok
    assert "required" in msg.lower()


def test_create_database_invalid_chars():
    ok, msg = gwsetup.create_database("bad name!")
    assert not ok
    assert "invalid database name" in msg.lower()


def test_cli_create_creates_file(tmp_path, monkeypatch):
    # run the real CLI and real SQLiteDatabaseService in an isolated cwd
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    result = runner.invoke(gwsetup.cli, ["database", "create", "mydb"])
    # CLI should exit with code 0 and create the file
    assert result.exit_code == 0, result.output
    assert Path(os.path.join(
        tmp_path, gwsetup.DEFAULT_BASES_DIR, "mydb.db")).exists()
    assert "created database" in result.output.lower()


def test_cli_delete_removes_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    p = Path(os.path.join(tmp_path, gwsetup.DEFAULT_BASES_DIR, "toremove.db"))
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("")

    runner = CliRunner()
    result = runner.invoke(gwsetup.cli, ["database", "delete", "toremove"])
    assert result.exit_code == 0, result.output
    assert not p.exists()
    assert "deleted database" in result.output.lower()


def test_cli_delete_nonexistent(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(gwsetup.cli, ["database", "delete", "nope"])
    # expected non-zero exit code for failure
    assert result.exit_code != 0
    assert "does not exist" in result.output.lower()
