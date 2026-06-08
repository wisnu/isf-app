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
    register_dispatcher('penghimpunan', penghimpunan_service.create_from_payload)
    register_dispatcher('penyaluran', penyaluran_service.create_from_payload)
    # coa, kas, bank dispatcher ditambahkan saat modul master tersedia


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


async def approve(
    submission_id: int, authorizer_id: str,
    branch_access: str = 'single', notes: str | None = None,
) -> dict:
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
        result_entity_id = None
        if dispatcher:
            result_entity_id = await dispatcher(
                payload=dict(sub['payload']),
                user_id=sub['submitted_by'],
                branch_code=sub['branch_code'],
            )
        await repo.authorize_submission(submission_id, result_entity_id)
        return {'id': submission_id, 'status': 'AUTHORIZED', 'result_entity_id': result_entity_id}

    await repo.advance_level(submission_id, level + 1)
    return {'id': submission_id, 'status': 'PENDING', 'level_current': level + 1}


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
    results = []
    for sid in ids:
        try:
            results.append(await approve(sid, authorizer_id, branch_access))
        except HTTPException as e:
            results.append({'id': sid, 'error': e.detail})
    return results


async def bulk_reject(ids: list[int], authorizer_id: str, notes: str) -> list[dict]:
    results = []
    for sid in ids:
        try:
            results.append(await reject(sid, authorizer_id, notes))
        except HTTPException as e:
            results.append({'id': sid, 'error': e.detail})
    return results
