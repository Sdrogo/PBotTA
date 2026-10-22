import pytest

from pbotta.bot import command_name


def test_default_command_name(monkeypatch):
    monkeypatch.delenv("COMMAND_NAME", raising=False)
    assert command_name() == "pbta"


def test_custom_command_name(monkeypatch):
    monkeypatch.setenv("COMMAND_NAME", "cuori")
    assert command_name() == "cuori"


@pytest.mark.parametrize("bad", ["Roll", "con spazio", "x" * 33])
def test_invalid_command_name(monkeypatch, bad):
    monkeypatch.setenv("COMMAND_NAME", bad)
    with pytest.raises(SystemExit):
        command_name()
