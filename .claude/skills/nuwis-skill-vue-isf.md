# Skill: nuwis-skill-vue-isf
## Konvensi Vue 3 Spesifik isf-app

Skill ini mencakup konvensi proyek yang **override** semua panduan Vue generik.
Sumber kebenaran akhir adalah CLAUDE.md project. Gunakan skill ini sebagai
quick reference saat menulis halaman untuk isf-app.

---

## Stack yang Digunakan

| Layer | Tool | Catatan |
|---|---|---|
| Framework | Vue 3.5 + TypeScript | Selalu `<script setup lang="ts">` |
| Components | PrimeVue 4 **unstyled** | Tidak ada default PrimeVue styles |
| Primitives | reka-ui + `components/ui/` | Buttons, inputs, alerts, badges |
| Styling | Tailwind CSS 4.0 | Layout + semua visual styling |
| Icons | `lucide-vue-next` | BUKAN PrimeIcons |
| HTTP | `lib/api/client.ts` | BUKAN fetch/axios langsung |
| Date | `lib/date.ts` `dmy()` | BUKAN Intl/dayjs inline |
| State | Pinia 2.2 | Tidak perlu store global — gunakan `ref` lokal jika cukup |

---

## Rule 1: Pagination Selalu di Atas — Dalam Satu Card

Toolbar, pagination, dan tabel **wajib dibungkus dalam satu card bersambung**
(`rounded-xl border overflow-hidden`). Tidak boleh berdiri sendiri.

```vue
<!-- BENAR — satu card container: -->
<div class="rounded-xl border border-border bg-surface overflow-hidden">

  <!-- Toolbar: search + action buttons -->
  <div class="px-4 py-2.5 border-b border-border flex items-center justify-between gap-3">
    <div class="relative flex-1 max-w-xs">
      <Search class="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" />
      <input
        v-model="searchInput"
        placeholder="Cari..."
        class="h-8 w-full rounded pl-8 pr-3 text-xs border border-border bg-background
               focus:outline-none focus:ring-1 focus:ring-ring"
      />
    </div>
    <Button v-if="auth.hasMenu(MENU_KEYS.TAMBAH_KEY)" size="sm" @click="openAdd">
      <Plus class="w-3.5 h-3.5 mr-1" /> Tambah
    </Button>
  </div>

  <!-- Pagination: SELALU di atas tabel, bukan di bawah -->
  <div class="px-4 py-2 border-b border-border flex items-center justify-between">
    <span class="text-[11px] text-muted tabular-nums">
      <template v-if="loading">Memuat...</template>
      <template v-else-if="totalRec > 0">
        {{ (page - 1) * pageSize + 1 }}–{{ Math.min(page * pageSize, totalRec) }} dari {{ totalRec }} data
      </template>
      <template v-else>Tidak ada data</template>
    </span>
    <TablePagination
      :page="page"
      :total-pages="totalPages"
      :total="totalRec"
      :page-size="pageSize"
      @prev="page > 1 && (page--, loadData())"
      @next="page < totalPages && (page++, loadData())"
      @update:page-size="(s) => { pageSize = s; page = 1; loadData() }"
    />
  </div>

  <!-- Tabel: TIDAK pakai :paginator="true" -->
  <div class="overflow-x-auto">
    <table class="w-full text-sm">
      <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border">
        <tr>
          <th class="px-4 py-2 text-left font-medium">Kolom 1</th>
          <th class="px-4 py-2 text-left font-medium">Kolom 2</th>
          <th class="px-4 py-2 text-right font-medium w-24">Aksi</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-border">
        <tr v-if="loading">
          <td colspan="3" class="px-4 py-8 text-center text-muted-foreground text-xs">Memuat...</td>
        </tr>
        <tr v-else-if="!rows.length">
          <td colspan="3" class="px-4 py-8 text-center text-muted-foreground text-xs italic">
            Tidak ada data yang ditemukan.
          </td>
        </tr>
        <tr v-for="row in rows" :key="row.id" class="hover:bg-muted/30 transition-colors">
          <td class="px-4 py-1 text-xs">{{ row.kolom1 }}</td>
          <td class="px-4 py-1 text-xs">{{ row.kolom2 }}</td>
          <td class="px-4 py-1 text-right">
            <!-- action buttons -->
          </td>
        </tr>
      </tbody>
    </table>
  </div>

</div>
```

Default rows per page: **25**.

---

## Rule 2: Date Input dan Display

```vue
<!-- INPUT — selalu DateField.vue, v-model = ISO string (YYYY-MM-DD) -->
<DateField v-model="tanggal" />
<!-- tanggal.value = "2026-01-15" (ISO, bukan localized) -->

<!-- DISPLAY — selalu dmy() wrapper -->
<template #body="{ data }">{{ dmy(data.tanggal) }}</template>
<!-- Output: "15-01-2026" -->

<!-- JANGAN inline format: -->
{{ new Date(data.tanggal).toLocaleDateString() }}  <!-- SALAH -->
{{ data.tanggal.split('-').reverse().join('-') }}   <!-- SALAH -->
```

```typescript
import { dmy } from '@/lib/date'
import DateField from '@/components/ui/DateField.vue'
```

---

## Rule 3: HTTP Client

```typescript
// BENAR:
import { GET, POST, blob } from '@/lib/api/client'

const res = await GET<{ rows: Item[]; pagination: Pagination }>(
  '/api/keuangan/kas',
  { page: 1, limit: 25 }
)
// res langsung berisi payload.data (client.ts sudah unwrap)

// POST
await POST('/api/keuangan/kas', { tanggal: '2026-01-15', jumlah: 100000 })

// Download file
const b = await blob('/api/keuangan/laporan/kas/export', { tgl_awal, tgl_akhir })
downloadBlob(b, 'laporan-kas.xlsx')

// JANGAN:
const res = await fetch('/api/...')
import axios from 'axios'
```

---

## Rule 4: Async Feedback Wajib

```typescript
// Pattern wajib — semua async operation:
const loading = ref(false)

async function save() {
  loading.value = true
  try {
    await POST('/api/...', payload.value)
    toast.add({ severity: 'success', summary: 'Berhasil', detail: 'Data disimpan', life: 3000 })
    formVisible.value = false
    await load()  // refresh list
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Error', detail: 'Gagal menyimpan data', life: 3000 })
  } finally {
    loading.value = false  // HARUS di finally
  }
}
```

---

## Rule 5: Icons

```vue
<!-- BENAR — Lucide icons: -->
<script setup>
import { PlusIcon, PencilIcon, TrashIcon, SearchIcon, ChevronRightIcon } from 'lucide-vue-next'
</script>
<template>
  <Button><PlusIcon class="w-4 h-4 mr-1" /> Tambah</Button>
</template>

<!-- SALAH — PrimeIcons tidak dipakai: -->
<Button icon="pi pi-plus" />
<i class="pi pi-search" />
```

---

## Rule 6: Komponen UI yang Sudah Ada

Cek `components/ui/` sebelum buat komponen baru:

| Komponen | Import | Gunakan untuk |
|---|---|---|
| `Button` | `@/components/ui/Button.vue` | Semua tombol |
| `Input` | `@/components/ui/Input.vue` | Text input |
| `Card` | `@/components/ui/Card.vue` | Container card |
| `Alert` | `@/components/ui/Alert.vue` | Error/warning messages |
| `DateField` | `@/components/ui/DateField.vue` | Semua date input |
| `SearchSelect` | `@/components/ui/SearchSelect.vue` | Dropdown dengan search (combobox) |
| `Modal` | `@/components/ui/Modal.vue` | Dialog/modal |
| `TablePagination` | `@/components/ui/TablePagination.vue` | Pagination display wrapper |

---

## Rule 9: Badge Status — Warna Standar

Gunakan palet yang konsisten untuk badge status di seluruh halaman:

```vue
<!-- Status Aktif / Non-aktif -->
<span
  class="inline-flex items-center px-1.5 py-px rounded text-[10px] font-semibold"
  :class="row.status === 'A'
    ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300'
    : 'bg-zinc-100 text-zinc-500 dark:bg-zinc-800 dark:text-zinc-400'"
>
  {{ row.status === 'A' ? 'Aktif' : 'Tidak Aktif' }}
</span>

<!-- Tipe Induk/Detail (contoh is_detail) -->
<span
  class="inline-flex items-center px-1.5 py-px rounded text-[10px] font-semibold"
  :class="row.is_detail === 'F'
    ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300'
    : 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300'"
>
  {{ row.is_detail === 'F' ? 'Induk' : 'Detail' }}
</span>
```

**Palet badge yang dipakai proyek ini:**

| Nilai | Background | Text | Konteks |
|---|---|---|---|
| Aktif / Active | `bg-emerald-100` | `text-emerald-700` | status='A' |
| Non-Aktif | `bg-zinc-100` | `text-zinc-500` | status='N' |
| Induk / Group | `bg-blue-100` | `text-blue-700` | is_detail='F' |
| Detail / Leaf | `bg-amber-100` | `text-amber-700` | is_detail='T' |
| Pending | `bg-yellow-100` | `text-yellow-700` | status=PENDING |
| Authorized | `bg-emerald-100` | `text-emerald-700` | status=AUTHORIZED |
| Rejected | `bg-red-100` | `text-red-700` | status=REJECTED |

> **Jangan** gunakan `green`/`gray` — selalu `emerald`/`zinc`.

---

## Rule 10: Modal — Ukuran & Padding Standar

```vue
<!-- BENAR — struktur modal CRUD: -->
<div class="fixed inset-0 z-50 bg-black/40 flex items-center justify-center p-4">
  <div class="bg-background rounded-xl shadow-xl flex flex-col max-h-[90vh] w-full max-w-2xl">

    <!-- Header -->
    <div class="flex items-center justify-between px-6 py-4 border-b border-border shrink-0">
      <h2 class="text-sm font-semibold">Judul Modal</h2>
      <button @click="$emit('close')" class="text-muted-foreground hover:text-foreground">
        <X class="w-4 h-4" />
      </button>
    </div>

    <!-- Body -->
    <div class="px-6 py-5 overflow-y-auto space-y-4">
      <!-- fields — grid 2 kolom di desktop: -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div class="flex flex-col gap-1">
          <label class="text-xs font-medium">Label <span class="text-red-500">*</span></label>
          <input class="h-9 w-full rounded-lg px-2.5 text-xs border border-border
                         bg-background focus:outline-none focus:ring-1 focus:ring-ring" />
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="flex justify-end gap-2 px-6 py-3 border-t border-border shrink-0">
      <Button variant="outline" size="sm" @click="$emit('close')">Batal</Button>
      <Button size="sm" :disabled="loading" @click="submit">
        {{ loading ? 'Menyimpan...' : 'Simpan' }}
      </Button>
    </div>

  </div>
</div>
```

**Standar modal:**
- Overlay: `bg-black/40` (bukan `/50`)
- Lebar: `max-w-2xl` untuk form CRUD, `max-w-sm` untuk konfirmasi/delete
- Padding header: `px-6 py-4`
- Padding body: `px-6 py-5`
- Padding footer: `px-6 py-3`
- Input: `h-9 rounded-lg px-2.5 text-xs`
- Field pairs: `grid grid-cols-1 sm:grid-cols-2 gap-4`

---

## Rule 11: Tabel — Padding & Typography Standar

```vue
<table class="w-full text-sm">
  <!-- Header: text-[10px], py-2, font-medium -->
  <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border">
    <tr>
      <th class="px-4 py-2 text-left font-medium">Label</th>
      <th class="px-4 py-2 text-right font-medium w-24">Aksi</th>
    </tr>
  </thead>
  <!-- Rows: py-1, text-xs -->
  <tbody class="divide-y divide-border">
    <tr class="hover:bg-muted/30 transition-colors">
      <td class="px-4 py-1 text-xs">nilai</td>
      <td class="px-4 py-1 text-right">
        <!-- action buttons -->
      </td>
    </tr>
  </tbody>
</table>
```

**Standar tabel:**
- Header: `text-[10px] py-2` — BUKAN `text-xs py-2.5`
- Data row: `py-1 text-xs` — BUKAN `py-2.5`
- Row hover: `hover:bg-muted/30 transition-colors`
- Loading/empty colspan selalu full + `py-8 text-center text-muted-foreground text-xs`

---

## Rule 12: Form Input / Create Page — Standar (referensi: Transaksi Umum)

Semua halaman input/Create dan modal form **wajib** mengikuti style ini.
Referensi kanonik: `pages/finance/general-transaction/GeneralTransactionCreatePage.vue`.
Palet: **slate** (netral) + **indigo** (fokus/aksen) + **emerald** (simpan/positif) + **red** (hapus/negatif).

### 12.1 Kerangka halaman

```vue
<template>
  <div class="p-3 sm:p-4 space-y-3">
    <!-- Tombol kembali (judul halaman ada di breadcrumb header — JANGAN tambah <h1>) -->
    <div class="flex items-center gap-2">
      <button
        class="flex items-center gap-1 rounded px-2 py-1 text-xs text-slate-500 hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-zinc-800"
        @click="router.push({ name: 'finance-...' })"
      >
        <ArrowLeft class="h-3.5 w-3.5" /> Kembali
      </button>
    </div>

    <Alert v-if="formError" variant="destructive">{{ formError }}</Alert>

    <!-- Card-card form di sini -->
  </div>
</template>
```

### 12.2 Card form — header gelap

```vue
<div class="rounded-lg border border-slate-200 bg-white dark:bg-zinc-900 overflow-hidden">
  <!-- Header bar gelap: bg-slate-800 (utama) / bg-slate-700 (sekunder) -->
  <div class="flex items-center justify-between bg-slate-800 px-4 py-2">
    <h2 class="font-bold text-xs tracking-widest text-white uppercase">Judul Card</h2>
    <!-- badge status opsional di kanan -->
    <span class="bg-slate-600 text-white text-xs px-2 py-0.5 rounded">DRAFT</span>
  </div>
  <!-- Body -->
  <div class="p-4 space-y-3">
    <!-- field di sini -->
  </div>
</div>
```

### 12.3 Field — label + input

```vue
<div>
  <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
    Label Field <span class="text-red-500">*</span>
  </label>

  <!-- Text input -->
  <input
    v-model="x"
    placeholder="Opsional"
    class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
  />

  <!-- Textarea (selalu resizable vertikal) -->
  <textarea
    v-model="keterangan"
    rows="3"
    class="w-full border border-slate-200 rounded px-3 py-1.5 text-sm text-slate-700 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-y min-h-[72px]"
  />

  <!-- Tanggal — selalu DateField (lihat Rule 2) -->
  <DateField v-model="tanggal" />

  <!-- Dropdown panjang (rekening, produk, program, donatur, COA) — selalu SearchSelect.
       JANGAN bikin pola "input + tombol Cari + list" manual. -->
  <SearchSelect v-model="selectedValue" :options="options" placeholder="Cari kode / nama..." />

  <!-- Dropdown pendek/enum tetap pakai <select> dengan style yang sama -->
  <select v-model="enumVal" class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
    <option v-for="o in OPTS" :key="o.value" :value="o.value">{{ o.label }}</option>
  </select>
</div>
```

Pola `SearchSelect`: `*SelectedValue = shallowRef('')` + `*Options = computed(() => rows.map(r => ({ value, label })))`
+ `load*Options()` muat di awal (mount / buka drawer) + `watch(*SelectedValue)` sinkron ke field yang disimpan.

### 12.4 Tombol aksi — Batal & Simpan

```vue
<div class="flex gap-2 pt-1">
  <button
    class="flex-1 border-2 border-slate-300 text-slate-600 font-semibold hover:bg-slate-50 px-4 py-2 rounded text-sm"
    @click="router.push({ name: 'finance-...' })"
  >Batal</button>
  <button
    class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-6 py-2 rounded text-sm shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
    :disabled="saving || !valid"
    @click="submitForm"
  >{{ saving ? 'Menyimpan...' : 'Simpan' }}</button>
</div>
```

### 12.5 Ikon aksi baris (edit/hapus) di tabel detail

```vue
<button class="rounded p-1.5 text-indigo-500 hover:bg-indigo-50 hover:text-indigo-700" title="Edit" @click="...">
  <Pencil class="h-4 w-4" />
</button>
<button class="rounded p-1.5 text-red-500 hover:bg-red-50 hover:text-red-700" title="Hapus" @click="...">
  <Trash2 class="h-4 w-4" />
</button>
```

### 12.6 Ringkasan token

| Elemen | Kelas |
|---|---|
| Wrapper halaman | `p-3 sm:p-4 space-y-3` |
| Card | `rounded-lg border border-slate-200 bg-white dark:bg-zinc-900 overflow-hidden` |
| Header card (utama/sekunder) | `bg-slate-800` / `bg-slate-700` + `px-4 py-2` |
| Judul header card | `font-bold text-xs tracking-widest text-white uppercase` |
| Body card | `p-4 space-y-3` |
| Label field | `mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide` |
| Wajib | `<span class="text-red-500">*</span>` |
| Input/select | `rounded border border-slate-200 px-3 py-1.5 text-sm focus:ring-2 focus:ring-indigo-500` |
| Textarea | + `resize-y min-h-[72px]` |
| Tombol Simpan | `bg-emerald-600 hover:bg-emerald-700 text-white font-bold` |
| Tombol Batal | `border-2 border-slate-300 text-slate-600 font-semibold` |
| Ikon edit / hapus | `text-indigo-500` `Pencil` / `text-red-500` `Trash2`, `h-4 w-4`, `p-1.5` |

> Layout split (header kiri sticky + tabel detail kanan) **khusus** transaksi multi-baris
> (jurnal/Transaksi Umum). Form satu-entitas cukup card tunggal/2-kolom — tetap pakai token di atas.

---

## Rule 13: Page Scaffold & Routing — Standar Membuat Halaman Baru

Setiap halaman baru wajib lewat 3 langkah yang **harus sinkron** (3-way consistency):

1. **`lib/menu/registry.ts`** — daftarkan key di `MENU_KEYS` (bahasa Inggris, mis. `finance.cash`).
2. **`router/index.ts`** — tambah route bernama (named route, kebab, prefix domain Inggris):
   ```ts
   {
     path: '/finance/cash/create',
     name: 'finance-cash-create',
     component: () => import('@/pages/finance/cash/CashCreatePage.vue'),
     meta: { title: 'Tambah Kas', menu_key: 'finance.cash' as MenuKey },
   },
   ```
3. **seed SQL** (`infra/db/migrations/isf_auth/seed-menu-*.sql`) — `menu` + `role_menu` (ditangani `nuwis-seed-gen`).

### `meta` wajib
- `title` — **string ini yang muncul di breadcrumb** app header. Wajib diisi & deskriptif.
- `menu_key` — `as MenuKey`; dipakai guard `beforeEach` untuk RBAC (Rule 8).
- `public: true` / `requiresNoTenant: true` hanya untuk login/no-tenant.

### Breadcrumb — JANGAN render judul halaman sendiri
App shell (`AppHeader.vue`) **otomatis** menampilkan breadcrumb `Induk / Judul`
dari `meta.title` + prefix nama route (`parentMap`: `finance-…`→domain). Maka:

- **JANGAN** ada `<PageHeader>` atau `<h1>` judul di halaman — itu duplikat breadcrumb.
- **List page**: langsung render card tabel (Rule 1). Tanpa judul.
- **Create / Detail page**: awali dengan **tombol Kembali** saja (Rule 12.1), bukan judul.
  Sub-judul/mode ("Edit"/"Input") boleh sebagai teks kecil `text-xs text-slate-400`.
- Beri nama route dengan prefix domain yang sudah ada (`finance-`, `dashboard-`, `parameter-`,
  `admin-`, `profile-`) agar breadcrumb induk benar. Jika butuh crumb eksplisit, set
  `meta.breadcrumb: string[]` (didukung AppHeader, default tidak dipakai).

### Pilih kerangka per jenis halaman
| Jenis halaman | Ikuti |
|---|---|
| Daftar/List (tabel + paginasi) | **Rule 1** (paginasi di atas, 1 card) + **Rule 11** (tabel) |
| Form input / Create / Edit | **Rule 12** (card header gelap, token slate/indigo) |
| Modal CRUD | **Rule 10** (shell) + **Rule 12** (isi field) |
| Laporan / Report | **Rule 7** (no auto-load, tombol Tampilkan) |

### Async, RBAC, tanggal, ikon
Selalu: feedback async (Rule 4), `v-if` dari `auth.menus`+`MENU_KEYS` (Rule 8),
`DateField`/`dmy()` (Rule 2), Lucide (Rule 5), `lib/api/client` (Rule 3).

> Referensi halaman yang sudah sesuai standar: List → `*ListPage.vue` mana pun di
> `pages/finance/`; Form → `general-transaction/GeneralTransactionCreatePage.vue`
> dan `fund-distribution/FundDistributionCreatePage.vue`.

---

## Rule 7: Report Page — Tidak Auto-Load

```vue
<script setup>
// BENAR — report page tidak auto-load:
const hasData = ref(false)  // false sampai user klik Tampilkan
const rows = ref([])

async function tampilkan() {
  // load data hanya saat user klik
  loading.value = true
  try {
    const res = await GET('/api/.../laporan', { tgl_awal, tgl_akhir })
    rows.value = res.rows
    hasData.value = true
  } finally {
    loading.value = false
  }
}

// TIDAK ada onMounted(load) untuk report page
</script>

<template>
  <!-- State kosong sebelum user klik: -->
  <div v-if="!hasData" class="flex items-center justify-center h-48 text-muted-foreground">
    Pilih periode dan klik "Tampilkan" untuk melihat laporan
  </div>

  <!-- Export disabled sampai ada data: -->
  <Button :disabled="!hasData" @click="exportXlsx">Export Excel</Button>
```

---

## Rule 8: Role-Based UI

```vue
<script setup>
import { useAuthStore } from '@/stores/auth'
import { MENU_KEYS } from '@/lib/menu/registry'

const auth = useAuthStore()
</script>

<template>
  <!-- BENAR — v-if dari auth store: -->
  <Button v-if="auth.menus.includes(MENU_KEYS.keuangan.transaksi.tambah)">
    Tambah
  </Button>

  <!-- SALAH — CSS hide: -->
  <Button :style="{ display: canAdd ? 'block' : 'none' }">  <!-- JANGAN -->

  <!-- SALAH — computed dari role: -->
  <Button v-if="auth.roles.includes('ADMIN')">  <!-- Gunakan menus[], bukan roles[] -->
</template>
```

---

## API Response Shape

`lib/api/client.ts` sudah unwrap `payload.data` otomatis:

```typescript
// Backend return: { data: { rows: [...], pagination: {...} }, meta: {...} }
// client.ts extracting: res = payload.data
// Jadi di component kamu terima langsung:
const res = await GET<{ rows: Item[]; pagination: Pagination }>('/api/...')
res.rows       // ← langsung available
res.pagination // ← langsung available

// Single object:
const item = await GET<Item>('/api/.../1')
item.id  // ← langsung available
```

---

## TypeScript: Type Definitions

```typescript
// Define interface untuk rows:
interface {Resource}Row {
  id: number
  tanggal: string   // ISO YYYY-MM-DD (tampilkan dengan dmy())
  jumlah: number
  keterangan?: string
}

// Pagination interface (sudah ada di project):
interface Pagination {
  page: number
  limit: number
  total: number
  total_pages: number
}
```
