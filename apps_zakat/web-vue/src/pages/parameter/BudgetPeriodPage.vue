<script setup lang="ts">
import { Plus, X } from 'lucide-vue-next'
import { onMounted, reactive, ref, shallowRef } from 'vue'

import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import { api, ApiError } from '@/lib/api/client'
import { useToast } from '@/lib/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────

interface BudgetPeriod {
  period_id: number
  period_year: number
  period_status: string
  month_count: number
}

// ── State ─────────────────────────────────────────────────────────────────────

const toast = useToast()

const periods = ref<BudgetPeriod[]>([])
const loading = shallowRef(false)

const modalOpen = shallowRef(false)
const submitting = shallowRef(false)

const form = reactive({
  period_year: new Date().getFullYear(),
})

// ── Load data ─────────────────────────────────────────────────────────────────

async function loadPeriods() {
  loading.value = true
  try {
    const res = await api.get<{ data: BudgetPeriod[] }>('/api/budget/parameter/periods')
    periods.value = (res.data ?? []).sort((a, b) => b.period_year - a.period_year)
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal memuat periode anggaran')
  } finally {
    loading.value = false
  }
}

// ── Modal handlers ────────────────────────────────────────────────────────────

function openAdd() {
  form.period_year = new Date().getFullYear() + 1
  modalOpen.value = true
}

function closeModal() {
  modalOpen.value = false
}

// ── Submit ────────────────────────────────────────────────────────────────────

async function submitForm() {
  if (!form.period_year || form.period_year < 2000 || form.period_year > 2099) {
    toast.error('Tahun harus antara 2000-2099')
    return
  }

  submitting.value = true
  try {
    await api.post('/api/budget/parameter/periods', {
      period_year: form.period_year,
    })

    toast.success(`Periode ${form.period_year} berhasil ditambahkan dengan 12 bulan`)
    closeModal()
    loadPeriods()
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal menambah periode')
  } finally {
    submitting.value = false
  }
}

onMounted(loadPeriods)
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Periode Anggaran" subtitle="Daftar tahun anggaran dan bulan-bulannya" />

    <!-- 3-part card layout -->
    <div class="rounded-xl border border-border bg-surface overflow-hidden">
      <!-- Toolbar -->
      <div class="px-4 py-2.5 border-b border-border flex items-center justify-between gap-3">
        <div></div>
        <Button size="sm" @click="openAdd">
          <Plus class="w-3.5 h-3.5 mr-1" /> Tambah Tahun
        </Button>
      </div>

      <!-- Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-[11px]">
          <thead class="text-[10px] text-muted uppercase tracking-widest border-b border-border">
            <tr>
              <th class="px-4 py-2 text-center font-medium w-24">Tahun</th>
              <th class="px-4 py-2 text-left font-medium">Status</th>
              <th class="px-4 py-2 text-center font-medium">Jumlah Bulan</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="3" class="px-4 py-8 text-center text-muted">Memuat...</td>
            </tr>
            <tr v-else-if="periods.length === 0">
              <td colspan="3" class="px-4 py-8 text-center text-muted italic">
                Belum ada periode anggaran. Tambahkan tahun anggaran baru.
              </td>
            </tr>
            <tr
              v-for="period in periods"
              :key="period.period_id"
              class="border-b border-border last:border-0 hover:bg-background/60"
            >
              <td class="px-4 py-2 text-center font-mono font-semibold">{{ period.period_year }}</td>
              <td class="px-4 py-2">
                <span
                  class="inline-block text-[10px] font-semibold px-1.5 py-px rounded"
                  :class="period.period_status === 'O' ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300' : 'bg-zinc-100 text-zinc-500 dark:bg-zinc-800 dark:text-zinc-400'"
                >
                  {{ period.period_status === 'O' ? 'Buka' : 'Tutup' }}
                </span>
              </td>
              <td class="px-4 py-2 text-center">{{ period.month_count }} bulan</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal -->
    <Teleport to="body">
      <div
        v-if="modalOpen"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4"
        @click.self="closeModal"
      >
        <div class="w-full max-w-sm rounded-xl border border-border bg-surface shadow-xl flex flex-col">
          <!-- Header -->
          <div class="flex items-center justify-between border-b border-border px-6 py-4">
            <div>
              <h2 class="text-base font-semibold">Tambah Periode Baru</h2>
              <p class="text-[11px] mt-0.5 text-muted">
                Akan otomatis membuat 12 bulan untuk tahun tersebut
              </p>
            </div>
            <button
              type="button"
              class="rounded-lg p-1.5 text-muted hover:bg-background transition-colors"
              @click="closeModal"
            >
              <X class="w-4 h-4" />
            </button>
          </div>

          <!-- Body -->
          <div class="px-6 py-5">
            <div>
              <label class="mb-1.5 block text-sm font-medium">
                Tahun <span class="text-red-500">*</span>
              </label>
              <input
                v-model.number="form.period_year"
                type="number"
                min="2000"
                max="2099"
                placeholder="mis. 2025"
                class="h-9 w-full rounded-lg border border-border px-2.5 text-sm tabular-nums focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
          </div>

          <!-- Footer -->
          <div class="border-t border-border px-6 py-3 flex justify-end gap-2">
            <Button variant="outline" size="sm" :disabled="submitting" @click="closeModal">
              Batal
            </Button>
            <Button size="sm" :disabled="submitting" @click="submitForm">
              {{ submitting ? 'Menambah...' : 'Tambah Periode' }}
            </Button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
