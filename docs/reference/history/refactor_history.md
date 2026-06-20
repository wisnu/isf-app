# Refactor History — apps_zakat/web-vue

**Tanggal:** 2026-06-06
**Commit:** `a0c22fc` — `[VUE-BP] refactor(web-vue): apply vue-best-practices across apps_zakat UI`
**Skill yang digunakan:** `vue-best-practices` (referensi: `reactivity.md`, `sfc.md`, `component-data-flow.md`, `composables.md`)

---

## 1. `shallowRef` untuk nilai primitif

### Apa yang diubah

Seluruh `ref()` yang membungkus nilai primitif diganti dengan `shallowRef()` di 36 file.

Nilai yang termasuk primitif dan harus pakai `shallowRef`:
- Boolean: `ref(false)` / `ref(true)`
- Number: `ref(0)` / `ref(1)` / `ref(20)`
- String: `ref('')` / `ref(today)` / `ref('actual')`
- Union primitif: `ref<string | null>(null)` / `ref<number | null>(null)`
- `Set<string>` yang selalu di-replace wholesale (bukan di-mutasi in-place dengan `.add()/.delete()`)

Nilai yang **tetap menggunakan `ref()`** (tidak diubah):
- Array of objects: `ref<SomeRow[]>([])` — template mengakses properti nested secara reaktif
- Complex response objects: `ref<PayloadType | null>(null)` — template mengakses properti dalam secara reaktif

**Contoh perubahan:**
```ts
// Sebelum
const loading = ref(false)
const errorMsg = ref<string | null>(null)
const page = ref(1)
const rows = ref<TransaksiRow[]>([])   // ← ini tetap ref()

// Sesudah
const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)
const page = shallowRef(1)
const rows = ref<TransaksiRow[]>([])   // ← tetap ref()
```

### Kenapa

`ref()` untuk nilai primitif membuat Vue membangun deep reactive proxy yang tidak berguna — primitif tidak punya properti nested yang perlu dilacak. `shallowRef()` hanya melacak perubahan pada `.value` itu sendiri, yang memang satu-satunya hal yang berubah untuk string/number/boolean. Hasilnya: overhead reaktivitas lebih rendah, tidak ada perubahan perilaku.

Referensi: `reactivity.md` — *"Always use `shallowRef()` instead of `ref()` for primitive values for better performance."*

### File yang diubah (36 file)

**Pages — Dashboard:**
- `pages/DashboardPage.vue`
- `pages/DashboardKeuanganPage.vue`
- `pages/DashboardPenghimpunanPage.vue`
- `pages/DashboardPenyaluranPage.vue`

**Pages — Auth & Umum:**
- `pages/LoginPage.vue`

**Pages — Admin:**
- `pages/admin/RoleMenuPage.vue`

**Pages — Keuangan (CRUD & Transaksi):**
- `pages/keuangan/CoaPage.vue`
- `pages/keuangan/HistoriTransaksiPage.vue`
- `pages/keuangan/HistoriTransaksiDetailPage.vue`

**Pages — Keuangan (Upload):**
- `pages/keuangan/UploadPenghimpunanPage.vue`
- `pages/keuangan/UploadPenghimpunanListPage.vue`
- `pages/keuangan/UploadPenghimpunanDetailPage.vue`

**Pages — Laporan (17 file):**
- `pages/keuangan/LaporanJurnalHarianPage.vue`
- `pages/keuangan/LaporanGeneralTransactionPage.vue`
- `pages/keuangan/LaporanCashDailyPage.vue`
- `pages/keuangan/LaporanCashSummaryPage.vue`
- `pages/keuangan/LaporanCashMonthlyPage.vue`
- `pages/keuangan/LaporanBukuBesarPage.vue`
- `pages/keuangan/LaporanTrialBalancePage.vue`
- `pages/keuangan/LaporanNeracaPage.vue`
- `pages/keuangan/LaporanArusKasPage.vue`
- `pages/keuangan/LaporanAmilPage.vue`
- `pages/keuangan/LaporanARSummaryPage.vue`
- `pages/keuangan/LaporanPenghimpunanDanaPage.vue`
- `pages/keuangan/LaporanPenyaluranDanaPage.vue`
- `pages/keuangan/LaporanPerubahanDanaPage.vue`
- `pages/keuangan/LaporanPerubahanDanaDetailPage.vue`
- `pages/keuangan/LaporanPiutangRealisasiPage.vue`
- `pages/keuangan/LaporanRealisasiMemoPage.vue`
- `pages/keuangan/LaporanListUangMukaPage.vue`
- `pages/keuangan/LaporanUpzPage.vue`

**Components:**
- `components/AppSidebar.vue` (`expandedParents: Set<string>` — replaced wholesale)
- `components/layout/FilterPanel.vue` (`tipsOpen`)
- `components/ui/SearchSelect.vue` (`open`, `query`, `activeIdx`)
- `components/ui/DateField.vue` (`text`)

**Lib:**
- `lib/useFetch.ts` (`loading`, `error` — `data` tetap `ref<T|null>`)

---

## 2. Hapus `{ deep: true }` dari watch CoaPage

### Apa yang diubah

`CoaPage.vue` — watch untuk `[typeFilters, sifatFilter, levelMax]` sebelumnya menggunakan `{ deep: true }`:

```ts
// Sebelum
watch([typeFilters, sifatFilter, levelMax], () => {
  page.value = 1
  load()
}, { deep: true })

// Sesudah
watch([typeFilters, sifatFilter, levelMax], () => {
  page.value = 1
  load()
})
```

### Kenapa

Setelah ketiga ref tersebut diubah ke `shallowRef`, `{ deep: true }` tidak hanya tidak diperlukan — tapi juga keliru secara konseptual. `shallowRef` hanya reaktif saat `.value` diganti (reference change). `{ deep: true }` dimaksudkan untuk melacak mutasi internal objek, yang tidak relevan untuk `shallowRef`. Opsi ini aman dihapus karena `typeFilters` selalu di-replace (`typeFilters.value = new Set(...)`) bukan dimutasi in-place.

---

## 3. Perbaikan pola debounce di CoaPage

### Apa yang diubah

`CoaPage.vue` — debounce search menggunakan variabel `let` di luar scope watch:

```ts
// Sebelum — mutable di luar watch, tidak menggunakan Vue cleanup
let searchTimer: ReturnType<typeof setTimeout> | undefined

watch(search, () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    page.value = 1
    load()
  }, 350)
})

// Sesudah — local const, cleanup via Vue's onCleanup
watch(search, (_val, _old, onCleanup) => {
  const timer = setTimeout(() => {
    page.value = 1
    load()
  }, 350)
  onCleanup(() => clearTimeout(timer))
})
```

### Kenapa

Pola lama menggunakan variabel mutable (`let searchTimer`) yang hidup di luar callback watch. Ini mengandalkan side effect manual yang tidak terikat lifecycle Vue. Pola yang benar menggunakan parameter `onCleanup` dari Vue — saat watcher dijalankan ulang (karena `search` berubah lagi) atau saat komponen di-unmount, Vue otomatis memanggil fungsi cleanup sehingga timer sebelumnya pasti dibatalkan. Lebih aman dan tidak ada kebocoran timer.

Referensi: `reactivity.md` — *"Clean up async effects for watchers."*

---

## 4. Ekstraksi komponen `TransaksiDeleteDialog`

### Apa yang diubah

`HistoriTransaksiPage.vue` sebelumnya memiliki modal konfirmasi hapus transaksi secara inline di bagian bawah template (26 baris). Komponen baru dibuat:

**File baru:** `components/keuangan/TransaksiDeleteDialog.vue`

```ts
// Props
transactionId: number
message: string | null
deleting: boolean

// Emits
cancel: []
confirm: []
```

Penggunaan di `HistoriTransaksiPage.vue`:
```html
<!-- Sebelum: 26 baris template inline di halaman -->
<div v-if="deleteConfirmId !== null" class="fixed inset-0 z-50 ...">
  ...26 baris...
</div>

<!-- Sesudah: 1 baris, concern terpisah -->
<TransaksiDeleteDialog
  v-if="deleteConfirmId !== null"
  :transaction-id="deleteConfirmId"
  :message="deleteMsg"
  :deleting="deleting"
  @cancel="deleteConfirmId = null; deleteMsg = null"
  @confirm="confirmDelete"
/>
```

### Kenapa

`HistoriTransaksiPage` memiliki 480 baris dengan beberapa concern berbeda: filter sidebar, tabel data, pagination, dan dialog konfirmasi hapus. Skill `vue-best-practices` menetapkan aturan split jika komponen memiliki 3+ seksi UI yang berbeda. Dialog konfirmasi adalah concern yang paling jelas untuk dipisah — ia punya state sendiri, logika tampil/sembunyi sendiri, dan berpotensi reusable. Memisahkannya membuat halaman lebih tipis dan dialog bisa diuji/dimodifikasi secara independen.

Referensi: `component-data-flow.md` — *"Props down, events up."* — Dialog menerima data lewat props, mengirim keputusan user lewat emits.

---

## 5. Migrasi ke `useTemplateRef()` untuk DOM refs

### Apa yang diubah

Dua komponen yang mengakses elemen DOM via template ref dimigrasi ke `useTemplateRef()` (Vue 3.5+):

**`components/ui/DateField.vue`:**
```ts
// Sebelum
const picker = ref<HTMLInputElement | null>(null)

// Sesudah
const picker = useTemplateRef<HTMLInputElement>('picker')
```

**`components/ui/SearchSelect.vue`:**
```ts
// Sebelum
const inputEl = ref<HTMLInputElement | null>(null)

// Sesudah
const inputEl = useTemplateRef<HTMLInputElement>('inputEl')
```

### Kenapa

`ref<HTMLElement | null>(null)` untuk mengakses DOM element adalah pola Vue 3 lama. Vue 3.5 memperkenalkan `useTemplateRef()` yang lebih eksplisit: nama string yang dipass ke `useTemplateRef('name')` langsung terikat ke `ref="name"` di template, membuat hubungan antara script dan template lebih mudah ditelusuri. Selain itu, `useTemplateRef` mengembalikan tipe yang lebih tepat — tidak perlu union `| null` manual.

Referensi: `sfc.md` — *"Access DOM / component refs with `useTemplateRef()` in Vue 3.5+."*

---

## Ringkasan

| # | Perubahan | File Terdampak | Alasan Utama |
|---|-----------|----------------|--------------|
| 1 | `ref()` → `shallowRef()` untuk primitif | 36 file | Kurangi overhead reaktivitas |
| 2 | Hapus `{ deep: true }` dari watch | `CoaPage.vue` | Tidak relevan setelah shallowRef |
| 3 | Perbaikan debounce pattern | `CoaPage.vue` | Gunakan Vue `onCleanup`, hindari mutable di luar scope |
| 4 | Ekstraksi `TransaksiDeleteDialog` | `HistoriTransaksiPage.vue` + 1 file baru | Single responsibility, props/emits contract |
| 5 | `ref<HTML*>` → `useTemplateRef()` | `DateField.vue`, `SearchSelect.vue` | API Vue 3.5 yang lebih eksplisit untuk DOM refs |

**Yang tidak diubah (sengaja):**
- Semua halaman sudah menggunakan `<script setup lang="ts">` — tidak perlu migrasi dari Options API
- Semua `v-for` sudah memiliki `:key` — sudah compliant
- Tidak ada penggunaan `v-html` — tidak ada isu XSS
- Semua komponen sudah PascalCase di template — sudah compliant
- SFC section order (`<script>` → `<template>`) sudah benar di seluruh codebase
