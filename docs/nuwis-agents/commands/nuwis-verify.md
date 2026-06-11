---
description: "Verifikasi implementasi fitur — /nuwis-verify <fitur-slug> [--portal=zakat|wakaf]"
---

Verifikasi implementasi fitur: $ARGUMENTS

1. @nuwis-validator — cek parity:
   - Cari MIGRATION_ANALYSIS di docs/todos/ untuk slug "$ARGUMENTS"
   - Bandingkan dengan implementasi di apps_{portal}/
   - Gunakan .claude/skills/nuwis-skill-parity-check.md
   - Hasilkan parity report

2. Cek 3-way consistency (tanpa agent):
   - grep menu_key di lib/menu/registry.ts
   - grep meta.menu_key di router/index.ts
   - psql check: SELECT menu_key FROM isf_auth.menu WHERE menu_key LIKE '...'

3. Tampilkan instruksi menjalankan E2E:
   ```bash
   bash testing/e2e-$ARGUMENTS.sh
   ```

4. Tampilkan summary:
   - Field coverage: X/Y fields
   - Role coverage: roles yang ada vs yang dibutuhkan
   - Discriminators: covered / missing
   - Recommended actions untuk setiap gap
