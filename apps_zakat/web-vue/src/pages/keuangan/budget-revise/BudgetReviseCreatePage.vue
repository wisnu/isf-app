<script setup lang="ts">
import { onMounted, ref, shallowRef, watch } from 'vue'
import { useRouter } from 'vue-router'

import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
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
    void router.push({ name: 'keuangan-anggaran-revisi' })
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal menyimpan anggaran')
  } finally {
    saving.value = false
  }
}

onMounted(loadOwners)
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Tambah Anggaran" subtitle="Tambah item anggaran baru untuk diotorisasi" />

    <Card class="max-w-2xl">
      <CardContent class="p-6 space-y-4">
        <!-- Pemilik & Periode -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="mb-1.5 block text-sm font-medium">Pemilik Anggaran <span class="text-red-500">*</span></label>
            <SearchSelect
              v-model="selectedOwner"
              :options="owners"
              :loading="ownersLoading"
              placeholder="Pilih pemilik..."
            />
          </div>
          <div>
            <label class="mb-1.5 block text-sm font-medium">Periode <span class="text-red-500">*</span></label>
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
          <label class="mb-1 block text-xs font-medium">Kode Budget <span class="text-red-500">*</span></label>
          <input
            v-model="budgetCode"
            placeholder="mis. BUD-001"
            class="h-9 w-full rounded-lg border border-border px-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </div>

        <!-- Kelompok Kegiatan & Rincian Kebutuhan -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="mb-1 block text-xs font-medium">Kelompok Kegiatan <span class="text-red-500">*</span></label>
            <input
              v-model="itemGroup"
              placeholder="mis. Program Zakat"
              class="h-9 w-full rounded-lg border border-border px-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
            />
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium">Rincian Kebutuhan <span class="text-red-500">*</span></label>
            <input
              v-model="itemName"
              placeholder="mis. Operasional Kantor"
              class="h-9 w-full rounded-lg border border-border px-2.5 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
            />
          </div>
        </div>

        <!-- Nilai Anggaran -->
        <div>
          <label class="mb-1 block text-xs font-medium">Nilai Anggaran <span class="text-red-500">*</span></label>
          <input
            v-model.number="amount"
            type="number"
            placeholder="0"
            class="h-9 w-full rounded-lg border border-border px-2.5 text-sm tabular-nums focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </div>

        <div class="flex justify-end gap-2 pt-2">
          <Button variant="outline" :disabled="saving" @click="router.push({ name: 'keuangan-anggaran-revisi' })">
            Batal
          </Button>
          <Button :disabled="saving" @click="submit">
            {{ saving ? 'Menyimpan...' : 'Simpan Anggaran' }}
          </Button>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
