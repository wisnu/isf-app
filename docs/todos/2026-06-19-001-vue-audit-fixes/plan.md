# Plan: Vue 3 Audit Fixes — apps_zakat/web-vue

**Dibuat**: 2026-06-19
**Target Portal**: zakat (dan berlaku untuk wakaf bila file mirip)
**Sumber**: Audit oleh vue-expert agent
**Kompleksitas**: MEDIUM — banyak file, tapi setiap fix independent

---

## Ringkasan Temuan

| Severity | Jumlah | Status |
|---|---|---|
| Critical | 1 | ⬜ Belum |
| High | 7 | ⬜ Belum |
| Medium | 10 | ⬜ Belum |
| Low | 5 | ⬜ Belum |

---

## CRITICAL

### C1 — `api.get()` silent param drop di PenghimpunanDanaFormPage
- **File**: `src/pages/keuangan/PenghimpunanDanaFormPage.vue` baris 106 dan 122
- **Masalah**: `api.get<T>(path, secondArg)` — `client.ts` memakai signature `(method, path, body?)`. GET tidak punya body. Parameter kedua (branch_code, q) diam-diam dibuang → lookup produk & donor dipanggil tanpa filter → kemungkinan return semua data atau data salah.
- **Fix**:
  ```ts
  // SEBELUM (bug)
  api.get<ProductOption[]>('/api/penghimpunan/lookup/produk', { branch_code: branchCode.value })
  api.get<DonorOption[]>('/api/penghimpunan/lookup/donor', { q: donorQuery.value })

  // SESUDAH
  api.get<ProductOption[]>(`/api/penghimpunan/lookup/produk?branch_code=${encodeURIComponent(branchCode.value)}`)
  api.get<DonorOption[]>(`/api/penghimpunan/lookup/donor?q=${encodeURIComponent(donorQuery.value)}`)
  ```
- [ ] Fix baris 106
- [ ] Fix baris 122
- [ ] Test: buka form penghimpunan, pastikan dropdown produk & donor terfilter sesuai cabang/query

---

## HIGH

### H1 — `downloadBlob` double HTTP request
- **File**: `src/lib/api/client.ts` baris 70–94
- **Masalah**: `downloadBlob()` melakukan 2 HTTP request ke URL yang sama — request pertama (`fetchBlob`) hanya ambil body blob, lalu request kedua dilakukan semata-mata untuk membaca header `Content-Disposition` (filename). Bandwidth boros, server kena double load, bisa gagal jika URL one-time/timestamped.
- **Fix**: Refactor `fetchBlob` agar return `{ blob: Blob; headers: Headers }`, ambil `Content-Disposition` dari response pertama.
  ```ts
  async function fetchBlob(path: string): Promise<{ blob: Blob; headers: Headers }> {
    const res = await fetch(`${BASE_URL}${path}`, { credentials: 'include' })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    return { blob: await res.blob(), headers: res.headers }
  }

  export async function downloadBlob(path: string): Promise<void> {
    const { blob, headers } = await fetchBlob(path)
    const disposition = headers.get('Content-Disposition') ?? ''
    const filename = disposition.match(/filename\*?=(?:UTF-8'')?([^;]+)/i)?.[1]
      ?? path.split('/').pop()
      ?? 'download'
    // ... buat object URL dan trigger download
  }
  ```
- [ ] Refactor `fetchBlob` return type
- [ ] Update `downloadBlob` pakai headers dari response pertama
- [ ] Test: export laporan jurnal harian, verifikasi filename benar dan tidak ada double request di Network tab

### H2 — `lookupLoaded` plain variable di SubmissionDetailDrawer
- **File**: `src/components/otorisasi/SubmissionDetailDrawer.vue` baris 46–57
- **Masalah**: `let lookupLoaded = false` adalah plain variable modul-level, bukan reaktif. Persists antar lifecycle komponen. Saat drawer dibuka untuk ke-2 kalinya setelah unmount, `bankMap` dan `branchMap` (ref baru, kosong) tidak di-reload karena guard sudah `true`.
- **Fix**:
  ```ts
  // SEBELUM
  let lookupLoaded = false

  // SESUDAH
  const lookupLoaded = shallowRef(false)
  // dan gunakan lookupLoaded.value di guard check
  ```
- [ ] Ubah ke `shallowRef(false)`
- [ ] Update semua referensi ke `lookupLoaded.value`
- [ ] Test: buka detail drawer, tutup, buka lagi → nama bank dan cabang harus muncul

### H3 — Hardcoded route paths (4 lokasi)
- **Masalah**: Melanggar aturan named routes only. Rapuh saat URL direfaktor.
- **Fix per file**:

  **`UploadHCZisPage.vue` baris 282:**
  ```ts
  // SEBELUM
  router.push('/keuangan/upload/zis-rutin-list')
  // SESUDAH
  router.push({ name: 'keuangan-upload-zis-rutin-list' })
  ```

  **`UploadPenghimpunanListPage.vue` baris 140:**
  ```ts
  // SEBELUM
  router.push(`/keuangan/upload/penghimpunan/${b.batch_id}`)
  // SESUDAH
  router.push({ name: 'keuangan-upload-penghimpunan-detail', params: { id: b.batch_id } })
  ```

  **`HistoriTransaksiPage.vue` baris 221:**
  ```ts
  // SEBELUM
  router.push(`/keuangan/transaksi/histori/${id}`)
  // SESUDAH
  router.push({ name: 'keuangan-transaksi-histori-detail', params: { id } })
  ```

  **`HistoriTransaksiDetailPage.vue` baris 92:**
  ```ts
  // SEBELUM
  router.push('/keuangan/transaksi/histori')
  // SESUDAH
  router.push({ name: 'keuangan-transaksi-histori' })
  ```

  > ⚠️ Verifikasi nama route di `router/index.ts` sebelum apply — nama di atas adalah perkiraan.

- [ ] `UploadHCZisPage.vue` — ganti ke named route
- [ ] `UploadPenghimpunanListPage.vue` — ganti ke named route
- [ ] `HistoriTransaksiPage.vue` — ganti ke named route
- [ ] `HistoriTransaksiDetailPage.vue` — ganti ke named route

### H4 — Date format bypass `dmy()` di KasPage dan RecentActivityWidget
- **File**: `src/pages/keuangan/KasPage.vue` baris 231, `src/components/widgets/RecentActivityWidget.vue` baris 27–33, 61
- **Masalah**: Keduanya pakai `formatDate()` berbasis `Intl.DateTimeFormat` yang menghasilkan `19 Mei 2026` — inkonsisten dengan standar proyek DD-MM-YYYY via `dmy()`.
- **Fix**:
  ```ts
  import { dmy } from '@/lib/date'
  // hapus formatDate lokal / import dari format.ts
  // ganti semua pemanggilan formatDate(...) → dmy(...)
  ```
- [ ] `KasPage.vue` — ganti `formatDate` → `dmy`
- [ ] `RecentActivityWidget.vue` — hapus inline `formatDate`, pakai `dmy`
- [ ] Evaluasi `lib/format.ts` — pertimbangkan deprecate atau hapus `formatDate` export untuk cegah misuse di masa depan

### H5 — `parsePayload()` dipanggil berulang di template OtorisasiPage
- **File**: `src/pages/keuangan/OtorisasiPage.vue` baris 408–432 (template), baris 78–83
- **Masalah**: `parsePayload(row.payload)` dipanggil 2–3x per baris per render cycle. JSON.parse dieksekusi berulang kali untuk data yang sama. Dengan 20+ baris dan auto-refresh 5 detik → overhead tidak perlu.
- **Fix**:
  ```ts
  const parsedRows = computed(() =>
    rows.value.map(r => ({ ...r, _parsed: parsePayload(r.payload) }))
  )
  // template: ganti rows → parsedRows, row.payload → row._parsed
  ```
- [ ] Tambah computed `parsedRows`
- [ ] Update template untuk iterasi `parsedRows` dan baca `row._parsed`

### H6 — Full rows di-serialize ke sessionStorage tiap load (HistoriTransaksiPage)
- **File**: `src/pages/keuangan/HistoriTransaksiPage.vue` baris 101–119
- **Masalah**: `saveState()` serialisasi seluruh array `rows.value` ke sessionStorage. Operasi JSON.stringify sinkron, blocking main thread. Juga berisiko menampilkan data stale saat restore.
- **Fix**: Simpan hanya filter state (bukan rows):
  ```ts
  function saveState() {
    sessionStorage.setItem(STATE_KEY, JSON.stringify({
      dateFrom: dateFrom.value,
      dateTo: dateTo.value,
      page: page.value,
      pageSize: pageSize.value,
    }))
  }
  // Saat restore: set filter values, lalu panggil load() untuk data fresh
  ```
- [ ] Refactor `saveState` — hanya simpan filter
- [ ] Refactor `restoreState` — set filter + trigger `load()` fresh

### H7 — COA fetch halaman 2…N sequential waterfall
- **File**: `src/pages/keuangan/CoaPage.vue` baris 186–202
- **Masalah**: `loadAll()` fetch halaman pertama, lalu halaman 2…N diambil satu per satu dalam `for` loop — total waktu = jumlah semua request, bukan request terlama.
- **Fix**: Parallelkan fetch setelah mengetahui `total_pages`:
  ```ts
  const first = await api.get<CoaListResponse>('/api/coa?page=1&limit=100')
  const totalPages = first.pagination.total_pages
  const rest = await Promise.all(
    Array.from({ length: totalPages - 1 }, (_, i) =>
      api.get<CoaListResponse>(`/api/coa?page=${i + 2}&limit=100`)
    )
  )
  allRows.value = [
    ...first.data,
    ...rest.flatMap(r => r.data),
  ]
  ```
- [ ] Refactor `loadAll()` — waterfall → `Promise.all`

---

## MEDIUM

### M1 — pageSize default 20 (harusnya 25) di banyak halaman
- **Aturan**: Default rows per page: **25**
- **File yang melanggar**: `OtorisasiPage.vue`, `BankPage.vue`, `HistoriTransaksiPage.vue`, `PenghimpunanDanaPage.vue`, `PenyaluranDanaPage.vue`, `RiwayatSubmissionPage.vue`
- **Fix**: `const pageSize = shallowRef(25)` di setiap file
- [ ] `OtorisasiPage.vue`
- [ ] `BankPage.vue`
- [ ] `HistoriTransaksiPage.vue`
- [ ] `PenghimpunanDanaPage.vue`
- [ ] `PenyaluranDanaPage.vue`
- [ ] `RiwayatSubmissionPage.vue`
- *Note: `LaporanJurnalHarianPage.vue` pakai 50 — bisa dipertahankan jika intentional untuk report page*

### M2 — `watch(filteredRows)` di CoaPage harusnya watch input mentah
- **File**: `src/pages/keuangan/CoaPage.vue` baris 181–182
- **Masalah**: Watch pada computed output (array besar) menyebabkan re-run filter penuh hanya untuk detect perubahan.
- **Fix**:
  ```ts
  // SEBELUM
  watch(filteredRows, () => { currentPage.value = 1 })

  // SESUDAH
  watch([() => f.global, () => f.typeLabels.length, () => f.isDetail], () => {
    currentPage.value = 1
  })
  ```
- [ ] Ganti watch target di CoaPage

### M3 — Timer debounce di BankPage tidak cleanup saat unmount
- **File**: `src/pages/keuangan/BankPage.vue` baris 73–77
- **Masalah**: Timer callback bisa fire setelah komponen unmount, memicu network request orphan.
- **Fix**:
  ```ts
  onUnmounted(() => { if (searchTimer) clearTimeout(searchTimer) })
  ```
- [ ] Tambah `onUnmounted` cleanup di BankPage

### M4 — Pinia stores pakai Options API (auth.ts, sidebar.ts)
- **File**: `src/stores/auth.ts`, `src/stores/sidebar.ts`
- **Masalah**: Inkonsisten dengan konvensi Composition API di seluruh proyek.
- **Fix**: Migrasi ke setup-function pattern `defineStore('auth', () => { ... })`
- [ ] `auth.ts` — migrasi ke setup store (hati-hati: banyak consumer)
- [ ] `sidebar.ts` — migrasi ke setup store
- *Note: lakukan saat ada dedicated refactor task, bukan emergency fix*

### M5 — `any` types di payload otorisasi (banyak file)
- **File**: `OtorisasiPage.vue`, `RiwayatSubmissionPage.vue`, `SubmissionDetailDrawer.vue`, `PenghimpunanDanaPage.vue`, `PenyaluranDanaPage.vue`, `PiutangPage.vue`, `PenghimpunanDanaFormPage.vue`
- **Masalah**: `Record<string, any>` dan `any[]` untuk payload & approval_log — kehilangan type safety.
- **Fix**: Buat `src/types/otorisasi.ts`:
  ```ts
  export interface ApprovalLogEntry {
    logged_at: string
    action: string
    actor: string
    note?: string
  }

  export interface SubmissionRow {
    id: string
    entity_type: string
    status: 'DRAFT' | 'PENDING' | 'PROCESSING' | 'AUTHORIZED' | 'REJECTED'
    payload: Record<string, unknown>
    approval_log: ApprovalLogEntry[]
    created_at: string
    inputer: string
    dispatch_error?: string
  }
  ```
- [ ] Buat `src/types/otorisasi.ts`
- [ ] Update imports di semua file yang pakai `any` untuk otorisasi

### M6 — Inline side effect di template (TransaksiUmumListPage)
- **File**: `src/pages/keuangan/TransaksiUmumListPage.vue` baris 220–224
- **Masalah**: `() => { page.value = 1; load() }` langsung di template — sulit test dan debug.
- **Fix**: Extract ke named function `search()` yang dipanggil dari template.
- [ ] Ekstrak `search()` function

### M7 — `SubmissionDetailDrawer` items computed bertipe `any[]`
- **File**: `src/components/otorisasi/SubmissionDetailDrawer.vue` baris 124
- **Masalah**: `computed<any[]>()` — akses ke `item.amount`, `item.product_name`, dll. tidak type-safe.
- **Fix**: Definisikan `SubmissionItem` interface dan pakai sebagai generic.
- [ ] Definisikan `SubmissionItem` type (bisa di `src/types/otorisasi.ts`)
- [ ] Update computed type ke `computed<SubmissionItem[]>()`

### M8 — Watch fragile di LaporanTrialBalancePage
- **File**: `src/pages/keuangan/LaporanTrialBalancePage.vue` baris 96
- **Masalah**: `watch([begin, end, branch], () => { data.value = null })` bisa race dengan `load()`.
- **Fix**: Hapus watcher, set `data.value = null` secara eksplisit di dalam `search()` sebelum `load()`.
- [ ] Hapus watch, pindahkan reset ke dalam `search()`

### M9 — `immediate: true` tidak perlu di UploadPenghimpunanListPage
- **File**: `src/pages/keuangan/UploadPenghimpunanListPage.vue` baris 51
- **Masalah**: `{ immediate: true }` dipasang pada watcher yang bergantung pada `hasProcessingBatch` yang starts `false` — watcher langsung fire tapi tidak ada efek.
- **Fix**: Hapus `{ immediate: true }`.
- [ ] Hapus `immediate: true` dari watcher

### M10 — Fetch lookup sequential di BankPage openEdit/openDelete
- **File**: `src/pages/keuangan/BankPage.vue` baris 184, 193, 290
- **Masalah**: `await loadLookups()` dijalankan sebelum fetch detail — keduanya independent tapi tidak diparalelkan.
- **Fix**:
  ```ts
  await Promise.all([loadLookups(), api.get(`/api/bank/${id}`)])
  ```
- [ ] Paralelkan di `openEdit`
- [ ] Paralelkan di `openDelete`

---

## LOW

### L1 — `ref` untuk boolean primitif (gunakan `shallowRef`)
- **File**: `src/components/otorisasi/SubmissionDetailDrawer.vue` baris 40; berbagai halaman lain
- **Fix**: `const loading = shallowRef(false)` (dan error, dsb.)
- [ ] `SubmissionDetailDrawer.vue` — loading ke shallowRef
- [ ] Sweep halaman lain saat ada waktu

### L2 — `useFetch.ts` — `data` pakai `ref` (harusnya `shallowRef`)
- **File**: `src/lib/useFetch.ts` baris 11–13
- **Masalah**: `data = ref<T | null>(null)` deep-converts seluruh API response ke reaktif proxy. Untuk widget dashboard yang hanya read, ini overhead tidak perlu.
- **Fix**: `const data = shallowRef<T | null>(null)`
- [ ] Update `useFetch.ts`

### L3 — `void` prefix untuk fire-and-forget di onMounted
- **File**: `src/pages/keuangan/CoaPage.vue` baris 219–222
- **Fix**: `void loadAll(); void loadSubmissions()`
- [ ] Update onMounted di CoaPage (dan sweep halaman lain bila ada eslint rule)

### L4 — `parentBaseClass` computed tidak perlu di AppSidebar
- **File**: `src/components/AppSidebar.vue` baris 264–266
- **Fix**: Inline ke template sebagai expression atau gunakan computed boolean `isCollapsed`.
- [ ] Simplifikasi (low priority)

---

## Urutan Eksekusi yang Direkomendasikan

**Batch 1 — Fix bug nyata dulu (langsung berdampak ke user):**
1. C1 — `api.get()` param drop (PenghimpunanDanaFormPage)
2. H2 — `lookupLoaded` plain var (SubmissionDetailDrawer)
3. H4 — `formatDate` → `dmy()` (KasPage + RecentActivityWidget)

**Batch 2 — Fix arsitektur & performa:**
4. H1 — `downloadBlob` double request (client.ts)
5. H5 — `parsePayload` berulang (OtorisasiPage computed)
6. H6 — sessionStorage rows → filter only (HistoriTransaksiPage)
7. H7 — COA waterfall → Promise.all

**Batch 3 — Konvensi & consistency:**
8. H3 — Hardcoded routes (4 file)
9. M1 — pageSize default 25 (6 file)
10. M2, M3, M6, M8, M9, M10 — watcher/pattern fixes

**Batch 4 — TypeScript & refactor (bisa PR tersendiri):**
11. M5 — `src/types/otorisasi.ts` + sweep
12. M7 — `SubmissionItem` type
13. M4 — Pinia store migration (major refactor, jadwalkan sendiri)
14. L1–L4 — low-impact cleanup

---

## Testing Checklist setelah Fix

```bash
# TypeScript check
cd apps_zakat/web-vue && npx tsc --noEmit

# Smoke test manual:
# 1. Buka form penghimpunan → dropdown produk & donor harus terfilter (C1)
# 2. Buka detail drawer otorisasi, tutup, buka lagi → nama bank harus muncul (H2)
# 3. Export laporan → filename benar, hanya 1 request di Network tab (H1)
# 4. Navigasi upload ZIS → tidak 404 (H3)
# 5. KasPage → tanggal tampil DD-MM-YYYY bukan "19 Mei 2026" (H4)
# 6. OtorisasiPage → buka devtools, verifikasi tidak ada berulang parse di profiler (H5)
```

---

*Plan created: 2026-06-19*
*Source: vue-expert audit agent*
