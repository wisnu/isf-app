<script setup lang="ts">
import { Loader2 } from 'lucide-vue-next'
import { onMounted, ref, watch } from 'vue'

import SummaryWidget from '@/components/SummaryWidget.vue'
import Alert from '@/components/ui/Alert.vue'
import { api, ApiError } from '@/lib/api/client'
import { useAuthStore } from '@/stores/auth'

interface AmountSummary { total: number; period: string }
interface DashboardSummary {
  tenant_id: string
  tenant_name: string
  penerimaan: AmountSummary
  penyaluran: AmountSummary
}

const auth = useAuthStore()
const data = ref<DashboardSummary | null>(null)
const loading = ref(false)
const errorMsg = ref<string | null>(null)

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    data.value = await api.get<DashboardSummary>('/api/dashboard/summary')
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat dashboard'
    data.value = null
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(
  () => auth.activeTenantId,
  () => { if (auth.activeTenantId) load() },
)
</script>

<template>
  <div class="space-y-6">
    <header>
      <h1 class="text-2xl font-bold tracking-tight">Dashboard</h1>
      <p v-if="data" class="text-sm text-muted">{{ data.tenant_name }}</p>
    </header>

    <div v-if="loading" class="flex justify-center p-8">
      <Loader2 class="w-8 h-8 animate-spin text-primary" />
    </div>

    <Alert v-else-if="errorMsg" variant="destructive">
      {{ errorMsg }}
    </Alert>

    <div v-else-if="data" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <SummaryWidget
        label="Penerimaan"
        :amount="data.penerimaan.total"
        :period="data.penerimaan.period"
        accent="in"
      />
      <SummaryWidget
        label="Penyaluran"
        :amount="data.penyaluran.total"
        :period="data.penyaluran.period"
        accent="out"
      />
    </div>
  </div>
</template>
