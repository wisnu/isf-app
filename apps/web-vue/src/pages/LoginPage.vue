<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

import { ApiError } from '@/lib/api/client'
import { useAuthStore } from '@/stores/auth'

const username = ref('')
const password = ref('')
const error = ref<string | null>(null)
const submitting = ref(false)
const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

async function submit() {
  error.value = null
  submitting.value = true
  try {
    await auth.login(username.value, password.value)
    const target = (route.query.redirect as string) ?? '/'
    router.replace(target)
  } catch (e) {
    error.value = e instanceof ApiError ? e.message : 'Login gagal'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="login-shell">
    <form class="card login-card" @submit.prevent="submit">
      <h1>Portal ZISWAF</h1>
      <p class="muted">Masuk dengan akun demo</p>
      <label>
        <span>Username</span>
        <input v-model="username" autocomplete="username" required />
      </label>
      <label>
        <span>Password</span>
        <input v-model="password" type="password" autocomplete="current-password" required />
      </label>
      <p v-if="error" class="error">{{ error }}</p>
      <button class="primary" type="submit" :disabled="submitting">
        {{ submitting ? 'Memproses…' : 'Masuk' }}
      </button>
      <details class="hint">
        <summary>Akun demo</summary>
        <ul>
          <li><code>admin</code> / <code>admin123</code> — 2 perusahaan</li>
          <li><code>finance.a</code> / <code>finance123</code> — Perusahaan A</li>
          <li><code>finance.b</code> / <code>finance123</code> — Perusahaan B</li>
        </ul>
      </details>
    </form>
  </div>
</template>

<style scoped>
.login-shell {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 1.5rem;
}
.login-card {
  width: 100%;
  max-width: 380px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.login-card h1 { margin: 0; font-size: 1.4rem; }
.muted { color: var(--color-text-muted); margin: -0.5rem 0 0; font-size: 0.9rem; }
label { display: flex; flex-direction: column; gap: 0.35rem; font-size: 0.85rem; color: var(--color-text-muted); }
.error { color: var(--color-danger); margin: 0; font-size: 0.9rem; }
.hint { font-size: 0.8rem; color: var(--color-text-muted); }
.hint ul { margin: 0.5rem 0 0 1rem; padding: 0; }
.hint code { background: var(--color-bg); padding: 0.05rem 0.3rem; border-radius: 4px; }
</style>
