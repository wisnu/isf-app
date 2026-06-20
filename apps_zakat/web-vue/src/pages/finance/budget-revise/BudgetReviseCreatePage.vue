<script setup lang="ts">
import { ArrowLeft } from 'lucide-vue-next'
import { onMounted, ref, shallowRef, watch } from 'vue'
import { useRouter } from 'vue-router'

import SearchSelect from '@/components/ui/SearchSelect.vue'
import { api, ApiError } from '@/lib/api/client'
import { useToast } from '@/lib/useToast'

interface BudgetOwner { owner_id: string; owner_name: string }
interface Period { period_id: number; period_value: number }
interface SelectOption { value: string; label: string }

const router = useRouter()
const toast = useToast()

const owners = ref<SelectOption[]>([])
const periods = ref<SelectOption[]>([])
const selectedOwner = ref('')
const selectedPeriod = ref('')
const ownersLoading = shallowRef(false)
const periodsLoading = shallowRef(false)

const budgetCode = shallowRef('')
const itemGroup = shallowRef('')
const itemName = shallowRef('')
const amount = shallowRef(0)
const saving = shallowRef(false)

async function loadOwners() {
  ownersLoading.value = true
  try {
    const res = await api.get<{ data: BudgetOwner[] }>('/api/budget/owners')
    owners.value = (res.data ?? []).map((o) => ({ value: o.owner_id, label: o.owner_name }))
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal memuat daftar pemilik')
  } finally {
    ownersLoading.value = false
  }
}

async function loadPeriods() {
  if (!selectedOwner.value) return
  periodsLoading.value = true
  periods.value = []
  selectedPeriod.value = ''
  try {
    const res = await api.get<{ data: Period[] }>(`/api/budget/periods/${selectedOwner.value}`)
    periods.value = (res.data ?? []).map((p) => ({ value: String(p.period_id), label: String(p.period_value) }))
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal memuat periode')
  } finally {
    periodsLoading.value = false
  }
}

watch(selectedOwner, () => { if (selectedOwner.value) loadPeriods() })

async function submit() {
  if (!selectedOwner.value) { toast.error('Pemilik Anggaran wajib dipilih'); return }
  if (!selectedPeriod.value) { toast.error('Periode wajib dipilih'); return }
  if (!budgetCode.value.trim()) { toast.error('Kode Budget wajib diisi'); return }
  if (!itemGroup.value.trim()) { toast.error('Kelompok Kegiatan wajib diisi'); return }
  if (!itemName.value.trim()) { toast.error('Rincian Kebutuhan wajib diisi'); return }
  if (amount.value <= 0) { toast.error('Nilai Anggaran harus lebih dari 0'); return }

  saving.value = true
  try {
    await api.post('/api/budget/', {
      owner_id: Number(selectedOwner.value),
      period_id: Number(selectedPeriod.value),
      budget_code: budgetCode.value.trim(),
      item_group: itemGroup.value.trim(),
      item_name: itemName.value.trim(),
      amount: amount.value,
    })
    toast.success('Anggaran baru berhasil disimpan. Silahkan diotorisasi.')
    void router.push({ name: 'finance-budget-revise' })
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal menyimpan anggaran')
  } finally {
    saving.value = false
  }
}

onMounted(loadOwners)
</script>

<template>
  <div class="p-3 sm:p-4 space-y-3">
    <!-- Back button -->
    <div class="flex items-center gap-2">
      <button
        class="flex items-center gap-1 rounded px-2 py-1 text-xs text-slate-500 hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-zinc-800"
        @click="router.push({ name: 'finance-budget-revise' })"
      >
        <ArrowLeft class="h-3.5 w-3.5" />
        Kembali
      </button>
      <span class="text-xs text-slate-400">Tambah item anggaran baru untuk diotorisasi</span>
    </div>

    <!-- Form card -->
    <div class="rounded-lg border border-slate-200 bg-white dark:bg-zinc-900 overflow-hidden max-w-2xl">
      <!-- Card header bar -->
      <div class="flex items-center justify-between bg-slate-800 px-4 py-2">
        <h2 class="font-bold text-xs tracking-widest text-white uppercase">Tambah Anggaran</h2>
      </div>
      <!-- Card body -->
      <div class="p-4 space-y-3">
        <!-- Pemilik & Periode -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
              Pemilik Anggaran <span class="text-red-500">*</span>
            </label>
            <SearchSelect
              v-model="selectedOwner"
              :options="owners"
              :loading="ownersLoading"
              placeholder="Pilih pemilik..."
            />
          </div>
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
              Periode <span class="text-red-500">*</span>
            </label>
            <SearchSelect
              v-model="selectedPeriod"
              :options="periods"
              :loading="periodsLoading"
              :disabled="!selectedOwner"
              placeholder="Pilih periode..."
            />
          </div>
        </div>

        <!-- Kode Budget -->
        <div>
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
            Kode Budget <span class="text-red-500">*</span>
          </label>
          <input
            v-model="budgetCode"
            placeholder="mis. BUD-001"
            class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <!-- Kelompok Kegiatan & Rincian Kebutuhan -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
              Kelompok Kegiatan <span class="text-red-500">*</span>
            </label>
            <input
              v-model="itemGroup"
              placeholder="mis. Program Zakat"
              class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
              Rincian Kebutuhan <span class="text-red-500">*</span>
            </label>
            <input
              v-model="itemName"
              placeholder="mis. Operasional Kantor"
              class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </div>

        <!-- Nilai Anggaran -->
        <div>
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
            Nilai Anggaran <span class="text-red-500">*</span>
          </label>
          <input
            v-model.number="amount"
            type="number"
            placeholder="0"
            class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm tabular-nums focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <!-- Actions -->
        <div class="flex gap-2 pt-1">
          <button
            class="flex-1 border-2 border-slate-300 text-slate-600 font-semibold hover:bg-slate-50 px-4 py-2 rounded text-sm"
            :disabled="saving"
            @click="router.push({ name: 'finance-budget-revise' })"
          >
            Batal
          </button>
          <button
            class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-6 py-2 rounded text-sm shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="saving"
            @click="submit"
          >
            {{ saving ? 'Menyimpan...' : 'Simpan Anggaran' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
