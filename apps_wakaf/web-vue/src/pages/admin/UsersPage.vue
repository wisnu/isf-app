<script setup lang="ts">
// PLACEHOLDER pasca-recovery (2026-05-27 NTFS corruption).
// Halaman + endpoint backend (users CRUD ke isf_auth.users / enterprise.userapp)
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
      title="Manajemen User"
      subtitle="Kelola akun pengguna, role, dan akses cabang"
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
          <div class="space-y-1">
            <p class="text-sm">
              Halaman ini belum tersedia. Modul manajemen user (beserta endpoint
              backend-nya) termasuk yang belum dipulihkan setelah pemulihan repo
              <span class="font-mono text-xs">2026-05-27</span>.
            </p>
            <p class="text-xs text-muted">
              Mapping role &rarr; menu sudah bisa dikelola di
              <RouterLink to="/admin/role-menu" class="underline">Mapping Role-Menu</RouterLink>.
            </p>
          </div>
        </Alert>
      </CardContent>
    </Card>
  </div>
</template>
