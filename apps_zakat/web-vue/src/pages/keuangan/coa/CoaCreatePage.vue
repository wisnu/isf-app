<script setup lang="ts">
import { useRouter } from 'vue-router'
import { reactive, shallowRef } from 'vue'

import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import { api } from '@/lib/api/client'
import { useToast } from '@/lib/useToast'

const TYPE_OPTIONS = [
  { code: 'A', label: 'Aset' },
  { code: 'L', label: 'Liabilitas' },
  { code: 'E', label: 'Saldo Dana' },
  { code: 'I', label: 'Pendapatan' },
  { code: 'X', label: 'Penyaluran' },
]

const router = useRouter()
const toast = useToast()

const form = reactive({ code: '', name: '', type_code: 'A', parent: '', is_detail: true })
const submitting = shallowRef(false)
const formError = shallowRef<string | null>(null)

async function submit() {
  if (!form.code.trim() || !form.name.trim()) {
    formError.value = 'Kode dan nama akun wajib diisi'
    return
  }
  formError.value = null
  submitting.value = true
  try {
    await api.post('/api/otorisasi/save-and-submit/', {
      entity_type: 'coa',
      module: 'keuangan',
      payload: {
        action: 'create',
        code: form.code.trim(),
        name: form.name.trim(),
        type_code: form.type_code,
        parent: form.parent.trim() || null,
        is_detail: form.is_detail,
      },
    })
    toast.success('Permintaan tambah COA dikirim untuk otorisasi')
    void router.push({ name: 'keuangan-coa' })
  } catch (e: unknown) {
    formError.value = e instanceof Error ? e.message : 'Gagal mengirim submission'
    toast.error(formError.value ?? '')
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Tambah Akun COA" subtitle="Permintaan akan diproses melalui otorisasi supervisor" />

    <div class="rounded-xl border border-border bg-surface p-6 space-y-4 max-w-md">
      <div
        v-if="formError"
        class="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700 dark:bg-red-900/10 dark:border-red-800 dark:text-red-400"
      >
        {{ formError }}
      </div>

      <!-- Kode + Tipe -->
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="mb-1 block text-xs font-medium">Kode Akun <span class="text-red-500">*</span></label>
          <input
            v-model="form.code"
            placeholder="mis. 110101"
            class="h-8 w-full rounded border border-border bg-background px-2 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </div>
        <div>
          <label class="mb-1 block text-xs font-medium">Tipe</label>
          <select
            v-model="form.type_code"
            class="h-8 w-full rounded border border-border bg-background px-2 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
          >
            <option v-for="t in TYPE_OPTIONS" :key="t.code" :value="t.code">{{ t.label }}</option>
          </select>
        </div>
      </div>

      <!-- Nama -->
      <div>
        <label class="mb-1 block text-xs font-medium">Nama Akun <span class="text-red-500">*</span></label>
        <input
          v-model="form.name"
          placeholder="Nama akun perkiraan"
          class="h-8 w-full rounded border border-border bg-background px-2 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
        />
      </div>

      <!-- Parent + Akun Detail -->
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="mb-1 block text-xs font-medium">Kode Parent</label>
          <input
            v-model="form.parent"
            placeholder="Opsional"
            class="h-8 w-full rounded border border-border bg-background px-2 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </div>
        <div class="flex items-end pb-1">
          <label class="flex items-center gap-1.5 text-xs font-medium cursor-pointer">
            <input v-model="form.is_detail" type="checkbox" class="rounded" />
            Akun Detail
          </label>
        </div>
      </div>

      <p class="text-[10px] text-muted">Akun baru aktif setelah disetujui supervisor melalui sistem otorisasi.</p>

      <div class="flex justify-end gap-2 pt-2">
        <Button variant="outline" size="sm" :disabled="submitting" @click="router.push({ name: 'keuangan-coa' })">
          Batal
        </Button>
        <Button size="sm" :disabled="submitting" @click="submit">
          {{ submitting ? 'Mengirim...' : 'Submit Otorisasi' }}
        </Button>
      </div>
    </div>
  </div>
</template>
