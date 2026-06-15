<script setup lang="ts">
import { FileUp, X } from 'lucide-vue-next'
import { reactive, ref, shallowRef } from 'vue'

import PageHeader from '@/components/layout/PageHeader.vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import { api, ApiError } from '@/lib/api/client'
import { useToast } from '@/lib/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────

interface Period { period_id: number; period_name: string }
interface SelectOption { value: string; label: string }

// ── State ─────────────────────────────────────────────────────────────────────

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
  <div class="space-y-4">
    <PageHeader title="Buat Anggaran Baru" subtitle="Impor anggaran dari file Excel" />

    <!-- Filter card -->
    <Card>
      <CardContent class="p-5">
        <div class="space-y-4">
          <!-- Periode -->
          <div>
            <label class="mb-1.5 block text-sm font-medium">
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
            <label class="mb-1.5 block text-sm font-medium">
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
                <span class="inline-flex items-center gap-2 rounded-lg border border-border px-4 py-2 text-sm font-medium bg-surface hover:bg-muted transition-colors">
                  <FileUp class="w-4 h-4" />
                  Pilih File
                </span>
              </label>
              <span v-if="selectedFile" class="text-sm text-muted-foreground">
                {{ selectedFile.name }}
              </span>
              <button
                v-if="selectedFile"
                type="button"
                class="p-1 rounded hover:bg-muted transition-colors"
                @click="clearFile"
              >
                <X class="w-4 h-4 text-muted-foreground" />
              </button>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex justify-end gap-2 pt-4">
            <Button
              :disabled="!selectedPeriod || !selectedFile || loading"
              :loading="loading"
              @click="submitImport"
            >
              Simpan Anggaran
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Info box -->
    <Card>
      <CardContent class="p-5">
        <div class="space-y-2 text-sm text-muted-foreground">
          <p><strong>Format File Excel:</strong></p>
          <ul class="ml-4 list-disc space-y-1">
            <li>Kolom 1: Kode Pemilik</li>
            <li>Kolom 2: Kelompok Kegiatan</li>
            <li>Kolom 3: Rincian Kebutuhan</li>
            <li>Kolom 4: Kode Budget</li>
            <li>Kolom 5: Nilai Anggaran (angka tanpa Rp.)</li>
          </ul>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
