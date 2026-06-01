"""Tests for snapshot export/import with disabled-skills state."""
import json
from io import StringIO
from unittest.mock import patch, MagicMock

import pytest
from rich.console import Console

from hermes_cli.skills_hub import do_snapshot_export, do_snapshot_import


class _DummyLockFile:
    def __init__(self, installed=None):
        self._installed = installed or []

    def list_installed(self):
        return self._installed


class _DummyTapsManager:
    def __init__(self, taps=None):
        self._taps = taps or []

    def list_taps(self):
        return self._taps

    def add(self, repo, path="skills/"):
        self._taps.append({"repo": repo, "path": path})


def _console() -> tuple[Console, StringIO]:
    sink = StringIO()
    return Console(file=sink, force_terminal=False, color_system=None), sink


# ---------------------------------------------------------------------------
# do_snapshot_export
# ---------------------------------------------------------------------------

class TestSnapshotExport:
    def _run_export(self, tmp_path, monkeypatch, installed=None, taps=None,
                    disabled=None, platform_disabled=None):
        import tools.skills_hub as hub

        config = {"skills": {}}
        if disabled is not None:
            config["skills"]["disabled"] = disabled
        if platform_disabled:
            config["skills"]["platform_disabled"] = platform_disabled

        monkeypatch.setattr(hub, "HubLockFile", lambda: _DummyLockFile(installed or []))
        monkeypatch.setattr(hub, "TapsManager", lambda: _DummyTapsManager(taps or []))

        with patch("hermes_cli.config.load_config", return_value=config):
            out_path = tmp_path / "snapshot.json"
            c, sink = _console()
            do_snapshot_export(str(out_path), console=c)

        return json.loads(out_path.read_text())

    def test_snapshot_includes_disabled_skills(self, tmp_path, monkeypatch):
        snapshot = self._run_export(
            tmp_path, monkeypatch,
            disabled=["skill-a", "skill-b"],
        )
        assert snapshot["disabled_skills"] == ["skill-a", "skill-b"]

    def test_snapshot_empty_disabled_is_empty_list(self, tmp_path, monkeypatch):
        snapshot = self._run_export(tmp_path, monkeypatch, disabled=[])
        assert snapshot["disabled_skills"] == []

    def test_snapshot_no_disabled_key_is_empty_list(self, tmp_path, monkeypatch):
        snapshot = self._run_export(tmp_path, monkeypatch)
        assert snapshot["disabled_skills"] == []

    def test_snapshot_includes_platform_disabled(self, tmp_path, monkeypatch):
        snapshot = self._run_export(
            tmp_path, monkeypatch,
            platform_disabled={"telegram": ["tg-skill"]},
        )
        assert snapshot["platform_disabled_skills"]["telegram"] == ["tg-skill"]

    def test_snapshot_only_includes_configured_platforms(self, tmp_path, monkeypatch):
        snapshot = self._run_export(
            tmp_path, monkeypatch,
            platform_disabled={"telegram": ["tg-skill"]},
        )
        assert "cli" not in snapshot["platform_disabled_skills"]

    def test_snapshot_includes_installed_skills(self, tmp_path, monkeypatch):
        installed = [{"name": "my-skill", "source": "github",
                      "identifier": "github/owner/my-skill", "install_path": "coding/my-skill"}]
        snapshot = self._run_export(tmp_path, monkeypatch, installed=installed)
        assert snapshot["skills"][0]["name"] == "my-skill"
        assert snapshot["skills"][0]["identifier"] == "github/owner/my-skill"

    def test_snapshot_disabled_sorted(self, tmp_path, monkeypatch):
        snapshot = self._run_export(
            tmp_path, monkeypatch,
            disabled=["zzz", "aaa", "mmm"],
        )
        assert snapshot["disabled_skills"] == ["aaa", "mmm", "zzz"]

    def test_snapshot_stdout_output(self, tmp_path, monkeypatch):
        import tools.skills_hub as hub

        config = {"skills": {"disabled": ["skill-x"]}}
        monkeypatch.setattr(hub, "HubLockFile", lambda: _DummyLockFile())
        monkeypatch.setattr(hub, "TapsManager", lambda: _DummyTapsManager())

        import sys
        from io import StringIO as _SIO
        captured = _SIO()

        with patch("hermes_cli.config.load_config", return_value=config), \
             patch.object(sys, "stdout", captured):
            do_snapshot_export("-")

        data = json.loads(captured.getvalue())
        assert data["disabled_skills"] == ["skill-x"]


# ---------------------------------------------------------------------------
# do_snapshot_import
# ---------------------------------------------------------------------------

class TestSnapshotImport:
    def _write_snapshot(self, tmp_path, snapshot: dict) -> str:
        p = tmp_path / "snap.json"
        p.write_text(json.dumps(snapshot))
        return str(p)

    def test_import_restores_global_disabled(self, tmp_path, monkeypatch):
        import tools.skills_hub as hub
        import hermes_cli.skills_hub as cli_hub

        monkeypatch.setattr(hub, "TapsManager", lambda: _DummyTapsManager())
        monkeypatch.setattr(cli_hub, "do_install", lambda *a, **kw: None)

        config = {}
        saved_calls = []

        def fake_save(cfg, disabled, platform=None):
            saved_calls.append((set(disabled), platform))

        snap_path = self._write_snapshot(tmp_path, {
            "skills": [],
            "taps": [],
            "disabled_skills": ["skill-a", "skill-b"],
            "platform_disabled_skills": {},
        })

        with patch("hermes_cli.config.load_config", return_value=config), \
             patch("hermes_cli.skills_config.save_disabled_skills", side_effect=fake_save):
            c, _ = _console()
            do_snapshot_import(snap_path, console=c)

        assert ({"skill-a", "skill-b"}, None) in saved_calls

    def test_import_restores_platform_disabled(self, tmp_path, monkeypatch):
        import tools.skills_hub as hub
        import hermes_cli.skills_hub as cli_hub

        monkeypatch.setattr(hub, "TapsManager", lambda: _DummyTapsManager())
        monkeypatch.setattr(cli_hub, "do_install", lambda *a, **kw: None)

        saved_calls = []

        def fake_save(cfg, disabled, platform=None):
            saved_calls.append((set(disabled), platform))

        snap_path = self._write_snapshot(tmp_path, {
            "skills": [],
            "taps": [],
            "disabled_skills": [],
            "platform_disabled_skills": {"telegram": ["tg-skill"]},
        })

        with patch("hermes_cli.config.load_config", return_value={}), \
             patch("hermes_cli.skills_config.save_disabled_skills", side_effect=fake_save):
            c, _ = _console()
            do_snapshot_import(snap_path, console=c)

        assert ({"tg-skill"}, "telegram") in saved_calls

    def test_import_skips_disabled_restore_when_absent(self, tmp_path, monkeypatch):
        import tools.skills_hub as hub
        import hermes_cli.skills_hub as cli_hub

        monkeypatch.setattr(hub, "TapsManager", lambda: _DummyTapsManager())
        monkeypatch.setattr(cli_hub, "do_install", lambda *a, **kw: None)

        snap_path = self._write_snapshot(tmp_path, {"skills": [], "taps": []})

        saved_calls = []
        with patch("hermes_cli.config.load_config", return_value={}), \
             patch("hermes_cli.skills_config.save_disabled_skills",
                   side_effect=lambda *a, **kw: saved_calls.append(1)):
            c, _ = _console()
            do_snapshot_import(snap_path, console=c)

        assert saved_calls == []

    def test_import_reinstalls_hub_skills(self, tmp_path, monkeypatch):
        import tools.skills_hub as hub
        import hermes_cli.skills_hub as cli_hub

        monkeypatch.setattr(hub, "TapsManager", lambda: _DummyTapsManager())

        installed = []
        monkeypatch.setattr(cli_hub, "do_install",
                            lambda identifier, category="", force=False, console=None:
                            installed.append(identifier))

        snap_path = self._write_snapshot(tmp_path, {
            "skills": [{"name": "my-skill", "identifier": "github/owner/my-skill",
                        "category": "coding", "source": "github"}],
            "taps": [],
        })

        with patch("hermes_cli.config.load_config", return_value={}), \
             patch("hermes_cli.skills_config.save_disabled_skills"):
            c, _ = _console()
            do_snapshot_import(snap_path, console=c)

        assert "github/owner/my-skill" in installed

    def test_import_file_not_found(self, tmp_path):
        c, sink = _console()
        do_snapshot_import(str(tmp_path / "missing.json"), console=c)
        assert "File not found" in sink.getvalue()

    def test_import_invalid_json(self, tmp_path):
        bad = tmp_path / "bad.json"
        bad.write_text("{not valid json}")
        c, sink = _console()
        do_snapshot_import(str(bad), console=c)
        assert "Invalid JSON" in sink.getvalue()

    def test_import_complete_message(self, tmp_path, monkeypatch):
        import tools.skills_hub as hub
        import hermes_cli.skills_hub as cli_hub

        monkeypatch.setattr(hub, "TapsManager", lambda: _DummyTapsManager())
        monkeypatch.setattr(cli_hub, "do_install", lambda *a, **kw: None)

        snap_path = self._write_snapshot(tmp_path, {"skills": [], "taps": []})

        with patch("hermes_cli.config.load_config", return_value={}), \
             patch("hermes_cli.skills_config.save_disabled_skills"):
            c, sink = _console()
            do_snapshot_import(snap_path, console=c)

        assert "import complete" in sink.getvalue().lower()
