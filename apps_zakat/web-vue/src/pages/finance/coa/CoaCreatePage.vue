<script setup lang="ts">
import { ArrowLeft } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { reactive, shallowRef } from 'vue'

import Alert from '@/shared/components/Alert.vue'
import { api } from '@/shared/api/client'
import { useToast } from '@/shared/composables/useToast'

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
    await api.post('/api/authorization/save-and-submit/', {
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
    void router.push({ name: 'finance-coa' })
  } catch (e: unknown) {
    formError.value = e instanceof Error ? e.message : 'Gagal mengirim submission'
    toast.error(formError.value ?? '')
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
        @click="router.push({ name: 'finance-coa' })"
      >
        <ArrowLeft class="h-3.5 w-3.5" />
        Kembali
      </button>
    </div>
    <p class="text-xs text-slate-400">Permintaan akan diproses melalui otorisasi supervisor</p>

    <Alert v-if="formError" variant="destructive">{{ formError }}</Alert>

    <div class="rounded-lg border border-slate-200 bg-white dark:bg-zinc-900 overflow-hidden max-w-md">
      <!-- Card header bar -->
      <div class="flex items-center justify-between bg-slate-800 px-4 py-2">
        <h2 class="font-bold text-xs tracking-widest text-white uppercase">Tambah Akun COA</h2>
      </div>
      <!-- Card body -->
      <div class="p-4 space-y-3">
        <!-- Kode + Tipe -->
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
              Kode Akun <span class="text-red-500">*</span>
            </label>
            <input
              v-model="form.code"
              placeholder="mis. 110101"
              class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Tipe</label>
            <select
              v-model="form.type_code"
              class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            >
              <option v-for="t in TYPE_OPTIONS" :key="t.code" :value="t.code">{{ t.label }}</option>
            </select>
          </div>
        </div>

        <!-- Nama -->
        <div>
          <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">
            Nama Akun <span class="text-red-500">*</span>
          </label>
          <input
            v-model="form.name"
            placeholder="Nama akun perkiraan"
            class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <!-- Parent + Akun Detail -->
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Kode Parent</label>
            <input
              v-model="form.parent"
              placeholder="Opsional"
              class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
          <div class="flex items-end pb-1.5">
            <label class="flex items-center gap-1.5 text-xs font-semibold text-slate-500 uppercase tracking-wide cursor-pointer">
              <input v-model="form.is_detail" type="checkbox" class="rounded" />
              Akun Detail
            </label>
          </div>
        </div>

        <p class="text-[10px] text-slate-400">Akun baru aktif setelah disetujui supervisor melalui sistem otorisasi.</p>

        <div class="flex gap-2 pt-1">
          <button
            class="flex-1 border-2 border-slate-300 text-slate-600 font-semibold hover:bg-slate-50 px-4 py-2 rounded text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="submitting"
            @click="router.push({ name: 'finance-coa' })"
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
