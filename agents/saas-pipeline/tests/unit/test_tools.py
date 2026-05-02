"""
Unit tests for pipeline_tools.py and github_tools.py.

These tests verify code correctness only — they do NOT assert LLM output content.
For agent behavior validation, use: agents-cli eval run
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class TestPipelineTools:
    """Tests for pipeline_tools.py subprocess wrappers."""

    def test_run_script_success(self, tmp_path: Path) -> None:
        """_run_script returns stdout on success."""
        from app.tools.pipeline_tools import _run_script

        # Use a trivial python -c command to avoid needing real scripts
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="hello", stderr="")
            result = _run_script(["some_script.py", "--arg", "val"])
        assert result == "hello"

    def test_run_script_failure(self) -> None:
        """_run_script raises RuntimeError on non-zero exit code."""
        from app.tools.pipeline_tools import _run_script

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="Something went wrong")
            with pytest.raises(RuntimeError, match="Script failed"):
                _run_script(["broken_script.py"])

    def test_validate_stage_returns_pass(self) -> None:
        """validate_stage returns the stripped stdout from agent_workflow.py."""
        from app.tools.pipeline_tools import validate_stage

        with patch("app.tools.pipeline_tools._run_script") as mock:
            mock.return_value = "PASS: brief\n"
            result = validate_stage("brief", "/tmp/my-project")
        assert result == "PASS: brief"


class TestGithubTools:
    """Tests for github_tools.py HTTP wrappers."""

    def test_post_github_issue_comment(self) -> None:
        """post_github_issue_comment returns the comment URL."""
        from app.tools.github_tools import post_github_issue_comment

        with patch("httpx.post") as mock_post:
            mock_resp = MagicMock()
            mock_resp.raise_for_status.return_value = None
            mock_resp.json.return_value = {"html_url": "https://github.com/org/repo/issues/1#comment-123"}
            mock_post.return_value = mock_resp

            result = post_github_issue_comment("org", "repo", 1, "Pipeline failed!")

        assert "github.com" in result
