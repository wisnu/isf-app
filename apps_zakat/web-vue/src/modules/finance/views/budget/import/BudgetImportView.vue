<script setup lang="ts">
import { ArrowLeft, FileUp, X } from 'lucide-vue-next'
import { ref, shallowRef } from 'vue'
import { useRouter } from 'vue-router'

import SearchSelect from '@/shared/components/SearchSelect.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────

interface Period { period_id: number; period_name: string }
interface SelectOption { value: string; label: string }

// ── State ─────────────────────────────────────────────────────────────────────

const router = useRouter()
const toast = useToast()

const periods = ref<SelectOption[]>([])
const selectedPeriod = ref('')
const selectedFile = ref<File | null>(null)
const loading = shallowRef(false)
const periodsLoading = shallowRef(false)

// ── Load periods ──────────────────────────────────────────────────────────────

async function loadPeriods() {
  periodsLoading.value = true
  try {
    const res = await api.get<{ data: Period[] }>('/api/budget/periods')
    periods.value = (res.data ?? []).map((p) => ({
      value: String(p.period_id),
      label: p.period_name,
    }))
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal memuat periode anggaran')
  } finally {
    periodsLoading.value = false
  }
}

// ── File handling ─────────────────────────────────────────────────────────────

function onFileSelected(event: Event) {
  const input = event.target as HTMLInputElement
  if (input.files && input.files[0]) {
    selectedFile.value = input.files[0]
  }
}

function clearFile() {
  selectedFile.value = null
  const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement
  if (fileInput) fileInput.value = ''
}

// ── Submit ────────────────────────────────────────────────────────────────────

async function submitImport() {
  if (!selectedPeriod.value) {
    toast.error('Pilih periode anggaran terlebih dahulu')
    return
  }
  if (!selectedFile.value) {
    toast.error('Pilih file Excel terlebih dahulu')
    return
  }

  loading.value = true
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('period_id', selectedPeriod.value)

    const res = await api.upload<{ submission_id: string; message: string }>('/api/budget/import', formData)

    toast.success('Anggaran berhasil disimpan. Silahkan diotorisasi di menu Otorisasi.')
    selectedFile.value = null
    selectedPeriod.value = ''
    clearFile()
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal mengunggah anggaran')
  } finally {
    loading.value = false
  }
}

loadPeriods()
</script>

<template>
  <div class="p-3 sm:p-4 space-y-3">
    <!-- Back button -->
    <div class="flex items-center gap-2">
      <button
        class="flex items-center gap-1 rounded px-2 py-1 text-xs text-slate-500 hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-zinc-800"
        @click="router.push({ name: 'finance-budget-inquiry' })"
      >
        <ArrowLeft class="h-3.5 w-3.5" />
        Kembali
      </button>
      <span class="text-xs text-slate-400">Impor anggaran dari file Excel</span>
    </div>

    <!-- Form card -->
    <div class="rounded-lg border border-slate-200 bg-white dark:bg-zinc-900 overflow-hidden max-w-2xl">
      <!-- Card header bar -->
      <div class="flex items-center justify-between bg-slate-800 px-4 py-2">
        <h2 class="font-bold text-xs tracking-widest text-white uppercase">Impor Anggaran</h2>
      </div>
      <!-- Card body -->
      <div class="p-4 space-y-3">
        <!-- Periode -->
        <div>
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
            Tahun Anggaran <span class="text-red-500">*</span>
          </label>
          <SearchSelect
            v-model="selectedPeriod"
            :options="periods"
            :loading="periodsLoading"
            placeholder="Pilih periode anggaran..."
          />
        </div>

        <!-- File input -->
        <div>
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
            File Excel <span class="text-red-500">*</span>
          </label>
          <div class="flex items-center gap-3">
            <label class="relative inline-flex cursor-pointer">
              <input
                type="file"
                accept=".xlsx,.xls"
                class="sr-only"
                @change="onFileSelected"
              />
              <span class="inline-flex items-center gap-2 rounded border border-slate-200 px-4 py-2 text-sm font-medium hover:bg-slate-50 transition-colors dark:hover:bg-zinc-800">
                <FileUp class="w-4 h-4" />
                Pilih File
              </span>
            </label>
            <span v-if="selectedFile" class="text-sm text-slate-500">
              {{ selectedFile.name }}
            </span>
            <button
              v-if="selectedFile"
              type="button"
              class="rounded p-1.5 text-red-500 hover:bg-red-50 hover:text-red-700"
              @click="clearFile"
            >
              <X class="w-4 h-4" />
            </button>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex justify-end pt-1">
          <button
            class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-6 py-2 rounded text-sm shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="!selectedPeriod || !selectedFile || loading"
            @click="submitImport"
          >
            {{ loading ? 'Menyimpan...' : 'Simpan Anggaran' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Info box -->
    <div class="rounded-lg border border-slate-200 bg-white dark:bg-zinc-900 overflow-hidden max-w-2xl">
      <div class="flex items-center justify-between bg-slate-700 px-4 py-2">
        <h2 class="font-bold text-xs tracking-widest text-white uppercase">Format File Excel</h2>
      </div>
      <div class="p-4">
        <ul class="ml-4 list-disc space-y-1 text-sm text-slate-500">
          <li>Kolom 1: Kode Pemilik</li>
          <li>Kolom 2: Kelompok Kegiatan</li>
          <li>Kolom 3: Rincian Kebutuhan</li>
          <li>Kolom 4: Kode Budget</li>
          <li>Kolom 5: Nilai Anggaran (angka tanpa Rp.)</li>
        </ul>
      </div>
    </div>
  </div>
</template>
