# nuwis-* untuk Gemini CLI

Gemini CLI membaca `GEMINI.md` di project root sebagai context utama.
Skills di-load on-demand via `activate_skill` tool — tidak perlu embed semua ke satu file.

## Install

```bash
bash docs/nuwis-agents/gemini/install.sh
# --update   : overwrite file yang sudah ada
# --dry-run  : preview tanpa tulis file
```

Hasilnya:
- `GEMINI.md` → di project root
- `.gemini/skills/nuwis-*.md` → skills yang bisa di-activate

## Cara Pakai

```
# Aktifkan skill sebelum task terkait
activate_skill("nuwis-vue-isf")
Buat halaman PenghimpunanPage untuk portal zakat

activate_skill("nuwis-fastapi-isf")
Tambah endpoint GET /api/penghimpunan/summary
```

## Files

| File | Keterangan |
|---|---|
| `GEMINI.md.template` | Template project context — di-copy ke GEMINI.md |
| `install.sh` | Install script: copy GEMINI.md + adapt skills ke .gemini/ |
| `README.md` | File ini |

Skills di-adapt dari `../claude/skills/` — Claude-specific syntax di-strip saat install.
