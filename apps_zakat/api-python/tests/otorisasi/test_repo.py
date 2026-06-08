import pytest
import json
from app.modules.otorisasi import repo


@pytest.mark.asyncio
async def test_create_and_get_submission():
    sub_id = await repo.create_submission(
        entity_type='penghimpunan', module='keuangan',
        branch_code='001',
        payload={"actual_date": "2026-06-08", "payment_type": "C", "items": []},
        submitted_by='RAIS'
    )
    assert isinstance(sub_id, int)

    sub = await repo.get_submission(sub_id)
    assert sub is not None
    assert sub['status'] == 'DRAFT'
    assert sub['entity_type'] == 'penghimpunan'
    assert isinstance(sub['payload'], dict)
    assert sub['payload']['payment_type'] == 'C'
    assert sub['entity_label'] == 'Penghimpunan Dana'  # dari join entity_config


@pytest.mark.asyncio
async def test_submit_and_reject_flow():
    sub_id = await repo.create_submission(
        entity_type='penyaluran', module='keuangan',
        branch_code='001', payload={"actual_date": "2026-06-08"},
        submitted_by='HADI'
    )
    await repo.submit_submission(sub_id)
    sub = await repo.get_submission(sub_id)
    assert sub['status'] == 'PENDING'
    assert sub['level_current'] == 1

    await repo.insert_approval_log(sub_id, 1, 'SPVDIST', 'REJECTED', 'Jumlah tidak sesuai')
    await repo.reject_submission_db(sub_id)
    sub = await repo.get_submission(sub_id)
    assert sub['status'] == 'REJECTED'

    log = await repo.get_approval_log(sub_id)
    assert len(log) == 1
    assert log[0]['status'] == 'REJECTED'
    assert log[0]['notes'] == 'Jumlah tidak sesuai'


@pytest.mark.asyncio
async def test_get_user_limit_no_limit():
    # RAIS has nilai_limit=0 → return 0.0
    result = await repo.get_user_limit('RAIS', 'DD001')
    assert isinstance(result, float)
    assert result == 0.0


@pytest.mark.asyncio
async def test_get_user_limit_unknown_user():
    result = await repo.get_user_limit('NONEXISTENT_USER_XYZ', 'DD001')
    assert result == 0.0


@pytest.mark.asyncio
async def test_get_user_limit_no_jenis_limit_mapping():
    # No jenis_limit mapping for this tx code → return 0.0
    result = await repo.get_user_limit('RAIS', 'COA999')
    assert result == 0.0
