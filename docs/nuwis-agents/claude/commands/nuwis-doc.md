---
description: "Generate dokumentasi untuk fitur — /nuwis-doc <fitur-slug> [--type=specs|adr|runbook]"
---

Generate dokumentasi untuk: $ARGUMENTS

@nuwis-doc-gen — buat dokumentasi berdasarkan implementasi yang ada:

1. Baca implementasi aktual:
   - specs.md yang ada di docs/todos/ (jika ada)
   - Kode di apps_{portal}/ untuk fitur terkait
   - testing/e2e-$ARGUMENTS.sh (jika ada)

2. Buat atau update docs/todos/{YYYY-MM-DD}-NNN-$ARGUMENTS/:
   - specs.md: arsitektur + Mermaid sequence diagram + API contract
   - plan.md: checklist implementasi (update status untuk yang sudah selesai)
   - adr-001.md: ADR jika ada keputusan arsitektur yang significant

3. Jika --type=runbook, buat runbook.md:
   - Cara deploy (apply migration, seed, restart)
   - Cara rollback
   - Cara test
   - Known issues / gotchas

4. Tampilkan link ke semua dokumen yang dibuat/diupdate.
