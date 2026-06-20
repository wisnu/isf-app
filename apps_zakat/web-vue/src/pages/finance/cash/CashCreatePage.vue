<script setup lang="ts">
import { ArrowLeft } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { reactive, shallowRef } from 'vue'

import Alert from '@/components/ui/Alert.vue'
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
    await api.post('/api/authorization/save-and-submit/', {
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
  <div class="p-3 sm:p-4 space-y-3">
    <!-- Tombol kembali (judul halaman ada di breadcrumb header) -->
    <div class="flex items-center gap-2">
      <button
        class="flex items-center gap-1 rounded px-2 py-1 text-xs text-slate-500 hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-zinc-800"
        @click="router.push({ name: 'finance-cash' })"
      >
        <ArrowLeft class="h-3.5 w-3.5" />
        Kembali
      </button>
    </div>
    <p class="text-xs text-slate-400">Permintaan akan diproses melalui otorisasi supervisor</p>

    <Alert v-if="formError" variant="destructive">{{ formError }}</Alert>

    <div class="rounded-lg border border-slate-200 bg-white dark:bg-zinc-900 overflow-hidden max-w-sm">
      <!-- Card header bar -->
      <div class="flex items-center justify-between bg-slate-800 px-4 py-2">
        <h2 class="font-bold text-xs tracking-widest text-white uppercase">Tambah Kas</h2>
      </div>
      <!-- Card body -->
      <div class="p-4 space-y-3">
        <div>
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
            Kode Kas <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.code"
            placeholder="mis. 1-1600"
            class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        <div>
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
            Nama Kas <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.name"
            placeholder="Nama kas / brankas"
            class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        <div>
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
            Pemegang Kas
          </label>
          <input
            v-model="form.holder"
            placeholder="Nama pemegang (opsional)"
            class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <p class="text-[10px] text-slate-400">Kas aktif setelah disetujui supervisor melalui sistem otorisasi.</p>

        <div class="flex gap-2 pt-1">
          <button
            class="flex-1 border-2 border-slate-300 text-slate-600 font-semibold hover:bg-slate-50 px-4 py-2 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="submitting"
            @click="router.push({ name: 'finance-cash' })"
          >
            Batal
          </button>
          <button
            class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold px-6 py-2 rounded text-sm shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="submitting"
            @click="submit"
          >
            {{ submitting ? 'Mengirim...' : 'Submit Otorisasi' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
