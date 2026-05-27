# Recovery 2026-05-27 — NTFS corruption audit trail

## Apa yang terjadi

Partisi NTFS Windows D: (`/dev/nvme0n1p5`, mount `/media/win_d`) yang menyimpan working repo isf-app mengalami MFT corruption pada 2026-05-27. Penyebab: 90× unsafe shutdowns (lihat SMART NVMe — Media Errors: 0, jadi murni filesystem-level corruption, bukan disk failure).

- 432 path di `.git/` jadi I/O error → loose objects + 1 pack file (`pack-e6b5...`) tidak terbaca
- 88 path di working tree corrupt → file source code + config + migration scripts
- `git status` fatal: index broken

74 commit lokal antara `47daf7f47` (line 44 reflog, common dengan GitHub) sampai `9e13e2615` (line 118 reflog, tip lokal terakhir) **belum di-push ke GitHub** — semua commit ini berisiko hilang permanen.

Setelah rescue snapshot, dijalankan `chkdsk D: /f` dari Windows. chkdsk pakai strategi "fix by deletion" untuk MFT entries yang tidak bisa di-repair — **tidak ada file yang berhasil di-recover**, file yang corrupt malah dihapus permanen.

## Cara recovery

Karena git objects hilang, **tidak bisa cherry-pick per-commit**. Strategi yang dipakai:

1. **Clone fresh** dari `origin/main` (= `ac3056...`) ke partisi ext4 (`~/workshop/isf-app/`)
2. **Overlay** rescued working tree (632 file dari 711 — 89%) ke clone
3. **Identifikasi** 51 file truly missing (file baru yang dibuat di 74 commit, tidak ada di base)
4. **Recover** migration schema dari pg_dump (DB masih hidup) ke `infra/db/migrations/`
5. **Rebuild** `CLAUDE.md` dari memory + reflog descriptions (file ini juga lihat `CLAUDE.md` di root)
6. **Mega-commit** semua di branch baru `recovery/2026-05-27-ntfs-corruption`

## File audit trail

| File | Isi |
|---|---|
| `reflog-main-118-entries.txt` | Reflog branch main lengkap (118 entries, dari init repo sampai tip lokal terakhir `9e13e26`) |
| `last-local-commit-message.txt` | Pesan commit untuk SHA `9e13e26` (`[ETL] migration 007 — drop stale unique indexes`) |
| `corrupt-paths-520.txt` | 520 path yang gagal di-rsync karena I/O error (audit kerusakan total) |
| `missing-files-88.txt` | 88 file working tree yang hilang akibat corruption |
| `truly-missing-51.txt` | 51 file yang TIDAK ADA di base commit `ac3056` — file baru yang dibuat di 74 commit lokal, harus rebuild manual post-recovery |

## Outstanding work (post-recovery commit)

Yang masih harus di-rebuild setelah recovery branch ini (commit terpisah per feature group):

**Backend Python**:
- `apps_zakat/api-python/etl/` — 14 file ETL (runner, scheduler, refresh_dim_*, refresh_dm_*, refresh_fact_*, db, utils, __init__)
- `apps_*/api-python/app/modules/admin/router.py & service.py`
- `apps_*/api-python/tests/test_admin.py`
- `apps_wakaf/bff-api/app/shared/db.py` (zakat side punya, wakaf hilang)
- `apps_*/bff-api/app/routers/admin.py`
- `apps_*/bff-api/tests/test_admin*.py`, `test_change_password.py`, `test_coa_gating.py`, `test_identity*.py`

**Frontend Vue**:
- `apps_*/web-vue/src/components/ui/Toast.vue`
- `apps_*/web-vue/src/lib/useFetch.ts`, `useToast.ts`
- `apps_*/web-vue/src/pages/admin/` (UsersPage, RoleMenuPage), `pages/profile/`
- `apps_zakat/web-vue/src/lib/menu/registry.ts` (MENU_KEYS — wakaf side punya, zakat hilang)

**Docs**:
- `docs/datadictionary/dwh.md`
- `docs/superpowers/specs/`, `plans/2026-05-24-role-menu-admin-ui.md`, `plans/2026-05-24-role-menu-mapping.md`
- `docs/legacy-apps/`, `docs/reference/` (mungkin tidak penting untuk dipulihkan)

**Testing**:
- `testing/e2e-admin-users.sh`
- `testing/e2e-etl-datamart.sh`

**Schema fix**:
- Rename schema `datamart` → `dwh` di DB `mziss_wakaf` (commit `[DWH] rename schema datamart→dwh` belum di-apply ke wakaf side)

## Pelajaran

- **Jangan host working repo di NTFS via ntfs-3g.** Repo sekarang di ext4 `~/workshop/isf-app/`. Partisi NTFS D: cuma untuk file sharing dengan Windows.
- **Push lebih sering.** 74 commit unpushed selama beberapa hari adalah window risiko yang terlalu besar.
- **Verify push state sebelum risk operations.** Sebelum reboot/shutdown yang berpotensi unsafe, cek `git log origin/main..HEAD --oneline` — kalau ada commit, push dulu.
