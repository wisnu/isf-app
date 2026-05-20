# Dashboard Widgets — Varied Types

> Combined spec + plan. Scope: `apps/api-python/app/modules/dashboard/*` + `apps/web-vue/src/{components/widgets,lib,pages/DashboardPage}`. Tidak menyentuh `bff-api` (proxy tetap pass-through).

## Goal

Dummy dashboard saat ini cuma 2 KPI card. Tambah variasi: KPI dengan delta, line chart trend 6 bulan, donut distribusi 8 asnaf, progress bar per channel fundraising, dan table transaksi terbaru. Tetap desktop-first + responsive.

## Layout (desktop-first)

```
┌─────────────────────────────────────────────────────────────┐
│ [Penerimaan] [Penyaluran] [Saldo] [Donatur Baru]            │  ← 4 KPI cards
├──────────────────────────────────────┬──────────────────────┤
│  Trend 6 bulan (line)                │  Distribusi Asnaf    │  ← 2 col / 1 col
│  ─────────────────                   │  (donut)             │
├──────────────────────┬───────────────┴──────────────────────┤
│  Capaian Channel     │  Transaksi Terbaru                   │  ← 1 col / 2 col
│  (progress bars)     │  (table)                             │
└──────────────────────┴──────────────────────────────────────┘

Mobile: semua stack vertikal (grid-cols-1).
Tablet (sm/md): KPI 2 kolom; chart + tabel tetap full-width 1 kolom.
Desktop (lg+): KPI 4 kolom; row chart 2+1; row bawah 1+2.
```

## API contract (extended `/api/v1/dashboard/summary`)

```json
{
  "data": {
    "tenant_id": "perusahaan_a",
    "tenant_name": "Lembaga ZISWAF A",
    "period": "2026-05",
    "kpis": {
      "penerimaan":   { "total": 1250000000, "delta_pct": 12.4  },
      "penyaluran":   { "total": 875000000,  "delta_pct": -3.2  },
      "saldo":        { "total": 4800000000, "delta_pct": 8.1   },
      "donatur_baru": { "total": 142,        "delta_pct": 21.5  }
    },
    "trend": {
      "labels": ["2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05"],
      "penerimaan": [820000000, 905000000, 980000000, 1100000000, 1112000000, 1250000000],
      "penyaluran": [610000000, 680000000, 740000000, 810000000, 905000000, 875000000]
    },
    "asnaf_distribution": [
      { "label": "Fakir", "amount": 245000000 },
      { "label": "Miskin", "amount": 198000000 },
      { "label": "Amil", "amount": 87500000 },
      { "label": "Mualaf", "amount": 52000000 },
      { "label": "Riqab", "amount": 0 },
      { "label": "Gharimin", "amount": 78000000 },
      { "label": "Fi Sabilillah", "amount": 132000000 },
      { "label": "Ibnu Sabil", "amount": 82500000 }
    ],
    "fundraising_channels": [
      { "label": "Transfer Bank", "actual": 720000000, "target": 800000000 },
      { "label": "Gerai & Booth", "actual": 240000000, "target": 200000000 },
      { "label": "Payroll", "actual": 180000000, "target": 250000000 },
      { "label": "E-Wallet", "actual": 110000000, "target": 150000000 }
    ],
    "recent_transactions": [
      { "id": "tx_001", "date": "2026-05-19", "type": "Zakat", "channel": "Transfer", "amount": 5000000, "donor": "Budi S." },
      ...
    ]
  },
  "meta": { "request_id": "req_xxx" }
}
```

## File changes

### `apps/api-python/`

| File | Aksi |
| --- | --- |
| `app/modules/dashboard/schema.py` | Ganti — model baru: `KpiPair`, `Trend`, `AsnafItem`, `Channel`, `Transaction`, `DashboardSummary` |
| `app/modules/dashboard/service.py` | Ganti — dummy data lebih lengkap per tenant |
| `app/modules/dashboard/router.py` | Minor — return shape baru |
| `tests/test_dashboard.py` | Update assertion |

### `apps/web-vue/`

| File | Aksi |
| --- | --- |
| `package.json` | + `chart.js`, `vue-chartjs` |
| `src/lib/charts.ts` | **Baru** — register Chart.js components |
| `src/components/SummaryWidget.vue` | **Hapus** — replaced by widgets/ |
| `src/components/widgets/KpiCard.vue` | **Baru** — KPI dengan trend arrow |
| `src/components/widgets/TrendChart.vue` | **Baru** — line chart |
| `src/components/widgets/AsnafDonut.vue` | **Baru** — donut chart |
| `src/components/widgets/FundraisingProgress.vue` | **Baru** — progress bars |
| `src/components/widgets/RecentActivity.vue` | **Baru** — table |
| `src/pages/DashboardPage.vue` | Refactor — grid mixed-span + 5 widget types |

## Eksekusi

1. Backend: tulis schema/service/router/test.
2. Frontend deps: update package.json (chart.js + vue-chartjs).
3. Frontend libs/components: charts.ts + 5 widget components.
4. Refactor DashboardPage.
5. Rebuild web-vue (`down -v && up -d --build web-vue` karena package.json berubah).
6. Verifikasi.

## Verifikasi

- `curl /api/v1/dashboard/summary?tenant_id=perusahaan_a` → JSON dengan semua field baru.
- `curl /api/dashboard/summary` (via BFF, butuh login) → sama.
- Browser desktop ≥1280px: 4 KPI card di row pertama, chart 2+1 di row dua, channel+table 1+2 di row tiga.
- Mobile (DevTools 375px): semua stack vertikal.
- Switch tenant → semua widget update sesuai tenant baru (delta_pct, trend, asnaf, channels, transactions semua beda).
- Dark mode toggle → semua widget (termasuk chart) ter-flip warna.

## Out of scope

- Filter periode interaktif (dashboard pakai periode saat ini).
- Drill-down detail per widget.
- Real-time refresh.
- Export PDF/Excel.
- Komponen widget yang lain (Stepper, Calendar, Map).
