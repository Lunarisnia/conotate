import os
import subprocess
import tempfile

SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "fetch_domain.py")

SAMPLE = """\
<!-- domain: src/auth -->
<!-- generated: 2026-04-05T00:00:00Z -->
<!-- commit: abc1234 -->

# src/auth: Knowledge Base

## src/auth: Overview
Auth overview content.

<!-- end:src/auth -->
"""


def _tmp(content):
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False)
    f.write(content)
    f.close()
    return f.name


def test_extracts_domain_block():
    path = _tmp(SAMPLE)
    result = subprocess.run(["python3", SCRIPT, "src/auth", path], capture_output=True, text=True)
    os.unlink(path)
    assert result.returncode == 0
    assert "<!-- domain: src/auth -->" in result.stdout
    assert "<!-- end:src/auth -->" in result.stdout
    assert "Auth overview content." in result.stdout


def test_missing_domain_exits_nonzero():
    path = _tmp(SAMPLE)
    result = subprocess.run(["python3", SCRIPT, "src/payments", path], capture_output=True, text=True)
    os.unlink(path)
    assert result.returncode != 0
    assert "not found" in result.stderr.lower()


def test_missing_closing_marker_exits_nonzero():
    broken = "<!-- domain: src/auth -->\nsome content\n"
    path = _tmp(broken)
    result = subprocess.run(["python3", SCRIPT, "src/auth", path], capture_output=True, text=True)
    os.unlink(path)
    assert result.returncode != 0
    assert "not found" in result.stderr.lower()


def test_missing_file_exits_nonzero():
    result = subprocess.run(
        ["python3", SCRIPT, "src/auth", "/nonexistent/path.md"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
