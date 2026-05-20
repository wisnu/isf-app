<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'

import { ApiError } from '@/lib/api/client'
import { useAuthStore } from '@/stores/auth'

const username = ref('')
const password = ref('')
const showPassword = ref(false)
const errorMsg = ref<string | null>(null)
const submitting = ref(false)

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const demoAccounts = [
  { user: 'admin', pass: 'admin123', scope: '2 perusahaan' },
  { user: 'finance.a', pass: 'finance123', scope: 'Perusahaan A saja' },
  { user: 'finance.b', pass: 'finance123', scope: 'Perusahaan B saja' },
]

async function submit() {
  errorMsg.value = null
  submitting.value = true
  try {
    await auth.login(username.value, password.value)
    const target = (route.query.redirect as string) ?? '/'
    router.replace(target)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Login gagal'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <q-page class="flex flex-center login-page">
    <q-card flat bordered class="login-card">
      <q-card-section>
        <div class="text-h6">Portal ZISWAF</div>
        <div class="text-caption text-grey">Masuk dengan akun demo</div>
      </q-card-section>

      <q-form class="q-gutter-md q-px-md q-pb-md" @submit.prevent="submit">
        <q-input
          v-model="username"
          outlined
          dense
          label="Username"
          autocomplete="username"
          :rules="[(v) => !!v || 'Wajib diisi']"
        />

        <q-input
          v-model="password"
          outlined
          dense
          label="Password"
          :type="showPassword ? 'text' : 'password'"
          autocomplete="current-password"
          :rules="[(v) => !!v || 'Wajib diisi']"
        >
          <template #append>
            <q-icon
              :name="showPassword ? 'visibility_off' : 'visibility'"
              class="cursor-pointer"
              @click="showPassword = !showPassword"
            />
          </template>
        </q-input>

        <q-banner v-if="errorMsg" class="bg-negative text-white" dense rounded>
          {{ errorMsg }}
        </q-banner>

        <q-btn
          type="submit"
          color="primary"
          class="full-width"
          :label="submitting ? 'Memproses…' : 'Masuk'"
          :loading="submitting"
          unelevated
        />

        <q-expansion-item icon="info" label="Akun demo" dense-toggle>
          <q-list dense>
            <q-item v-for="acc in demoAccounts" :key="acc.user">
              <q-item-section>
                <q-item-label>
                  <code>{{ acc.user }}</code> / <code>{{ acc.pass }}</code>
                </q-item-label>
                <q-item-label caption>{{ acc.scope }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-expansion-item>
      </q-form>
    </q-card>
  </q-page>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  padding: 1.5rem;
}
.login-card {
  width: 100%;
  max-width: 420px;
}
</style>
