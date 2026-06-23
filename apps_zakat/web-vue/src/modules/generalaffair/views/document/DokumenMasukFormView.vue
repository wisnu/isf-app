<script setup lang="ts">
import { ArrowLeft, Plus, Trash2, X } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef } from 'vue'
import { useRouter, useRoute } from 'vue-router'

import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import Input from '@/shared/components/Input.vue'
import SearchSelect from '@/shared/components/SearchSelect.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────

interface DokumenMasukDetail {
  dokumen_id: number
  nomor: string
  pengirim: string
  perihal: string
  ditujukan_ke: string | null
  nomor_eksternal: string | null
  tanggal_dokumen: string
  tanggal_terima: string
  keterangan: string | null
  id_jenis_dokumen: number
  nama_jenis_dokumen: string
  disposisi: Array<{ tanggal: string; disposisi_oleh: string; keterangan_disposisi: string | null }>
}

interface JenisDokumenOption {
  id_jenis_dokumen: number
  kode_jenis_dokumen: string
  nama_jenis_dokumen: string
}

interface DisposisiRow {
  tanggal: string
  disposisi_oleh: string
  keterangan_disposisi: string
}

// ── State ─────────────────────────────────────────────────────────────────────

const toast = useToast()
const router = useRouter()
const route = useRoute()

const isEdit = computed(() => !!route.params.id)
const loading = shallowRef(false)
const saving = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

const jenisDokumenOptions = ref<JenisDokumenOption[]>([])

const formData = ref({
  id_jenis_dokumen: 0,
  pengirim: '',
  perihal: '',
  ditujukan_ke: '',
  nomor_eksternal_dokumen: '',
  tanggal_dokumen: '',
  tanggal_terima: '',
  keterangan: '',
  disposisi: [] as DisposisiRow[],
})

const nomor = ref('')

// ── API Calls ─────────────────────────────────────────────────────────────────

async function loadJenisDokumen() {
  try {
    const res = await api.get<{ rows: JenisDokumenOption[] }>('/api/generalaffair/document-types?page=1&page_size=100')
    jenisDokumenOptions.value = res.rows
  } catch {
    jenisDokumenOptions.value = []
  }
}

async function loadDetail() {
  if (!isEdit.value) return
  loading.value = true
  errorMsg.value = null
  try {
    const res = await api.get<DokumenMasukDetail>(`/api/generalaffair/document/incoming/${route.params.id}`)
    nomor.value = res.nomor
    formData.value = {
      id_jenis_dokumen: res.id_jenis_dokumen,
      pengirim: res.pengirim,
      perihal: res.perihal,
      ditujukan_ke: res.ditujukan_ke || '',
      nomor_eksternal_dokumen: res.nomor_eksternal || '',
      tanggal_dokumen: res.tanggal_dokumen,
      tanggal_terima: res.tanggal_terima,
      keterangan: res.keterangan || '',
      disposisi: res.disposisi || [],
    }
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data'
  } finally {
    loading.value = false
  }
}

async function save() {
  // Validate required fields
  if (!formData.value.id_jenis_dokumen) {
    toast.add({ severity: 'warn', summary: 'Validasi', detail: 'Jenis dokumen wajib dipilih', life: 3000 })
    return
  }
  if (!formData.value.pengirim.trim()) {
    toast.add({ severity: 'warn', summary: 'Validasi', detail: 'Pengirim wajib diisi', life: 3000 })
    return
  }
  if (!formData.value.perihal.trim()) {
    toast.add({ severity: 'warn', summary: 'Validasi', detail: 'Perihal wajib diisi', life: 3000 })
    return
  }
  if (!formData.value.tanggal_dokumen) {
    toast.add({ severity: 'warn', summary: 'Validasi', detail: 'Tanggal dokumen wajib diisi', life: 3000 })
    return
  }
  if (!formData.value.tanggal_terima) {
    toast.add({ severity: 'warn', summary: 'Validasi', detail: 'Tanggal terima wajib diisi', life: 3000 })
    return
  }

  saving.value = true
  try {
    const payload = {
      id_jenis_dokumen: formData.value.id_jenis_dokumen,
      pengirim: formData.value.pengirim.trim(),
      perihal: formData.value.perihal.trim(),
      ditujukan_ke: formData.value.ditujukan_ke.trim() || null,
      nomor_eksternal_dokumen: formData.value.nomor_eksternal_dokumen.trim() || null,
      tanggal_dokumen: formData.value.tanggal_dokumen,
      tanggal_terima: formData.value.tanggal_terima,
      keterangan: formData.value.keterangan.trim() || null,
      disposisi: formData.value.disposisi,
    }

    if (isEdit.value) {
      await api.put(`/api/generalaffair/document/incoming/${route.params.id}`, payload)
      toast.add({ severity: 'success', summary: 'Berhasil', detail: 'Dokumen berhasil diperbarui', life: 3000 })
    } else {
      await api.post('/api/generalaffair/document/incoming', payload)
      toast.add({ severity: 'success', summary: 'Berhasil', detail: 'Dokumen berhasil dibuat', life: 3000 })
    }
    router.push({ name: 'generalaffair-dokumen-masuk-list' })
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Error', detail: e instanceof ApiError ? e.message : 'Gagal menyimpan', life: 3000 })
  } finally {
    saving.value = false
  }
}

function addDisposisi() {
  formData.value.disposisi.push({
    tanggal: '',
    disposisi_oleh: '',
    keterangan_disposisi: '',
  })
}

function removeDisposisi(idx: number) {
  formData.value.disposisi.splice(idx, 1)
}

onMounted(() => {
  loadJenisDokumen()
  if (isEdit.value) {
    loadDetail()
  }
})
</script>

<template>
  <div class="space-y-4">
    <!-- Header with back button -->
    <div class="flex items-center gap-3 mb-6">
      <button
        @click="() => router.push({ name: 'generalaffair-dokumen-masuk-list' })"
        class="p-2 rounded hover:bg-muted transition-colors"
        title="Kembali"
      >
        <ArrowLeft class="w-4 h-4" />
      </button>
      <div>
        <h1 class="text-2xl font-bold tracking-tight">{{ isEdit ? 'Edit' : 'Tambah' }} Dokumen Masuk</h1>
        <p class="text-sm text-muted">{{ isEdit ? 'Perbarui informasi dokumen' : 'Buat dokumen masuk baru' }}</p>
      </div>
    </div>

    <!-- Error message -->
    <div v-if="errorMsg" class="flex items-center gap-2 rounded-lg border border-red-200
                                bg-red-50 dark:bg-red-900/20 px-4 py-3 text-sm text-red-700">
      {{ errorMsg }}
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="flex items-center justify-center py-16">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
    </div>

    <!-- Form -->
    <div v-else class="grid gap-6">
      <!-- Main card -->
      <div class="rounded-xl border border-border bg-surface p-6">
        <div class="space-y-4">
          <!-- Row 1: Jenis Dokumen & Nomor -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="flex flex-col gap-1">
              <label class="text-sm font-medium">Jenis Dokumen <span class="text-red-600">*</span></label>
              <SearchSelect
                :model-value="formData.id_jenis_dokumen"
                :options="jenisDokumenOptions.map(x => ({ value: x.id_jenis_dokumen, label: x.nama_jenis_dokumen }))"
                placeholder="Pilih jenis dokumen..."
                @update:model-value="formData.id_jenis_dokumen = $event"
              />
            </div>
            <div class="flex flex-col gap-1">
              <label class="text-sm font-medium">Nomor Register</label>
              <Input
                v-model="nomor"
                :placeholder="isEdit ? nomor : 'Akan digenerate otomatis'"
                disabled
                class="text-sm"
              />
            </div>
          </div>

          <!-- Row 2: Pengirim & Perihal -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="flex flex-col gap-1">
              <label class="text-sm font-medium">Pengirim <span class="text-red-600">*</span></label>
              <Input
                v-model="formData.pengirim"
                placeholder="Nama pengirim dokumen"
                class="text-sm"
              />
            </div>
            <div class="flex flex-col gap-1">
              <label class="text-sm font-medium">Perihal <span class="text-red-600">*</span></label>
              <Input
                v-model="formData.perihal"
                placeholder="Perihal dokumen"
                class="text-sm"
              />
            </div>
          </div>

          <!-- Row 3: Ditujukan Ke & No Eksternal -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="flex flex-col gap-1">
              <label class="text-sm font-medium">Ditujukan Ke</label>
              <Input
                v-model="formData.ditujukan_ke"
                placeholder="Kepada siapa dokumen ditujukan"
                class="text-sm"
              />
            </div>
            <div class="flex flex-col gap-1">
              <label class="text-sm font-medium">No. Surat/Dok Eksternal</label>
              <Input
                v-model="formData.nomor_eksternal_dokumen"
                placeholder="Nomor referensi eksternal"
                class="text-sm"
              />
            </div>
          </div>

          <!-- Row 4: Tanggal Dokumen & Terima -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div class="flex flex-col gap-1">
              <label class="text-sm font-medium">Tanggal Dokumen <span class="text-red-600">*</span></label>
              <DateField v-model="formData.tanggal_dokumen" />
            </div>
            <div class="flex flex-col gap-1">
              <label class="text-sm font-medium">Tanggal Terima <span class="text-red-600">*</span></label>
              <DateField v-model="formData.tanggal_terima" />
            </div>
          </div>

          <!-- Keterangan -->
          <div class="flex flex-col gap-1">
            <label class="text-sm font-medium">Keterangan</label>
            <textarea
              v-model="formData.keterangan"
              placeholder="Informasi tambahan atau catatan"
              rows="3"
              class="h-24 rounded-lg border border-border bg-background px-2.5 py-2 text-xs
                     focus:outline-none focus:ring-1 focus:ring-ring"
            ></textarea>
          </div>
        </div>
      </div>

      <!-- Disposisi Section -->
      <div class="rounded-xl border border-border bg-surface p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-sm font-semibold">Disposisi</h3>
          <Button size="sm" variant="outline" @click="addDisposisi" class="gap-1">
            <Plus class="w-3.5 h-3.5" /> Tambah Disposisi
          </Button>
        </div>

        <div v-if="formData.disposisi.length === 0" class="text-center py-8 text-muted-foreground text-xs italic">
          Belum ada disposisi. Klik "Tambah Disposisi" untuk menambahkan.
        </div>

        <div v-else class="space-y-4">
          <div v-for="(d, idx) in formData.disposisi" :key="idx" class="border border-border rounded-lg p-4 space-y-3">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-medium text-muted">Disposisi {{ idx + 1 }}</span>
              <button
                @click="removeDisposisi(idx)"
                class="p-1 rounded hover:bg-red-100 text-red-600 transition-colors"
                title="Hapus disposisi"
              >
                <Trash2 class="w-3.5 h-3.5" />
              </button>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div class="flex flex-col gap-1">
                <label class="text-xs font-medium">Tanggal</label>
                <DateField v-model="d.tanggal" />
              </div>
              <div class="flex flex-col gap-1">
                <label class="text-xs font-medium">Disposisi Oleh</label>
                <Input
                  v-model="d.disposisi_oleh"
                  placeholder="Nama disposisi"
                  class="text-xs h-9"
                />
              </div>
              <div class="flex flex-col gap-1">
                <label class="text-xs font-medium">Keterangan</label>
                <Input
                  v-model="d.keterangan_disposisi"
                  placeholder="Catatan disposisi"
                  class="text-xs h-9"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Action buttons -->
      <div class="flex items-center justify-between">
        <Button
          variant="outline"
          @click="() => router.push({ name: 'generalaffair-dokumen-masuk-list' })"
        >
          Batal
        </Button>
        <Button
          :loading="saving"
          @click="save"
        >
          {{ isEdit ? 'Perbarui' : 'Simpan' }} Dokumen
        </Button>
      </div>
    </div>
  </div>
</template>
