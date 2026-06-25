from __future__ import annotations

from pydantic import BaseModel


class BankAccountItem(BaseModel):
    bank_account_id: int | None = None
    bank_account_no: str | None = None
    bank_account_name: str | None = None
    bank_code: str | None = None


class CommitmentItem(BaseModel):
    commitment_id: int | None = None
    account_no: str | None = None
    commitment_amount: float | None = None


class DonorRow(BaseModel):
    donor_id: int
    donor_no: str | None
    donor_name: str | None
    join_date: str | None
    phone_number: str | None
    status: str | None


class Pagination(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class DonorList(BaseModel):
    rows: list[DonorRow]
    pagination: Pagination


# ── Corporate Detail ──────────────────────────────────────────────────────────

class CorporateDonorDetail(BaseModel):
    donor_id: int
    donor_no: str | None
    donor_name: str | None
    corporation: str | None
    economic_sector: str | None
    siupp: str | None
    join_date: str | None
    npwp: str | None
    npwz: str | None
    status: str | None
    branch_code: str | None
    marketer_id: int | None
    marketer_code: str | None
    marketer_name: str | None
    id_negara: int | None
    country_name: str | None
    id_propinsi: int | None
    province_name: str | None
    address_city: str | None
    address_postal_code: str | None
    address_kecamatan: str | None
    address_kelurahan: str | None
    address_street: str | None
    phone_number: str | None
    fax: str | None
    cp_name: str | None
    cp_phone: str | None
    cp_mobile: str | None
    cp_email: str | None
    bank_accounts: list[BankAccountItem]
    commitments: list[CommitmentItem]


# ── Individual Detail ─────────────────────────────────────────────────────────

class IndividualDonorDetail(BaseModel):
    donor_id: int
    donor_no: str | None
    donor_name: str | None
    identity_number: str | None
    identity_type: str | None
    gender: str | None
    join_date: str | None
    birth_place: str | None
    birth_date: str | None
    religion: int | None
    marital_state: str | None
    mobile_phone: str | None
    phone_number: str | None
    fax: str | None
    email: str | None
    npwp: str | None
    npwz: str | None
    status: str | None
    status_rumah: str | None
    is_internal_employee: str | None
    work_identity_number: str | None
    work_area_id: int | None
    work_area_code: str | None
    work_area_name: str | None
    work_area_id_initial: int | None
    work_area_initial_code: str | None
    work_area_initial_name: str | None
    work_unit: str | None
    work_position: str | None
    work_business_area: str | None
    economic_sector: str | None
    fwork_id: int | None
    fwork_code: str | None
    fwork_name: str | None
    donor_group: str | None
    id_negara: int | None
    country_name: str | None
    id_propinsi: int | None
    province_name: str | None
    address_city: str | None
    address_postal_code: str | None
    address_kecamatan: str | None
    address_kelurahan: str | None
    address_street: str | None
    id_propinsi_office: int | None
    office_province_name: str | None
    office_address: str | None
    office_kelurahan: str | None
    office_kecamatan: str | None
    office_city: str | None
    office_phone_number: str | None
    office_postal_code: str | None
    corporate_name: str | None
    job_position: str | None
    couple_name: str | None
    child: int | None
    marketer_id: int | None
    marketer_code: str | None
    marketer_name: str | None
    branch_code: str | None
    bank_accounts: list[BankAccountItem]
    commitments: list[CommitmentItem]


# ── Create / Update Bodies ────────────────────────────────────────────────────

class CreateUpdateCorporateBody(BaseModel):
    donor_name: str
    corporation: str | None = None
    economic_sector: str | None = None
    siupp: str | None = None
    join_date: str | None = None
    npwp: str | None = None
    npwz: str | None = None
    status: str | None = 'A'
    marketer_id: int | None = None
    id_negara: int | None = None
    id_propinsi: int | None = None
    address_city: str | None = None
    address_postal_code: str | None = None
    address_kecamatan: str | None = None
    address_kelurahan: str | None = None
    address_street: str | None = None
    phone_number: str | None = None
    fax: str | None = None
    cp_name: str | None = None
    cp_phone: str | None = None
    cp_mobile: str | None = None
    cp_email: str | None = None
    branch_code: str | None = None
    bank_accounts: list[BankAccountItem] = []
    commitments: list[CommitmentItem] = []


class CreateUpdateIndividualBody(BaseModel):
    donor_name: str
    identity_number: str | None = None
    gender: str | None = None
    join_date: str | None = None
    birth_place: str | None = None
    birth_date: str | None = None
    religion: int | None = None
    marital_state: str | None = None
    mobile_phone: str | None = None
    phone_number: str | None = None
    fax: str | None = None
    email: str | None = None
    npwp: str | None = None
    npwz: str | None = None
    status: str | None = 'A'
    status_rumah: str | None = None
    is_internal_employee: str | None = 'F'
    work_identity_number: str | None = None
    work_area_id: int | None = None
    work_area_id_initial: int | None = None
    work_unit: str | None = None
    work_position: str | None = None
    work_business_area: str | None = None
    economic_sector: str | None = None
    fwork_id: int | None = None
    donor_group: str | None = None
    id_negara: int | None = None
    id_propinsi: int | None = None
    address_city: str | None = None
    address_postal_code: str | None = None
    address_kecamatan: str | None = None
    address_kelurahan: str | None = None
    address_street: str | None = None
    id_propinsi_office: int | None = None
    office_address: str | None = None
    office_kelurahan: str | None = None
    office_kecamatan: str | None = None
    office_city: str | None = None
    office_phone_number: str | None = None
    office_postal_code: str | None = None
    corporate_name: str | None = None
    job_position: str | None = None
    couple_name: str | None = None
    child: int | None = None
    marketer_id: int | None = None
    branch_code: str | None = None
    bank_accounts: list[BankAccountItem] = []
    commitments: list[CommitmentItem] = []


class ToggleStatusBody(BaseModel):
    status: str


# ── Lookup schemas ────────────────────────────────────────────────────────────

class ProvinceLookupItem(BaseModel):
    id_propinsi: int
    province_name: str


class CountryLookupItem(BaseModel):
    id_negara: int
    country_name: str


class MarketerLookupItem(BaseModel):
    marketer_id: int
    marketer_code: str | None
    marketer_name: str | None


class FieldOfWorkLookupItem(BaseModel):
    fwork_id: int
    fwork_code: str | None
    fwork_name: str | None
    fnpwz_code: str | None


class WorkAreaLookupItem(BaseModel):
    work_area_id: int
    work_area_code: str | None
    work_area_name: str | None
