# ADR-001: Revisi Amount & Delete Budget Bypass Otorisasi

**Status**: Pending Decision (v1: Accept Legacy Behavior)
**Tanggal**: 2026-06-15
**Portal**: zakat
**Terkait**: Specs section "Catatan Implementasi" > "Revisi Amount tanpa Otorisasi"

---

## Konteks

Modul Buat Anggaran Baru memiliki 3 jenis operasi transaksi:

| Operasi | Endpoint | Otorisasi | Alasan Legacy |
|---|---|---|---|
| CREATE (Import) | POST /api/budget/import | ✓ Maker-Checker | Perubahan policy baru → harus approval supervisor |
| REVISI AMOUNT | PUT /api/budget/{id}/revise | ✗ Direct Commit | Adjustment operasional → tidak perlu approval |
| DELETE | DELETE /api/budget/{id} | ✗ Direct Commit | Pembatalan → langsung hapus |

**Inkonsistensi**: Alasan operational adjustment vs policy change tidak jelas di legacy. Risiko:
- Audit trail incomplete untuk revisi
- Kemungkinan kesalahan amount tidak terekam
- Supervisor tidak tahu ada revisi (jika perubahan signifikan)

---

## Keputusan

**v1 (2026-06-15)**: **Adopt Legacy Behavior** — Revisi amount dan delete langsung ke DB tanpa otorisasi.

**Alasan**:
1. Migrasi cepat: tidak perlu refactor workflow lama
2. Data integrity tidak risiko (hanya amount, not policy)
3. Dapat dievaluasi post-launch dengan feedback pengguna
4. Audit log bisa ditambah di layer BFF/DB trigger (later)

---

## Alasan

**Menerima legacy pattern**:
- Revisi amount terjadi sering (adjustment biasa) → approval overhead tinggi
- Delete jarang (pembatalan anggaran exceptional) → worth direct commit
- Operasi ini non-critical path (impact ke laporan, bukan transaksi langsung)

**Mitigasi risiko**:
- Hardcode menu auth: hanya SPVKEU/ADMSYS bisa revisi/delete (tidak semua user)
- Tambah `revision_by` + `revision_date` ke table `budget.budgetrevision` (audit trail)
- Log di BFF router setiap revisi/delete (syslog atau DB audit table)
- Dokumentasi jelas di code: why bypass

---

## Konsekuensi

**Positif**:
- Migrasi selesai lebih cepat (tidak perlu refactor otorisasi workflow)
- UX lebih lancar untuk adjustment rutin
- Backward-compatible dengan legacy behavior

**Negatif**:
- Audit trail incomplete (revisi tidak tercatat di otorisasi.submission)
- Risk: supervisor tidak notified jika ada revisi signifikan
- Maintenance burden: harus ingat ini exception di code review

---

## Alternatif Dipertimbangkan

### Opsi 2: Strict Otorisasi (Semua via Maker-Checker)

```
CREATE (import) → PENDING → AUTHORIZED
REVISI amount   → PENDING → AUTHORIZED (same workflow)
DELETE          → PENDING → AUTHORIZED
```

**Pro**: Konsisten, audit trail lengkap, supervisor control penuh
**Con**: Breaking change, UX lambat, perlu refactor approval logic per operation

### Opsi 3: Hybrid (Revisi OK, Delete Harus Approval)

```
CREATE → approval required
REVISI → direct commit (operational)
DELETE → approval required (destructive)
```

**Pro**: Balance antara agility dan control
**Con**: Masih inkonsisten, lebih kompleks

---

## Plan Tindak Lanjut (Sprint Mendatang)

1. **Collect feedback** dari pengguna (SPVKEU) setelah go-live
   - Apakah revisi sering terjadi?
   - Apakah ada kesalahan amount yg fatal?

2. **Evaluate opsi 2 atau 3** berdasarkan feedback

3. **Refactor jika diperlukan**:
   - Move revisi/delete ke otorisasi workflow
   - Update BFF routes
   - Migrate data (jika ada revisi sebelumnya)

4. **Add audit logging**:
   - BFF layer: log semua revisi/delete
   - DB trigger: auto-record di `audit_log` table

---

## Decision Owner

- **Lead**: Kepala Tim Teknis / Product Manager
- **Approved**: (signature + date)
- **Implemented**: (sprint + PR link)

