"""Pydantic schemas for Transaksi Umum (GT - General Transaction)."""
from __future__ import annotations

from pydantic import BaseModel, field_validator


class TransaksiUmumItem(BaseModel):
    account_code: str
    account_name: str
    mutation_type: str  # 'D' | 'C'
    amount: float
    description: str = ''

    @field_validator('mutation_type')
    @classmethod
    def validate_mutation(cls, v: str) -> str:
        if v.upper() not in ('D', 'C'):
            raise ValueError("mutation_type harus 'D' (Debet) atau 'C' (Kredit)")
        return v.upper()

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('amount harus lebih dari 0')
        return v


class TransaksiUmumCreate(BaseModel):
    actual_date: str       # YYYY-MM-DD
    description: str
    reference_no: str = ''
    items: list[TransaksiUmumItem]
    inputer_id: str = ''   # injected by BFF
    branch_code: str = ''  # injected by BFF

    @field_validator('items')
    @classmethod
    def validate_items(cls, v: list) -> list:
        if len(v) < 2:
            raise ValueError('Minimal 2 item jurnal (1 debet + 1 kredit)')
        total_d = sum(i.amount for i in v if i.mutation_type == 'D')
        total_c = sum(i.amount for i in v if i.mutation_type == 'C')
        if abs(total_d - total_c) > 0.01:
            raise ValueError(
                f'Jurnal tidak balance: Total Debet {total_d:,.2f} ≠ Total Kredit {total_c:,.2f}'
            )
        return v
