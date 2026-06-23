"""Unit tests for role_menu_permission service logic."""
import pytest
from unittest.mock import AsyncMock, patch

from app.modules.appadmin.service import (
    _build_permission_map,
    ValidationError,
)


def test_build_permission_map_groups_actions():
    rows = [
        {"role_id": "KEU", "menu_key": "finance.dashboard", "action": "view"},
        {"role_id": "KEU", "menu_key": "finance.dashboard", "action": "tambah"},
        {"role_id": "ADM", "menu_key": "finance.dashboard", "action": "view"},
    ]
    result = _build_permission_map(rows)
    assert set(result[("KEU", "finance.dashboard")]) == {"view", "tambah"}
    assert set(result[("ADM", "finance.dashboard")]) == {"view"}


def test_build_permission_map_empty():
    result = _build_permission_map([])
    assert result == {}
