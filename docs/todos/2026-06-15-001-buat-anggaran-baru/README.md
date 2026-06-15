# Budget Management (Buat Anggaran Baru) — Migrasi DAF → isf-app

**Generated**: 2026-06-15 | **Reference ID**: 001-buat-anggaran-baru | **Portal**: zakat
**Status**: Documentation Complete | **Estimasi Implementasi**: 8–10 sprint days

---

## Struktur Dokumentasi

```
docs/todos/2026-06-15-001-buat-anggaran-baru/
├── README.md                           (file ini)
├── specs.md                            ← arsitektur + API contract + database schema
├── plan.md                             ← checklist implementasi per layer
├── MIGRATION_ANALYSIS.md               ← analisis legacy DAF (input reference)
├── adr-001-*.md                        ← ADR: Revisi/Delete bypass otorisasi
├── adr-002-*.md                        ← ADR: BudgetYear discriminator pattern
├── adr-003-*.md                        ← ADR: Item hierarki 2-level
└── testing/
    └── e2e-budget-import.sh            ← template E2E smoke test
```

---

## Ringkasan Fitur

**Modul**: Buat Anggaran Baru (Budget Management)  
**Portal**: zakat  
**Domain**: keuangan + parameter  
**Tipe**: CRUD + Approval (maker-checker) + Excel Import/Export  
**Kompleksitas**: TINGGI (8 tabel, 6 halaman UI, 16+ endpoint, hierarki ganda)

### 6 Fitur Utama

1. **Import Anggaran** — Upload Excel dengan item + amount
2. **Revisi Anggaran** — Edit amount per-item (bypass otorisasi)
3. **Inquiry Anggaran** — Bandingkan budget vs realisasi dengan variance
4. **Master Pemilik Anggaran** — CRUD budget owner (hierarki 2-level)
5. **Master Item Anggaran** — CRUD item/kategori (hierarki 2-level)
6. **Master Periode Anggaran** — CRUD budget period (tahun root)

---

## Quick Start — Developer

### 1. Baca Dokumentasi (Urutan)

1. **specs.md** — Pahami konteks, alur data (Mermaid), endpoint contract, database schema
2. **plan.md** — Lihat checklist implementasi per layer + perkiraan effort
3. **ADR** (opsional) — Review keputusan design (revisi bypass otorisasi, dll)

### 2. Setup Database (Layer 1)

```bash
cd /home/wishnew/workshop/isf-app

# Apply DB migrations
psql -U transaction -d mziss_zakat <<EOF
-- Copy-paste dari infra/db/migrations/V026_*.sql
-- (belum ada file, nuwis-db-migrator akan buat)
EOF
```

### 3. Implementasi Layer-by-Layer

Ikuti order di `plan.md`:

| Layer | Task | File | Durasi |
|---|---|---|---|
| 1 | DB migrations | infra/db/migrations/V026_* | 4 jam |
| 2 | Python API | apps_zakat/api-python/app/modules/budget/ | 6 jam |
| 3 | BFF routes | apps_zakat/bff-api/app/routers/budget.py | 3 jam |
| 4 | Seed SQL | infra/db/migrations/seed/budget-* | 2 jam |
| 5 | Vue pages | apps_zakat/web-vue/src/pages/keuangan/Budget*.vue | 8 jam |
| 6 | E2E tests | testing/e2e-budget-*.sh | 3 jam |

Layers 2–3 dan 5 bisa paralel setelah Layer 1 selesai.

### 4. Testing & Deployment

```bash
# Start containers
cd infra && podman-compose -f docker-compose.zakat.yml up -d

# Run E2E
bash testing/e2e-budget-import.sh --verbose

# Manual QA: Login as SPVKEU (Supervisor Keuangan)
# - Navigate to "Keuangan" > "Anggaran" > "Import Anggaran"
# - Upload sample Excel, trigger otorisasi, verify approval flow
```

---

## Kontak & Ownership

- **Tech Lead / Architect**: (TBA)
- **Backend (API/BFF)**: (assign nuwis-python-builder + nuwis-bff-builder)
- **Frontend (UI)**: (assign nuwis-ui-builder)
- **Database**: (assign nuwis-db-migrator)
- **Test & QA**: (assign nuwis-test-gen)

---

## Key Decisions (ADRs)

### ADR-001: Revisi & Delete Bypass Otorisasi ✓ Accepted

**Decision**: Revisi amount dan delete langsung ke DB (tidak via otorisasi submission).

**Alasan**: Operational adjustment, bukan policy change. v1 adopt legacy, v2 evaluate.

**Status**: Implemented (see implementation notes in plan.md Layer 2-3)

---

### ADR-002: BudgetYear via Discriminator ✓ Accepted

**Decision**: Single table `budget.budget` dengan field `budget_type='Y'|'M'|'Q'`.

**Alasan**: Schema sudah ada, queryable, flexible untuk future types tanpa refactor.

**Status**: Implemented (Layer 1)

---

### ADR-003: Item Hierarki 2-Level via Single Table ✓ Accepted

**Decision**: Single table `budget.budgetitem` dengan `level` + self-referencing `parent_item_id`.

**Alasan**: Migrasi cepat, flexible untuk level 3+ nanti, simpler queries.

**Status**: Implemented (Layer 1)

---

## Catatan Khusus

### ⚠️ Inkonsistensi Otorisasi (ADR-001)

- **CREATE (import)**: via otorisasi.submission → maker-checker PENDING → AUTHORIZED
- **REVISI amount**: direct DB commit (bypass otorisasi) — no submission
- **DELETE**: direct DB commit (bypass otorisasi) — no submission

Ini intentional untuk v1 (operational efficiency), akan dievaluasi v2.

### ⚠️ Monthly Breakdown Inactive

Kolom `amount_01` ... `amount_12` ada di schema tapi tidak dipakai di v1.
Jangan hardcode monthly logic — preserve untuk future activation.

### ⚠️ Bug Legacy: fBudgetImport_data.py baris 241

Nama tabel salah: `BranchCashAccount` seharusnya `Budget`.
Fix: saat implement Layer 2 (api-python), gunakan nama yang benar di log/error handling.

### 📋 Menu Key Registry

Semua menu keys sudah didefinisikan di `specs.md` section "Menu Key Registry".
Sync dengan `src/lib/menu/registry.ts` (Vue) + `isf_auth.menu` table (seed SQL).

---

## Troubleshooting

### Q: API returns 403 MENU_DENIED saat akses /api/budget/import

**A**: User tidak punya menu key `keuangan.anggaran.import`. Verify:
- Role di `isf_auth_zakat.role_menu` includes menu `keuangan.anggaran.import`
- Seed SQL sudah applied: `psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/budget-menu-and-rolemenu.sql`

### Q: Excel upload stuck di PENDING status

**A**: Background dispatcher mungkin crash. Check:
- Logs: `podman logs isf-zakat-api-python | grep -i budget`
- `dispatch_error` column di `otorisasi.submission` untuk error message
- Manual fix: `UPDATE otorisasi.submission SET status='PENDING' WHERE status='PROCESSING' AND id={id};`

### Q: Revisi amount tidak muncul di UI

**A**: Check BFF route `/api/budget/{id}/revise` return structure. Verify:
- Response includes `revision_number`, `revision_date`, `items_revised`
- UI properly extract dan display toast message

---

## Known Limitations (v1)

1. **No monthly breakdown** — `amount_01...12` columns inactive
2. **Single owner per budget** — tidak support shared ownership (future: redesign owner model)
3. **No budget template** — copy-budget feature belum ada
4. **No historical audit** — revisi/delete tidak tercatat di submission (v2 add audit logging)
5. **Excel validation basic** — hanya duplikat + FK check, tidak validate business rules

---

## Next Steps (v2+)

- [ ] Evaluate ADR-001: Consider making revisi/delete go through otorisasi
- [ ] Implement audit logging (BFF layer + DB trigger)
- [ ] Add budget template / copy-budget feature
- [ ] Support monthly breakdown (amount_01...12)
- [ ] Laporan anggaran (dwh views + MkDocs user guide)
- [ ] Performance optimization (index tuning, query caching)

---

## Reference Material

### Legacy DAF Source

- **TRANS031**: Master Pemilik Anggaran (fBudgetOwner)
- **TRANS032**: Master Item Anggaran (fBudgetItem)
- **TRANS033**: Master Periode Anggaran (fBudgetPeriod)
- **TRANS036**: Import Anggaran (fBudgetImport)
- **TRANS037**: Revisi Anggaran (fBudgetRevision)
- **TRANS038**: Buat Anggaran Baru (fBudgetNew)
- **TRANS039**: Inquiry Anggaran (fBudgetInquiry)

See `MIGRATION_ANALYSIS.md` for detailed field mapping.

### isf-app Documentation

- [CLAUDE.md](/CLAUDE.md) — Project conventions, tech stack, workflow
- [architecture.md](/docs/architecture.md) — System topology, layer boundaries
- [Otorisasi System](/CLAUDE.md#otorisasi-system-maker-checker-workflow) — maker-checker pattern

---

## File Checksums (Verification)

```
specs.md                                      947 lines
plan.md                                       573 lines
adr-001-revisi-delete-bypass-otorisasi.md     118 lines
adr-002-budget-year-subclass-vs-inheritance.md 193 lines
adr-003-hierarki-item-2level.md               243 lines
testing/e2e-budget-import.sh                  293 lines
```

Total: ~2,925 lines of documentation + code template

---

## Approval & Sign-Off

**Generated by**: nuwis-doc-gen (2026-06-15 13:45 UTC)  
**Reviewed by**: (TBA)  
**Approved by**: (TBA)  

**Status**: ✅ Ready for Implementation Handoff

---

*Last updated: 2026-06-15*
