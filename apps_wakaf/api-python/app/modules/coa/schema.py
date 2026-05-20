from pydantic import BaseModel


# Type code → label mapping (existing DB convention: A/L/E/I/X)
TYPE_LABELS = {
    "A": "Aset",
    "L": "Liabilitas",
    "E": "Saldo Dana",
    "I": "Pendapatan",
    "X": "Penyaluran",
}


class CoaRow(BaseModel):
    code: str
    name: str | None
    type_code: str | None
    type_label: str
    level: int | None
    is_detail: bool
    is_system: bool
    parent: str | None
    balance: float


class CoaStats(BaseModel):
    total: int
    by_type: dict[str, int]


class CoaList(BaseModel):
    rows: list[CoaRow]
    stats: CoaStats
