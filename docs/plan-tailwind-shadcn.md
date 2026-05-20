# Refactor UI: Quasar → Tailwind v4 + shadcn-vue (reka-ui)

## Context

Setelah integrasi Quasar di iterasi sebelumnya, user mengejar **footprint ringan secara menyeluruh** — bundle browser yang dimuat user, container dev di laptop, dan nantinya backend image. Plan ini fokus ke **swap UI di `apps/web-vue/`**; optimasi backend (`api-python` + `bff-api`) jadi follow-up plan terpisah.

Quasar terlalu berat untuk kebutuhan MVP yang sederhana (login + dashboard 2 widget). Bundle produksi diperkirakan turun **3–10×** setelah swap, build time **50–70% lebih cepat**, dev cold start setengah lebih cepat. Komponen yang lebih advance (DataTable, Dialog, Stepper) bisa diadopsi per-komponen dari shadcn-vue saat dibutuhkan di Fase 2+, tanpa biaya keep-Quasar di MVP.

Keputusan terkunci:
- **Bahasa styling**: Tailwind CSS v4 (CSS-first config, plugin `@tailwindcss/vite`).
- **Komponen**: shadcn-vue style — copy-paste SFC ke `src/components/ui/` yang wrap **reka-ui** primitives.
- **Icons**: `lucide-vue-next` (tree-shake per icon, idiomatic shadcn).
- **Dark mode**: class `.dark` di `<html>`, Tailwind `dark:` variant; Pinia `theme` store toggle DOM class + persist `localStorage`.
- **Hapus**: quasar, @quasar/extras, @quasar/vite-plugin, sass-embedded.
- **No backend changes.**

## Arsitektur

- `apps/web-vue/src/styles.css` jadi single CSS entry: `@import "tailwindcss"` + `@theme { ... }` blok untuk tokens (primary, positive, warning, accent, dll) + sedikit base resets.
- `tailwind.config.ts` **tidak dibuat** — Tailwind v4 pakai CSS-first config. Hanya `vite.config.ts` yang ditambah plugin.
- `src/components/ui/` jadi rumah komponen primitif: `Button.vue`, `Input.vue`, `Label.vue`, `Card.vue`, `CardHeader.vue`, `CardContent.vue`, `Alert.vue`, plus DropdownMenu yang ditulis pakai `reka-ui` `<DropdownMenuRoot/>` family.
- `src/lib/utils.ts` punya helper `cn(...inputs)` (clsx + tailwind-merge) — pattern shadcn standar.
- `src/App.vue` jadi plain `<div class="min-h-screen flex flex-col">` — tidak butuh layout primitive lagi.
- `src/components/AppHeader.vue` jadi `<header class="border-b ...">` dengan Tailwind utility.
- Halaman (`LoginPage`, `DashboardPage`) refactor pakai komponen `ui/*` + Tailwind.

## Responsive: Desktop-first, mobile friendly

Portal ini diprimer untuk **desktop** (target utama internal staff: 1280×800+) dan **degrade dengan rapi** ke tablet/mobile (tidak rusak, masih usable, walau bukan target utama).

**Breakpoint target** (mengacu default Tailwind):

| Tier | Lebar | Status |
| --- | --- | --- |
| Mobile | < 640px (Tailwind `< sm`) | usable, layout stack vertikal |
| Tablet | 640–1023px (`sm`–`md`) | usable, layout adaptasi |
| Desktop | ≥ 1024px (`lg`+) | **target utama**, layout penuh |
| Wide | ≥ 1280px (`xl`+) | aman, tidak terlalu lebar |

**Prinsip implementasi:**

1. **Tulis style dasar untuk desktop**, lalu pakai variant `max-md:` / `max-sm:` untuk adjust ke layar kecil. Ini membalik default Tailwind (mobile-first), tapi cocok dengan filosofi desktop-first kita. Boleh juga pakai `sm:` / `lg:` saat lebih natural (mis. grid yang grow dari 1 → 2 kolom).
2. **Container utama** punya `max-w-screen-xl mx-auto` agar di layar lebar tidak terlalu lebar; padding responsive (`px-4 sm:px-6 lg:px-8`).
3. **Header**:
   - Brand kiri, kontrol kanan, horizontal di desktop.
   - Di mobile (<640px): hide nama user (`max-sm:hidden`), hide label tombol logout (cuma icon), dropdown tenant tetap visible (kunci fungsi multi-tenant).
   - Tinggi header tetap, tidak collapse ke hamburger di MVP (komponennya cuma 4: brand, tenant, dark, logout — masih muat).
4. **Login page**: card center dengan `w-full max-w-md` — sudah responsif by design.
5. **Dashboard widgets**: `grid grid-cols-1 sm:grid-cols-2` — stack di mobile, side-by-side mulai `sm` (≥640px). Cukup karena cuma 2 widget MVP; saat widget bertambah di Fase 2+, tambah breakpoint (`lg:grid-cols-3` dst).
6. **Touch target**: tombol minimum 40px tinggi (default `h-10`) supaya nyaman di mobile.
7. **Tabel & data dense (Fase 2+)** akan butuh horizontal scroll wrapper (`overflow-x-auto`) di mobile — di luar scope MVP.
8. **Tidak ada media query manual di CSS** — semua via Tailwind variants supaya konsisten dengan token & purge.

Catatan: tidak ada plan untuk PWA / install prompt / offline mode di Fase 1.

## File yang berubah

### Hapus

```
apps/web-vue/src/quasar-variables.sass
```

### Modify

| File | Perubahan |
| --- | --- |
| `apps/web-vue/package.json` | Hapus quasar/@quasar/extras/@quasar/vite-plugin/sass-embedded. Tambah tailwindcss, @tailwindcss/vite, reka-ui, class-variance-authority, clsx, tailwind-merge, lucide-vue-next |
| `apps/web-vue/vite.config.ts` | Hapus `quasar()` plugin, hapus `transformAssetUrls`. Tambah `import tailwindcss from '@tailwindcss/vite'` + `tailwindcss()` di plugins array |
| `apps/web-vue/src/main.ts` | Hapus `Quasar`, `Dark` import; hapus `Quasar/extras icons` & `quasar/src/css/index.sass` imports; hapus `app.use(Quasar, ...)` |
| `apps/web-vue/src/styles.css` | Ganti seluruh isi: `@import "tailwindcss"` + `@theme` block tokens + dark variant + base resets |
| `apps/web-vue/src/stores/theme.ts` | `Dark.set(v)` → `document.documentElement.classList.toggle('dark', v)`. Hapus `import { Dark } from 'quasar'` |
| `apps/web-vue/src/App.vue` | `<q-layout>...<q-page-container>` → plain `<div class="min-h-screen flex flex-col">` + `<router-view/>` di `<main>` |
| `apps/web-vue/src/components/AppHeader.vue` | `<q-header>`/`<q-toolbar>` → `<header>` + Tailwind. Tenant dropdown pakai `<DropdownMenu>` (reka-ui via `ui/`), dark toggle & logout pakai `<Button>` + lucide icons |
| `apps/web-vue/src/components/SummaryWidget.vue` | `<q-card>` → `<Card>` (ui/) + Tailwind warna (`text-emerald-600` / `text-amber-600`) |
| `apps/web-vue/src/pages/LoginPage.vue` | `<q-form>`/`<q-input>`/`<q-btn>` → `<form>` + `<Input>` + `<Button>` + `<Alert>` (semua dari `ui/`) |
| `apps/web-vue/src/pages/DashboardPage.vue` | `<q-page>`/`<q-spinner>`/`<q-banner>` → `<div>` + Tailwind grid + `<Loader2>` lucide icon + `<Alert>` |

### Add

```
apps/web-vue/src/lib/utils.ts                  — cn() helper
apps/web-vue/src/components/ui/Button.vue      — CVA variants (default/secondary/ghost/destructive)
apps/web-vue/src/components/ui/Input.vue       — outlined input
apps/web-vue/src/components/ui/Label.vue
apps/web-vue/src/components/ui/Card.vue        — wrapper + CardHeader.vue + CardContent.vue + CardTitle.vue + CardDescription.vue
apps/web-vue/src/components/ui/Alert.vue       — variants default/destructive
apps/web-vue/src/components/ui/DropdownMenu.vue — wrap reka-ui DropdownMenu* with styled trigger + content
```

## Kunci implementasi

### `vite.config.ts`

```ts
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  resolve: { alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) } },
  server: { host: true, port: 5173 },
})
```

### `src/styles.css` (Tailwind v4 CSS-first)

```css
@import "tailwindcss";

@variant dark (&:where(.dark, .dark *));

@theme {
  --color-background: #f7f7f8;
  --color-foreground: #1a1a1c;
  --color-muted: #6b6b70;
  --color-border: #e3e3e6;
  --color-surface: #ffffff;

  --color-primary: #1976d2;
  --color-primary-foreground: #ffffff;
  --color-accent: #0f766e;

  --color-positive: #16a34a;     /* hijau penerimaan */
  --color-warning: #d97706;      /* kuning penyaluran */
  --color-destructive: #b91c1c;
  --color-destructive-foreground: #ffffff;

  --radius: 0.5rem;
}

.dark {
  --color-background: #0a0a0b;
  --color-foreground: #f5f5f5;
  --color-muted: #9b9ba0;
  --color-border: #27272a;
  --color-surface: #18181b;
}

html, body, #app { margin: 0; height: 100%; }
body {
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  background: var(--color-background);
  color: var(--color-foreground);
}
```

### `src/lib/utils.ts`

```ts
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs))
}
```

### `src/stores/theme.ts`

```ts
import { defineStore } from 'pinia'

const STORAGE_KEY = 'isf-theme'
type Mode = 'light' | 'dark'

function readStored(): Mode {
  return localStorage.getItem(STORAGE_KEY) === 'dark' ? 'dark' : 'light'
}
function applyDom(mode: Mode) {
  document.documentElement.classList.toggle('dark', mode === 'dark')
}

export const useThemeStore = defineStore('theme', {
  state: () => ({ mode: 'light' as Mode }),
  getters: { isDark: (s) => s.mode === 'dark' },
  actions: {
    init() { this.mode = readStored(); applyDom(this.mode) },
    setMode(m: Mode) { this.mode = m; applyDom(m); localStorage.setItem(STORAGE_KEY, m) },
    toggle() { this.setMode(this.mode === 'dark' ? 'light' : 'dark') },
  },
})
```

### `src/components/ui/Button.vue` (CVA pattern)

```vue
<script setup lang="ts">
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center gap-2 rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-border bg-surface hover:bg-background',
        ghost: 'hover:bg-background',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 px-3',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: { variant: 'default', size: 'default' },
  },
)

type Props = VariantProps<typeof buttonVariants> & { class?: string }
const props = defineProps<Props>()
</script>

<template>
  <button :class="cn(buttonVariants({ variant: props.variant, size: props.size }), props.class)">
    <slot />
  </button>
</template>
```

### `src/components/ui/Card.vue`

```vue
<script setup lang="ts">
import { cn } from '@/lib/utils'
const props = defineProps<{ class?: string }>()
</script>

<template>
  <div :class="cn('rounded-lg border border-border bg-surface text-foreground shadow-sm', props.class)">
    <slot />
  </div>
</template>
```

Plus `CardHeader.vue` (`p-6 flex flex-col gap-1.5`), `CardContent.vue` (`p-6 pt-0`), `CardTitle.vue` (`text-lg font-semibold`), `CardDescription.vue` (`text-sm text-muted`).

### `src/components/ui/Input.vue`

```vue
<script setup lang="ts">
import { cn } from '@/lib/utils'
const props = defineProps<{ class?: string; modelValue?: string | number }>()
const emit = defineEmits<{ 'update:modelValue': [string | number] }>()
</script>

<template>
  <input
    :class="cn('flex h-10 w-full rounded-md border border-border bg-surface px-3 py-2 text-sm placeholder:text-muted focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary disabled:opacity-50', props.class)"
    :value="modelValue"
    @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
  />
</template>
```

### `src/components/ui/Alert.vue`

```vue
<script setup lang="ts">
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const variants = cva('relative w-full rounded-md border p-3 text-sm', {
  variants: {
    variant: {
      default: 'bg-surface text-foreground border-border',
      destructive: 'bg-destructive/10 text-destructive border-destructive/30',
    },
  },
  defaultVariants: { variant: 'default' },
})
type Props = VariantProps<typeof variants> & { class?: string }
const props = defineProps<Props>()
</script>

<template>
  <div role="alert" :class="cn(variants({ variant: props.variant }), props.class)">
    <slot />
  </div>
</template>
```

### `src/components/ui/DropdownMenu.vue` (wrap reka-ui)

```vue
<script setup lang="ts">
import { DropdownMenuRoot, DropdownMenuTrigger, DropdownMenuPortal, DropdownMenuContent, DropdownMenuItem } from 'reka-ui'
import { cn } from '@/lib/utils'

const props = defineProps<{ contentClass?: string }>()
defineSlots<{ trigger(): unknown; default(): unknown }>()
</script>

<template>
  <DropdownMenuRoot>
    <DropdownMenuTrigger as-child><slot name="trigger" /></DropdownMenuTrigger>
    <DropdownMenuPortal>
      <DropdownMenuContent
        :class="cn('min-w-[220px] rounded-md border border-border bg-surface p-1 shadow-md', props.contentClass)"
        :side-offset="6"
      >
        <slot />
      </DropdownMenuContent>
    </DropdownMenuPortal>
  </DropdownMenuRoot>
</template>
```

Plus tipis `DropdownMenuItem.vue` yang wrap reka-ui `DropdownMenuItem` dengan Tailwind class hover/focus.

### Komponen aplikasi (sketch refactor, desktop-first responsive)

- **`App.vue`** — `<div class="min-h-screen flex flex-col"><AppHeader v-if="showHeader" /><main class="flex-1 w-full max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8 py-6"><router-view/></main></div>`. `max-w-screen-xl` membatasi lebar konten di monitor besar; padding adaptif.
- **`AppHeader.vue`** — `<header class="border-b border-border bg-primary text-primary-foreground px-4 sm:px-6 py-3 flex items-center justify-between gap-3 sm:gap-4">`. Brand kiri (`<span class="font-bold">isf-app</span><span class="text-xs max-sm:hidden">· Portal ZISWAF</span>`). Kanan: `<DropdownMenu>` tenant (selalu tampil), `<span class="text-xs max-sm:hidden">{{ user.name }}</span>`, `<Button variant="ghost" size="icon">` dark toggle, `<Button variant="ghost">` logout dengan label `max-sm:sr-only` (icon `LogOut` tetap terlihat). Icons lucide: `Building2`, `Check`, `Sun`, `Moon`, `LogOut`.
- **`SummaryWidget.vue`** — `<Card><CardHeader class="pb-2"><CardDescription>{{ label }}</CardDescription><CardTitle class="text-xs font-normal text-muted">{{ period }}</CardTitle></CardHeader><CardContent><div :class="['text-2xl sm:text-3xl font-bold tabular-nums', accent==='in' ? 'text-positive' : 'text-warning']">{{ formatIdr(amount) }}</div></CardContent></Card>`. `tabular-nums` agar angka rapi sejajar.
- **`LoginPage.vue`** — `<div class="min-h-screen grid place-items-center p-4 sm:p-6"><Card class="w-full max-w-md">…<form class="space-y-4">…<Input>…<Button class="w-full">`. Dengan Eye/EyeOff lucide untuk visibility toggle, `<Alert variant="destructive">` untuk error. Card cukup responsif: full-width di mobile, max 28rem di desktop.
- **`DashboardPage.vue`** — `<div class="space-y-6">` + heading (`<h1 class="text-2xl font-bold">Dashboard</h1>` + tenant name `text-sm text-muted`) + grid `<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">` untuk 2 widget. Loading: `<div class="flex justify-center p-8"><Loader2 class="w-8 h-8 animate-spin text-primary" /></div>`. Error: `<Alert variant="destructive">{{ errorMsg }}</Alert>`.

## Dependencies (final)

`package.json` setelah refactor:

```json
{
  "dependencies": {
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "lucide-vue-next": "^0.460.0",
    "pinia": "^2.2.0",
    "reka-ui": "^1.0.0-alpha",
    "tailwind-merge": "^2.5.0",
    "vue": "^3.5.0",
    "vue-router": "^4.4.0"
  },
  "devDependencies": {
    "@tailwindcss/vite": "^4.0.0",
    "@vitejs/plugin-vue": "^5.1.0",
    "tailwindcss": "^4.0.0",
    "typescript": "~5.6.0",
    "vite": "^5.4.0",
    "vue-tsc": "^2.1.0"
  }
}
```

## Eksekusi (urutan langkah)

1. **Cleanup file lama** — hapus `quasar-variables.sass`; hapus file yang akan ditulis ulang (package.json, vite.config.ts, main.ts, styles.css, theme.ts, App.vue, AppHeader.vue, SummaryWidget.vue, LoginPage.vue, DashboardPage.vue).
2. **Tulis `package.json` baru** (deps di atas).
3. **Tulis `vite.config.ts`** (Tailwind plugin, hapus Quasar).
4. **Tulis `src/styles.css`** (Tailwind import + @theme tokens + dark variant + base).
5. **Tulis `src/lib/utils.ts`** dengan `cn()`.
6. **Tulis `src/main.ts`** — tanpa Quasar; tetap init theme store sebelum mount.
7. **Tulis `src/stores/theme.ts`** — class toggle, no Quasar import.
8. **Tulis `src/components/ui/*.vue`** (Button, Input, Label, Card+sub, Alert, DropdownMenu, DropdownMenuItem).
9. **Tulis `src/App.vue`** baru (no QLayout).
10. **Tulis `src/components/AppHeader.vue`** baru — DropdownMenu untuk tenant, lucide icons, dark toggle button.
11. **Tulis `src/components/SummaryWidget.vue`** baru — Card-based.
12. **Tulis `src/pages/LoginPage.vue`** baru — Card + Input + Button + Alert; visibility toggle dengan Eye/EyeOff.
13. **Tulis `src/pages/DashboardPage.vue`** baru — grid + Loader2 spinner + Alert.
14. **Rebuild container web-vue**:
    ```bash
    cd infra
    podman-compose down -v
    podman-compose up -d --build web-vue
    ```
    (api-python + bff-api di-recreate juga, tapi reuse image — cepat. node_modules anonymous volume harus dibuang biar npm install pakai package.json baru.)

## Verifikasi

1. `podman ps --filter name=isf-` — tiga container running.
2. `curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:5173/` → 200.
3. `curl -s http://localhost:5173/src/main.ts | head -20` → tidak ada `quasar` import; ada `vue` & `pinia`.
4. `curl -s http://localhost:5173/src/styles.css | head -5` → `@import "tailwindcss"` (atau transformed equivalent).
5. Backend tetap jalan: `curl -s http://localhost:7000/health` → ok.
6. End-to-end auth flow tetap lulus (sama dengan tes setelah swap Quasar — login admin, tenant list, switch, dashboard).
7. **Browser desktop** (≥ 1280px, target utama) di `http://localhost:5173` — verifikasi visual:
   - Login page bersih, Card center, Input outlined, Button primary biru.
   - Setelah login: header dengan dropdown tenant (lucide Building2 + Check di tenant aktif), nama user, Sun/Moon toggle, logout dengan icon.
   - Dashboard 2 widget Card side-by-side; Penerimaan hijau (`text-positive`), Penyaluran kuning oranye (`text-warning`); angka pakai `tabular-nums`.
   - Toggle dark → seluruh UI flip; refresh → tetap dark (localStorage).
   - Switch tenant → dashboard data berubah, tetap di halaman yang sama.
8. **Browser mobile** (DevTools responsive mode, mis. iPhone SE 375×667) — verifikasi tidak rusak:
   - Login card full-width dengan padding 16px; tetap usable.
   - Header tetap satu baris; nama user & label "Logout" tersembunyi (cuma icon); dropdown tenant tetap accessible & jelas.
   - Dashboard 2 widget stack vertikal.
   - Toggle dark + switch tenant tetap jalan.
9. **Bundle size sanity check (opsional)** — di dalam container: `npm run build`, lalu `du -sh dist/assets/*.js dist/assets/*.css` — JS hopefully < 100KB total, CSS < 20KB.

## Risiko & mitigasi

- **reka-ui versi alpha** — masih ~1.0-alpha. Aksesibilitas & API kemungkinan stabil tapi version-pin disarankan. Mitigasi: pin major version di `package.json`, ikuti changelog.
- **Tailwind v4** — relatif baru (rilis 2025). Beberapa plugin v3 belum kompatibel. Untuk kebutuhan kita (utility + custom theme tokens), v4 cukup. Mitigasi: kalau ada issue, fallback ke v3 setup dengan `postcss + autoprefixer` (sedikit lebih ribet config).
- **Anonymous volume gotcha kambuh** — selalu `down -v` saat ubah `package.json`. Sudah didokumentasikan di `docs/runbook-local.md`.

## Follow-up (di luar plan ini)

- **Backend slim plan terpisah** — multi-stage Dockerfile untuk `api-python` & `bff-api` dengan `python:3.12-alpine` base + builder/runtime stage split. Hemat ~100MB image. Akan saya buat plan terpisah saat user OK lanjut ke sana.
