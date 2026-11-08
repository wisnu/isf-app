# Bug Fix Plan: Dispatcher Otorisasi `coa` & `kas`

**Dibuat**: 2026-11-08
**Sumber**: ditemukan saat verifikasi faktual `docs/reference/prd/PRD_Portal_ZISWAF_v1.0.md` (lihat revision history v1.2–v1.3)

---

## Masalah

Form **Tambah COA** dan **Tambah Kas** (`finance.coa`, `finance.cash`) mengirim submission ke alur
otorisasi terpusat (`POST /api/finance/monitoring/authorization/save-and-submit/` dengan
`entity_type: 'coa'` / `entity_type: 'kas'`), dan kedua entity type ini **sudah** terdaftar di
`otorisasi.entity_config` (`infra/db/migrations/seed/seed-otorisasi-entity-config.sql:8-9`).

Tapi di `_register_defaults()` — `apps_zakat/api-python/app/modules/finance/monitoring/authorization/service.py` —
tidak ada `register_dispatcher('coa', ...)` maupun `register_dispatcher('kas', ...)`. Kode bahkan
punya komentar eksplisit yang mengakui ini:

```python
# coa, kas dispatcher ditambahkan saat modul master tersedia
```

### Dampak

1. Submission `coa`/`kas` berhasil dibuat (`DRAFT` → `PENDING`) karena `entity_config` ada.
2. Supervisor bisa approve → status pindah ke `PROCESSING`.
3. Saat dispatcher di-resolve untuk `entity_type='coa'`/`'kas'`, tidak ditemukan → dispatch gagal
   → status **kembali ke `PENDING`** dengan `dispatch_error` terisi (sesuai mekanisme recovery yang
   didokumentasikan di `CLAUDE.md` §Otorisasi System).
4. Submission ini akan **stuck permanen** di `PENDING`/`dispatch_error` — tidak pernah
   `AUTHORIZED`, dan baris COA/Kas yang baru **tidak pernah benar-benar dibuat** di tabel legacy.
5. Secara UX: user dapat toast sukses ("Permintaan tambah COA/kas dikirim untuk otorisasi") yang
   menyesatkan — tidak ada indikasi bahwa transaksi ini tidak akan pernah selesai.

### Temuan tambahan (di luar scope dispatcher, dicatat agar tidak hilang)

`CashListView.vue` (`apps_zakat/web-vue/src/modules/finance/views/master/cash/CashListView.vue:24-41`)
**100% hardcoded dummy data** (`const accounts: KasAccount[] = [...]`) — tidak ada pemanggilan API
sama sekali, berbeda dari `CoaListView.vue` dan `BankListView.vue` yang sudah fetch dari endpoint
nyata (`/api/finance/master/coa/accounts`, `/api/finance/master/bank/accounts`). Artinya menu
**Master Kas belum punya backend list endpoint sama sekali** — ini pekerjaan yang lebih besar dari
sekadar daftarkan dispatcher. Rekomendasi: jadikan sub-task terpisah, lihat §Scope di bawah.

---

## Scope

- [ ] **In scope**: dispatcher `coa` — implementasi `create_from_payload` + registrasi, agar approval
      submission COA benar-benar membuat row di tabel COA legacy dan mencapai `AUTHORIZED`.
- [ ] **In scope**: dispatcher `kas` — implementasi `create_from_payload` + registrasi, SETELAH modul
      backend Kas (list + target table) ada. Lihat catatan di bawah — kemungkinan kas perlu modul
      baru `finance/master/cash/` (saat ini tidak ada direktorinya sama sekali, hanya `petty_cash/`).
- [ ] **Out of scope** (sub-task terpisah bila disetujui): bangun endpoint list/detail Master Kas
      (`GET /api/finance/master/cash/accounts`) untuk mengganti dummy data di `CashListView.vue`.

---

## Investigasi Awal

### COA

- Router saat ini (`apps_zakat/api-python/app/modules/finance/master/coa/router.py`) **hanya** punya
  `GET /accounts` dan `GET /accounts.xlsx` — tidak ada endpoint tulis sama sekali. Semua tulis COA
  lewat otorisasi (sesuai desain), jadi dispatcher adalah satu-satunya jalur insert.
- Payload dari `CoaCreateView.vue`:
  ```json
  { "action": "create", "code": "...", "name": "...", "type_code": "A|L|E|I|X", "parent": "...|null", "is_detail": true }
  ```
- Perlu ditentukan: tabel legacy target untuk insert COA baru (`transaction.account` atau sejenis —
  cross-check ke `coa/service.py` query `list_accounts`/`list_all_rows` untuk tabel sumbernya), dan
  sequence/nomor akun yang dipakai (ikuti pola `bank/service.py:269-284` — pakai `nextval()` sequence
  legacy, bukan bikin sequence baru, sesuai constraint §6.2 PRD).

### Kas

- Tidak ada modul `finance/master/cash/` di `api-python` sama sekali — cek apakah "Kas" ini
  sebenarnya row di tabel `cashaccount` yang sama dengan Bank (dibedakan oleh flag tertentu, mirip
  pola `is_amil_account` di `bank/service.py`), atau tabel terpisah. **Harus dikonfirmasi ke domain
  lead / baca legacy DAF sebelum implementasi** — jangan asumsikan skema.
- Payload dari `CashCreateView.vue` perlu dibaca lengkap untuk tahu field apa saja yang dikirim
  (baru dicek baris submit-nya, belum seluruh form).

---

## Rencana Fix

1. [ ] Baca `coa/service.py` penuh untuk identifikasi tabel & kolom target insert COA.
2. [ ] Implementasikan `create_from_payload(payload, user_id, branch_code) -> str` di
       `coa/service.py`, pola serupa `bank_service.create_from_payload` (ambil sequence legacy,
       insert, return id/kode akun baru untuk `result_entity_id`).
3. [ ] Registrasi: tambah `from app.modules.finance.master.coa import service as coa_service` dan
       `register_dispatcher('coa', coa_service.create_from_payload)` di `_register_defaults()`.
4. [ ] Untuk Kas: konfirmasi dulu skema target (lihat Investigasi di atas) — bila ternyata cukup
       mirip Bank (field berbeda tipis), evaluasi reuse `bank_service.create_from_payload` dengan
       parameter berbeda, atau buat modul `finance/master/cash/service.py` baru.
5. [ ] Registrasi `register_dispatcher('kas', ...)` setelah service tersedia.
6. [ ] Hapus komentar TODO `# coa, kas dispatcher ditambahkan saat modul master tersedia`.
7. [ ] **Recovery data lama**: cek apakah sudah ada submission `coa`/`kas` yang stuck di
       `PENDING`/`dispatch_error` di DB produksi/staging sebelum fix ini — bila ada, perlu
       re-approve manual setelah dispatcher terdaftar (lihat prosedur recovery `CLAUDE.md`).
8. [ ] E2E smoke test: submit COA baru → approve → verifikasi status `AUTHORIZED` dan row baru
       muncul di `GET /api/finance/master/coa/accounts`. Sama untuk Kas.
9. [ ] Update PRD (`docs/reference/prd/PRD_Portal_ZISWAF_v1.0.md` §7.1.2, OTO-07, OTO-13) — status
       COA/Kas naik kembali ke ✅ setelah fix ini selesai & terverifikasi.

---

## Testing Checklist

```bash
# Backend
cd apps_zakat/api-python && pytest tests/ -k "coa or kas" -v   # bila test ada/dibuat

# Manual E2E (ikuti testing/e2e-*.sh convention bila dibuat)
# 1. Login sebagai ACC/KEU → Tambah COA baru → submit
# 2. Login sebagai SPVACC/SPVKEU → approve submission COA di halaman Otorisasi
# 3. Tunggu auto-refresh / refresh manual → status harus AUTHORIZED (bukan stuck PENDING)
# 4. Buka Master COA list → akun baru harus muncul
# 5. Ulangi langkah 1-4 untuk Kas
```
