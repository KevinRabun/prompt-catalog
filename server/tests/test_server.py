"""Tests for the MCP server handlers."""

from __future__ import annotations

from pathlib import Path

import pytest
import importlib.util

# Only run if mcp package is available
HAS_MCP = importlib.util.find_spec("mcp") is not None


@pytest.mark.skipif(not HAS_MCP, reason="mcp package not installed")
class TestMCPServer:
    """Test MCP server resource and prompt handlers directly."""

    @pytest.fixture(autouse=True)
    def _setup_env(self, catalog_root: Path, monkeypatch):
        """Set CATALOG_ROOT before server module loads."""
        monkeypatch.setenv("CATALOG_ROOT", str(catalog_root))

    def test_server_module_imports(self) -> None:
        """Verify the server module can be imported without errors."""
        import importlib
        import prompt_catalog_mcp.server as srv
        importlib.reload(srv)
        assert hasattr(srv, "app")

    def test_catalog_loads_in_server(self, catalog_root: Path) -> None:
        """Verify the server's catalog loads the test fixtures."""
        import importlib
        import prompt_catalog_mcp.server as srv
        importlib.reload(srv)
        # Reset cached catalog so it reloads with test env
        srv._catalog = None
        catalog = srv._get_catalog()
        assert len(catalog.prompts) == 2
