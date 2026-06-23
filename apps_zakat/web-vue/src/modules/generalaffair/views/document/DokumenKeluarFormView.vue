<script setup lang="ts">
import { ArrowLeft } from 'lucide-vue-next'
import { computed, onMounted, ref, shallowRef } from 'vue'
import { useRouter, useRoute } from 'vue-router'

import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import Input from '@/shared/components/Input.vue'
import SearchSelect from '@/shared/components/SearchSelect.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'

// ── Types ─────────────────────────────────────────────────────────────────────

interface DokumenKeluarDetail {
  dokumen_id: number
  nomor: string
  id_jenis_dokumen: number
  nama_jenis_dokumen: string
  work_unit_id: number
  work_unit_desc: string
  pic: string
  konseptor: string | null
  tanggal_dokumen: string
  tanggal_kirim: string | null
  perihal: string
  tujuan: string
  keterangan: string | null
  status_kirim: string | null
}

interface JenisDokumenOption {
  id_jenis_dokumen: number
  kode_jenis_dokumen: string
  nama_jenis_dokumen: string
}

interface WorkUnitOption {
  work_unit_id: number
  description: string
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
const workUnitOptions = ref<WorkUnitOption[]>([])

const formData = ref({
  id_jenis_dokumen: 0,
  work_unit_id: 0,
  pic: '',
  konseptor: '',
  tanggal_dokumen: '',
  tanggal_kirim: '',
  perihal: '',
  tujuan: '',
  keterangan: '',
  status_kirim: '',
})

const nomor = ref('')

// ── API Calls ─────────────────────────────────────────────────────────────────

async function loadOptions() {
  try {
    const [jd, wu] = await Promise.all([
      api.get<{ rows: JenisDokumenOption[] }>('/api/generalaffair/document-types?page=1&page_size=100'),
      api.get<{ data: WorkUnitOption[] }>('/api/generalaffair/document/work-units'),
    ])
    jenisDokumenOptions.value = jd.rows
    workUnitOptions.value = (wu as any).data ?? wu as any
  } catch {
    jenisDokumenOptions.value = []
    workUnitOptions.value = []
  }
}

async function loadDetail() {
  if (!isEdit.value) return
  loading.value = true
  errorMsg.value = null
  try {
    const res = await api.get<DokumenKeluarDetail>(`/api/generalaffair/document/outgoing/${route.params.id}`)
    nomor.value = res.nomor
    formData.value = {
      id_jenis_dokumen: res.id_jenis_dokumen,
      work_unit_id: res.work_unit_id,
      pic: res.pic,
      konseptor: res.konseptor || '',
      tanggal_dokumen: res.tanggal_dokumen,
      tanggal_kirim: res.tanggal_kirim || '',
      perihal: res.perihal,
      tujuan: res.tujuan,
      keterangan: res.keterangan || '',
      status_kirim: res.status_kirim || '',
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
  if (!formData.value.work_unit_id) {
    toast.add({ severity: 'warn', summary: 'Validasi', detail: 'Unit kerja wajib dipilih', life: 3000 })
    return
  }
  if (!formData.value.pic.trim()) {
    toast.add({ severity: 'warn', summary: 'Validasi', detail: 'PIC wajib diisi', life: 3000 })
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
  if (!formData.value.tujuan.trim()) {
    toast.add({ severity: 'warn', summary: 'Validasi', detail: 'Tujuan wajib diisi', life: 3000 })
    return
  }

  saving.value = true
  try {
    const payload = {
      id_jenis_dokumen: formData.value.id_jenis_dokumen,
      work_unit_id: formData.value.work_unit_id,
      pic: formData.value.pic.trim(),
      konseptor: formData.value.konseptor.trim() || null,
      tanggal_dokumen: formData.value.tanggal_dokumen,
      tanggal_kirim: formData.value.tanggal_kirim || null,
      perihal: formData.value.perihal.trim(),
      tujuan: formData.value.tujuan.trim(),
      keterangan: formData.value.keterangan.trim() || null,
      ...(isEdit.value && { status_kirim: formData.value.status_kirim || null }),
    }

    if (isEdit.value) {
      await api.put(`/api/generalaffair/document/outgoing/${route.params.id}`, payload)
      toast.add({ severity: 'success', summary: 'Berhasil', detail: 'Dokumen berhasil diperbarui', life: 3000 })
    } else {
      await api.post('/api/generalaffair/document/outgoing', payload)
      toast.add({ severity: 'success', summary: 'Berhasil', detail: 'Dokumen berhasil dibuat', life: 3000 })
    }
    router.push({ name: 'generalaffair-dokumen-keluar-list' })
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Error', detail: e instanceof ApiError ? e.message : 'Gagal menyimpan', life: 3000 })
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadOptions()
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
        @click="() => router.push({ name: 'generalaffair-dokumen-keluar-list' })"
        class="p-2 rounded hover:bg-muted transition-colors"
        title="Kembali"
      >
        <ArrowLeft class="w-4 h-4" />
      </button>
      <div>
        <h1 class="text-2xl font-bold tracking-tight">{{ isEdit ? 'Edit' : 'Tambah' }} Dokumen Keluar</h1>
        <p class="text-sm text-muted">{{ isEdit ? 'Perbarui informasi dokumen' : 'Buat dokumen keluar baru' }}</p>
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
    <div v-else class="rounded-xl border border-border bg-surface p-6 space-y-4">
      <!-- Row 1: Jenis Dokumen & Unit Kerja -->
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
          <label class="text-sm font-medium">Unit Kerja (Bidang Kerja) <span class="text-red-600">*</span></label>
          <SearchSelect
            :model-value="formData.work_unit_id"
            :options="workUnitOptions.map(x => ({ value: x.work_unit_id, label: x.description }))"
            placeholder="Pilih unit kerja..."
            @update:model-value="formData.work_unit_id = $event"
          />
        </div>
      </div>

      <!-- Row 2: PIC & Konseptor -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium">PIC <span class="text-red-600">*</span></label>
          <Input
            v-model="formData.pic"
            placeholder="Nama PIC"
            class="text-sm"
          />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium">Konseptor</label>
          <Input
            v-model="formData.konseptor"
            placeholder="Nama konseptor"
            class="text-sm"
          />
        </div>
      </div>

      <!-- Row 3: Nomor Register -->
      <div class="flex flex-col gap-1">
        <label class="text-sm font-medium">Nomor Register</label>
        <Input
          v-model="nomor"
          :placeholder="isEdit ? nomor : 'Akan digenerate otomatis'"
          disabled
          class="text-sm"
        />
      </div>

      <!-- Row 4: Tanggal Dokumen & Kirim -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium">Tanggal Dokumen <span class="text-red-600">*</span></label>
          <DateField v-model="formData.tanggal_dokumen" />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium">Tanggal Kirim</label>
          <DateField v-model="formData.tanggal_kirim" />
        </div>
      </div>

      <!-- Row 5: Perihal & Tujuan -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium">Perihal <span class="text-red-600">*</span></label>
          <Input
            v-model="formData.perihal"
            placeholder="Perihal dokumen"
            class="text-sm"
          />
        </div>
        <div class="flex flex-col gap-1">
          <label class="text-sm font-medium">Tujuan <span class="text-red-600">*</span></label>
          <Input
            v-model="formData.tujuan"
            placeholder="Tujuan dokumen"
            class="text-sm"
          />
        </div>
      </div>

      <!-- Row 6: Keterangan -->
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

      <!-- Row 7: Status Kirim (only on edit) -->
      <div v-if="isEdit" class="flex flex-col gap-1">
        <label class="text-sm font-medium">Status Kirim</label>
        <Input
          v-model="formData.status_kirim"
          placeholder="Status pengiriman dokumen"
          class="text-sm"
        />
      </div>

      <!-- Action buttons -->
      <div class="flex items-center justify-between pt-4 border-t border-border">
        <Button
          variant="outline"
          @click="() => router.push({ name: 'generalaffair-dokumen-keluar-list' })"
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
