<script setup lang="ts">
import { Mail } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

import Alert from '@/shared/components/Alert.vue'
import Button from '@/shared/components/Button.vue'
import Card from '@/shared/components/Card.vue'
import CardContent from '@/shared/components/CardContent.vue'
import CardDescription from '@/shared/components/CardDescription.vue'
import CardHeader from '@/shared/components/CardHeader.vue'
import CardTitle from '@/shared/components/CardTitle.vue'
import { useAuthStore } from '@/app/stores/auth.store'

const auth = useAuthStore()
const router = useRouter()

async function logout() {
  await auth.logout()
  router.replace({ name: 'login' })
}
</script>

<template>
  <div class="min-h-[80vh] grid place-items-center p-4 sm:p-6 -mt-6">
    <Card class="w-full max-w-md">
      <CardHeader>
        <CardTitle>Akun belum punya akses</CardTitle>
        <CardDescription>
          Login Anda terverifikasi, tetapi belum di-assign ke perusahaan mana pun.
        </CardDescription>
      </CardHeader>
      <CardContent class="space-y-4">
        <Alert class="items-start">
          <Mail class="w-4 h-4 mt-0.5 text-muted shrink-0" />
          <div>
            <p class="text-sm">
              Akun <strong class="text-foreground">{{ auth.user?.name }}</strong>
              ({{ auth.user?.username }}) sudah terdaftar di portal,
              namun belum punya hak akses ke perusahaan ZISWAF mana pun.
            </p>
            <p class="text-sm mt-2 text-muted">
              Silakan hubungi administrator portal untuk meminta akses.
            </p>
          </div>
        </Alert>
        <Button variant="outline" class="w-full" @click="logout">Logout</Button>
      </CardContent>
    </Card>
  </div>
</template>
