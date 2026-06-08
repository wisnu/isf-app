from __future__ import annotations
import json
from app.shared.db import fetch_all, fetch_one, get_pool


async def create_submission(
    entity_type: str, module: str, branch_code: str,
    payload: dict, submitted_by: str,
) -> int:
    async with get_pool().acquire() as conn:
        row = await conn.fetchrow(
            """INSERT INTO otorisasi.submission
               (entity_type, module, branch_code, payload, submitted_by)
               VALUES ($1, $2, $3, CAST($4 AS jsonb), $5)
               RETURNING id""",
            entity_type, module, branch_code, json.dumps(payload), submitted_by,
        )
        if row is None:
            raise RuntimeError("INSERT into otorisasi.submission returned no row")
        return int(row['id'])


async def get_submission(submission_id: int) -> dict | None:
    row = await fetch_one(
        """SELECT s.*, ec.label AS entity_label, ec.level_required, ec.menu_key
           FROM otorisasi.submission s
           LEFT JOIN otorisasi.entity_config ec ON ec.entity_type = s.entity_type
           WHERE s.id = $1""",
        submission_id,
    )
    if row is None:
        return None
    r = dict(row)
    if isinstance(r.get('payload'), str):
        r['payload'] = json.loads(r['payload'])
    return r


async def get_approval_log(submission_id: int) -> list[dict]:
    return await fetch_all(
        """SELECT * FROM otorisasi.approval_log
           WHERE submission_id = $1 ORDER BY level, logged_at""",
        submission_id,
    )


async def submit_submission(submission_id: int) -> None:
    async with get_pool().acquire() as conn:
        await conn.execute(
            """UPDATE otorisasi.submission
               SET status = 'PENDING', level_current = 1,
                   submitted_at = NOW(), updated_at = NOW()
               WHERE id = $1""",
            submission_id,
        )


async def update_payload(submission_id: int, payload: dict) -> None:
    async with get_pool().acquire() as conn:
        await conn.execute(
            """UPDATE otorisasi.submission
               SET payload = CAST($1 AS jsonb), status = 'DRAFT', updated_at = NOW()
               WHERE id = $2""",
            json.dumps(payload), submission_id,
        )


async def delete_submission(submission_id: int) -> None:
    async with get_pool().acquire() as conn:
        await conn.execute(
            "DELETE FROM otorisasi.submission WHERE id = $1", submission_id,
        )


async def insert_approval_log(
    submission_id: int, level: int, authorizer_id: str,
    status: str, notes: str | None,
) -> int:
    async with get_pool().acquire() as conn:
        row = await conn.fetchrow(
            """INSERT INTO otorisasi.approval_log
               (submission_id, level, authorizer_id, status, notes)
               VALUES ($1, $2, $3, $4, $5) RETURNING id""",
            submission_id, level, authorizer_id, status, notes,
        )
        if row is None:
            raise RuntimeError("INSERT into otorisasi.approval_log returned no row")
        return int(row['id'])


async def advance_level(submission_id: int, new_level: int) -> None:
    async with get_pool().acquire() as conn:
        await conn.execute(
            """UPDATE otorisasi.submission
               SET level_current = $1, updated_at = NOW() WHERE id = $2""",
            new_level, submission_id,
        )


async def authorize_submission(submission_id: int, result_entity_id: int | None) -> None:
    async with get_pool().acquire() as conn:
        await conn.execute(
            """UPDATE otorisasi.submission
               SET status = 'AUTHORIZED', result_entity_id = $1, updated_at = NOW()
               WHERE id = $2""",
            result_entity_id, submission_id,
        )


async def reject_submission_db(submission_id: int) -> None:
    async with get_pool().acquire() as conn:
        await conn.execute(
            """UPDATE otorisasi.submission
               SET status = 'REJECTED', updated_at = NOW() WHERE id = $1""",
            submission_id,
        )


async def list_submissions(
    module: str | None = None,
    entity_type: str | None = None,
    status: str | None = None,
    submitted_by: str | None = None,
    branch: str | None = None,
    branch_access: str = 'single',
    page: int = 1,
    page_size: int = 25,
) -> tuple[list[dict], int]:
    total_row = await fetch_one(
        """SELECT COUNT(*) AS n FROM otorisasi.submission s
           WHERE ($1 IS NULL OR s.module = $1)
             AND ($2 IS NULL OR s.entity_type = $2)
             AND ($3 IS NULL OR s.status = $3)
             AND ($4 IS NULL OR s.submitted_by = $4)
             AND ($5 IS NULL OR $6 = 'all' OR s.branch_code = $5)""",
        module, entity_type, status, submitted_by, branch, branch_access,
    )
    total = int(total_row['n']) if total_row else 0
    offset = (page - 1) * page_size
    rows = await fetch_all(
        """SELECT s.*, ec.label AS entity_label, ec.level_required
           FROM otorisasi.submission s
           LEFT JOIN otorisasi.entity_config ec ON ec.entity_type = s.entity_type
           WHERE ($1 IS NULL OR s.module = $1)
             AND ($2 IS NULL OR s.entity_type = $2)
             AND ($3 IS NULL OR s.status = $3)
             AND ($4 IS NULL OR s.submitted_by = $4)
             AND ($5 IS NULL OR $6 = 'all' OR s.branch_code = $5)
           ORDER BY s.created_at DESC
           LIMIT $7 OFFSET $8""",
        module, entity_type, status, submitted_by, branch, branch_access,
        page_size, offset,
    )
    return rows, total


async def get_entity_config(entity_type: str) -> dict | None:
    return await fetch_one(
        "SELECT * FROM otorisasi.entity_config WHERE entity_type = $1", entity_type,
    )


async def list_entity_configs(module: str | None = None) -> list[dict]:
    if module:
        return await fetch_all(
            "SELECT * FROM otorisasi.entity_config WHERE module = $1 ORDER BY entity_type",
            module,
        )
    return await fetch_all(
        "SELECT * FROM otorisasi.entity_config ORDER BY module, entity_type",
    )
