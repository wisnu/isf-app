<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'

import SummaryWidget from '@/components/SummaryWidget.vue'
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
  <q-page padding>
    <div class="q-mb-md">
      <div class="text-h5">Dashboard</div>
      <div v-if="data" class="text-subtitle2 text-grey">{{ data.tenant_name }}</div>
    </div>

    <div v-if="loading" class="row justify-center q-pa-xl">
      <q-spinner color="primary" size="32px" />
    </div>

    <q-banner v-else-if="errorMsg" class="bg-negative text-white" dense rounded>
      {{ errorMsg }}
    </q-banner>

    <div v-else-if="data" class="row q-col-gutter-md">
      <div class="col-12 col-sm-6">
        <SummaryWidget
          label="Penerimaan"
          :amount="data.penerimaan.total"
          :period="data.penerimaan.period"
          accent="in"
        />
      </div>
      <div class="col-12 col-sm-6">
        <SummaryWidget
          label="Penyaluran"
          :amount="data.penyaluran.total"
          :period="data.penyaluran.period"
          accent="out"
        />
      </div>
    </div>
  </q-page>
</template>
