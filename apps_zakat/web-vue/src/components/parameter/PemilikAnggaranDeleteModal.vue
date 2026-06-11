<script setup lang="ts">
import { shallowRef } from 'vue'
import { AlertTriangle, X } from 'lucide-vue-next'

import Button from '@/components/ui/Button.vue'
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

const props = defineProps<{ row: OwnerRow }>()
const emit  = defineEmits<{ close: []; deleted: [] }>()

const toast      = useToast()
const submitting = shallowRef(false)
const errorMsg   = shallowRef<string | null>(null)

async function confirmDelete() {
  submitting.value = true
  errorMsg.value   = null
  try {
    await api.post('/api/otorisasi/save-and-submit/', {
      entity_type: 'budget_owner',
      module:      'keuangan',
      payload: {
        action:  'delete',
        ownerid: props.row.ownerid,
      },
    })
    toast.success('Permintaan hapus pemilik anggaran dikirim untuk otorisasi')
    emit('deleted')
  } catch (e) {
    const msg = e instanceof ApiError ? e.message : 'Gagal mengirim permintaan hapus'
    errorMsg.value = msg
    toast.error(msg)
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
    <div class="w-full max-w-sm bg-background rounded-xl shadow-xl border border-border">
      <!-- Header -->
      <div class="flex items-center justify-between px-5 py-4 border-b border-border">
        <h2 class="text-sm font-semibold text-red-600 flex items-center gap-1.5">
          <AlertTriangle class="w-4 h-4" />
          Hapus Pemilik Anggaran
        </h2>
        <button class="text-muted-foreground hover:text-foreground" @click="emit('close')">
          <X class="w-4 h-4" />
        </button>
      </div>

      <!-- Data preview -->
      <div class="px-5 py-4 space-y-3">
        <p class="text-xs text-muted-foreground">Data berikut akan dihapus:</p>
        <dl class="space-y-1.5 text-sm">
          <div class="flex gap-3">
            <dt class="w-28 text-xs text-muted-foreground shrink-0">Kode</dt>
            <dd class="font-mono text-xs">{{ row.ownercode }}</dd>
          </div>
          <div class="flex gap-3">
            <dt class="w-28 text-xs text-muted-foreground shrink-0">Nama</dt>
            <dd class="text-xs">{{ row.ownername }}</dd>
          </div>
          <div class="flex gap-3">
            <dt class="w-28 text-xs text-muted-foreground shrink-0">Tipe</dt>
            <dd class="text-xs">{{ row.is_detail === 'T' ? 'Detail (Leaf)' : 'Induk (Grup)' }}</dd>
          </div>
          <div class="flex gap-3">
            <dt class="w-28 text-xs text-muted-foreground shrink-0">Level</dt>
            <dd class="text-xs">{{ row.level }}</dd>
          </div>
          <div class="flex gap-3">
            <dt class="w-28 text-xs text-muted-foreground shrink-0">Status</dt>
            <dd class="text-xs">{{ row.status === 'A' ? 'Aktif' : 'Tidak Aktif' }}</dd>
          </div>
        </dl>

        <div class="rounded-md border border-amber-200 bg-amber-50 dark:border-amber-800 dark:bg-amber-900/20 px-3 py-2">
          <p class="text-xs text-amber-700 dark:text-amber-400">
            Permintaan hapus akan masuk ke antrian otorisasi. Data tidak dapat dihapus jika masih memiliki child atau direferensi oleh anggaran.
          </p>
        </div>

        <div v-if="errorMsg" class="rounded-md border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700">
          {{ errorMsg }}
        </div>
      </div>

      <!-- Footer -->
      <div class="flex justify-end gap-2 px-5 py-4 border-t border-border">
        <Button variant="outline" size="sm" @click="emit('close')">Batal</Button>
        <Button
          size="sm"
          class="bg-red-600 hover:bg-red-700 text-white"
          :disabled="submitting"
          @click="confirmDelete"
        >
          {{ submitting ? 'Mengirim…' : 'Hapus' }}
        </Button>
      </div>
    </div>
  </div>
</template>
