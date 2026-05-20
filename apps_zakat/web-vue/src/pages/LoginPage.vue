<script setup lang="ts">
import { Eye, EyeOff, Globe, Info } from 'lucide-vue-next'
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import Input from '@/components/ui/Input.vue'
import Label from '@/components/ui/Label.vue'
import { ApiError } from '@/lib/api/client'
import { useAuthStore } from '@/stores/auth'

const username = ref('')
const password = ref('')
const showPassword = ref(false)
const errorMsg = ref<string | null>(null)
const submitting = ref(false)
const demoOpen = ref(false)

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const demoAccounts = [
  { user: 'admin', pass: 'admin123', scope: '2 perusahaan' },
  { user: 'finance.a', pass: 'finance123', scope: 'Perusahaan A saja' },
  { user: 'finance.b', pass: 'finance123', scope: 'Perusahaan B saja' },
]

const ssoErrorMessages: Record<string, string> = {
  invalid_state: 'Sesi SSO tidak valid. Silakan coba lagi.',
  verification_failed: 'Verifikasi token Google gagal.',
  email_not_allowed: 'Email Anda tidak diizinkan akses portal.',
  access_denied: 'Permintaan login Google dibatalkan.',
}
const ssoError = computed(() => {
  const code = (route.query.sso_error as string) || ''
  if (!code) return null
  return ssoErrorMessages[code] ?? `Login Google gagal: ${code}`
})

onMounted(() => {
  auth.loadProviders()
})

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

function loginWithGoogle() {
  const base = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:7000'
  const redirect = (route.query.redirect as string) ?? '/'
  window.location.assign(
    `${base}/api/auth/google/start?redirect=${encodeURIComponent(redirect)}`,
  )
}
</script>

<template>
  <div class="min-h-[80vh] grid place-items-center p-4 sm:p-6 -mt-6">
    <Card class="w-full max-w-md">
      <CardHeader>
        <CardTitle>Portal Zakat</CardTitle>
        <CardDescription>Manajemen ZIS · masuk dengan akun demo atau Google</CardDescription>
      </CardHeader>
      <CardContent>
        <Alert v-if="ssoError" variant="destructive" class="mb-4">
          {{ ssoError }}
        </Alert>

        <form class="space-y-4" @submit.prevent="submit">
          <div class="space-y-1.5">
            <Label for="username">Username</Label>
            <Input
              id="username"
              v-model="username"
              autocomplete="username"
              required
            />
          </div>

          <div class="space-y-1.5">
            <Label for="password">Password</Label>
            <div class="relative">
              <Input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                autocomplete="current-password"
                required
                class="pr-10"
              />
              <button
                type="button"
                class="absolute right-0 top-0 h-10 w-10 grid place-items-center text-muted hover:text-foreground"
                :title="showPassword ? 'Sembunyikan' : 'Tampilkan'"
                @click="showPassword = !showPassword"
              >
                <EyeOff v-if="showPassword" class="w-4 h-4" />
                <Eye v-else class="w-4 h-4" />
              </button>
            </div>
          </div>

          <Alert v-if="errorMsg" variant="destructive">
            {{ errorMsg }}
          </Alert>

          <Button type="submit" class="w-full" :disabled="submitting">
            {{ submitting ? 'Memproses…' : 'Masuk' }}
          </Button>

          <div class="relative py-2">
            <div class="absolute inset-0 flex items-center">
              <span class="w-full border-t border-border"></span>
            </div>
            <div class="relative flex justify-center text-xs">
              <span class="bg-surface px-2 text-muted uppercase tracking-wide">atau</span>
            </div>
          </div>

          <Button
            type="button"
            variant="outline"
            class="w-full"
            :disabled="!auth.providers.google"
            :title="auth.providers.google ? '' : 'Google SSO belum dikonfigurasi'"
            @click="loginWithGoogle"
          >
            <Globe class="w-4 h-4" />
            Continue with Google
          </Button>
          <p
            v-if="auth.providersLoaded && !auth.providers.google"
            class="text-xs text-muted text-center"
          >
            Google SSO belum dikonfigurasi.
          </p>

          <div class="border border-border rounded-md">
            <button
              type="button"
              class="w-full flex items-center gap-2 px-3 py-2 text-sm text-muted hover:text-foreground"
              @click="demoOpen = !demoOpen"
            >
              <Info class="w-4 h-4" />
              <span>Akun demo</span>
              <span class="ml-auto text-xs">{{ demoOpen ? '−' : '+' }}</span>
            </button>
            <ul v-if="demoOpen" class="border-t border-border divide-y divide-border">
              <li
                v-for="acc in demoAccounts"
                :key="acc.user"
                class="px-3 py-2 text-sm"
              >
                <div>
                  <code class="text-xs bg-background px-1.5 py-0.5 rounded">{{ acc.user }}</code>
                  <span class="text-muted mx-1">/</span>
                  <code class="text-xs bg-background px-1.5 py-0.5 rounded">{{ acc.pass }}</code>
                </div>
                <div class="text-xs text-muted mt-0.5">{{ acc.scope }}</div>
              </li>
            </ul>
          </div>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
