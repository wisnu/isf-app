# Plan — Refactor BFF + api-python Naming to English

**Slug:** `2026-06-20-002-refactor-naming-english` · Portal: **zakat only** · See [`specs.md`](./specs.md) + [`glossary.md`](./glossary.md)

**Strategy:** vertical slices per domain, ascending risk. Each slice = api-python + bff + web-vue changed together, then `make health` + the domain's `testing/e2e-*.sh` + a browser smoke check before moving on. Naming-only — **no logic/query-result changes**.

**Convention reminders (CLAUDE.md):** `CAST(x AS t)` not `x::t`; never `:paginator`; `DateField`/`dmy()`; menu keys via `registry.ts`; no raw `fetch`. Commit tag: `[REFACTOR-NAMING]`.

---

## Phase 0 — Decisions & freeze (DECIDED 2026-06-20)
- [x] **`entity_type` values → FREEZE.** Treat as opaque codes; no rename, no data migration.
- [x] **`uang_muka_pengembalian` → `cash-advance-settlement`** (canonical).
- [x] **Module consolidation → IN-SCOPE NOW**, pulled forward to **Phase 1** (runs before path/field renames so later work happens in the final tree; leaves URL prefixes untouched → no contract break).
- [x] glossary.md frozen as source of truth.

## Phase 1 — Module consolidation + internal symbols (backend, no contract change) — LOW RISK
**Paths & JSON fields stay Indonesian in this phase** → no FE/contract break. Pure backend restructure + symbol rename. Verify with imports load + `make health` + existing E2E.

### 1a. api-python consolidation (specs §4) — ✅ DONE 2026-06-20 (verified: `import app.main` green, dispatcher keys frozen, zero stale refs)
- [x] Flat-merge `modules/transaksi/*` into `modules/transaction/` with English filenames (cash_advance_*, cash_advance_settlement_*, inter_account_transfer_*, receivable_*, general_*, amil_income_*, hc_zis_*). Renamed `penghimpunan_*→fund_collection_*`, `penyaluran_*→fund_distribution_*`. `transaksi/` removed.
- [x] Rename standalone modules: `kas_kecil/ → petty_cash/`, `otorisasi/ → authorization/`, `transaksi_histori/ → transaction_history/`.
- [x] Rewrote 22 files' imports + `main.py`. URL prefixes kept unchanged (contract-safe).
- [x] Dispatcher registry `entity_type` keys FROZEN; only module import paths fixed.

### 1b. bff consolidation + internal symbols
- [ ] Mirror bff router filenames where it aids clarity (optional; prefixes unchanged).
- [ ] api-python service fns: `create_penghimpunan→create_fund_collection`, `create_penyaluran→create_fund_distribution`, `list_uang_muka→list_cash_advance`, `list_piutang→list_receivable`, `lookup_kasbank→lookup_cash_bank`, `lookup_produk→lookup_product`, `create/update/delete_kas_kecil→…_petty_cash`.
- [ ] bff helpers: `_session→_extract_session`, `_branch_for_session→_resolve_branch_code`, `_inject→_extract_context`, `_period_params→_build_period_params`.
- [ ] Verify: imports load (`python -c`), `make health`; existing E2E still green (paths unchanged).

## Phase 2 — Low-traffic URL path renames (lockstep) — MED RISK
Per domain: rename api-python prefix → bff prefix → bff downstream string → web-vue call string. One domain per commit.
- [x] **petty-cash** (`/kas-kecil`→`/petty-cash`) — ✅ DONE 2026-06-20. api-python prefix+symbols (`KasKecil*→PettyCash*`, `*_kas_kecil→*_petty_cash`), bff `kas_kecil.py→petty_cash.py` + prefix + 8 downstream paths, web-vue 12 call strings + TS interfaces. Fields already English. Verified: imports green, zero stale refs. (E2E script TODO.)
- [x] **budget-owner** (`/parameter/pemilik-anggaran`→`/parameter/budget-owner`) — ✅ DONE 2026-06-20. api-python: path + `{ownerid}→{owner_id}`, SELECT aliases (`ownerid AS owner_id`,`ownercode AS owner_code`,`ownername AS owner_name`,`parentownerid AS parent_owner_id`,`tglubah AS updated_date`,`userpengubah AS updated_by`,`terminalubah AS updated_terminal`), payload-read keys (`owner_code`/`owner_name`/`owner_id`/`parent_owner_id`), dead-code schema.py refreshed. **DB columns untouched in SQL.** bff: path + param. web-vue: 3 files (page + 2 modals) paths+fields; `entity_type:'budget_owner'` frozen. Verified: imports green, grep-clean. **First JSON-field-alias slice — template for Phase 4.**
- [ ] **receivable** (`/piutang`→`/receivable`): bff `piutang.py`, api-python `transaksi/piutang_router.py`, web-vue `ReceivableListPage.vue`/`ReceivableCreatePage.vue`. Sub-path `debitur*→debtor*`.
- [ ] **inter-account-transfer** (`/transaksi/transfer-antar-rekening`→`/transaction/inter-account-transfer`): web-vue `FundTransfer*Page.vue`.
- [ ] **cash-advance** + **cash-advance-return**: web-vue `CashAdvance*Page.vue`, `CashAdvance*FormModal.vue`, LPJ pages.
- [ ] **general-transaction** (`/transaksi-umum`→`/general-transaction`, downstream `/transaksi/umum`→`/transaction/general`): web-vue `GeneralTransaction*Page.vue`. Sub-paths `lookup/kasbank→cash-bank`, `lookup/produk→product`, `lookup/penyaluran→distribution`.

## Phase 3 — High-traffic URL path renames (lockstep) — HIGH RISK
- [ ] **fund-collection** (`/penghimpunan`→`/fund-collection`): bff `penghimpunan.py`, api-python `transaction/router.py`, web-vue `FundCollection*Page.vue` + lookups (`rekening→account`, `produk→product`). Plus batch upload `/transaction/upload/penghimpunan`→`/transaction/upload/fund-collection` (`UploadCollectionMulti*Page.vue`).
- [ ] **fund-distribution** (`/penyaluran`→`/fund-distribution`): web-vue `FundDistribution*Page.vue` + `DashboardDistributionPage.vue` (`/dashboard/penyaluran/*`). Sub-paths `rekening→account`, `produk→product`.
- [ ] **transaction-history** (`/transaksi-histori`→`/transaction-history`): web-vue `TransactionHistory*Page.vue`.
- [ ] **hc-zis upload** (`/transaksi/upload/hc-zis`→`/transaction/upload/hc-zis`): web-vue `UploadCollectionHCZis*Page.vue`.
- [ ] **authorization** (`/otorisasi`→`/authorization`): **28 FE call sites** — `AuthorizationPage.vue`, `SubmissionHistoryPage.vue`, `SubmissionDetailDrawer.vue`, every `*ListPage` `my-submissions`/`submission/{id}` call. Largest single slice; do alone, grep-verify zero `otorisasi` strings remain in `web-vue/src` + `bff-api`. **Note:** `entity_type` query *values* stay frozen.

## Phase 4 — JSON field renames (lockstep, via SELECT alias) — HIGH RISK
Per domain: add `SELECT col AS english` in api-python service + update Pydantic schema + update web-vue TS interface + template binding. Glossary §3.
- [ ] **fund-collection items**: `no_rekening→account_no`, `tanggal→date`, `keterangan→description`, `no_ref→reference_no`, `total_kredit→total_credit`, `pesan→message`, `zakat_profesi→zakat_profession`, `zakat_maal→zakat_wealth`, `zakat_perusahaan→zakat_company`, `infaq_terikat→infaq_restricted`, `anak_yatim→orphan`, `anak_asuh→foster_child`, `titipan_wakaf→waqf_deposit`, `titipan_qurban→qurban_deposit`. **Keep** `zakat_fitrah`, `infaq`, `ashnaf`.
- [ ] **upload ParsedRow**: `rekening→account_no`, `tanggal→date`, `keterangan→description`, `nominal→amount` (`UploadCollectionMultiPage.vue`).
- [ ] **HC-ZIS**: `tanggal_transaksi→transaction_date`, `namafile→filename`, `batch_period_desc→batch_period_description`, `anak_asuh_amount→foster_child_amount`, `anak_yatim_amount→orphan_amount`, `taqurma_amount→qurban_deposit_amount`.
- [ ] **budget-owner**: `ownerid→owner_id`, `ownercode→owner_code`, `ownername→owner_name`, `tglubah→updated_date`, `userpengubah→updated_by`, `terminalubah→updated_terminal`.
- [ ] **amil-income**: `ekuivalen_amount→equivalent_amount`.
- [ ] **transaction-history**: `valuta_code→currency_code` + camelCase→snake_case normalization (glossary §3) — grep report pages for `saldo_awal`/`saldo_akhir`/`mutasi` (`opening_balance`/`closing_balance`/`movement`).
- [ ] **dashboard**: `rekening→account`, `produk→product`, `anggaran→budget`; query params `bulan→month`, `tahun→year`, `tanggal→date`, `jenisperiode→period_type` across `report.py` + report pages.

## Phase 5 — Auth/identity fields (lockstep, single atomic slice) — HIGH RISK
- [ ] api-python `identity/schema.py` + `admin/schema.py`: `id_peran→role_id`, `nama_peran→role_name`, `kode_cabang→branch_code`.
- [ ] bff `auth.py` session-build + `admin.py` role-menu payload.
- [ ] web-vue `stores/auth.ts`, `AppSidebar.vue` menu filtering, `admin/RoleMenuPage.vue`.
- [ ] Verify: full login → RBAC → sidebar → branch-access E2E (users HADI all-branch, RAIS single-branch). **Re-test logout/login** (menus snapshot at login).

## Phase 6 — (MOVED to Phase 1 per 2026-06-20 decision)
Module consolidation now runs first as Phase 1a. This slot intentionally empty.

## Phase 7 — Verify & close
- [ ] Grep guard: zero Indonesian tokens in `apps_zakat/{bff-api,web-vue/src}` paths/fields (penghimpunan, penyaluran, piutang, uang-muka, kas-kecil, transaksi, otorisasi, rekening, produk, pemilik-anggaran) — except frozen `entity_type` values.
- [ ] All `testing/e2e-*.sh` green; browser smoke of each finance page (`/run` or run-isf-app skill).
- [ ] Update CLAUDE.md references (Otorisasi section paths `/otorisasi`→`/authorization`, etc.) + `docs/menu-structure.md` if paths quoted.
- [ ] Write wakaf-mirror follow-up note capturing the same slices for `apps_wakaf`.

---

## Files touched (summary)

**api-python** (`apps_zakat/api-python/app/`): `main.py`; `modules/{kas_kecil,otorisasi,transaksi,transaksi_histori,parameter,identity,admin}/`; `modules/transaction/{penghimpunan,penyaluran}_*`; all `transaksi/*_router.py` + `*_service.py` + `*_schema.py`.
**bff-api** (`apps_zakat/bff-api/app/`): `main.py`; `routers/{penghimpunan,penyaluran,piutang,uang_muka,uang_muka_pengembalian,transfer_antar_rekening,transaksi,transaksi_umum,histori_transaksi,kas_kecil,otorisasi,parameter,transaction,amil_income,auth,admin,dashboard,report}.py`; `services/`.
**web-vue** (`apps_zakat/web-vue/src/`): `pages/finance/*` (fund-collection, fund-distribution, receivable, cash-advance*, general-transaction, transaction-history, fund-transfer, petty-cash, upload-collection*); `pages/dashboard/*`; `pages/admin/RoleMenuPage.vue`; `stores/auth.ts`; `components/AppSidebar.vue`; report pages.
**infra**: only if `entity_type` decision = migrate (seed + data migration).
