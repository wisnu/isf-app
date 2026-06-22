from __future__ import annotations

from pydantic import BaseModel
from typing import Optional


class DocumentTypeRow(BaseModel):
    id_jenis_dokumen: int
    kode_jenis_dokumen: str
    nama_jenis_dokumen: str


class DocumentTypeDetail(BaseModel):
    id_jenis_dokumen: int
    kode_jenis_dokumen: str
    nama_jenis_dokumen: str


class CreateDocumentTypeBody(BaseModel):
    kode_jenis_dokumen: str
    nama_jenis_dokumen: str


class DisposisiItem(BaseModel):
    tanggal: Optional[str] = None
    disposisi_oleh: Optional[str] = None
    keterangan_disposisi: Optional[str] = None


class DisposisiCreate(BaseModel):
    tanggal: Optional[str] = None
    disposisi_oleh: Optional[str] = None
    keterangan_disposisi: Optional[str] = None


class IncomingDocumentRow(BaseModel):
    dokumen_id: int
    nomor: Optional[str] = None
    pengirim: Optional[str] = None
    perihal: Optional[str] = None
    tanggal_dokumen: Optional[str] = None
    tanggal_terima: Optional[str] = None
    nama_jenis_dokumen: Optional[str] = None
    branch_code: Optional[str] = None


class IncomingDocumentDetail(BaseModel):
    dokumen_id: int
    nomor: Optional[str] = None
    pengirim: Optional[str] = None
    perihal: Optional[str] = None
    tanggal_dokumen: Optional[str] = None
    tanggal_terima: Optional[str] = None
    nama_jenis_dokumen: Optional[str] = None
    ditujukan_ke: Optional[str] = None
    nomor_eksternal: Optional[str] = None
    keterangan: Optional[str] = None
    branch_code: Optional[str] = None
    disposisi: list[DisposisiItem] = []


class CreateIncomingBody(BaseModel):
    id_jenis_dokumen: int
    pengirim: str
    perihal: str
    ditujukan_ke: Optional[str] = None
    nomor_eksternal_dokumen: Optional[str] = None
    tanggal_dokumen: str
    tanggal_terima: str
    keterangan: Optional[str] = None
    disposisi: list[DisposisiCreate] = []
    user_input: str = 'system'
    branch_code: str = '001'


class UpdateIncomingBody(BaseModel):
    id_jenis_dokumen: int
    pengirim: str
    perihal: str
    ditujukan_ke: Optional[str] = None
    nomor_eksternal_dokumen: Optional[str] = None
    tanggal_dokumen: str
    tanggal_terima: str
    keterangan: Optional[str] = None
    disposisi: list[DisposisiCreate] = []
    user_input: str = 'system'


class OutgoingDocumentRow(BaseModel):
    dokumen_id: int
    nomor: Optional[str] = None
    pic: Optional[str] = None
    tujuan: Optional[str] = None
    perihal: Optional[str] = None
    tanggal_dokumen: Optional[str] = None
    tanggal_kirim: Optional[str] = None
    work_unit_id: Optional[str] = None
    work_unit_desc: Optional[str] = None
    nama_jenis_dokumen: Optional[str] = None
    status_kirim: Optional[str] = None
    branch_code: Optional[str] = None


class OutgoingDocumentDetail(BaseModel):
    dokumen_id: int
    nomor: Optional[str] = None
    pic: Optional[str] = None
    tujuan: Optional[str] = None
    perihal: Optional[str] = None
    tanggal_dokumen: Optional[str] = None
    tanggal_kirim: Optional[str] = None
    work_unit_id: Optional[str] = None
    work_unit_desc: Optional[str] = None
    nama_jenis_dokumen: Optional[str] = None
    status_kirim: Optional[str] = None
    konseptor: Optional[str] = None
    keterangan: Optional[str] = None
    branch_code: Optional[str] = None


class CreateOutgoingBody(BaseModel):
    id_jenis_dokumen: int
    work_unit_id: str
    pic: str
    konseptor: Optional[str] = None
    tanggal_dokumen: str
    tanggal_kirim: Optional[str] = None
    perihal: str
    tujuan: str
    keterangan: Optional[str] = None
    user_input: str = 'system'
    branch_code: str = '001'


class UpdateOutgoingBody(BaseModel):
    id_jenis_dokumen: int
    work_unit_id: str
    pic: str
    konseptor: Optional[str] = None
    tanggal_dokumen: str
    tanggal_kirim: Optional[str] = None
    perihal: str
    tujuan: str
    keterangan: Optional[str] = None
    status_kirim: Optional[str] = None
    user_input: str = 'system'


class Pagination(BaseModel):
    page: int
    page_size: int
    total: int
    total_pages: int


class DocumentTypeListResponse(BaseModel):
    rows: list[DocumentTypeRow]
    pagination: Pagination


class IncomingDocumentListResponse(BaseModel):
    rows: list[IncomingDocumentRow]
    pagination: Pagination


class OutgoingDocumentListResponse(BaseModel):
    rows: list[OutgoingDocumentRow]
    pagination: Pagination


class WorkUnitLookupItem(BaseModel):
    work_unit_id: str
    description: str
