<script setup lang="ts">
import { useRouter } from 'vue-router'
import { reactive, shallowRef } from 'vue'

import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import { api } from '@/lib/api/client'
import { useToast } from '@/lib/useToast'

const router = useRouter()
const toast = useToast()

const form = reactive({ code: '', name: '', holder: '' })
const submitting = shallowRef(false)
const formError = shallowRef<string | null>(null)

async function submit() {
  if (!form.code.trim() || !form.name.trim()) {
    formError.value = 'Kode dan nama kas wajib diisi'
    return
  }
  formError.value = null
  submitting.value = true
  try {
    await api.post('/api/otorisasi/save-and-submit/', {
      entity_type: 'kas',
      module: 'keuangan',
      payload: {
        code: form.code.trim(),
        name: form.name.trim(),
        holder: form.holder.trim() || null,
      },
    })
    toast.success('Permintaan tambah kas disubmit untuk otorisasi')
    void router.push({ name: 'finance-cash' })
  } catch (e: unknown) {
    const msg = e instanceof Error ? e.message : 'Gagal mengirim submission'
    formError.value = msg
    toast.error(msg)
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="space-y-4">
    <PageHeader title="Tambah Kas" subtitle="Permintaan akan diproses melalui otorisasi supervisor" />

    <div class="rounded-xl border border-border bg-surface p-6 space-y-4 max-w-sm">
      <div
        v-if="formError"
        class="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700 dark:bg-red-900/10 dark:border-red-800 dark:text-red-400"
      >
        {{ formError }}
      </div>

      <div>
        <label class="mb-1 block text-xs font-medium">Kode Kas <span class="text-red-500">*</span></label>
        <input
          v-model="form.code"
          placeholder="mis. 1-1600"
          class="h-8 w-full rounded border border-border bg-background px-2 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
        />
      </div>
      <div>
        <label class="mb-1 block text-xs font-medium">Nama Kas <span class="text-red-500">*</span></label>
        <input
          v-model="form.name"
          placeholder="Nama kas / brankas"
          class="h-8 w-full rounded border border-border bg-background px-2 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
        />
      </div>
      <div>
        <label class="mb-1 block text-xs font-medium">Pemegang Kas</label>
        <input
          v-model="form.holder"
          placeholder="Nama pemegang (opsional)"
          class="h-8 w-full rounded border border-border bg-background px-2 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
        />
      </div>

      <p class="text-[10px] text-muted">Kas aktif setelah disetujui supervisor melalui sistem otorisasi.</p>

      <div class="flex justify-end gap-2">
        <Button variant="outline" size="sm" :disabled="submitting" @click="router.push({ name: 'finance-cash' })">
          Batal
        </Button>
        <Button size="sm" :disabled="submitting" @click="submit">
          {{ submitting ? 'Mengirim...' : 'Submit Otorisasi' }}
        </Button>
      </div>
    </div>
  </div>
</template>
