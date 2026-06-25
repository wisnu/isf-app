# Plan: Konfirmasi Transaksi Donasi
**Dibuat**: 2026-06-26
**Target Portal**: zakat

## Urutan Eksekusi

Layer 1–2 bisa paralel. Layer 3–5 sequential (3→4→5 dependency).

---

## Layer 1 — DB / DWH (nuwis-db-migrator, haiku)

Tidak ada migration baru (semua tabel sudah ada). Opsional: buat DWH view jika akan ada laporan donor transaction.

- [ ] `infra/db/migrations/dwh/v_donor_transaction_confirm.sql` — view dwh.v_donor_transaction_confirm (opsional, jika ada laporan mendatang)

**Catatan**: Jika skip DWH view sekarang, dapat ditambah later saat fitur laporan.

---

## Layer 2 — Seed (nuwis-seed-gen, haiku)

Daftarkan menu key dan role assignment di auth DB.

- [ ] `infra/db/migrations/seed/menu-fundraising-donation-confirm.sql`
   - INSERT menu rows (5 key: view + delete + post + print + edit_donor)
   - INSERT role_menu_permission rows (ADMIN: view, FUND: view+delete+edit_donor, SPVFUND: view+delete+post+print+edit_donor)
   - Terapkan ke both portals: `isf_auth_zakat`

**Apply setelah selesai**:
```bash
psql -U transaction -d isf_auth_zakat -f infra/db/migrations/seed/menu-fundraising-donation-confirm.sql
```

---

## Layer 3 — API Python (nuwis-python-builder, haiku)

Router + service + schema untuk donation confirm endpoints.

- [ ] `apps_zakat/api-python/app/modules/fundraising/donation_confirm_router.py`
   - GET /api/fundraising/donation-confirm — list + filter + pagination
   - DELETE /api/fundraising/donation-confirm/{transaction_id} — cascade delete
   - POST /api/fundraising/donation-confirm/{transaction_id}/post-journal — create journal
   - GET /api/fundraising/donation-confirm/{transaction_id}/receipt — generate kwitansi
   - PUT /api/fundraising/donation-confirm/{transaction_item_id}/donor — edit donor

- [ ] `apps_zakat/api-python/app/modules/fundraising/donation_confirm_service.py`
   - `list_transactions()` — query dengan DISCRIMINATOR mutationtype='C' AND transactioncode IN ('SD001','SD002')
   - `delete_transaction()` — BEGIN/DELETE cascade/COMMIT dengan validasi
   - `post_journal()` — CreateJournal() → services/transaction_handler
   - `get_receipt()` — GetKwitansi() → Voucher.GetKwitansiVoucherDebet
   - `update_donor()` — UPDATE accounttransactionitem SET donorid

- [ ] `apps_zakat/api-python/app/modules/fundraising/donation_confirm_schema.py`
   - TransactionFilterParams (begin_date, end_date, branch_code, is_all_branch, search_category, search_text, amount_from, amount_to, description, limit, page)
   - DonationTransactionRow (transaction_id, transaction_no, actual_date, donor_no, donor_name, amount, description, branch_code, branch_name, channel_name, channel_code, product_name, auth_status, is_posted, transaction_item_id)
   - PostJournalRequest, UpdateDonorRequest

- [ ] `apps_zakat/api-python/app/modules/fundraising/donation_confirm_repo.py` (jika query kompleks, pisahkan ke repo)
   - `fetch_transactions()` — query transaction + transactionitem + accounttransactionitem + financialaccount x2 + donor + cabang dengan 5-table JOIN

- [ ] Daftarkan router di `apps_zakat/api-python/app/main.py`
   - `app.include_router(donation_confirm_router.router, prefix="/api/fundraising")`

---

## Layer 4 — BFF (nuwis-bff-builder, haiku)

Proxy routes + auth guards ke api-python.

- [ ] `apps_zakat/bff-api/app/routers/fundraising_donation_confirm.py`
   - GET /api/fundraising/donation-confirm → @require_menu('fundraising.donation.confirm') → proxy + _resolve_branch
   - DELETE /api/fundraising/donation-confirm/{transaction_id} → @require_menu('fundraising.donation.confirm.delete')
   - POST /api/fundraising/donation-confirm/{transaction_id}/post-journal → @require_menu('fundraising.donation.confirm.post')
   - GET /api/fundraising/donation-confirm/{transaction_id}/receipt → @require_menu('fundraising.donation.confirm.print')
   - PUT /api/fundraising/donation-confirm/{transaction_item_id}/donor → @require_menu('fundraising.donation.confirm.edit_donor')

- [ ] Daftarkan router di `apps_zakat/bff-api/app/main.py`
   - `app.include_router(fundraising_donation_confirm.router)`

---

## Layer 5 — Frontend (nuwis-ui-builder, haiku)

Vue 3 halaman list + filter + DataTable + action modals.

- [ ] `apps_zakat/web-vue/src/modules/fundraising/views/DonationConfirmPage.vue`
   - Layout: filter panel (atas) + pagination + DataTable (bawah) + action modals
   - Filter fields: begin_date, end_date, branch_code, is_all_branch, search_category, search_text, amount_from, amount_to, description, limit
   - DataTable kolom: transaction_no, actual_date (dmy), donor_no, donor_name, channel_name, product_name, amount (format), description, branch_name, auth_status (badge), is_posted (badge), [action buttons]
   - Action buttons: Hapus (conditional), Jurnal (conditional), Kwitansi (conditional), Edit Donatur (conditional)
   - Modal konfirmasi: ReadOnlyForm (untuk delete), POST form (untuk post journal), Edit form (untuk edit donor)
   - Pagination: standalone Paginator di atas DataTable
   - No auto-load on mount → empty state sampai "Tampilkan" ditekan

- [ ] Register menu key di `apps_zakat/web-vue/src/shared/constants/menu-keys.ts`
   - `fundraising.donation.confirm`
   - `fundraising.donation.confirm.delete`
   - `fundraising.donation.confirm.post`
   - `fundraising.donation.confirm.print`
   - `fundraising.donation.confirm.edit_donor`

- [ ] Register route di `apps_zakat/web-vue/src/modules/fundraising/routes.ts`
   - `/fundraising/donation-confirm` → DonationConfirmPage (meta.domain='fundraising', meta.menu_key='fundraising.donation.confirm')

- [ ] Register menu sidebar di `apps_zakat/web-vue/src/modules/fundraising/menu.ts`
   - DomainConfig — tambah child di group (misal di "Penghimpunan" atau "Transaksi")
   - Label: "Konfirmasi Transaksi Donasi", menu_key: "fundraising.donation.confirm"

- [ ] Update sidebar di `apps_zakat/web-vue/src/layouts/AppSidebar.vue` (jika group "Penghimpunan" belum ada)
   - Tambah menu group baru atau masukkan ke group existing

---

## Layer 6 — Test (nuwis-test-gen, haiku)

E2E smoke test script.

- [ ] `testing/e2e-donation-confirm.sh`
   - Test list (GET dengan berbagai filter — date, branch, donor, amount, description)
   - Test delete (DELETE dengan validasi branch + auth_status)
   - Test post journal (POST post-journal dengan cek is_posted flag berubah)
   - Test receipt (GET receipt → check HTTP 200 + PDF header)
   - Test edit donor (PUT donor → verify grid update)

- [ ] `apps_zakat/api-python/tests/test_donation_confirm_service.py` (jika logic delete cascade kompleks)
   - Unit test: service methods dengan mock DB
   - Test cascade delete: verify semua tabel terpengaruh ter-delete

---

## Verifikasi

```bash
# Restart container setelah semua layer selesai
cd infra
podman-compose -f docker-compose.zakat.yml restart api-python bff-api web-vue
sleep 5

# Jalankan E2E smoke test
bash testing/e2e-donation-confirm.sh

# Manual test di browser
# 1. Login http://localhost:5173 → username SPVFUND, password test1234
# 2. Navigate ke Fundraising > Konfirmasi Transaksi Donasi
# 3. Isi filter (tanggal hari ini, cabang 001, limit 50) + klik Tampilkan
# 4. Verifikasi list muncul (hanya mutationtype='C' + transactioncode IN ('SD001','SD002'))
# 5. Test aksi:
#    - Hapus baris dengan auth_status='F' (jika punya permisi delete)
#    - Klik Jurnal pada baris dengan auth_status='T' dan is_posted='F'
#    - Klik Kwitansi pada baris dengan auth_status='T'
#    - Klik Edit Donatur, ubah donor, simpan
# 6. Verifikasi toast messages dan tabel refresh otomatis
# 7. Verifikasi aksi tidak visible jika user tidak punya menu_key (FUND tidak lihat Jurnal, dll)
```

**Acceptance Criteria**:
- [ ] E2E smoke test passed (curl checks)
- [ ] List halaman tampil dengan empty state on mount
- [ ] Filter "Tampilkan" load data dengan pagination
- [ ] Delete cascade works (verify transactionitem/accounttransactionitem ter-delete)
- [ ] Post journal updates is_posted flag
- [ ] Receipt download berfungsi (PDF/RTF diterima)
- [ ] Edit donor updates grid live
- [ ] Validasi branch: FUND tidak bisa delete cabang lain
- [ ] Validasi auth_status: FUND tidak bisa delete auth_status='T'
- [ ] Manual login + CRUD di browser — semua menu key gated dengan benar

---

## Notes

- **Menu key consistency**: setiap menu_key di layer 5 (routes.ts, menu.ts, shared/constants/menu-keys.ts) harus match dengan seed SQL di layer 2
- **Cascade delete pattern**: di api-python service, gunakan transaction context (BEGIN/COMMIT/ROLLBACK) seperti yang dilakukan di legacy Transaction.OnDelete()
- **Journal posting**: jika accounting subsystem (services/transaction_handler) blocking, consider BackgroundTask pattern — respond immediately, post di background
- **Receipt generation**: Voucher.GetKwitansiVoucherDebet pattern sudah ada di legacy — adapt ke api-python (baca stream RTF/PDF dari template atau generate dinamis)
- **Donor update**: UpdateDonor tidak perlu otorisasi — dapat diubah anytime sebelum posting jurnal
