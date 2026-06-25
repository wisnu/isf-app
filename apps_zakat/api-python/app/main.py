from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

# ── Finance — Master Data ─────────────────────────────────────────────────────
from app.modules.finance.master.coa.router import router as coa_router
from app.modules.finance.master.bank.router import router as bank_router
from app.modules.finance.master.petty_cash.router import router as petty_cash_router
from app.modules.finance.master.parameter.router import router as parameter_router

# ── Finance — Budget ──────────────────────────────────────────────────────────
from app.modules.finance.budget.router import router as budget_router

# ── Finance — Transaction ─────────────────────────────────────────────────────
from app.modules.finance.transaction.fund_collection.router import router as fund_collection_router
from app.modules.finance.transaction.fund_distribution.router import router as fund_distribution_router
from app.modules.finance.transaction.amil_income.router import router as amil_income_router
from app.modules.finance.transaction.amil_expense.router import router as amil_expense_router
from app.modules.finance.transaction.cash_advance.router import router as cash_advance_router
from app.modules.finance.transaction.cash_advance_settlement.router import router as cash_advance_settlement_router
from app.modules.finance.transaction.inter_account_transfer.router import router as inter_account_transfer_router
from app.modules.finance.transaction.general.router import router as general_transaction_router
from app.modules.finance.transaction.receivable.router import router as receivable_router

# ── Finance — Upload ──────────────────────────────────────────────────────────
from app.modules.finance.upload.collection.router import router as upload_collection_router
from app.modules.finance.upload.hc_zis.router import router as hc_zis_router

# ── Finance — Inquiry ─────────────────────────────────────────────────────────
from app.modules.finance.inquiry.transaction_history.router import router as transaction_history_router
from app.modules.finance.inquiry.cash_advance.router import router as ca_inquiry_router
from app.modules.finance.inquiry.receivable.router import router as receivable_inquiry_router

# ── Finance — Monitoring ──────────────────────────────────────────────────────
from app.modules.finance.monitoring.authorization.router import router as authorization_router
from app.modules.finance.monitoring.authorization.service import _register_defaults

# ── Distribution ─────────────────────────────────────────────────────────────
from app.modules.distribution.mustahiq.router import router as mustahiq_router
from app.modules.distribution.partner.router import router as partner_router
from app.modules.distribution.proposal.router import router as proposal_router
from app.modules.distribution.regular_program.router import router as regular_program_router
from app.modules.distribution.non_regular_program.router import router as non_regular_program_router
from app.modules.distribution.realization_memo.router import regular_router as realization_memo_regular_router, non_regular_router as realization_memo_non_regular_router
from app.modules.distribution.realization.router import regular_router as realization_regular_router, non_regular_router as realization_non_regular_router
from app.modules.distribution.monitoring.router import router as monitoring_router
from app.modules.distribution.realization_return.router import router as realization_return_router
from app.modules.distribution.parameter.program_type.router import router as dist_param_program_type_router
from app.modules.distribution.parameter.program.router import router as dist_param_program_router
from app.modules.distribution.parameter.work_sector.router import router as dist_param_work_sector_router
from app.modules.distribution.parameter.cost_item.router import router as dist_param_cost_item_router

# ── Fundraising ──────────────────────────────────────────────────────────────
from app.modules.fundraising.donors.router import router as fundraising_donors_router
from app.modules.fundraising.donation_confirm_router import router as donation_confirm_router

# ── Administration ────────────────────────────────────────────────────────────
from app.modules.appadmin.router import router as admin_router
from app.modules.appadmin.identity.router import router as identity_router

# ── General Affair ────────────────────────────────────────────────────────────
from app.modules.generalaffair.document.router import router as ga_document_router

# ── Shared ────────────────────────────────────────────────────────────────────
from app.shared.db import close_pool, init_isf_auth_pool, init_pool, ping
from app.shared.response import err, ok


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = await init_pool()
    isf_auth_pool = await init_isf_auth_pool()
    app.state.db_pool = pool
    app.state.isf_auth_pool = isf_auth_pool
    _register_defaults()
    yield
    await close_pool()


app = FastAPI(title="isf-app api-python", version="0.2.0", lifespan=lifespan)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=err('HTTP_ERROR', exc.detail))


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse(status_code=400, content=err('VALIDATION_ERROR', str(exc)))


@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content=err('INTERNAL_ERROR', 'Internal server error'))


@app.get("/health")
def health() -> dict:
    return ok({"status": "ok"})


@app.get("/ready")
async def ready() -> dict:
    db_ok = await ping() if app.state.db_pool else False
    return ok({"status": "ready", "db": db_ok})


# ── Finance — Master Data ─────────────────────────────────────────────────────
app.include_router(coa_router,        prefix="/api")
app.include_router(bank_router,       prefix="/api")
app.include_router(petty_cash_router, prefix="/api")
app.include_router(parameter_router,  prefix="/api")

# ── Finance — Budget ──────────────────────────────────────────────────────────
app.include_router(budget_router, prefix="/api")

# ── Finance — Transaction ─────────────────────────────────────────────────────
app.include_router(fund_collection_router,         prefix="/api")
app.include_router(fund_distribution_router,       prefix="/api")
app.include_router(amil_income_router,             prefix="/api")
app.include_router(amil_expense_router,            prefix="/api")
app.include_router(cash_advance_router,            prefix="/api")
app.include_router(cash_advance_settlement_router, prefix="/api")
app.include_router(inter_account_transfer_router,  prefix="/api")
app.include_router(general_transaction_router,     prefix="/api")
app.include_router(receivable_router,              prefix="/api")

# ── Finance — Upload ──────────────────────────────────────────────────────────
app.include_router(upload_collection_router, prefix="/api")
app.include_router(hc_zis_router,            prefix="/api")

# ── Finance — Inquiry ─────────────────────────────────────────────────────────
app.include_router(transaction_history_router, prefix="/api")
app.include_router(ca_inquiry_router,            prefix="/api")
app.include_router(receivable_inquiry_router,    prefix="/api")

# ── Finance — Monitoring ──────────────────────────────────────────────────────
app.include_router(authorization_router, prefix="/api")

# ── Distribution ─────────────────────────────────────────────────────────────
app.include_router(mustahiq_router,        prefix="/api")
app.include_router(partner_router,         prefix="/api")
app.include_router(proposal_router,        prefix="/api")
app.include_router(regular_program_router,     prefix="/api")
app.include_router(non_regular_program_router, prefix="/api")
app.include_router(realization_memo_regular_router,     prefix="/api")
app.include_router(realization_memo_non_regular_router, prefix="/api")
app.include_router(realization_regular_router,     prefix="/api")
app.include_router(realization_non_regular_router, prefix="/api")
app.include_router(monitoring_router,            prefix="/api")
app.include_router(realization_return_router,    prefix="/api")
app.include_router(dist_param_program_type_router, prefix="/api")
app.include_router(dist_param_program_router,      prefix="/api")
app.include_router(dist_param_work_sector_router,  prefix="/api")
app.include_router(dist_param_cost_item_router,    prefix="/api")

# ── Fundraising ──────────────────────────────────────────────────────────────
app.include_router(fundraising_donors_router, prefix="/api")
app.include_router(donation_confirm_router, prefix="/api")

# ── Administration ────────────────────────────────────────────────────────────
app.include_router(admin_router,    prefix="/api")
app.include_router(identity_router, prefix="/api")

# ── General Affair ────────────────────────────────────────────────────────────
app.include_router(ga_document_router, prefix="/api")
