<script setup lang="ts">
// PLACEHOLDER pasca-recovery (2026-05-27 NTFS corruption).
// Form ubah-password + endpoint backend (set_password ke isf_auth.user_credentials)
// belum direkonstruksi. Lihat docs/recovery/README.md §"Still TODO".
import { Construction } from 'lucide-vue-next'

import Alert from '@/components/ui/Alert.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
</script>

<template>
  <div class="space-y-4">
    <PageHeader
      title="Ubah Password"
      subtitle="Ganti kata sandi akun Anda"
    />
    <Card class="max-w-2xl">
      <CardHeader>
        <CardTitle class="flex items-center gap-2">
          <Construction class="w-4 h-4 text-muted shrink-0" />
          Dalam rekonstruksi
        </CardTitle>
      </CardHeader>
      <CardContent class="space-y-3">
        <Alert class="items-start">
          <p class="text-sm">
            Fitur ubah password belum tersedia. Form ini beserta endpoint
            backend-nya termasuk yang belum dipulihkan setelah pemulihan repo
            <span class="font-mono text-xs">2026-05-27</span>.
          </p>
        </Alert>
      </CardContent>
    </Card>
  </div>
</template>
