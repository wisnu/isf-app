<script setup lang="ts">
import { onMounted, reactive, ref, shallowRef } from 'vue'
import { X } from 'lucide-vue-next'

import Button from '@/components/ui/Button.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import { api, ApiError } from '@/lib/api/client'
import { useToast } from '@/lib/useToast'

interface OwnerRow {
  ownerid: number
  ownercode: string
  ownername: string
  level: number
  is_detail: string
  parentownerid: number | null
  status: string
}

interface LookupItem {
  ownerid: number
  ownercode: string
  ownername: string
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
  ownercode:     '',
  ownername:     '',
  is_detail:     'F' as 'F' | 'T',
  parentownerid: '' as string,
  status:        'A' as 'A' | 'N',
})

onMounted(async () => {
  if (props.mode === 'edit' && props.initialData) {
    form.ownername     = props.initialData.ownername
    form.ownercode     = props.initialData.ownercode
    form.is_detail     = props.initialData.is_detail as 'F' | 'T'
    form.parentownerid = props.initialData.parentownerid
      ? String(props.initialData.parentownerid)
      : ''
    form.status = props.initialData.status as 'A' | 'N'
  }
  await loadParentLookup()
})

async function loadParentLookup() {
  try {
    const res = await api.get<{ data: LookupItem[] }>('/api/parameter/pemilik-anggaran/lookup')
    parentOpts.value = (res.data ?? []).map((item) => ({
      value: String(item.ownerid),
      label: `${item.ownercode} — ${item.ownername}`,
    }))
  } catch {
    toast.error('Gagal memuat daftar pemilik induk')
  }
}

function validate(): string | null {
  if (!form.ownercode.trim() && props.mode === 'create') return 'Kode Pemilik wajib diisi'
  if (!form.ownername.trim()) return 'Nama Pemilik wajib diisi'
  if (form.is_detail === 'T' && !form.parentownerid) return 'Pemilik Induk wajib dipilih untuk tipe Detail'
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
        ownercode:     form.ownercode.trim().toUpperCase(),
        ownername:     form.ownername.trim(),
        is_detail:     form.is_detail,
        parentownerid: form.parentownerid ? Number(form.parentownerid) : null,
        status:        form.status,
      }
      await api.post('/api/otorisasi/save-and-submit/', {
        entity_type: 'budget_owner',
        module:      'keuangan',
        payload,
      })
      toast.success('Permintaan tambah pemilik anggaran dikirim untuk otorisasi')
    } else {
      const payload = {
        action:    'edit',
        ownerid:   props.initialData!.ownerid,
        ownername: form.ownername.trim(),
        status:    form.status,
      }
      await api.post('/api/otorisasi/save-and-submit/', {
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
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
    <div class="w-full max-w-md bg-background rounded-xl shadow-xl border border-border">
      <!-- Header -->
      <div class="flex items-center justify-between px-5 py-4 border-b border-border">
        <h2 class="text-sm font-semibold">
          {{ mode === 'create' ? 'Tambah Pemilik Anggaran' : 'Ubah Pemilik Anggaran' }}
        </h2>
        <button class="text-muted-foreground hover:text-foreground" @click="emit('close')">
          <X class="w-4 h-4" />
        </button>
      </div>

      <!-- Form -->
      <div class="px-5 py-4 space-y-4">
        <!-- Kode -->
        <div>
          <label class="block text-xs font-medium text-muted-foreground mb-1">Kode Pemilik *</label>
          <input
            v-model="form.ownercode"
            :disabled="mode === 'edit'"
            type="text"
            maxlength="10"
            class="w-full h-8 px-3 text-sm border border-border rounded-md bg-background focus:outline-none focus:ring-1 focus:ring-ring uppercase disabled:opacity-50 disabled:cursor-not-allowed"
            placeholder="mis. PRD"
          />
        </div>

        <!-- Nama -->
        <div>
          <label class="block text-xs font-medium text-muted-foreground mb-1">Nama Pemilik *</label>
          <input
            v-model="form.ownername"
            type="text"
            maxlength="100"
            class="w-full h-8 px-3 text-sm border border-border rounded-md bg-background focus:outline-none focus:ring-1 focus:ring-ring"
            placeholder="Nama lengkap pemilik anggaran"
          />
        </div>

        <!-- Tipe (is_detail) -->
        <div>
          <label class="block text-xs font-medium text-muted-foreground mb-1">Tipe *</label>
          <div class="flex gap-4">
            <label class="flex items-center gap-1.5 text-sm cursor-pointer">
              <input
                v-model="form.is_detail"
                type="radio"
                value="F"
                :disabled="mode === 'edit'"
                class="disabled:cursor-not-allowed"
              />
              Induk (Grup)
            </label>
            <label class="flex items-center gap-1.5 text-sm cursor-pointer">
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
          <p v-if="mode === 'edit'" class="text-xs text-muted-foreground mt-1">Tipe tidak dapat diubah setelah tersimpan</p>
        </div>

        <!-- Parent -->
        <div v-if="form.is_detail === 'T'">
          <label class="block text-xs font-medium text-muted-foreground mb-1">
            Pemilik Induk *
          </label>
          <SearchSelect
            v-model="form.parentownerid"
            :options="parentOpts"
            :disabled="mode === 'edit'"
            placeholder="Pilih pemilik induk..."
            class="disabled:opacity-50"
          />
          <p v-if="mode === 'edit'" class="text-xs text-muted-foreground mt-1">Induk tidak dapat diubah setelah tersimpan</p>
        </div>

        <!-- Status -->
        <div>
          <label class="block text-xs font-medium text-muted-foreground mb-1">Status</label>
          <select
            v-model="form.status"
            class="w-full h-8 px-3 text-sm border border-border rounded-md bg-background focus:outline-none focus:ring-1 focus:ring-ring"
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
      <div class="flex justify-end gap-2 px-5 py-4 border-t border-border">
        <Button variant="outline" size="sm" @click="emit('close')">Batal</Button>
        <Button size="sm" :disabled="submitting" @click="submit">
          {{ submitting ? 'Menyimpan…' : 'Simpan' }}
        </Button>
      </div>
    </div>
  </div>
</template>
