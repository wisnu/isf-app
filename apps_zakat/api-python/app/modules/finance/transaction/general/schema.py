"""Pydantic schemas for Transaksi Umum (GT - General Transaction)."""
from __future__ import annotations

from typing import Annotated, Union, Literal
from pydantic import BaseModel, Field, field_validator


# Item type 'G' — GL/Ledger (existing)
class ItemGL(BaseModel):
    item_type: Literal['G']
    account_code: str       # kode COA (refaccountno)
    account_name: str       # nama akun (refaccountname)
    mutation_type: str      # 'D' | 'C'
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


# Item type 'B' — Kas/Bank
class ItemKasBank(BaseModel):
    item_type: Literal['B']
    account_no: str         # nomor rekening kas/bank (dari financialaccount)
    account_name: str       # nama rekening
    mutation_type: str      # 'D' | 'C'
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


# Item type 'C' — Penghimpunan (Donor)
class ItemPenghimpunan(BaseModel):
    item_type: Literal['C']
    product_account_no: str   # nomor rekening produk ZIS
    product_name: str         # nama produk
    donor_id: int = 0         # 0 = HAMBA ALLAH (anonymous)
    donor_name: str = 'HAMBA ALLAH'
    fund_entity: int          # 1=Zakat,2=Infaq,3=Wakaf,4=Amil,5=Non-halal
    amount: float
    description: str = ''
    is_reversal: bool = False

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('amount harus lebih dari 0')
        return v

    @field_validator('fund_entity')
    @classmethod
    def validate_fund_entity(cls, v: int) -> int:
        if v not in (1, 2, 3, 4, 5):
            raise ValueError('fund_entity harus 1-5 (Zakat/Infaq/Wakaf/Amil/Non-halal)')
        return v


# Item type 'D' — Penyaluran
class ItemPenyaluran(BaseModel):
    item_type: Literal['D']
    dist_account_no: str    # nomor rekening program penyaluran
    dist_account_name: str  # nama program
    fund_account_no: str    # nomor rekening sumber dana
    fund_account_name: str  # nama sumber dana
    ashnaf: str             # 'F'/'M'/'U'/'H'/'G'/'S'/'I'/'A'
    fund_entity: int        # 1=Zakat,2=Infaq,3=Wakaf,4=Amil,5=Non-halal
    mutation_type: str      # 'D' | 'C' (usually 'D' for distribution)
    amount: float
    description: str = ''
    is_correction: bool = False

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

    @field_validator('ashnaf')
    @classmethod
    def validate_ashnaf(cls, v: str) -> str:
        if v.upper() not in ('F', 'M', 'U', 'H', 'G', 'S', 'I', 'A'):
            raise ValueError("ashnaf harus F/M/U/H/G/S/I/A")
        return v.upper()

    @field_validator('fund_entity')
    @classmethod
    def validate_fund_entity(cls, v: int) -> int:
        if v not in (1, 2, 3, 4, 5):
            raise ValueError('fund_entity harus 1-5 (Zakat/Infaq/Wakaf/Amil/Non-halal)')
        return v


# Union dengan discriminator
TransaksiUmumItem = Annotated[
    Union[ItemGL, ItemKasBank, ItemPenghimpunan, ItemPenyaluran],
    Field(discriminator='item_type')
]


class GeneralCreate(BaseModel):
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

        # Calculate totals considering item_type rules
        total_d = 0.0
        total_c = 0.0

        for item in v:
            # Handle both dict and Pydantic model
            if isinstance(item, dict):
                amount = float(item.get('amount', 0))
                item_type = item.get('item_type', '')
                mutation = item.get('mutation_type', '')
            else:
                amount = float(item.amount)
                item_type = item.item_type
                mutation = getattr(item, 'mutation_type', '')

            # Penghimpunan (type 'C') always credits
            if item_type == 'C':
                total_c += amount
            else:
                if mutation == 'D':
                    total_d += amount
                elif mutation == 'C':
                    total_c += amount

        if abs(total_d - total_c) > 0.01:
            raise ValueError(
                f'Jurnal tidak balance: Total Debet {total_d:,.2f} ≠ Total Kredit {total_c:,.2f}'
            )
        return v
