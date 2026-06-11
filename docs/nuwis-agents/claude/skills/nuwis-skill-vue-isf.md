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

## Rule 1: Pagination Selalu di Atas

```vue
<!-- BENAR — layout wajib untuk semua list page: -->
<div>
  <!-- Toolbar: search + filter + action buttons -->
  <div class="... rounded-t-lg border border-b-0">
    <Input v-model="search" />
    <Button @click="load">Cari</Button>
  </div>

  <!-- Paginator: SELALU di atas tabel, BUKAN di bawah -->
  <div class="... border border-b-0">
    <span>Menampilkan {{ from }}–{{ to }} dari {{ total }} data</span>
    <Paginator :rows="limit" :totalRecords="total" @page="onPageChange" />
  </div>

  <!-- DataTable: TIDAK pakai :paginator="true" -->
  <DataTable :value="rows" class="border rounded-b-lg">
    ...
  </DataTable>
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
