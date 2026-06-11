# nuwis-* Model Routing Strategy

## Prinsip: Biaya Proporsional dengan Risiko Kesalahan

```
ANALISIS & REASONING    → claude-sonnet-4-6   (default reasoning, cukup untuk sebagian besar)
ANALISIS SUPER KOMPLEKS → claude-opus-4-8     (hanya jika sonnet tidak cukup)
GENERASI TEMPLATED      → claude-haiku-4-5    (pola berulang, minim reasoning)
```

---

## Model Matrix per Agent

| Agent | Model Default | Escalasi ke Opus | Downgrade ke Haiku |
|---|---|---|---|
| **nuwis-architect** | `sonnet` | Domain baru tanpa precedent | — |
| **nuwis-legacy-reader** | `sonnet` | >5 dialog saling-linked, logika akuntansi, 5+ JOIN | Cek nama field / struktur saja |
| **nuwis-schema-analyst** | `sonnet` | Schema 50+ tabel, many-to-many kompleks | Lookup/reference table saja |
| **nuwis-python-builder** | `haiku` | ETL runners, running balance, otorisasi dispatcher baru | — |
| **nuwis-ui-builder** | `haiku` | Design system baru, refactor besar halaman | — |
| **nuwis-bff-builder** | `haiku` | Perubahan auth flow, OAuth | — |
| **nuwis-db-migrator** | `haiku` | DWH view dengan 5+ JOIN + window functions | Migration kolom/index sederhana |
| **nuwis-seed-gen** | `haiku` | Audit 3-way consistency besar | — |
| **nuwis-test-gen** | `haiku` | — | — |
| **nuwis-validator** | `sonnet` | Perbedaan hasil yang membutuhkan root-cause | — |
| **nuwis-doc-gen** | `haiku` | — | — |

---

## Estimasi Biaya Relatif per Workflow

### Migrasi Modul Medium (3–5 dialog)

```
nuwis-architect      sonnet  ~8k tokens   → ~15%
nuwis-legacy-reader  sonnet  ~12k tokens  → ~22%  ← terbesar kedua
nuwis-doc-gen        haiku   ~3k tokens   → ~3%
nuwis-db-migrator    haiku   ~4k tokens   → ~4%
nuwis-python-builder haiku   ~6k tokens   → ~6%   per modul
nuwis-bff-builder    haiku   ~3k tokens   → ~3%
nuwis-seed-gen       haiku   ~2k tokens   → ~2%
nuwis-ui-builder     haiku   ~8k tokens   → ~8%   per halaman
nuwis-test-gen       haiku   ~3k tokens   → ~3%
nuwis-validator      sonnet  ~6k tokens   → ~11%
─────────────────────────────────────────────────
Total estimasi: ~55k tokens (vs all-sonnet: ~90k → hemat ~40%)
```

### Fitur Baru Sederhana (CRUD 1 entitas)

```
nuwis-architect      sonnet  ~5k tokens
nuwis-doc-gen        haiku   ~2k tokens
nuwis-python-builder haiku   ~4k tokens
nuwis-bff-builder    haiku   ~2k tokens
nuwis-seed-gen       haiku   ~1k tokens
nuwis-ui-builder     haiku   ~6k tokens
nuwis-test-gen       haiku   ~2k tokens
─────────────────────────────────────────────────
Total estimasi: ~22k tokens
```

---

## Kapan Override Manual?

### Naik ke Sonnet (dari haiku)

- `nuwis-python-builder` menemukan business logic edge case yang tidak ada di specs
- `nuwis-ui-builder` membangun halaman dengan interaction kompleks (multi-step wizard)
- `nuwis-db-migrator` menemukan anomali schema yang membutuhkan keputusan

### Naik ke Opus (dari sonnet)

- `nuwis-legacy-reader` menganalisis modul core/ keuangan dengan jurnal berlapis
- `nuwis-architect` merancang domain baru tanpa referensi di codebase

### Turun ke Haiku (dari sonnet)

- `nuwis-legacy-reader` hanya mengecek nama field atau struktur sederhana
- `nuwis-validator` memvalidasi CRUD sederhana tanpa discriminator

---

## Implementasi di Workflow Script

```javascript
// Contoh di .claude/workflows/migrate-modul.js
const MODELS = {
  architect:     'sonnet',
  legacyReader:  'sonnet',
  schemaAnalyst: 'sonnet',
  pythonBuilder: 'haiku',
  uiBuilder:     'haiku',
  bffBuilder:    'haiku',
  dbMigrator:    'haiku',
  seedGen:       'haiku',
  testGen:       'haiku',
  validator:     'sonnet',
  docGen:        'haiku',
}

// Override per-call jika diperlukan
const analysis = await agent(
  `Analisis modul ${modul} — sangat kompleks, >10 dialog akuntansi`,
  { agentType: 'nuwis-legacy-reader', model: 'opus' }  // ← explicit override
)
```

---

## Catatan Model ID

Model ID yang valid untuk digunakan:

| Label | Model ID |
|---|---|
| haiku | `claude-haiku-4-5-20251001` |
| sonnet | `claude-sonnet-4-6` |
| opus | `claude-opus-4-8` |

Di agent frontmatter, gunakan label singkat (`haiku`, `sonnet`, `opus`) karena
Claude Code memetakan secara otomatis ke model ID terbaru.
