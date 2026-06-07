---
name: vue-primevue-zakat-ui
description: >
  Use this skill when building or generating Vue 3 UI components, pages, or
  layouts for the isf-app ZISWAF platform (Zakat + Wakaf portals) using
  PrimeVue 4 unstyled + Tailwind CSS v4 + reka-ui hybrid stack. Triggers
  whenever the user asks to: create a table, form, dialog, page, dashboard,
  or any UI component; scaffold a new page or route; add pagination (ALWAYS
  top-placed using standalone Paginator, never DataTable built-in); build
  filters, status badges, approval workflows, report pages, or role-gated UI.
  Also triggers on requests like "add a list page", "create the muzakki table",
  "build the distribution form", "scaffold the admin layout", "add a laporan
  page", or any frontend task in the web-vue service. When in doubt, use this
  skill — it encodes all project-specific conventions that override generic
  Vue or PrimeVue defaults.
---

# isf-app web-vue — UI Skill
# Stack: Vue 3.5 + PrimeVue 4.5 (unstyled) + Tailwind CSS v4 + reka-ui

This skill encodes all UI conventions, stack rules, and code patterns for the
isf-app ZISWAF platform frontend (web-vue service). Always consult this before
generating any Vue component, page, or layout in this project.

---

## Stack Quick Reference

- **Vue 3.5** — `<script setup lang="ts">` + Composition API. No Options API. No `.js` files in `src/`.
- **PrimeVue 4.5** — **unstyled mode**. Zero default styles. Used for headless complex components only.
- **reka-ui** — shadcn-vue pattern. Used for primitives alongside `components/ui/`.
- **Tailwind CSS v4** — ALL visual styling. Layout, spacing, colors, responsive.
- **Pinia 2.2** — All shared state. No Vuex.
- **Vue Router 4.4** — Named routes only. Every protected route has `meta.menu_key`.
- **Lucide icons** — Only icon library. No PrimeIcons, no Heroicons.
- **`lib/api/client.ts`** — Only HTTP layer. No Axios, no raw `fetch()`.

> ⚠️ CRITICAL: PrimeVue is UNSTYLED. Never assume or generate PrimeVue default
> theme classes. All visual appearance comes from Tailwind utilities.

---

## #1 Rule — Stack Boundaries

| What | Tool |
|---|---|
| Headless complex components (DataTable, Dialog, Steps, Paginator) | PrimeVue (unstyled) |
| Primitives (Button, Input, Card, Alert, Badge, Modal) | `components/ui/` + reka-ui |
| All visual styling, layout, spacing, colors | Tailwind CSS |
| Charts | Chart.js via vue-chartjs |
| Icons | Lucide icons only |
| HTTP calls | `lib/api/client.ts` — GET/POST/blob |

Never install new UI libraries. Use what exists in `components/ui/` first.

---

## #2 Rule — Pagination ALWAYS on Top

> NEVER use DataTable's `:paginator="true"` built-in prop.
> ALWAYS use a standalone `<Paginator>` placed ABOVE the `<DataTable>`.

```vue
<!-- TOP PAGINATION — always this pattern -->
<div class="flex items-center justify-between px-4 py-2 bg-white border-x border-surface-200">
  <span class="text-sm text-surface-400">
    Showing {{ from }}–{{ to }} of <strong>{{ total }}</strong> records
  </span>
  <Paginator
    v-model:first="first"
    :rows="rows"
    :total-records="total"
    :rows-per-page-options="[10, 25, 50, 100]"
    template="RowsPerPageDropdown FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink"
    class="!p-0 !bg-transparent"
    @page="onPage"
  />
</div>
<DataTable :value="records" lazy :loading="loading" ...>
  ...
</DataTable>
```

Default rows per page: **25**. Always lazy mode — all data is server-side.

---

## #3 Rule — Table 3-Part Layout

Every list page MUST follow this structure:

```
┌─────────────────────────────────────────────┐
│ TOOLBAR: [Search] [Filter]   [Export] [Add] │  ← rounded-t, border-t, border-x
├─────────────────────────────────────────────┤
│ PAGINATION: Showing 1–25 of 342   [< 1 2 >] │  ← border-x
├─────────────────────────────────────────────┤
│ TABLE HEADERS                               │
│ row 1                                       │  ← border, rounded-b
│ row 2 ...                                   │
└─────────────────────────────────────────────┘
```

---

## #4 Rule — Date Handling

- **Display in template:** always `dmy(isoString)` from `lib/date.ts` → `DD-MM-YYYY`
- **API payload / v-model:** always ISO `YYYY-MM-DD`
- **User date input:** always `<DateField v-model="..." />` from `components/ui/DateField.vue`
- Never format dates inline — never use `new Date().toLocaleDateString()` in templates

```vue
<!-- correct -->
<span>{{ dmy(row.tanggal) }}</span>
<DateField v-model="form.tanggal" />

<!-- wrong -->
<span>{{ new Date(row.tanggal).toLocaleDateString() }}</span>
<input type="date" v-model="form.tanggal" />
```

---

## #5 Rule — Use Existing UI Components

Before building anything new, check `components/ui/` for:

| Need | Component |
|---|---|
| Any date input | `DateField.vue` |
| Long dropdown / combobox | `SearchSelect.vue` (keyboard nav + clear) |
| Pagination display | `TablePagination.vue` |
| Modal / dialog | `Modal.vue` |
| Button, Card, Input, Alert | `components/ui/` primitives |

Only create a new `components/ui/` file if nothing fits.

---

## #6 Rule — Report Pages: No Auto-Load

Report / laporan pages MUST NOT fetch data on component mount.

```vue
<!-- correct — fetch only on button click -->
<template>
  <div>
    <!-- filter form -->
    <button @click="fetchReport">Tampilkan</button>
    <!-- show empty state until fetched -->
    <EmptyState v-if="!data.length && !loading" message="Pilih filter lalu klik Tampilkan" />
    <DataTable v-else :value="data" ... />
  </div>
</template>

<script setup lang="ts">
const data = ref([])
const loading = ref(false)

async function fetchReport() {
  loading.value = true
  try {
    const res = await GET('/api/report/...')
    data.value = res.data
  } finally {
    loading.value = false
  }
}
// NO onMounted() fetch here
</script>
```

---

## #7 Rule — Menu Keys

- All menu keys live in `lib/menu/registry.ts` as `MENU_KEYS` constant
- Every protected route must have `meta.menu_key` referencing a key from registry
- Never hardcode menu key strings outside the registry file

```ts
// lib/menu/registry.ts
export const MENU_KEYS = {
  DASHBOARD: 'dashboard',
  KEUANGAN_COA: 'keuangan.coa',
  KEUANGAN_LAPORAN_KAS: 'keuangan.report.kas',
  // add new keys here
}

// router/index.ts
{ path: '/keuangan/coa', component: CoaPage, meta: { menu_key: MENU_KEYS.KEUANGAN_COA } }
```

---

## #8 Rule — API Calls

Use `lib/api/client.ts` exclusively:

```ts
import { GET, POST, blob } from '@/lib/api/client'

// fetch list
const res = await GET('/api/coa', { page: 1, limit: 25 })
// res.data → array, res.pagination → { page, limit, total, total_pages }

// mutation
const res = await POST('/api/coa', payload)

// download xlsx
const file = await blob('/api/report/kas/export.xlsx', params)
```

Handle API response shape:
```ts
// success list: { data: [], pagination: { page, limit, total, total_pages }, meta }
// success single: { data: {}, meta }
// error: { error: { code, message, details }, meta }
```

Handle these error codes in UI:
- `UNAUTHORIZED` (401) → redirect to `/login`
- `MENU_DENIED` (403) → show access denied message
- `BRANCH_DENIED` (403) → show branch restriction message
- `VALIDATION_ERROR` (422) → show field-level validation errors

---

## #9 Rule — Async Feedback

Every async operation MUST have all three states:

```ts
const loading = ref(false)

async function save() {
  loading.value = true
  try {
    await POST('/api/...', form.value)
    toast.success('Berhasil disimpan')
  } catch (e) {
    toast.error('Gagal menyimpan data')
  } finally {
    loading.value = false
  }
}
```

Never use `alert()`, `confirm()`, or `console.log` in components.

---

## #10 Rule — Role-Based UI

```ts
// stores/auth.ts exposes:
// user, roles[], menus[], branches[], active_tenant_id
const auth = useAuthStore()

// check menu access
const canViewLaporan = computed(() => auth.menus.includes(MENU_KEYS.KEUANGAN_LAPORAN_KAS))
```

```vue
<!-- v-if only — never CSS display:none -->
<Button v-if="auth.roles.includes('admin')" label="Hapus" />
<Button v-if="canViewLaporan" label="Export" />
```

---

## #11 Rule — RTL Support

```vue
<!-- pair all directional classes -->
<div class="text-left rtl:text-right ml-4 rtl:ml-0 rtl:mr-4 pl-3 rtl:pl-0 rtl:pr-3">
```

---

## #12 Rule — Layout Width: Maximize for 1080p, Mobile Friendly

**Primary target:** desktop 1920×1080 (office workstation). **Secondary target:** mobile (branch staff smartphones).

### Core Principle

Content must **fill the full width** of the working area. With a ~256px sidebar, the effective content area on 1080p is ~1660px — use it. Do not shrink pages with narrow `max-w-*` wrappers.

```vue
<!-- correct — fills the content area -->
<div class="p-4 sm:p-6 space-y-4">...</div>

<!-- wrong — unnecessarily constrains content -->
<div class="max-w-4xl mx-auto p-6">...</div>
```

Exception: dialogs and modals may use a bounded width (`max-w-xl`, `max-w-2xl`, etc.).

### Page Wrapper

Every page component should open with a full-width wrapper and responsive padding:

```vue
<template>
  <div class="p-4 sm:p-6 space-y-4">
    <!-- content here -->
  </div>
</template>
```

### Responsive Grid

Collapse to 1 column on mobile, expand on larger screens:

```vue
<!-- Dashboard summary cards / KPI widgets -->
<div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">...</div>

<!-- Two-column form layout -->
<div class="grid grid-cols-1 md:grid-cols-2 gap-4">...</div>

<!-- Filter bar (laporan) -->
<div class="flex flex-wrap gap-3 items-end">...</div>
```

### Tables — Full Width + Horizontal Scroll on Mobile

DataTable must be `w-full`. Wrap with `overflow-x-auto` so mobile users can scroll horizontally:

```vue
<div class="overflow-x-auto rounded-b border border-surface-200">
  <DataTable :value="records" class="w-full" ...>
    <Column field="..." header="..." class="min-w-[120px]" />
  </DataTable>
</div>
```

Use `min-w-[Xpx]` on columns as a floor — never fixed pixel widths that block growth.

### Sidebar Pivot Breakpoint

- **`lg:` and above** — sidebar visible, content offset right
- **Below `lg:`** — sidebar hidden, shown as drawer overlay on toggle

Use `lg:` as the single pivot between mobile and desktop layout variants.

### Breakpoint Reference (Tailwind v4)

| Prefix | Min-width | Context |
|---|---|---|
| *(none)* | 0px | Mobile base |
| `sm:` | 640px | Tablet portrait |
| `md:` | 768px | Tablet landscape |
| `lg:` | 1024px | Small desktop / laptop — sidebar pivot |
| `xl:` | 1280px | 1080p desktop — primary target |
| `2xl:` | 1536px | Wide monitor |

---

## CSS Layer Order (main.css — do not change)

```css
@layer tailwind-base, primevue, tailwind-utilities;
@import "tailwindcss/base"       layer(tailwind-base);
@import "tailwindcss/components";
@import "tailwindcss/utilities"  layer(tailwind-utilities);
```

---

## File & Naming Conventions

| Type | Pattern | Example |
|---|---|---|
| Pages | `[Feature]Page.vue` | `CoaPage.vue` |
| List pages | `[Feature]ListPage.vue` | `MuzakkiListPage.vue` |
| Laporan pages | `Laporan[Name]Page.vue` | `LaporanKasPage.vue` |
| Reusable UI | `components/ui/[Name].vue` | `SearchSelect.vue` |
| Widget (chart) | `components/widgets/[Name]Widget.vue` | `PenghimpunanWidget.vue` |
| Composables | `lib/use[Name].ts` | `useFetch.ts` |
| Stores | `stores/[feature].ts` | `stores/auth.ts` |

All files use **TypeScript** (`.ts`, `<script setup lang="ts">`).

---

## Key PrimeVue Headless Components

| Feature | PrimeVue Component |
|---|---|
| Data listing | DataTable, Column, Paginator |
| Multi-step workflow | Steps / Stepper |
| Overlays | Dialog, OverlayPanel |
| Confirmations | ConfirmDialog + useConfirm() |
| File upload | FileUpload |

All other UI (buttons, inputs, cards) → use `components/ui/` instead of PrimeVue.

---

## Brand Color Tokens

```
brand-primary:   #1B4F72  (deep navy — buttons, sidebar, headers)
brand-secondary: #1A5276  (darker navy — hover states)
brand-accent:    #1ABC9C  (teal — zakat green, success highlights)
brand-warning:   #F39C12  (amber — pending status)
brand-danger:    #E74C3C  (red — rejected, errors)
brand-surface:   #F4F6F9  (page background)
brand-muted:     #7F8C8D  (secondary text, placeholders)
```

---

## Adding a New Laporan Page (Frontend Steps Only)

1. Create `src/pages/keuangan/Laporan[Name]Page.vue`
   - Filter form at top
   - "Tampilkan" button to trigger fetch (no auto-load on mount)
   - DataTable with top Paginator
   - Export xlsx button → calls `blob('/api/report/[name]/export.xlsx', params)`
2. Add menu key to `lib/menu/registry.ts`
3. Add route to `router/index.ts` with `meta.menu_key`
4. Add sidebar entry under "Laporan" group in `AppSidebar.vue`
