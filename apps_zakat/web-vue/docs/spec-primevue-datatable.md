# Spec: PrimeVue DataTable — Hybrid Integration

**Status:** In Progress (POC: LaporanJurnalHarianPage)
**Tanggal:** 2026-06-06
**Scope:** apps_zakat/web-vue — 17 halaman laporan

---

## Latar Belakang

Setiap halaman laporan saat ini memiliki ~40–60 baris HTML manual: `<table>`, `<thead>`, `<tbody>`, loading spinner, empty state, dan pagination buttons. Pola ini diulang di setiap halaman dengan variasi kecil yang sulit di-maintain.

**Keputusan:** Adopsi `p-DataTable` dari PrimeVue dalam mode **unstyled** sebagai pengganti custom `<table>` di seluruh halaman laporan. Tailwind v4 dan semua komponen custom lainnya (Button, Alert, DateField, dll.) tidak diubah.

---

## Arsitektur

### Mode: Unstyled + Passthrough

PrimeVue diregister dengan `unstyled: true` — tidak ada CSS PrimeVue yang dimuat. Setiap token visual (warna, border, spacing) diberikan via prop `pt` (passthrough) menggunakan Tailwind class yang sudah ada di proyek.

```ts
// main.ts
app.use(PrimeVue, { unstyled: true })
```

Tidak ada konflik dengan Tailwind v4 atau design token ISF (`--color-primary`, `--color-border`, dll.).

### Wrapper: `AppDataTable.vue`

Satu wrapper component di `components/ui/AppDataTable.vue` yang:
- Pre-konfigurasi `pt` dengan ISF table style (font `text-[11px]`, border, hover)
- Meneruskan semua props via `v-bind="$attrs"`
- Meneruskan slot Column definitions via `<slot />`
- Zero styling yang perlu diulang di setiap halaman

---

## Komponen: `AppDataTable.vue`

### File
`src/components/ui/AppDataTable.vue`

### API

```ts
// Props (semua dari DataTable PrimeVue, diteruskan via $attrs)
value: T[]           // data rows
loading: boolean     // tampilkan loading overlay
// ... semua props DataTable lainnya (lazy, rows, totalRecords, dll.)

// Slots
default              // Column definitions
empty                // custom empty state message
```

### Passthrough tokens (pt)

| Token | Tailwind class | Keterangan |
|-------|---------------|------------|
| `root` | `overflow-x-auto` | scroll horizontal |
| `table` | `w-full text-[11px]` | ukuran font standar laporan |
| `thead` | `text-[10px] text-muted uppercase tracking-widest border-b border-border bg-background/50` | header row |
| `headerCell` | `text-left px-3 py-1 font-semibold whitespace-nowrap` | setiap `<th>` |
| `row` | `border-b border-border/40 hover:bg-muted/5 transition-colors` | setiap `<tr>` body |
| `bodyCell` | `px-3 py-1` | setiap `<td>` |
| `emptyMessageCell` | `p-10 text-center text-sm text-muted italic` | tampil saat data kosong |
| `loadingOverlay` | `absolute inset-0 flex items-center justify-center bg-surface/80 z-10` | loading overlay |
| `loadingIcon` | `w-7 h-7 animate-spin text-primary` | spinner |

### Override per kolom

Untuk header kolom yang butuh alignment berbeda (misal: Debet/Kredit rata kanan), gunakan prop `pt` di level `<Column>`:

```html
<Column header="Debet" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold' } }">
  <template #body="{ data: r }">
    <span class="block text-right tabular-nums">{{ fmt(r.debit) }}</span>
  </template>
</Column>
```

---

## Pola Migrasi per Halaman Laporan

### Yang dihapus dari setiap halaman

```ts
// Script — hapus:
import { Loader2 } from 'lucide-vue-next'  // diganti loading bawaan DataTable

// Template — hapus (3 blok kondisional):
<div v-if="loading && !data">               // loading spinner manual
<div v-else-if="data && rows.length === 0"> // empty state manual
<div v-else-if="data" class="overflow-x-auto">
  <table class="w-full text-[11px]">        // seluruh <table> manual
    <thead>...</thead>
    <tbody>...</tbody>
  </table>
</div>
```

### Yang ditambahkan

```ts
// Script — tambah:
import Column from 'primevue/column'
import AppDataTable from '@/components/ui/AppDataTable.vue'
```

```html
<!-- Template — ganti seluruh blok table dengan: -->

<!-- state sebelum pertama kali klik Tampilkan (standar laporan: tidak auto-load) -->
<div v-if="!data && !loading" class="p-10 text-center text-sm text-muted italic">
  Atur filter lalu klik "Tampilkan"
</div>

<!-- DataTable handle loading + empty + rows -->
<AppDataTable v-else :value="data?.rows ?? []" :loading="loading">
  <Column header="Kolom A">
    <template #body="{ data: r }">{{ r.field_a }}</template>
  </Column>
  <!-- ... column lainnya -->
  <template #empty>Tidak ada data untuk filter ini.</template>
</AppDataTable>
```

### Pagination

Pagination di halaman laporan bersifat **server-side** (API yang mengembalikan halaman data). DataTable paginator tidak digunakan untuk ini — pagination manual dipertahankan. Hanya `<table>` yang diganti DataTable, bukan pagination.

State `page`, `pageSize`, `totalPages`, `goto()` tetap ada di setiap halaman.

---

## Column Patterns

### Kolom teks biasa

```html
<Column field="inputer" header="Inputer" />
```

### Kolom dengan format custom

```html
<Column field="journal_date" header="Tanggal">
  <template #body="{ data: r }">
    <span class="whitespace-nowrap tabular-nums">{{ dmy(r.journal_date) }}</span>
  </template>
</Column>
```

### Kolom angka (rata kanan)

```html
<Column header="Debet" :pt="{ headerCell: { class: 'text-right px-3 py-1 font-semibold' } }">
  <template #body="{ data: r }">
    <span class="block text-right tabular-nums">{{ fmt(r.debit_ekuiv) }}</span>
  </template>
</Column>
```

### Kolom composite (dua field dalam satu cell)

```html
<Column header="Akun">
  <template #body="{ data: r }">
    <span class="font-mono text-[11px] text-muted">{{ r.account_code }}</span>
    <span class="ml-1">{{ r.account_name }}</span>
  </template>
</Column>
```

### Kolom dengan truncate + tooltip

```html
<Column header="Keterangan">
  <template #body="{ data: r }">
    <span class="max-w-[24rem] truncate block" :title="r.description ?? ''">
      {{ r.description }}
    </span>
  </template>
</Column>
```

---

## Rollout: Halaman Laporan

### Selesai — Full Migration (AppDataTable)
- [x] `main.ts` — register PrimeVue unstyled
- [x] `components/ui/AppDataTable.vue` — wrapper + #empty + #footer slot
- [x] `LaporanJurnalHarianPage.vue`
- [x] `LaporanGeneralTransactionPage.vue` — grouped cards, inner table migrated
- [x] `LaporanCashDailyPage.vue`
- [x] `LaporanCashSummaryPage.vue` — groupRows helper + subtotal rows
- [x] `LaporanBukuBesarPage.vue` — per-account AppDataTable
- [x] `LaporanNeracaPage.vue` — 2 AppDataTable (aktiva+pasiva), computed rows dengan total sentinel
- [x] `LaporanArusKasPage.vue` — discriminated union AKTableRow, flat computed tableRows
- [x] `LaporanAmilPage.vue` — Column v-if untuk kolom kondisional
- [x] `LaporanARSummaryPage.vue` — _isTotal flag + row-class
- [x] `LaporanPenghimpunanDanaPage.vue` — 2 tabel (rekap dana + detail transaksi)
- [x] `LaporanPenyaluranDanaPage.vue`
- [x] `LaporanPiutangRealisasiPage.vue` — total row + highlight amber Outstanding
- [x] `LaporanRealisasiMemoPage.vue` — #footer grand-total
- [x] `LaporanListUangMukaPage.vue` — status LPJ conditional color
- [x] `LaporanUpzPage.vue` — per-account AppDataTable + #footer subtotal

### Partial Migration (state guard saja — tabel terlalu kompleks)
- [~] `LaporanCashMonthlyPage.vue` — pivot matrix kolom bulan dinamis; custom `<table>` dipertahankan
- [~] `LaporanTrialBalancePage.vue` — group header + colspan dinamis; custom `<table>` dipertahankan
- [~] `LaporanPerubahanDanaPage.vue` — card-grid hierarkis per dana; bukan flat table
- [~] `LaporanPerubahanDanaDetailPage.vue` — bertingkat per dana × seksi; bukan flat table

### Halaman non-laporan (opsional)
- [ ] `HistoriTransaksiPage.vue`
- [ ] `CoaPage.vue`
- [ ] `RoleMenuPage.vue`

---

## Verifikasi per Halaman

Setelah migrasi setiap halaman, cek:

1. **Tabel muncul** dengan style yang sama (font kecil, border, hover effect)
2. **Loading state** tampil saat fetch berjalan
3. **Empty state** tampil jika tidak ada data
4. **Kolom angka** rata kanan dengan `tabular-nums`
5. **Kolom tanggal** format DD-MM-YYYY
6. **Pagination manual** masih kerja (prev/next page)
7. **Export Excel** masih kerja
8. **Tidak ada CSS leak** dari PrimeVue (inspect element)
9. **Dark mode** tidak rusak
