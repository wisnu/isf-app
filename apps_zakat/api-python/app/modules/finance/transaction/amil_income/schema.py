"""Pydantic schemas for Penerimaan Amil (CI - Cash In Amil)."""
from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field, field_validator


class AmilIncomeItemCreate(BaseModel):
    """Item in amil income transaction (GL account for amil revenue)."""
    account_code: str       # kode COA pendapatan amil (430xxx)
    account_name: str       # nama akun (auto-resolved, optional in create)
    amount: float = Field(gt=0)
    currency_code: str = 'IDR'
    rate: float = 1.0
    ekuivalen_amount: Optional[float] = None  # auto-computed
    description: Optional[str] = None
    cash_account_no: Optional[str] = None       # rekening sumber (Bank mode) — leg C20
    cash_account_name: Optional[str] = None     # auto-resolved
    fund_account_no: Optional[str] = None        # akun produk sumber dana (untuk leg C20)
    fund_product_code: Optional[str] = None     # referensi produk (optional)
    fund_product_name: Optional[str] = None     # auto-resolved
    budget_id: Optional[int] = None
    budget_code: Optional[str] = None
    budget_owner: Optional[str] = None

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('amount harus lebih dari 0')
        return v

    @field_validator('rate')
    @classmethod
    def validate_rate(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('rate harus lebih dari 0')
        return v


class AmilIncomeCreate(BaseModel):
    """Request body untuk POST /api/transaction/amil-income/save-and-submit."""
    actual_date: str        # YYYY-MM-DD
    payment_type: str       # 'K' (Kas Kecil), 'C' (Kas Cabang), 'B' (Bank)
    cash_type: Optional[str] = None  # 'K' atau 'C', only for payment_type='K'/'C'
    bank_account_no: Optional[str] = None  # for payment_type='B'
    reference_no: Optional[str] = None
    description: Optional[str] = None
    rate: float = 1.0
    paid_to: Optional[str] = None
    received_from: Optional[str] = None
    items: list[AmilIncomeItemCreate]

    # Injected by BFF
    inputer_id: str = ''
    branch_code: str = ''

    @field_validator('payment_type')
    @classmethod
    def validate_payment_type(cls, v: str) -> str:
        if v.upper() not in ('K', 'C', 'B'):
            raise ValueError("payment_type harus 'K' (Kas Kecil), 'C' (Kas Cabang), atau 'B' (Bank)")
        return v.upper()

    @field_validator('items')
    @classmethod
    def validate_items(cls, v: list) -> list:
        if len(v) < 1:
            raise ValueError('Minimal 1 item GL account wajib')
        return v

    @field_validator('rate')
    @classmethod
    def validate_rate(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('rate harus lebih dari 0')
        return v


class AmilIncomeItemResponse(BaseModel):
    """Item dalam response GET /api/transaction/amil-income/{id}."""
    transaction_item_id: int
    account_code: str
    account_name: str
    amount: float
    currency_code: str
    rate: float
    ekuivalen_amount: float
    mutation_type: str  # 'C' untuk GL item (kredit pendapatan)
    description: Optional[str]
    cash_account_no: Optional[str]
    cash_account_name: Optional[str]
    fund_product_code: Optional[str]
    fund_product_name: Optional[str]


class AmilIncomeResponse(BaseModel):
    """Response untuk GET /api/transaction/amil-income (list item)."""
    transaction_id: int
    transaction_no: str
    actual_date: str        # YYYY-MM-DD
    bank_account_no: Optional[str]
    bank_account_name: Optional[str]
    total_amount: float
    reference_no: Optional[str]
    description: Optional[str]
    inputer: str
    branch_code: str
    status: str            # 'PENDING' atau 'AUTHORIZED'
    auth_status: str       # 'F' (belum), 'T' (sudah)
    auth_user: Optional[str]
    auth_date: Optional[str]
    payment_type: str
    channel_code: str


class AmilIncomeDetailResponse(BaseModel):
    """Response untuk GET /api/transaction/amil-income/{id} (detail lengkap)."""
    transaction_id: int
    transaction_no: str
    actual_date: str
    payment_type: str
    bank_account_no: Optional[str]
    bank_account_name: Optional[str]
    reference_no: Optional[str]
    description: Optional[str]
    rate: float
    total_amount: float
    inputer: str
    branch_code: str
    paid_to: Optional[str]
    received_from: Optional[str]
    status: str
    auth_status: str
    auth_user: Optional[str]
    auth_date: Optional[str]
    channel_code: str
    items: list[AmilIncomeItemResponse]


class KasAccountLookupItem(BaseModel):
    """Lookup response untuk GET /api/transaction/amil-income/lookup/kas-account."""
    account_no: str
    account_name: str
    bank_name: Optional[str]
    cash_code: str
    currency_code: str
    status: str
    is_amil_account: bool
    branch_code: str


class GLAccountLookupItem(BaseModel):
    """Lookup response untuk GET /api/transaction/amil-income/lookup/gl-account."""
    account_code: str
    account_name: str
    account_type: str
    parent_account_code: str
    parent_account_name: str
    status: str


class NextNumberResponse(BaseModel):
    """Response untuk GET /api/transaction/amil-income/next-number."""
    next_number: str
    prefix: str
    sequence: int
