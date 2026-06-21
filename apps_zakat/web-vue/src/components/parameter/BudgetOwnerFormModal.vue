<script setup lang="ts">
import { onMounted, reactive, ref, shallowRef } from 'vue'
import { X } from 'lucide-vue-next'

import SearchSelect from '@/shared/components/SearchSelect.vue'
import { api, ApiError } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'

interface OwnerRow {
  owner_id: number
  owner_code: string
  owner_name: string
  level: number
  is_detail: string
  parent_owner_id: number | null
  status: string
}

interface LookupItem {
  owner_id: number
  owner_code: string
  owner_name: string
  is_detail: string
}

interface SelectOption { value: string; label: string }

const props = defineProps<{
  mode: 'create' | 'edit'
  initialData: OwnerRow | null
}>()

const emit = defineEmits<{
  close: []
  saved: []
}>()

const toast       = useToast()
const submitting  = shallowRef(false)
const formError   = shallowRef<string | null>(null)
const parentOpts  = ref<SelectOption[]>([])

const form = reactive({
  owner_code:     '',
  owner_name:     '',
  is_detail:     'F' as 'F' | 'T',
  parent_owner_id: '' as string,
  status:        'A' as 'A' | 'N',
})

onMounted(async () => {
  if (props.mode === 'edit' && props.initialData) {
    form.owner_name     = props.initialData.owner_name
    form.owner_code     = props.initialData.owner_code
    form.is_detail     = props.initialData.is_detail as 'F' | 'T'
    form.parent_owner_id = props.initialData.parent_owner_id
      ? String(props.initialData.parent_owner_id)
      : ''
    form.status = props.initialData.status as 'A' | 'N'
  }
  await loadParentLookup()
})

async function loadParentLookup() {
  try {
    const res = await api.get<{ data: LookupItem[] }>('/api/parameter/budget-owner/lookup')
    parentOpts.value = (res.data ?? []).map((item) => ({
      value: String(item.owner_id),
      label: `${item.owner_code} — ${item.owner_name}`,
    }))
  } catch {
    toast.error('Gagal memuat daftar pemilik induk')
  }
}

function validate(): string | null {
  if (!form.owner_code.trim() && props.mode === 'create') return 'Kode Pemilik wajib diisi'
  if (!form.owner_name.trim()) return 'Nama Pemilik wajib diisi'
  if (form.is_detail === 'T' && !form.parent_owner_id) return 'Pemilik Induk wajib dipilih untuk tipe Detail'
  return null
}

async function submit() {
  formError.value = null
  const err = validate()
  if (err) { formError.value = err; toast.error(err); return }

  submitting.value = true
  try {
    if (props.mode === 'create') {
      const payload = {
        action:        'create',
        owner_code:     form.owner_code.trim().toUpperCase(),
        owner_name:     form.owner_name.trim(),
        is_detail:     form.is_detail,
        parent_owner_id: form.parent_owner_id ? Number(form.parent_owner_id) : null,
        status:        form.status,
      }
      await api.post('/api/authorization/save-and-submit/', {
        entity_type: 'budget_owner',
        module:      'keuangan',
        payload,
      })
      toast.success('Permintaan tambah pemilik anggaran dikirim untuk otorisasi')
    } else {
      const payload = {
        action:    'edit',
        owner_id:   props.initialData!.owner_id,
        owner_name: form.owner_name.trim(),
        status:    form.status,
      }
      await api.post('/api/authorization/save-and-submit/', {
        entity_type: 'budget_owner',
        module:      'keuangan',
        payload,
      })
      toast.success('Permintaan ubah pemilik anggaran dikirim untuk otorisasi')
    }
    emit('saved')
  } catch (e) {
    const msg = e instanceof ApiError ? e.message : 'Gagal mengirim submission'
    formError.value = msg
    toast.error(msg)
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
    <div class="w-full max-w-2xl bg-background rounded-xl shadow-xl border border-border flex flex-col max-h-[90vh]">
      <!-- Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-border shrink-0">
        <h2 class="text-sm font-semibold text-slate-800 dark:text-slate-100">
          {{ mode === 'create' ? 'Tambah Pemilik Anggaran' : 'Ubah Pemilik Anggaran' }}
        </h2>
        <button class="text-muted-foreground hover:text-foreground" @click="emit('close')">
          <X class="w-4 h-4" />
        </button>
      </div>

      <!-- Form -->
      <div class="px-6 py-5 space-y-4 overflow-y-auto">
        <!-- Kode + Nama -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div class="flex flex-col gap-1">
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Kode Pemilik <span class="text-red-500">*</span></label>
            <input
              v-model="form.owner_code"
              :disabled="mode === 'edit'"
              type="text"
              maxlength="10"
              class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 uppercase disabled:opacity-50 disabled:cursor-not-allowed"
              placeholder="mis. PRD"
            />
          </div>

          <div class="flex flex-col gap-1">
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Nama Pemilik <span class="text-red-500">*</span></label>
            <input
              v-model="form.owner_name"
              type="text"
              maxlength="100"
              class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              placeholder="Nama lengkap pemilik anggaran"
            />
          </div>
        </div>

        <!-- Tipe (is_detail) -->
        <div class="flex flex-col gap-1">
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Tipe <span class="text-red-500">*</span></label>
          <div class="flex gap-4">
            <label class="flex items-center gap-1.5 text-xs cursor-pointer">
              <input
                v-model="form.is_detail"
                type="radio"
                value="F"
                :disabled="mode === 'edit'"
                class="disabled:cursor-not-allowed"
              />
              Induk (Grup)
            </label>
            <label class="flex items-center gap-1.5 text-xs cursor-pointer">
              <input
                v-model="form.is_detail"
                type="radio"
                value="T"
                :disabled="mode === 'edit'"
                class="disabled:cursor-not-allowed"
              />
              Detail (Leaf)
            </label>
          </div>
          <p v-if="mode === 'edit'" class="text-xs text-muted-foreground">Tipe tidak dapat diubah setelah tersimpan</p>
        </div>

        <!-- Parent -->
        <div v-if="form.is_detail === 'T'" class="flex flex-col gap-1">
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
            Pemilik Induk <span class="text-red-500">*</span>
          </label>
          <SearchSelect
            v-model="form.parent_owner_id"
            :options="parentOpts"
            :disabled="mode === 'edit'"
            placeholder="Pilih pemilik induk..."
            class="disabled:opacity-50"
          />
          <p v-if="mode === 'edit'" class="text-xs text-muted-foreground">Induk tidak dapat diubah setelah tersimpan</p>
        </div>

        <!-- Status -->
        <div class="flex flex-col gap-1">
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Status</label>
          <select
            v-model="form.status"
            class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="A">Aktif</option>
            <option value="N">Tidak Aktif</option>
          </select>
        </div>

        <!-- Error -->
        <div
          v-if="formError"
          class="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700"
        >
          {{ formError }}
        </div>
      </div>

      <!-- Footer -->
      <div class="flex justify-end gap-2 px-6 py-3 border-t border-border shrink-0">
        <button
          class="border-2 border-slate-300 text-slate-600 font-semibold hover:bg-slate-50 px-4 py-2 rounded text-sm"
          @click="emit('close')"
        >Batal</button>
        <button
          class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-4 py-2 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="submitting"
          @click="submit"
        >{{ submitting ? 'Menyimpan...' : 'Simpan' }}</button>
      </div>
    </div>
  </div>
</template>
