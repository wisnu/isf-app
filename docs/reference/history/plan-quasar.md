# Quasar Theme Integration — `web-vue`

> **For agentic workers:** Combined spec + plan. Single subsystem (`apps/web-vue`); backend tidak disentuh.

**Goal:** Adopt Quasar UI library di `web-vue` — refactor login, dashboard, dan header pakai komponen Quasar; tambah dark mode toggle yang persist ke `localStorage`; brand color = Quasar default biru.

**Architecture:** Quasar di-register via official Vite plugin. Sass variables file mengontrol theme tokens. App shell di-wrap `<q-layout>` + `<q-page-container>`. Dark mode dikelola Pinia store yang drive Quasar `Dark` plugin. **No backend changes.**

**Tech Stack:** Quasar ^2.16, `@quasar/vite-plugin` ^1.7, `@quasar/extras` (Material Icons), `sass-embedded`, Pinia.

---

## Locked decisions

- **Scope:** Full refactor pakai komponen Quasar untuk login, dashboard, header. Widget tetap pakai `<q-card>` dengan slot custom.
- **Dark mode:** Light + dark, toggle icon di header. Persist `localStorage['isf-theme']` (`'light' | 'dark'`). Default `'light'`.
- **Brand color:** `$primary: #1976d2` (Quasar default biru). Teal lama (`#0f766e`) dipindah jadi `$accent`.
- **Accents:** Widget Penerimaan pakai `text-positive` (hijau), Penyaluran pakai `text-warning` (kuning oranye) — sesuai semantik Quasar.
- **Icons:** Material Icons via `@quasar/extras`.
- **Sass syntax:** indented (`.sass`).
- **Lang:** default English Quasar (kontent tetap Indonesia via template string kita).

---

## File inventory

| File | Status | Tujuan |
| --- | --- | --- |
| `apps/web-vue/package.json` | modify | + quasar, @quasar/extras, @quasar/vite-plugin, sass-embedded |
| `apps/web-vue/vite.config.ts` | modify | Register `quasar({ sassVariables })` |
| `apps/web-vue/src/quasar-variables.sass` | **new** | Theme tokens |
| `apps/web-vue/src/main.ts` | modify | Register Quasar + Dark plugin, import icon CSS, init theme store |
| `apps/web-vue/src/styles.css` | modify | Slim down — Quasar handles resets & typography |
| `apps/web-vue/src/App.vue` | modify | `<q-layout view="hHh lpr fFf">` + `<q-page-container>` |
| `apps/web-vue/src/components/AppHeader.vue` | modify | `<q-header><q-toolbar>` + q-btn-dropdown tenant + dark toggle + logout |
| `apps/web-vue/src/components/SummaryWidget.vue` | modify | `<q-card flat bordered>` |
| `apps/web-vue/src/pages/LoginPage.vue` | modify | `<q-page>` + `<q-card>` + `<q-form>` + `<q-input>` + `<q-btn>` + q-expansion-item akun demo |
| `apps/web-vue/src/pages/DashboardPage.vue` | modify | `<q-page>`, loading→`<q-spinner>`, error→`<q-banner type=negative>` |
| `apps/web-vue/src/stores/theme.ts` | **new** | Pinia store: `mode`, `setMode`, `toggle`, `init` |

---

## Tasks (eksekusi linear)

### Task 1 — Dependencies

Edit `apps/web-vue/package.json`. Tambahan: `quasar`, `@quasar/extras` di deps; `@quasar/vite-plugin`, `sass-embedded` di devDeps.

### Task 2 — Vite plugin config

Edit `apps/web-vue/vite.config.ts`. Tambah import `quasar, transformAssetUrls` dari `@quasar/vite-plugin`. Pass `transformAssetUrls` ke vue plugin; tambah `quasar({ sassVariables: fileURLToPath(new URL('./src/quasar-variables.sass', import.meta.url)) })`.

> **Catatan:** path sass variables **harus absolut** (pakai `fileURLToPath`). String relatif `'src/quasar-variables.sass'` di-inline mentah ke `@import` di dalam `quasar/src/css/index.sass` dan gagal di-resolve oleh sass-embedded.

### Task 3 — Theme tokens

Create `apps/web-vue/src/quasar-variables.sass`:
```sass
$primary:   #1976d2
$secondary: #26a69a
$accent:    #0f766e

$dark:      #1d1d1d
$dark-page: #121212

$positive:  #21ba45
$negative:  #c10015
$info:      #31ccec
$warning:   #f2c037
```

### Task 4 — Theme store

Create `apps/web-vue/src/stores/theme.ts` — Pinia store dengan `mode: 'light' | 'dark'`, action `setMode`, `toggle`, `init`. Saat `setMode` dipanggil, call `Dark.set(...)` dari `quasar` dan tulis `localStorage['isf-theme']`. `init()` baca localStorage saat boot.

### Task 5 — Bootstrap Quasar

Edit `apps/web-vue/src/main.ts`. Import `Quasar, Dark` dari `quasar`, import `@quasar/extras/material-icons/material-icons.css`, import `quasar/src/css/index.sass`. Daftar `app.use(Quasar, { plugins: { Dark } })`. Panggil `useThemeStore().init()` sebelum `app.mount('#app')`.

### Task 6 — Slim global CSS

Edit `apps/web-vue/src/styles.css`. Pertahankan hanya font-family dan reset minimal. Hapus styling button/input/card/utility custom (Quasar mengelola).

### Task 7 — App.vue → QLayout

Edit `apps/web-vue/src/App.vue`. Replace template:
```vue
<template>
  <q-layout view="hHh lpr fFf">
    <AppHeader v-if="showHeader" />
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>
```
Hapus `<style scoped>` (q-page-container handle padding).

### Task 8 — AppHeader → QHeader

Refactor `apps/web-vue/src/components/AppHeader.vue` jadi q-header + q-toolbar. Tenant switcher pakai `<q-btn-dropdown>` + `<q-list>` dengan checkmark di tenant aktif. Tambah dark toggle `<q-btn flat round :icon="theme.isDark ? 'light_mode' : 'dark_mode'" @click="theme.toggle" />`. Logout pakai `<q-btn flat icon-right="logout">`.

### Task 9 — SummaryWidget → q-card

Refactor jadi `<q-card flat bordered>` dengan `<q-card-section>`. Label pakai `text-overline text-grey`, amount pakai `text-h5`, accent in/out pakai class `text-positive` / `text-warning`.

### Task 10 — LoginPage → q-form

Refactor `apps/web-vue/src/pages/LoginPage.vue`:
- `<q-page class="flex flex-center">`
- `<q-card flat bordered>` width 420px
- `<q-form @submit.prevent="submit">` dengan `<q-input outlined dense>` × 2, password punya append icon visibility toggle.
- Error pakai `<q-banner class="bg-negative text-white" dense>`
- Submit pakai `<q-btn type="submit" color="primary" :loading="submitting">`
- Akun demo pakai `<q-expansion-item icon="info" label="Akun demo">` dengan `<q-list dense>`

### Task 11 — DashboardPage → q-page

Refactor:
- `<q-page padding>`
- Header dashboard pakai `text-h5` + `text-subtitle2 text-grey` (tenant name)
- Loading: `<q-spinner color="primary" size="32px" />` di tengah
- Error: `<q-banner class="bg-negative text-white" dense>`
- Widgets grid: `<div class="row q-col-gutter-md">` + `<div class="col-12 col-sm-6">` × 2

### Task 12 — Rebuild container

`web-vue` image perlu rebuild karena `package.json` berubah:
```bash
cd infra
podman-compose stop web-vue && podman-compose rm -f web-vue && podman-compose up -d --build web-vue
# atau (docker): docker compose up -d --build web-vue
```

### Task 13 — Verify

- `curl -s http://localhost:5173 | head -c 200` — HTML keluar
- Browser di `http://localhost:5173`:
  1. Login form tampil dengan styling Quasar (q-card, q-input outlined, q-btn biru).
  2. Login `admin / admin123` → header biru muncul dengan tenant dropdown.
  3. Toggle icon kanan (sun/moon) — UI flip light↔dark.
  4. Refresh — mode tersimpan.
  5. Switch tenant via dropdown — dashboard reload.
  6. Logout.

---

## Out of scope

- Sidebar drawer / `<q-drawer>` (dashboard masih 1 halaman).
- Quasar Notify / Dialog plugins.
- Quasar i18n (lang pack).
- Komponen lain di scaffolded `apps/web-vue/src/pages/DonorDetailPage.vue` (tetap empty stub Fase berikut).
