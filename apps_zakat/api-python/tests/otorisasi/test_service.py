import pytest
from unittest.mock import AsyncMock, patch
from app.modules.otorisasi import service


@pytest.mark.asyncio
async def test_save_draft_unknown_entity_type():
    with patch('app.modules.otorisasi.service.repo.get_entity_config', return_value=None):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            await service.save_draft('unknown', 'keuangan', {}, 'RAIS', '001')
        assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_submit_rejects_already_pending():
    mock_sub = {'submitted_by': 'RAIS', 'status': 'PENDING'}
    with patch('app.modules.otorisasi.service.repo.get_submission', return_value=mock_sub):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            await service.submit_for_auth(1, 'RAIS')
        assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_approve_single_level_dispatches():
    mock_sub = {
        'status': 'PENDING', 'level_current': 1, 'level_required': 1,
        'entity_type': 'penghimpunan', 'submitted_by': 'RAIS', 'branch_code': '001',
        'payload': {'actual_date': '2026-06-08'},
    }
    mock_dispatcher = AsyncMock(return_value=42)
    with patch('app.modules.otorisasi.service.repo.get_submission', return_value=mock_sub), \
         patch('app.modules.otorisasi.service.repo.insert_approval_log', return_value=1), \
         patch('app.modules.otorisasi.service.repo.authorize_submission') as mock_auth, \
         patch.dict('app.modules.otorisasi.service._DISPATCHERS', {'penghimpunan': mock_dispatcher}):
        result = await service.approve(1, 'SPVDIST', 'single', 'OK')
    assert result['status'] == 'AUTHORIZED'
    assert result['result_entity_id'] == 42
    mock_dispatcher.assert_called_once_with(
        payload={'actual_date': '2026-06-08'}, user_id='RAIS', branch_code='001'
    )


@pytest.mark.asyncio
async def test_reject_requires_pending():
    mock_sub = {'status': 'DRAFT', 'level_current': 0}
    with patch('app.modules.otorisasi.service.repo.get_submission', return_value=mock_sub):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            await service.reject(1, 'SPVDIST', 'Alasan penolakan')
        assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_save_and_submit_below_limit_dispatches():
    """Total ≤ limit → AUTHORIZED, dispatcher called."""
    mock_dispatcher = AsyncMock(return_value=999)
    with patch('app.modules.otorisasi.service.repo.get_entity_config',
               return_value={'entity_type': 'penyaluran'}), \
         patch('app.modules.otorisasi.service.repo.get_user_limit', return_value=500000.0), \
         patch('app.modules.otorisasi.service.repo.create_submission', return_value=42), \
         patch('app.modules.otorisasi.service.repo.insert_approval_log', return_value=1), \
         patch('app.modules.otorisasi.service.repo.authorize_submission'), \
         patch.dict('app.modules.otorisasi.service._DISPATCHERS', {'penyaluran': mock_dispatcher}):
        result = await service.save_and_submit(
            'penyaluran', 'keuangan',
            {'items': [{'amount': 100000}]},
            'RAIS', '001',
        )
    assert result['status'] == 'AUTHORIZED'
    assert result['bypassed_auth'] is True
    assert result['transaction_id'] == 999
    mock_dispatcher.assert_called_once_with(
        payload={'items': [{'amount': 100000}]}, user_id='RAIS', branch_code='001',
    )


@pytest.mark.asyncio
async def test_save_and_submit_above_limit_goes_pending():
    """Total > limit → PENDING, dispatcher NOT called."""
    mock_dispatcher = AsyncMock(return_value=999)
    with patch('app.modules.otorisasi.service.repo.get_entity_config',
               return_value={'entity_type': 'penyaluran'}), \
         patch('app.modules.otorisasi.service.repo.get_user_limit', return_value=50000.0), \
         patch('app.modules.otorisasi.service.repo.create_submission', return_value=43), \
         patch('app.modules.otorisasi.service.repo.submit_submission'), \
         patch.dict('app.modules.otorisasi.service._DISPATCHERS', {'penyaluran': mock_dispatcher}):
        result = await service.save_and_submit(
            'penyaluran', 'keuangan',
            {'items': [{'amount': 100000}]},
            'RAIS', '001',
        )
    assert result['status'] == 'PENDING'
    assert result['bypassed_auth'] is False
    assert result['transaction_id'] is None
    mock_dispatcher.assert_not_called()


@pytest.mark.asyncio
async def test_save_and_submit_zero_limit_goes_pending():
    """nilai_limit = 0 (not set) → always PENDING."""
    with patch('app.modules.otorisasi.service.repo.get_entity_config',
               return_value={'entity_type': 'penghimpunan'}), \
         patch('app.modules.otorisasi.service.repo.get_user_limit', return_value=0.0), \
         patch('app.modules.otorisasi.service.repo.create_submission', return_value=44), \
         patch('app.modules.otorisasi.service.repo.submit_submission'):
        result = await service.save_and_submit(
            'penghimpunan', 'keuangan',
            {'items': [{'amount': 1}]},
            'RAIS', '001',
        )
    assert result['status'] == 'PENDING'
    assert result['bypassed_auth'] is False
