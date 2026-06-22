# Skill: nuwis-skill-parity-check
## Metodologi Validasi Parity Legacy vs ISF-App

---

## Tujuan

Memastikan implementasi isf-app mencakup SEMUA behavior legacy DAF yang relevan.
Bukan 100% reproduksi — beberapa hal sengaja diubah/disederhanakan — tapi setiap
perbedaan harus disengaja dan terdokumentasi.

---

## 5 Dimensi Validasi

### Dimensi 1: Field Coverage

**Sumber**: `MIGRATION_ANALYSIS.FORM_FIELDS`
**Target**: Vue form + Pydantic schema + DB columns

Checklist per field:
```
□ Ada di Vue form (v-model)
□ Ada di Pydantic schema (Create{Resource})
□ Ada di DB kolom (atau sudah ada di tabel yang direferensikan)
□ Type cocok (Date→DateField, Currency→Decimal, dll)
□ Required/Optional sesuai legacy
□ ReadOnly fields tidak ditampilkan sebagai editable input
```

### Dimensi 2: Role Coverage

**Sumber**: `MIGRATION_ANALYSIS.FITUR_LIST[].ROLES`
**Target**: `isf_auth.role_menu`

```sql
-- Verifikasi:
SELECT rm.role_code, m.menu_key
FROM isf_auth.role_menu rm
JOIN isf_auth.menu m ON m.menu_key = rm.menu_key
WHERE m.menu_key LIKE '{domain}.%'
ORDER BY m.menu_key, rm.role_code;
```

### Dimensi 3: Discriminator Coverage (KRITIS)

**Sumber**: `MIGRATION_ANALYSIS.DISCRIMINATORS`
**Target**: SQL query di service.py / DWH view

**Ini yang paling sering menyebabkan bug production.**

```python
# Cari di service.py:
grep -n "accounttitype\|accountreceivabletype\|authstatus" \
  apps_{portal}/api-python/app/modules/{domain}/service.py
```

Setiap discriminator HARUS hardcoded sebagai kondisi WHERE, bukan parameter.

### Dimensi 4: Save Logic Coverage

**Sumber**: `MIGRATION_ANALYSIS.SAVE_LOGIC`
**Target**: service.py atau otorisasi dispatcher

Checklist:
```
□ Main INSERT/UPDATE ada
□ CreateJournal → accounting_service.create_journal() (jika ada)
□ Transaction wrap (async with db.transaction())
□ Error handling (try/except/rollback)
□ Branch context disertakan
```

### Dimensi 5: UI Flow Coverage

**Sumber**: `MIGRATION_ANALYSIS.UI_FLOW`
**Target**: Vue page onMounted + form interactions

```
□ Pre-fill fields dari session (tanggal hari ini, branch, user)
□ Dropdown/lookup yang ada di legacy → SearchSelect atau GET endpoint
□ Client-side validasi ada (atau Pydantic schema menggantikannya)
□ Toast feedback setelah save
```

---

## Cara Membaca Parity Report

### Status Icons

| Icon | Arti |
|---|---|
| ✅ | Terimplementasi dengan benar |
| ❌ | Hilang — harus diimplementasi |
| ⚠️ | Ada tapi berbeda (nama/type/behavior) — perlu konfirmasi |
| ❓ | Tidak bisa dikonfirmasi (file tidak ditemukan) |

### Severity Tiers

| Tier | Kondisi | Tindakan |
|---|---|---|
| 🔴 CRITICAL | Discriminator hilang, data corruption possible | Fix sebelum deploy |
| 🔴 CRITICAL | Role tidak ada di seed, user tidak bisa akses | Fix sebelum deploy |
| 🟡 MEDIUM | Field Required menjadi Optional | Fix sebelum release |
| 🟡 MEDIUM | Dropdown lookup hilang dari UI | Fix sebelum release |
| 🟢 LOW | Field Optional hilang, naming berbeda | Bisa fix iterasi berikut |

---

## Template Parity Check Manual

Untuk melakukan parity check secara manual tanpa nuwis-validator:

```bash
# 1. Cek field coverage — bandingkan .svr dengan schema.py:
grep "FieldName=" docs/legacy-apps/{modul}/dialogs/{path}/*.svr | awk -F"'" '{print $2}'
grep ":" apps_{portal}/api-python/app/modules/{domain}/schema.py | grep -v "class\|def\|import"

# 2. Cek discriminator di service.py:
grep -n "WHERE\|AND" apps_{portal}/api-python/app/modules/{domain}/service.py | grep -i "type\|status"

# 3. Cek role di seed:
psql -d isf_auth_zakat -c "SELECT role_code FROM isf_auth.role_menu WHERE menu_key = '{menu_key}'"

# 4. Cek field di Vue form:
grep "v-model" apps_{portal}/web-vue/src/modules/{domain}/views/{subpath}/{Nama}View.vue
```

---

## Yang Sengaja Berbeda (Acceptable Gaps)

Beberapa hal yang sengaja tidak diimplementasi 1:1:

| Legacy Behavior | ISF-App | Alasan |
|---|---|---|
| `config.SecurityContext.UserId` | `session["user_id"]` | Framework baru |
| `config.BeginTransaction()` | `async with db.transaction():` | asyncpg pattern |
| Integer timestamp (`config.Now()`) | ISO date string | Standarisasi |
| Hardcoded branch di form | `_resolve_branch()` | Security |
| Client-side validation di `_intr.py` | Pydantic schema | Validation di server |
| Error message format DAF | `HTTPException` + `err()` | Standarisasi |

Gap-gap ini acceptable dan tidak perlu dilaporkan sebagai issue.
