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
const error = ref<string | null>(null)

async function load() {
  loading.value = true
  error.value = null
  try {
    data.value = await api.get<DashboardSummary>('/api/dashboard/summary')
  } catch (e) {
    error.value = e instanceof ApiError ? e.message : 'Gagal memuat dashboard'
    data.value = null
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(() => auth.activeTenantId, () => { if (auth.activeTenantId) load() })
</script>

<template>
  <section class="dashboard">
    <header>
      <h1>Dashboard</h1>
      <p class="muted" v-if="data">{{ data.tenant_name }}</p>
    </header>

    <div v-if="loading" class="muted">Memuat…</div>
    <div v-else-if="error" class="card error">{{ error }}</div>
    <div v-else-if="data" class="widgets">
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
  </section>
</template>

<style scoped>
.dashboard { display: flex; flex-direction: column; gap: 1.5rem; }
.dashboard header h1 { margin: 0; }
.muted { color: var(--color-text-muted); margin: 0.3rem 0 0; }
.widgets {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}
.error { color: var(--color-danger); }
</style>
