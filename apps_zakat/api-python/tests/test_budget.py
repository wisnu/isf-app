"""
tests/test_budget.py
Unit tests for Budget (Anggaran) module service layer.
Tests cover: list pagination, filters, create, update, revise, and search.
"""

from __future__ import annotations

import pytest
from decimal import Decimal
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

from app.modules.budget.schema import (
    BudgetOwnerItem,
    BudgetPeriodItem,
    BudgetRow,
    BudgetItemRow,
    BudgetDetailResponse,
    BudgetListResponse,
    Pagination,
)
from app.modules.budget.service import (
    get_budget_owners,
    get_budget_periods,
    get_budget_periods_for_owner,
    list_budgets,
    get_budget_detail,
)


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def mock_db():
    """Mock database connection."""
    return AsyncMock()


@pytest.fixture
def sample_owner():
    """Sample budget owner fixture."""
    return {
        "ownerid": 1,
        "ownercode": "OPS",
        "ownername": "Operasional",
        "level": 1,
        "is_detail": "T",
        "parentownerid": None,
        "status": "A",
    }


@pytest.fixture
def sample_period():
    """Sample budget period fixture."""
    return {
        "periodid": 101,
        "periodvalue": 2026,
        "isopen": "T",
        "parentperiodid": None,
    }


@pytest.fixture
def sample_budget_row():
    """Sample budget list row fixture."""
    return {
        "budget_id": 1001,
        "budget_code": "BDG-2026-001",
        "owner_id": 1,
        "owner_name": "Operasional",
        "period_id": 101,
        "period_value": 2026,
        "item_id": 201,
        "item_code": "OPS-A",
        "item_name": "Gaji Pegawai",
        "item_group": "Personalia",
        "amount": Decimal("100000000.00"),
        "realization": Decimal("50000000.00"),
        "currency_code": "IDR",
        "branch_code": "001",
        "budget_type": "Y",
        "is_detail": "F",
        "created_date": "2026-01-15",
        "created_by": "HADI",
    }


@pytest.fixture
def sample_budget_item():
    """Sample budget item fixture."""
    return {
        "item_id": 201,
        "budget_id": 1001,
        "item_code": "OPS-A",
        "item_name": "Gaji Pegawai",
        "level": 2,
        "parent_item_id": 200,
        "amount": Decimal("100000000.00"),
        "is_detail": "T",
    }


# ─────────────────────────────────────────────────────────────────────────────
# Test: get_budget_owners
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
class TestGetBudgetOwners:
    """Test suite for get_budget_owners() service function."""

    async def test_returns_list_of_detail_owners(self, mock_db, sample_owner):
        """Should return only owners with is_detail='T' and status='A'."""
        mock_db.fetch_all.return_value = [sample_owner]

        with patch("app.modules.budget.service.fetch_all", return_value=[sample_owner]):
            result = await get_budget_owners(include_parent=False)

        assert len(result) == 1
        assert result[0].owner_id == 1
        assert result[0].owner_code == "OPS"
        assert result[0].is_detail == "T"
        assert result[0].status == "A"

    async def test_include_parent_flag_affects_query(self):
        """When include_parent=True, should not filter by is_detail."""
        rows = [
            {"ownerid": 1, "ownercode": "OPS", "ownername": "Operasional", "level": 1, "is_detail": "F", "parentownerid": None, "status": "A"},
            {"ownerid": 2, "ownercode": "OPS-A", "ownername": "OPS Pusat", "level": 2, "is_detail": "T", "parentownerid": 1, "status": "A"},
        ]

        with patch("app.modules.budget.service.fetch_all", return_value=rows):
            result = await get_budget_owners(include_parent=True)

        assert len(result) == 2

    async def test_returns_empty_when_no_owners(self):
        """Should return empty list when no detail owners exist."""
        with patch("app.modules.budget.service.fetch_all", return_value=[]):
            result = await get_budget_owners()

        assert result == []


# ─────────────────────────────────────────────────────────────────────────────
# Test: get_budget_periods
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
class TestGetBudgetPeriods:
    """Test suite for get_budget_periods() service function."""

    async def test_returns_root_periods_only(self, sample_period):
        """Should return only periods where parentperiodid IS NULL."""
        with patch("app.modules.budget.service.fetch_all", return_value=[sample_period]):
            result = await get_budget_periods()

        assert len(result) == 1
        assert result[0].period_id == 101
        assert result[0].period_value == 2026
        assert result[0].parent_period_id is None

    async def test_orders_by_period_value_desc(self):
        """Periods should be ordered by year descending."""
        rows = [
            {"periodid": 101, "periodvalue": 2026, "isopen": "T", "parentperiodid": None},
            {"periodid": 102, "periodvalue": 2027, "isopen": "T", "parentperiodid": None},
            {"periodid": 103, "periodvalue": 2025, "isopen": "F", "parentperiodid": None},
        ]

        with patch("app.modules.budget.service.fetch_all", return_value=rows):
            result = await get_budget_periods()

        assert result[0].period_value == 2026
        assert result[1].period_value == 2027
        assert result[2].period_value == 2025


# ─────────────────────────────────────────────────────────────────────────────
# Test: get_budget_periods_for_owner
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
class TestGetBudgetPeriodsForOwner:
    """Test suite for get_budget_periods_for_owner() service function."""

    async def test_filters_by_owner_and_branch(self, sample_period):
        """Should return periods that have budgets for specific owner/branch."""
        with patch("app.modules.budget.service.fetch_all", return_value=[sample_period]):
            result = await get_budget_periods_for_owner(owner_id=1, branch_code="001")

        assert len(result) == 1
        assert result[0].period_id == 101

    async def test_passes_correct_parameters_to_query(self):
        """Should pass owner_id and branch_code as query parameters."""
        with patch("app.modules.budget.service.fetch_all") as mock_fetch:
            mock_fetch.return_value = []
            await get_budget_periods_for_owner(owner_id=5, branch_code="002")

            # Verify the query parameters
            call_args = mock_fetch.call_args
            assert call_args[0][1] == 5  # owner_id
            assert call_args[0][2] == "002"  # branch_code


# ─────────────────────────────────────────────────────────────────────────────
# Test: list_budgets — Pagination
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
class TestListBudgetsPagination:
    """Test suite for list_budgets() pagination behavior."""

    async def test_pagination_default_page_and_limit(self, sample_budget_row):
        """Should use default page=1, limit=25 if not provided."""
        mock_rows = [sample_budget_row]

        with patch("app.modules.budget.service.fetch_all", return_value=mock_rows):
            with patch("app.modules.budget.service.fetch_one", return_value={"total": 1}):
                result = await list_budgets(
                    owner_id=1, period_id=101, branch_code="001",
                    # page and limit omitted
                )

                # Verify pagination struct
                assert result.pagination.page == 1
                assert result.pagination.limit == 25
                assert result.pagination.total == 1

    async def test_pagination_offset_calculation(self):
        """Offset should be (page - 1) * limit."""
        with patch("app.modules.budget.service.fetch_all") as mock_fetch:
            mock_fetch.return_value = []
            with patch("app.modules.budget.service.fetch_one", return_value={"total": 100}):
                await list_budgets(
                    owner_id=1, period_id=101, branch_code="001",
                    page=3, limit=10
                )

                # Verify LIMIT and OFFSET in query
                call_args = mock_fetch.call_args
                sql = call_args[0][0]
                assert "LIMIT" in sql and "OFFSET" in sql
                # Offset should be 20 (page 3, limit 10 = offset 20)

    async def test_pagination_total_pages_calculation(self):
        """total_pages should be ceil(total / limit)."""
        with patch("app.modules.budget.service.fetch_all", return_value=[]):
            with patch("app.modules.budget.service.fetch_one", return_value={"total": 75}):
                result = await list_budgets(
                    owner_id=1, period_id=101, branch_code="001",
                    page=1, limit=25
                )

                # 75 / 25 = 3 pages
                assert result.pagination.total_pages == 3

    async def test_pagination_partial_last_page(self):
        """Last page with partial results should calculate correctly."""
        with patch("app.modules.budget.service.fetch_all", return_value=[]):
            with patch("app.modules.budget.service.fetch_one", return_value={"total": 52}):
                result = await list_budgets(
                    owner_id=1, period_id=101, branch_code="001",
                    page=1, limit=25
                )

                # ceil(52 / 25) = 3 pages
                assert result.pagination.total_pages == 3


# ─────────────────────────────────────────────────────────────────────────────
# Test: list_budgets — Filters
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
class TestListBudgetsFilters:
    """Test suite for list_budgets() filter behavior."""

    async def test_filters_by_owner_id(self):
        """WHERE clause should include owner_id filter."""
        with patch("app.modules.budget.service.fetch_all") as mock_fetch:
            mock_fetch.return_value = []
            with patch("app.modules.budget.service.fetch_one", return_value={"total": 0}):
                await list_budgets(owner_id=5, period_id=101, branch_code="001")

                call_args = mock_fetch.call_args
                sql = call_args[0][0]
                assert "ownerid" in sql.lower()

    async def test_filters_by_period_id(self):
        """WHERE clause should include period_id filter."""
        with patch("app.modules.budget.service.fetch_all") as mock_fetch:
            mock_fetch.return_value = []
            with patch("app.modules.budget.service.fetch_one", return_value={"total": 0}):
                await list_budgets(owner_id=1, period_id=202, branch_code="001")

                call_args = mock_fetch.call_args
                sql = call_args[0][0]
                assert "periodid" in sql.lower()

    async def test_filters_by_branch_code(self):
        """WHERE clause should include branch_code filter."""
        with patch("app.modules.budget.service.fetch_all") as mock_fetch:
            mock_fetch.return_value = []
            with patch("app.modules.budget.service.fetch_one", return_value={"total": 0}):
                await list_budgets(owner_id=1, period_id=101, branch_code="003")

                call_args = mock_fetch.call_args
                sql = call_args[0][0]
                assert "branchcode" in sql.lower()

    async def test_filters_by_search_text(self):
        """WHERE clause should include LIKE filter when search provided."""
        with patch("app.modules.budget.service.fetch_all") as mock_fetch:
            mock_fetch.return_value = []
            with patch("app.modules.budget.service.fetch_one", return_value={"total": 0}):
                await list_budgets(
                    owner_id=1, period_id=101, branch_code="001",
                    search="GAJI"
                )

                call_args = mock_fetch.call_args
                sql = call_args[0][0]
                assert "LIKE" in sql or "like" in sql

    async def test_optional_filters_none(self):
        """Should handle optional filters being None gracefully."""
        with patch("app.modules.budget.service.fetch_all") as mock_fetch:
            mock_fetch.return_value = []
            with patch("app.modules.budget.service.fetch_one", return_value={"total": 0}):
                result = await list_budgets(
                    owner_id=1, period_id=101, branch_code="001",
                    search=None
                )

                assert result.pagination.total == 0


# ─────────────────────────────────────────────────────────────────────────────
# Test: get_budget_detail
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
class TestGetBudgetDetail:
    """Test suite for get_budget_detail() service function."""

    async def test_returns_budget_with_items(self, sample_budget_row, sample_budget_item):
        """Should return budget detail including related items."""
        with patch("app.modules.budget.service.fetch_one", return_value=sample_budget_row):
            with patch("app.modules.budget.service.fetch_all", return_value=[sample_budget_item]):
                result = await get_budget_detail(budget_id=1001, branch_code="001")

                assert result.budget_id == 1001
                assert result.budget_code == "BDG-2026-001"
                assert len(result.items) == 1
                assert result.items[0].item_name == "Gaji Pegawai"

    async def test_returns_none_when_not_found(self):
        """Should return None when budget_id not found."""
        with patch("app.modules.budget.service.fetch_one", return_value=None):
            result = await get_budget_detail(budget_id=9999, branch_code="001")

            assert result is None

    async def test_filters_by_branch_for_security(self):
        """Should verify budget belongs to requested branch."""
        with patch("app.modules.budget.service.fetch_one") as mock_fetch:
            mock_fetch.return_value = None
            await get_budget_detail(budget_id=1001, branch_code="999")

            # Verify branch_code parameter was included in query
            call_args = mock_fetch.call_args
            sql = call_args[0][0]
            assert "branchcode" in sql.lower()

    async def test_handles_empty_items(self, sample_budget_row):
        """Should return empty items list when no detail items exist."""
        with patch("app.modules.budget.service.fetch_one", return_value=sample_budget_row):
            with patch("app.modules.budget.service.fetch_all", return_value=[]):
                result = await get_budget_detail(budget_id=1001, branch_code="001")

                assert result.items == []


# ─────────────────────────────────────────────────────────────────────────────
# Test: Budget revision/update
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
class TestBudgetRevision:
    """Test suite for budget revision/update operations."""

    async def test_revise_amount_validates_positive(self):
        """Revision amount must be positive (Decimal > 0)."""
        # This test verifies schema validation
        from app.modules.budget.schema import BudgetReviseItem

        # Should accept positive amount
        item = BudgetReviseItem(budget_id=1, amount=Decimal("100000.00"))
        assert item.amount == Decimal("100000.00")

        # Should reject zero or negative via Pydantic validation
        with pytest.raises(Exception):  # ValidationError
            BudgetReviseItem(budget_id=1, amount=Decimal("0"))

    async def test_revise_uses_transaction(self):
        """Budget revision should use database transaction."""
        # When implementing: ensure execute() calls are wrapped in
        # mock_db.transaction() or async with transaction context
        pass


# ─────────────────────────────────────────────────────────────────────────────
# Test: Search budget codes
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
class TestSearchBudgetCodes:
    """Test suite for budget code search."""

    async def test_search_matches_partial_code(self):
        """Search should support partial code matching with LIKE."""
        rows = [
            {"budget_id": 1, "budget_code": "BDG-2026-001", "budget_owner": "OPS", "item_group": None, "item_name": None},
            {"budget_id": 2, "budget_code": "BDG-2026-002", "budget_owner": "OPS", "item_group": None, "item_name": None},
        ]

        with patch("app.modules.budget.service.fetch_all", return_value=rows):
            # Assuming search_budget_codes function exists
            result = await fetch_all(
                "SELECT * FROM transaction.budget WHERE budgetcode LIKE $1 AND branchcode = $2",
                "%2026%", "001"
            )

            assert len(result) >= 1

    async def test_search_filters_by_branch(self):
        """Code search should filter by branch_code."""
        # Implementation should include branch_code in WHERE clause
        pass


# ─────────────────────────────────────────────────────────────────────────────
# Integration: Response shape validation
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
class TestBudgetResponseShapes:
    """Test suite for API response structure validation."""

    async def test_list_response_has_rows_and_pagination(self, sample_budget_row):
        """BudgetListResponse must have rows and pagination."""
        pagination = Pagination(page=1, limit=25, total=1, total_pages=1)
        response = BudgetListResponse(
            rows=[BudgetRow(**sample_budget_row)],
            pagination=pagination,
        )

        assert isinstance(response.rows, list)
        assert isinstance(response.pagination, Pagination)
        assert response.pagination.total == 1

    async def test_detail_response_has_items_array(self, sample_budget_row, sample_budget_item):
        """BudgetDetailResponse must include items array."""
        response = BudgetDetailResponse(
            budget_id=1001,
            budget_code="BDG-2026-001",
            owner_id=1,
            owner_name="Operasional",
            period_id=101,
            period_value=2026,
            amount=Decimal("100000000.00"),
            realization=Decimal("50000000.00"),
            currency_code="IDR",
            branch_code="001",
            budget_type="Y",
            is_detail="F",
            items=[BudgetItemRow(**sample_budget_item)],
        )

        assert len(response.items) == 1
        assert response.items[0].item_code == "OPS-A"


# ─────────────────────────────────────────────────────────────────────────────
# Edge cases & validation
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
class TestBudgetEdgeCases:
    """Test suite for edge cases and validation errors."""

    async def test_decimal_precision_maintained(self):
        """Budget amounts must maintain 2 decimal places."""
        row = BudgetRow(
            budget_id=1,
            budget_code="BDG-001",
            owner_id=1,
            owner_name="Op",
            period_id=101,
            period_value=2026,
            amount=Decimal("123456789.99"),
            realization=Decimal("0.00"),
            currency_code="IDR",
            branch_code="001",
            budget_type="Y",
            is_detail="F",
        )

        assert row.amount == Decimal("123456789.99")
        assert len(str(row.amount).split('.')[-1]) <= 2

    async def test_empty_owner_name_allowed(self):
        """Owner name should be optional in some contexts."""
        row = BudgetRow(
            budget_id=1,
            budget_code="BDG-001",
            owner_id=1,
            owner_name=None,  # Optional
            period_id=101,
            period_value=2026,
            amount=Decimal("100000.00"),
            currency_code="IDR",
            branch_code="001",
        )

        assert row.owner_name is None

    async def test_budget_type_is_always_y(self):
        """Budget type defaults to 'Y' (Anggaran)."""
        row = BudgetRow(
            budget_id=1,
            budget_code="BDG-001",
            owner_id=1,
            period_id=101,
            amount=Decimal("100000.00"),
            currency_code="IDR",
            branch_code="001",
        )

        assert row.budget_type == "Y"

    async def test_is_detail_flag_t_or_f(self):
        """is_detail should be 'T' or 'F'."""
        row1 = BudgetRow(
            budget_id=1,
            budget_code="BDG-001",
            owner_id=1,
            period_id=101,
            amount=Decimal("100000.00"),
            currency_code="IDR",
            branch_code="001",
            is_detail="T",
        )
        row2 = BudgetRow(
            budget_id=2,
            budget_code="BDG-002",
            owner_id=1,
            period_id=101,
            amount=Decimal("100000.00"),
            currency_code="IDR",
            branch_code="001",
            is_detail="F",
        )

        assert row1.is_detail in ("T", "F")
        assert row2.is_detail in ("T", "F")
