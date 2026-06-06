# Alternatif UI Library untuk apps_zakat/web-vue

## Konteks Stack Saat Ini

- **Tailwind v4** (74/75 file — tidak mau diganti)
- **reka-ui** sudah terinstall (headless primitives: Dialog, Dropdown, Tooltip)
- **16 custom UI components** (Button, Alert, Card, DateField, dll.)
- **Kebutuhan utama**: DataTable untuk 17 halaman laporan (sort, pagination, loading, empty state)
- **Constraint**: DD-MM-YYYY date format wajib, RBAC menu system di sidebar

---

## Kategori Alternatif

### A. Khusus DataTable (tanpa ganti komponen lain)

#### 1. TanStack Table v8 (Vue adapter) ⭐ Rekomendasi kuat
- **Apa**: Headless table engine — zero UI, zero CSS, hanya logic
- **Kelebihan**:
  - Tailwind-native, zero konflik
  - Fitur lengkap: sort, filter, pagination, row selection, virtual scroll, grouping
  - TypeScript excellent
  - Paling populer di ekosistem (React, Vue, Solid — satu API)
  - Bundle size kecil (~15kb)
- **Kekurangan**:
  - Harus buat UI table sendiri (row, cell, header rendering)
  - Lebih banyak boilerplate per tabel vs PrimeVue DataTable
  - Tidak ada loading overlay / empty state bawaan
- **Cocok jika**: Mau kontrol penuh styling, tidak mau dependency besar

```ts
// Contoh minimal
import { useVueTable, getCoreRowModel } from '@tanstack/vue-table'
const table = useVueTable({ data, columns, getCoreRowModel: getCoreRowModel() })
```

#### 2. AG Grid Community (free tier)
- **Apa**: Grid paling powerful di dunia web
- **Kelebihan**:
  - Fitur enterprise-grade gratis: virtual scroll 1M baris, Excel export, row grouping
  - Tailwind support ada
- **Kekurangan**:
  - Bundle besar (~400kb)
  - Overkill untuk laporan sederhana
  - Style override butuh effort (opinionated CSS)
  - Lisensi Community terbatas (tidak untuk semua use case commercial)
- **Cocok jika**: Ada kebutuhan grid kompleks seperti pivot table atau jutaan baris

#### 3. vue3-easy-data-table
- **Apa**: Simple DataTable khusus Vue 3
- **Kelebihan**: Ringan, mudah setup
- **Kekurangan**: Fitur terbatas, styling terbatas, komunitas kecil
- **Tidak direkomendasikan** untuk produksi skala ISF

---

### B. Component Library Lengkap (alternatif Sakai/PrimeVue)

#### 4. shadcn-vue ⭐ Paling cocok dengan stack saat ini
- **Apa**: Koleksi komponen di atas reka-ui + Tailwind — **bukan library, tapi copy-paste komponen**
- **Kelebihan**:
  - **reka-ui sudah terinstall** — zero dependency tambahan untuk primitives
  - Tailwind-native by design
  - Komponen di-copy ke codebase (full ownership, tidak ada breaking change dari upstream)
  - Ada: Button, Card, Dialog, Toast, Badge, Table, Select, DatePicker, dll.
  - Tidak ada CSS konflik sama sekali
- **Kekurangan**:
  - **Table-nya hanya HTML table biasa** — tidak ada sort/filter/pagination bawaan (perlu pair dengan TanStack Table)
  - Komponen harus di-install satu per satu via CLI (`npx shadcn-vue@latest add table`)
  - Belum ada DataTable sekelas PrimeVue out of the box
- **Cocok jika**: Mau upgrade komponen dialog, toast, badge, dll. tanpa tambah library baru

#### 5. Nuxt UI v3 (standalone)
- **Apa**: Component library dari tim Nuxt, Tailwind-first, bisa dipakai tanpa Nuxt
- **Kelebihan**:
  - Design modern, polish tinggi
  - Ada UTable dengan sort/filter/pagination
  - Tailwind v4 compatible (versi terbaru)
  - Tree-shakeable
- **Kekurangan**:
  - Desain untuk Nuxt — standalone mode masih relatif baru, dokumentasi kurang
  - Punya sistem warna sendiri yang perlu di-override untuk brand ISF
  - Dependency tambahan (@nuxt/ui)
- **Cocok jika**: Mau tampilan polished tanpa PrimeVue, dan siap debug incompatibility

#### 6. Vuestic UI
- **Apa**: Component library Vue 3 dengan DataTable
- **Kelebihan**: Design clean, DataTable ada, gratis
- **Kekurangan**: Kurang populer, Tailwind integration tidak seamless, punya CSS sendiri
- **Tidak direkomendasikan** untuk proyek yang sudah heavy Tailwind

#### 7. Naive UI
- **Apa**: Component library Vue 3 populer (China origin)
- **Kelebihan**: DataTable powerful (virtual scroll, tree data), TypeScript excellent
- **Kekurangan**: Styling system sendiri (CSS-in-JS), tidak bisa coexist dengan Tailwind secara bersih
- **Tidak direkomendasikan** jika Tailwind dipertahankan

---

## Matriks Keputusan

| Opsi | DataTable | Tailwind v4 | Dep baru? | Effort | Rekomendasi |
|------|-----------|-------------|-----------|--------|-------------|
| **PrimeVue** (sedang dicoba) | ✅ Full | ✅ Unstyled | Ya | Rendah | ✅ Pragmatis |
| **TanStack Table** | ✅ Headless | ✅ Native | Ya (kecil) | Sedang | ✅ Kontrol penuh |
| **shadcn-vue** | ⚠️ Table biasa | ✅ Native | Tidak (reka-ui ada) | Sedang | ✅ Untuk non-table components |
| **shadcn-vue + TanStack** | ✅ Full | ✅ Native | Ya (tanstack kecil) | Sedang-Tinggi | ✅ Best of both |
| **AG Grid** | ✅ Enterprise | ⚠️ Partial | Ya (besar) | Tinggi | ❌ Overkill |
| **Nuxt UI** | ✅ UTable | ✅ v4 | Ya | Sedang | ⚠️ Risiko standalone |
| **Naive UI** | ✅ Powerful | ❌ Konflik | Ya | Tinggi | ❌ |

---

## Rekomendasi Akhir

**Untuk kebutuhan DataTable laporan**: lanjutkan PrimeVue yang sedang dicoba — paling cepat, unstyled mode bersih, sudah setengah jalan.

**Alternatif terbaik jika PrimeVue tidak cocok**: TanStack Table v8 — buat satu `useDataTable` composable + `AppTable.vue` wrapper, dipakai di semua 17 halaman laporan. Lebih effort di awal tapi zero CSS konflik dan lebih lightweight.

**shadcn-vue**: bukan untuk DataTable, tapi worth dipertimbangkan untuk upgrade Dialog, Toast, DatePicker — karena reka-ui sudah ada, tinggal copy komponen yang dibutuhkan.
