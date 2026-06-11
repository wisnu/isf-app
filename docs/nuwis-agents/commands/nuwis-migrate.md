---
description: "Full pipeline migrasi dari legacy DAF — /nuwis-migrate <modul> [--portal=zakat|wakaf]"
---

Jalankan pipeline migrasi lengkap untuk modul: $ARGUMENTS

Semua langkah dijalankan berurutan. Langkah paralel ditandai [PARALEL].

1. @nuwis-legacy-reader — analisis modul $ARGUMENTS di docs/legacy-apps/
   - Gunakan .claude/skills/nuwis-skill-daf-reader.md
   - Hasilkan MIGRATION_ANALYSIS (simpan ke docs/todos/...)

2. @nuwis-doc-gen — buat specs.md + plan.md dari MIGRATION_ANALYSIS
   - Tentukan workflow type (CRUD/Report/Approval)
   - Buat testing/e2e-{slug}.sh template

--- SETELAH ANALISIS + SPECS DIKONFIRMASI ---

3. [PARALEL] @nuwis-db-migrator — jalankan jika laporan atau tabel baru:
   - DWH view jika laporan
   - Migration DDL jika tabel baru
   - Gunakan .claude/skills/nuwis-skill-pg-migration.md

4. [PARALEL] @nuwis-python-builder — generate modul api-python:
   - router.py, service.py, schema.py
   - Sertakan DISCRIMINATORS dari MIGRATION_ANALYSIS
   - Gunakan .claude/skills/nuwis-skill-fastapi-isf.md

5. @nuwis-bff-builder — generate routes BFF:
   - Proxy endpoints dengan require_menu()
   - Stream laporan jika report module
   - Gunakan .claude/skills/nuwis-skill-bff-proxy.md

6. @nuwis-seed-gen — generate menu + role_menu seed SQL:
   - Gunakan .claude/skills/nuwis-skill-seed-sql.md
   - Verifikasi 3-way consistency (registry.ts + router.ts + seed)

7. @nuwis-ui-builder — generate halaman Vue:
   - Input: menu_key (dari seed), endpoint (dari BFF), fields (dari MIGRATION_ANALYSIS)
   - Gunakan .claude/skills/nuwis-skill-vue-isf.md

8. @nuwis-test-gen — generate E2E script:
   - testing/e2e-{slug}.sh dengan semua CRUD covered
   - Gunakan .claude/skills/nuwis-skill-e2e-script.md

9. @nuwis-validator — validasi parity:
   - Bandingkan MIGRATION_ANALYSIS dengan implementasi baru
   - Gunakan .claude/skills/nuwis-skill-parity-check.md
   - Laporkan semua gap

10. Tampilkan instruksi apply:
    ```bash
    # Apply DB migration (jika ada):
    psql -U transaction -d mziss_{portal} -f infra/db/migrations/V{NNN}__...sql

    # Apply seed:
    psql -U transaction -d isf_auth_{portal} -f infra/db/migrations/seed/{slug}-seed.sql

    # Restart:
    cd infra && podman-compose -f docker-compose.{portal}.yml restart api-python bff-api web-vue

    # E2E test:
    bash testing/e2e-{slug}.sh
    ```
