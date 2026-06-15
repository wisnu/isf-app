from __future__ import annotations
from fastapi import HTTPException
from . import repo

# Registry: entity_type → async fn(payload, user_id, branch_code) → int
_DISPATCHERS: dict = {}


def register_dispatcher(entity_type: str, fn) -> None:
    _DISPATCHERS[entity_type] = fn


def _register_defaults() -> None:
    """Dipanggil di app startup untuk daftarkan semua dispatcher."""
    from app.modules.transaction import penghimpunan_service, penyaluran_service
    from app.modules.bank import service as bank_service
    register_dispatcher('penghimpunan', penghimpunan_service.create_from_payload)
    register_dispatcher('penyaluran', penyaluran_service.create_from_payload)
    register_dispatcher('bank', bank_service.create_from_payload)
    from app.modules.parameter import service as parameter_service
    register_dispatcher('budget_owner', parameter_service.create_from_payload)
    # HC ZIS dispatchers
    from app.modules.transaksi import hc_zis_commit
    register_dispatcher('hc_zis_upload', hc_zis_commit.create_from_payload)
    register_dispatcher('hc_zis_delete', hc_zis_commit.delete_from_payload)
    register_dispatcher('hc_zis_update_date', hc_zis_commit.update_date_from_payload)
    # Uang Muka dispatcher
    from app.modules.transaksi import uang_muka_service
    register_dispatcher('uang_muka', uang_muka_service.create_from_payload)
    # coa, kas dispatcher ditambahkan saat modul master tersedia


async def save_draft(
    entity_type: str, module: str, payload: dict,
    user_id: str, branch_code: str,
) -> dict:
    config = await repo.get_entity_config(entity_type)
    if not config:
        raise HTTPException(400, f"entity_type '{entity_type}' tidak dikenal")
    submission_id = await repo.create_submission(
        entity_type, module, branch_code, payload, user_id,
    )
    return {'id': submission_id, 'status': 'DRAFT'}


async def submit_for_auth(submission_id: int, user_id: str) -> dict:
    sub = await repo.get_submission(submission_id)
    if not sub:
        raise HTTPException(404, 'Submission tidak ditemukan')
    if sub['submitted_by'] != user_id:
        raise HTTPException(403, 'Bukan submission Anda')
    if sub['status'] not in ('DRAFT', 'REJECTED'):
        raise HTTPException(400, f"Status '{sub['status']}' tidak bisa disubmit")
    await repo.submit_submission(submission_id)
    return {'id': submission_id, 'status': 'PENDING'}


async def start_approve(
    submission_id: int,
    authorizer_id: str,
    branch_access: str = 'single',
    notes: str | None = None,
) -> dict:
    """Validate, log approval, set PROCESSING jika dispatcher ada. Returns dict dengan 'needs_dispatch' flag.
    Tidak memanggil dispatcher — caller (router) yang menjadwalkan BackgroundTask."""
    sub = await repo.get_submission(submission_id)
    if not sub:
        raise HTTPException(404, 'Submission tidak ditemukan')
    if sub['status'] != 'PENDING':
        raise HTTPException(400, f"Status '{sub['status']}' tidak bisa diotorisasi")

    level = sub['level_current']
    level_required = sub['level_required']

    await repo.insert_approval_log(submission_id, level, authorizer_id, 'APPROVED', notes)

    if level >= level_required:
        dispatcher = _DISPATCHERS.get(sub['entity_type'])
        if dispatcher:
            await repo.set_processing(submission_id)
            return {
                'id': submission_id,
                'status': 'PROCESSING',
                'needs_dispatch': True,
                'entity_type': sub['entity_type'],
                'payload': dict(sub['payload']),
                'submitted_by': sub['submitted_by'],
                'branch_code': sub['branch_code'],
            }
        else:
            await repo.authorize_submission(submission_id, None)
            return {'id': submission_id, 'status': 'AUTHORIZED', 'needs_dispatch': False}

    await repo.advance_level(submission_id, level + 1)
    return {'id': submission_id, 'status': 'PENDING', 'needs_dispatch': False, 'level_current': level + 1}


async def execute_dispatch(
    submission_id: int,
    entity_type: str,
    payload: dict,
    submitted_by: str,
    branch_code: str,
) -> None:
    """Background task: panggil dispatcher → AUTHORIZED. Jika gagal → revert ke PENDING + catat error."""
    try:
        dispatcher = _DISPATCHERS[entity_type]
        result_entity_id = await dispatcher(
            payload=payload,
            user_id=submitted_by,
            branch_code=branch_code,
        )
        await repo.authorize_submission(submission_id, result_entity_id)
    except Exception as exc:
        await repo.revert_to_pending_with_error(submission_id, str(exc)[:500])


async def reject(submission_id: int, authorizer_id: str, notes: str) -> dict:
    sub = await repo.get_submission(submission_id)
    if not sub:
        raise HTTPException(404, 'Submission tidak ditemukan')
    if sub['status'] != 'PENDING':
        raise HTTPException(400, f"Status '{sub['status']}' tidak bisa ditolak")
    await repo.insert_approval_log(submission_id, sub['level_current'], authorizer_id, 'REJECTED', notes)
    await repo.reject_submission_db(submission_id)
    return {'id': submission_id, 'status': 'REJECTED'}


async def bulk_approve(ids: list[int], authorizer_id: str, branch_access: str) -> list[dict]:
    """Returns list of start_approve results. Router menjadwalkan BackgroundTask untuk setiap needs_dispatch=True."""
    results = []
    for sid in ids:
        try:
            results.append(await start_approve(sid, authorizer_id, branch_access))
        except HTTPException as e:
            results.append({'id': sid, 'error': e.detail, 'needs_dispatch': False})
    return results


async def bulk_reject(ids: list[int], authorizer_id: str, notes: str) -> list[dict]:
    results = []
    for sid in ids:
        try:
            results.append(await reject(sid, authorizer_id, notes))
        except HTTPException as e:
            results.append({'id': sid, 'error': e.detail})
    return results


ENTITY_TRANSACTION_CODE: dict[str, str] = {
    'penghimpunan':        'SD001',
    'penyaluran':          'DD001',
    'upload_penghimpunan': 'SDULBA',
    'uang_muka':           'KK',
}


async def get_user_limit_for_entity(user_id: str, entity_type: str) -> float:
    """Return nilai_limit user untuk entity_type. 0.0 jika tidak ada mapping atau belum diset."""
    tx_code = ENTITY_TRANSACTION_CODE.get(entity_type)
    if not tx_code:
        return 0.0
    return await repo.get_user_limit(user_id, tx_code)


async def _decide_and_finalize(
    sub_id: int, entity_type: str, payload: dict,
    user_id: str, branch_code: str, nilai_limit: float,
) -> dict:
    """Cek limit, dispatch atau set PENDING. Dipanggil dari save_and_submit dan update_and_submit."""
    total = sum(float(i.get('amount', 0)) for i in payload.get('items', []))
    bypassed = nilai_limit > 0 and total <= nilai_limit

    if bypassed:
        dispatcher = _DISPATCHERS.get(entity_type)
        result_entity_id = None
        if dispatcher:
            result_entity_id = await dispatcher(
                payload=dict(payload), user_id=user_id, branch_code=branch_code,
            )
        await repo.insert_approval_log(sub_id, 0, 'SYSTEM_AUTO', 'APPROVED', 'Dalam limit')
        await repo.authorize_submission(sub_id, result_entity_id)
        return {
            'submission_id': sub_id,
            'status': 'AUTHORIZED',
            'transaction_id': result_entity_id,
            'bypassed_auth': True,
        }
    else:
        await repo.submit_submission(sub_id)
        return {
            'submission_id': sub_id,
            'status': 'PENDING',
            'transaction_id': None,
            'bypassed_auth': False,
        }


async def save_and_submit(
    entity_type: str, module: str, payload: dict,
    user_id: str, branch_code: str,
) -> dict:
    """Buat submission baru + cek limit + dispatch atau set PENDING."""
    config = await repo.get_entity_config(entity_type)
    if not config:
        raise HTTPException(400, f"entity_type '{entity_type}' tidak dikenal")

    nilai_limit = await get_user_limit_for_entity(user_id, entity_type)
    sub_id = await repo.create_submission(entity_type, module, branch_code, payload, user_id)
    return await _decide_and_finalize(sub_id, entity_type, payload, user_id, branch_code, nilai_limit)


async def update_and_submit(
    submission_id: int, payload: dict, user_id: str,
) -> dict:
    """Update payload submission REJECTED + cek limit + dispatch atau set PENDING."""
    sub = await repo.get_submission(submission_id)
    if not sub:
        raise HTTPException(404, 'Submission tidak ditemukan')
    if sub['submitted_by'] != user_id:
        raise HTTPException(403, 'Bukan submission Anda')
    if sub['status'] != 'REJECTED':
        raise HTTPException(400, f"Hanya submission REJECTED yang bisa di-update. Status saat ini: '{sub['status']}'")

    await repo.update_payload(submission_id, payload)

    entity_type = sub['entity_type']
    branch_code = sub['branch_code']
    nilai_limit = await get_user_limit_for_entity(user_id, entity_type)
    return await _decide_and_finalize(submission_id, entity_type, payload, user_id, branch_code, nilai_limit)
