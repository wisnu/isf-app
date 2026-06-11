---
description: "Analisis modul legacy DAF — /nuwis-analyze <modul> [--portal=zakat|wakaf]"
---

Jalankan analisis lengkap untuk modul legacy: $ARGUMENTS

Langkah berurutan:

1. @nuwis-legacy-reader — baca semua file relevan di docs/legacy-apps/ yang berkaitan dengan "$ARGUMENTS":
   - Cari di menus/*.mnu untuk entry yang cocok
   - Trace ke dialogs/{path}/ yang relevan
   - Baca _intr.py, _data.py, *.svr, *.dfr
   - Trace scripts/ dan script_modules/ untuk save logic
   - Ikuti panduan di .claude/skills/nuwis-skill-daf-reader.md
   - Hasilkan MIGRATION_ANALYSIS lengkap

2. Setelah step 1 selesai — @nuwis-doc-gen — buat docs/todos/{YYYY-MM-DD}-001-analyze-$ARGUMENTS/:
   - specs.md: arsitektur target + Mermaid diagram + endpoint contract
   - plan.md: checklist implementasi per layer

3. Tampilkan ringkasan:
   - Modul, portal, kompleksitas level
   - Daftar fitur dan roles
   - Discriminators yang ditemukan (KRITIS)
   - Rekomendasi workflow (CRUD | Report | Approval)
   - File yang perlu dibuat (dari plan.md)
