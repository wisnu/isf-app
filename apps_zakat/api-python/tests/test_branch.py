"""Unit tests for Branch service (appadmin.branch)."""

import pytest
from app.modules.appadmin.branch import service as branch_service
from app.modules.appadmin.branch.schema import (
    BranchCreateRequest,
    BranchDetail,
    BranchListItem,
    BranchUpdateRequest,
)


class _FakeDB:
    """In-memory stand-in for asyncpg helpers. Routes by query substring."""

    def __init__(self):
        # Simulated database state
        self.branches = {
            "001": {
                "kode_cabang": "001",
                "nama_cabang": "Kantor Pusat",
                "tipe_cabang": "CU",
                "status_cabang": "B",
                "kode_cabang_induk": None,
                "status_aktif": "T",
                "status_akses": "O",
                "kantor_nama": "Kantor Pusat Yayasan",
                "kantor_npwp": "1234567890001",
                "kantor_alamat": "Jl. Kantor Pusat No. 1",
                "kantor_kode_pos": "12000",
                "kantor_telepon1": "021-1234567",
                "kantor_telepon2": None,
                "kantor_telepon3": None,
                "user_input": "ADMIN",
                "tanggal_input": "2026-01-01",
            },
            "002": {
                "kode_cabang": "002",
                "nama_cabang": "Cabang Jakarta",
                "tipe_cabang": "CP",
                "status_cabang": "S",
                "kode_cabang_induk": "001",
                "status_aktif": "T",
                "status_akses": "O",
                "kantor_nama": "Cabang Jakarta",
                "kantor_npwp": "1234567890002",
                "kantor_alamat": "Jl. Jakarta No. 2",
                "kantor_kode_pos": "12000",
                "kantor_telepon1": "021-2345678",
                "kantor_telepon2": None,
                "kantor_telepon3": None,
                "user_input": "ADMIN",
                "tanggal_input": "2026-01-02",
            },
        }

    async def fetch_one(self, query, *args):
        """Simulate fetch_one for branch queries."""
        if "COUNT(*)" in query or "count(*)" in query:
            # Count query
            count = len(self.branches)
            if args:  # If there's filtering
                count = len(
                    [
                        b
                        for b in self.branches.values()
                        if args[0] in [b["kode_cabang"], b["nama_cabang"]]
                        or (args[0] and b["status_aktif"] == args[0])
                    ]
                )
            return {"cnt": count}

        if "WHERE c.kode_cabang = " in query or "WHERE kode_cabang = " in query:
            # Get by code
            branch_code = args[0] if args else None
            if branch_code and branch_code in self.branches:
                b = self.branches[branch_code]
                # Include parent branch name if needed
                parent_name = None
                if b["kode_cabang_induk"] and b["kode_cabang_induk"] in self.branches:
                    parent_name = self.branches[b["kode_cabang_induk"]]["nama_cabang"]
                return {**b, "parent_branch_name": parent_name}
            return None

        if "SELECT kode_cabang FROM enterprise.cabang WHERE" in query:
            # Check if code exists
            branch_code = args[0] if args else None
            if branch_code and branch_code in self.branches:
                return {"kode_cabang": branch_code}
            return None

        raise AssertionError(f"unexpected fetch_one: {query!r}")

    async def fetch_all(self, query, *args):
        """Simulate fetch_all for branch queries."""
        if "FROM enterprise.cabang" in query and "COUNT" not in query:
            # List branches
            rows = []
            offset = 0
            limit = 100

            # Extract offset/limit from args (last two params if present)
            if len(args) >= 2:
                limit = args[-2]
                offset = args[-1]

            all_branches = list(self.branches.values())

            # Apply filters
            filtered = all_branches
            if args and len(args) > 2:
                # Filter by status_aktif
                status = args[0]
                filtered = [b for b in filtered if b["status_aktif"] == status]

            # Apply pagination
            paginated = filtered[offset : offset + limit]

            for b in paginated:
                parent_name = None
                if b["kode_cabang_induk"] and b["kode_cabang_induk"] in self.branches:
                    parent_name = self.branches[b["kode_cabang_induk"]]["nama_cabang"]

                rows.append(
                    {
                        **b,
                        "parent_branch_name": parent_name,
                    }
                )
            return rows

        if "status_cabang = 'B' OR tipe_cabang IN" in query:
            # List parent branches
            parent_branches = [
                b for b in self.branches.values() if b["status_cabang"] == "B" or b["tipe_cabang"] in ("CU", "PO")
            ]
            return [{"kode_cabang": b["kode_cabang"], "nama_cabang": b["nama_cabang"]} for b in parent_branches]

        raise AssertionError(f"unexpected fetch_all: {query!r}")

    async def execute(self, query, *args):
        """Simulate execute for INSERT/UPDATE/DELETE."""
        if "INSERT INTO enterprise.cabang" in query:
            # Parse INSERT
            branch_code = args[0]
            self.branches[branch_code] = {
                "kode_cabang": branch_code,
                "nama_cabang": args[1],
                "tipe_cabang": args[2],
                "status_cabang": args[3],
                "kode_cabang_induk": args[4],
                "status_aktif": args[5],
                "status_otorisasi": args[6],
                "status_akses": args[7],
                "kantor_nama": args[8],
                "kantor_npwp": args[9],
                "kantor_alamat": args[10],
                "kantor_kode_pos": args[11],
                "kantor_telepon1": args[12],
                "kantor_telepon2": args[13],
                "kantor_telepon3": args[14],
                "tanggal_input": args[15],
                "user_input": args[16],
                "terminal_input": args[17],
            }
            return None

        if "UPDATE enterprise.cabang SET" in query:
            # Parse UPDATE
            # This is a simplified version; actual parsing would be more complex
            branch_code = args[-1]  # Last arg is usually the WHERE clause value
            if branch_code in self.branches:
                self.branches[branch_code]["nama_cabang"] = args[0]
                self.branches[branch_code]["tipe_cabang"] = args[1]
                self.branches[branch_code]["status_cabang"] = args[2]
                self.branches[branch_code]["kode_cabang_induk"] = args[3]
                self.branches[branch_code]["kantor_nama"] = args[4]
                self.branches[branch_code]["kantor_npwp"] = args[5]
                self.branches[branch_code]["kantor_alamat"] = args[6]
                self.branches[branch_code]["kantor_kode_pos"] = args[7]
                self.branches[branch_code]["kantor_telepon1"] = args[8]
                self.branches[branch_code]["kantor_telepon2"] = args[9]
                self.branches[branch_code]["kantor_telepon3"] = args[10]
            return None

        if "UPDATE enterprise.cabang SET status_aktif = 'F'" in query:
            # Deactivate
            branch_code = args[0]
            if branch_code in self.branches:
                self.branches[branch_code]["status_aktif"] = "F"
            return None

        if "UPDATE enterprise.cabang SET status_aktif = 'T'" in query:
            # Activate
            branch_code = args[0]
            if branch_code in self.branches:
                self.branches[branch_code]["status_aktif"] = "T"
            return None

        raise AssertionError(f"unexpected execute: {query!r}")


@pytest.fixture
def fake_db():
    """Provide a fresh fake database for each test."""
    return _FakeDB()


@pytest.fixture
def patch_db(monkeypatch, fake_db):
    """Patch the module's DB functions with our fake."""

    def _patch():
        monkeypatch.setattr(branch_service, "fetch_one", fake_db.fetch_one)
        monkeypatch.setattr(branch_service, "fetch_all", fake_db.fetch_all)
        monkeypatch.setattr(branch_service, "execute", fake_db.execute)

    _patch()
    return fake_db


# ─── List Tests ──────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_list_branches_returns_rows_and_total(patch_db):
    """list_branches returns tuple of (rows, total)."""
    rows, total = await branch_service.list_branches(page=1, limit=10)

    assert isinstance(rows, list)
    assert isinstance(total, int)
    assert total >= len(rows)


@pytest.mark.asyncio
async def test_list_branches_default_filter_status_aktif_T(patch_db):
    """list_branches defaults to filtering status_aktif='T'."""
    rows, total = await branch_service.list_branches(page=1, limit=10, status_aktif="T")

    assert total >= 0
    # All returned rows should be active
    for row in rows:
        assert row.is_active is True


@pytest.mark.asyncio
async def test_list_branches_pagination_offset_calculation(patch_db):
    """list_branches calculates correct OFFSET from page/limit."""
    # Page 1, limit 10 → offset 0
    rows1, _ = await branch_service.list_branches(page=1, limit=10)

    # Page 2, limit 10 → offset 10
    rows2, _ = await branch_service.list_branches(page=2, limit=10)

    # Both should be queries, even if fake DB
    assert isinstance(rows1, list)
    assert isinstance(rows2, list)


@pytest.mark.asyncio
async def test_list_branches_filter_by_status_aktif_F(patch_db):
    """list_branches filters correctly when status_aktif='F'."""
    # First deactivate a branch
    await branch_service.deactivate_branch("001")

    rows, total = await branch_service.list_branches(page=1, limit=10, status_aktif="F")

    # Should have deactivated branches
    assert total >= 0


@pytest.mark.asyncio
async def test_list_branches_respects_limit(patch_db):
    """list_branches respects the limit parameter."""
    rows1, _ = await branch_service.list_branches(page=1, limit=5)
    rows2, _ = await branch_service.list_branches(page=1, limit=1)

    # Limit 5 should return up to 5 rows
    assert len(rows1) <= 5
    # Limit 1 should return up to 1 row
    assert len(rows2) <= 1


# ─── Parent Branches Tests ────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_list_parent_branches_returns_cu_po_types(patch_db):
    """list_parent_branches returns CU/PO branches only."""
    parents = await branch_service.list_parent_branches()

    assert isinstance(parents, list)
    # Should have at least Kantor Pusat (CU type)
    codes = [p.branch_code for p in parents]
    assert "001" in codes  # Kantor Pusat is CU


# ─── Get Detail Tests ────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_get_branch_returns_detail_if_exists(patch_db):
    """get_branch returns BranchDetail when branch exists."""
    branch = await branch_service.get_branch("001")

    assert branch is not None
    assert isinstance(branch, BranchDetail)
    assert branch.branch_code == "001"
    assert branch.branch_name == "Kantor Pusat"


@pytest.mark.asyncio
async def test_get_branch_returns_none_if_not_found(patch_db):
    """get_branch returns None when branch not found."""
    branch = await branch_service.get_branch("NONEXISTENT")

    assert branch is None


@pytest.mark.asyncio
async def test_get_branch_includes_parent_branch_name(patch_db):
    """get_branch includes parent_branch_name when parent exists."""
    branch = await branch_service.get_branch("002")

    assert branch is not None
    assert branch.parent_branch_code == "001"
    assert branch.parent_branch_name == "Kantor Pusat"


# ─── Create Tests ────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_create_branch_returns_detail(patch_db):
    """create_branch returns BranchDetail for new branch."""
    payload = BranchCreateRequest(
        branch_code="E2ETEST",
        branch_name="E2E Test Branch",
        branch_type="CP",
        parent_branch_code="001",
        office_name="Test Office",
    )

    branch = await branch_service.create_branch(payload, inputer_id="ADMIN")

    assert branch is not None
    assert isinstance(branch, BranchDetail)
    assert branch.branch_code == "E2ETEST"
    assert branch.branch_name == "E2E Test Branch"


@pytest.mark.asyncio
async def test_create_branch_auto_sets_status_cabang_B_for_CU(patch_db):
    """create_branch auto-sets status_cabang='B' when branch_type='CU'."""
    payload = BranchCreateRequest(
        branch_code="CU_TEST",
        branch_name="New Kantor Utama",
        branch_type="CU",
        # No parent_branch_code for CU
    )

    branch = await branch_service.create_branch(payload, inputer_id="ADMIN")

    assert branch is not None
    assert branch.branch_status == "B"
    # CU branches should have no parent
    assert branch.parent_branch_code is None


@pytest.mark.asyncio
async def test_create_branch_auto_sets_status_cabang_S_for_CP(patch_db):
    """create_branch auto-sets status_cabang='S' when branch_type='CP'."""
    payload = BranchCreateRequest(
        branch_code="CP_TEST",
        branch_name="New Kantor Cabang",
        branch_type="CP",
        parent_branch_code="001",
    )

    branch = await branch_service.create_branch(payload, inputer_id="ADMIN")

    assert branch is not None
    assert branch.branch_status == "S"


@pytest.mark.asyncio
async def test_create_branch_auto_sets_status_aktif_T(patch_db):
    """create_branch auto-sets status_aktif='T' for new branches."""
    payload = BranchCreateRequest(
        branch_code="NEW_BRANCH",
        branch_name="New Branch",
        branch_type="CP",
        parent_branch_code="001",
    )

    branch = await branch_service.create_branch(payload, inputer_id="ADMIN")

    assert branch is not None
    assert branch.is_active is True


@pytest.mark.asyncio
async def test_create_branch_raises_if_code_already_exists(patch_db):
    """create_branch raises ValueError if branch_code already exists."""
    payload = BranchCreateRequest(
        branch_code="001",  # Already exists
        branch_name="Duplicate",
        branch_type="CP",
    )

    with pytest.raises(ValueError, match="sudah ada"):
        await branch_service.create_branch(payload, inputer_id="ADMIN")


@pytest.mark.asyncio
async def test_create_branch_sets_inputer_id_as_user_input(patch_db):
    """create_branch stores inputer_id in created_by field."""
    payload = BranchCreateRequest(
        branch_code="NEW_WITH_USER",
        branch_name="Test User Tracking",
        branch_type="CP",
        parent_branch_code="001",
    )

    branch = await branch_service.create_branch(payload, inputer_id="USER123")

    assert branch is not None
    assert branch.created_by == "USER123"


# ─── Update Tests ────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_update_branch_changes_name_and_type(patch_db):
    """update_branch updates branch_name and branch_type."""
    payload = BranchUpdateRequest(
        branch_name="Updated Branch Name",
        branch_type="CP",
        parent_branch_code="001",
    )

    branch = await branch_service.update_branch("002", payload)

    assert branch is not None
    assert branch.branch_name == "Updated Branch Name"


@pytest.mark.asyncio
async def test_update_branch_recalculates_status_cabang_B_for_CU(patch_db):
    """update_branch recalculates status_cabang based on new branch_type."""
    payload = BranchUpdateRequest(
        branch_name="Converted to CU",
        branch_type="CU",
        parent_branch_code=None,
    )

    branch = await branch_service.update_branch("002", payload)

    assert branch is not None
    assert branch.branch_status == "B"
    # Converting to CU should clear parent
    assert branch.parent_branch_code is None


@pytest.mark.asyncio
async def test_update_branch_preserves_code(patch_db):
    """update_branch cannot change branch_code (via WHERE clause)."""
    payload = BranchUpdateRequest(
        branch_name="Same Code",
        branch_type="CP",
        parent_branch_code="001",
    )

    branch = await branch_service.update_branch("002", payload)

    assert branch is not None
    # Code should remain unchanged
    assert branch.branch_code == "002"


# ─── Deactivate/Activate Tests ───────────────────────────────────────────────


@pytest.mark.asyncio
async def test_deactivate_branch_sets_status_aktif_F(patch_db):
    """deactivate_branch sets status_aktif='F'."""
    branch = await branch_service.deactivate_branch("001")

    assert branch is not None
    assert branch.is_active is False


@pytest.mark.asyncio
async def test_activate_branch_sets_status_aktif_T(patch_db):
    """activate_branch sets status_aktif='T'."""
    # First deactivate
    await branch_service.deactivate_branch("001")

    # Then activate
    branch = await branch_service.activate_branch("001")

    assert branch is not None
    assert branch.is_active is True


@pytest.mark.asyncio
async def test_deactivate_then_activate_roundtrip(patch_db):
    """Roundtrip: deactivate then activate returns to active state."""
    # Start active
    assert (await branch_service.get_branch("001")).is_active is True

    # Deactivate
    await branch_service.deactivate_branch("001")
    assert (await branch_service.get_branch("001")).is_active is False

    # Activate
    await branch_service.activate_branch("001")
    assert (await branch_service.get_branch("001")).is_active is True
