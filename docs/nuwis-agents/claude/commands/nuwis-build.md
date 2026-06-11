---
description: "Build fitur baru dari specs — /nuwis-build <nama-fitur> [--type=crud|report|approval] [--portal=zakat|wakaf]"
---

Build fitur baru (bukan migrasi legacy): $ARGUMENTS

1. @nuwis-architect — analisis request dan buat specs + plan:
   - Tentukan tipe: CRUD | Report | Approval
   - Tentukan portal dari argumen atau tanya user
   - Buat docs/todos/{YYYY-MM-DD}-NNN-{slug}/specs.md
   - Buat docs/todos/{YYYY-MM-DD}-NNN-{slug}/plan.md

--- TUNGGU KONFIRMASI USER SEBELUM IMPLEMENTASI ---

2. [PARALEL jika tidak ada dependency]

   @nuwis-db-migrator (jika Report atau tabel baru diperlukan):
   - DWH view specs dari schema-analyst
   - Migration DDL

   @nuwis-python-builder:
   - Module api-python sesuai specs.md
   - Gunakan .claude/skills/nuwis-skill-fastapi-isf.md

3. @nuwis-bff-builder:
   - Routes BFF sesuai specs.md
   - Gunakan .claude/skills/nuwis-skill-bff-proxy.md

4. @nuwis-seed-gen:
   - Menu + role_menu seed
   - Verifikasi 3-way consistency
   - Gunakan .claude/skills/nuwis-skill-seed-sql.md

5. @nuwis-ui-builder:
   - Halaman Vue sesuai specs.md
   - Input: menu_key (dikonfirmasi seed), endpoint (dikonfirmasi BFF)
   - Gunakan .claude/skills/nuwis-skill-vue-isf.md

6. @nuwis-test-gen:
   - E2E script untuk semua endpoints
   - Gunakan .claude/skills/nuwis-skill-e2e-script.md

7. Tampilkan instruksi apply + verify.
