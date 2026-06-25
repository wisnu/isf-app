<script setup lang="ts">
import { ArrowLeft, Pencil } from 'lucide-vue-next'
import { onMounted, ref, shallowRef } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import Button from '@/shared/components/Button.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import { api, ApiError } from '@/shared/api/client'

interface BankAccountDetail {
  bank_account_id: number
  account_no: string | null
  account_name: string | null
  bank_code: string | null
  is_default: string | null
}

interface CorporateDetail {
  mustahiq_id: number
  no_mustahiq: string | null
  name: string
  address: string | null
  address_kelurahan: string | null
  address_kecamatan: string | null
  province_id: number | null
  postal_code: string | null
  reference_by: string | null
  phone_number: string | null
  cp_name: string | null
  cp_phone_number: string | null
  cp_mobile_number: string | null
  status: string | null
  bank_accounts: BankAccountDetail[]
}

const route  = useRoute()
const router = useRouter()

const detail  = ref<CorporateDetail | null>(null)
const loading = shallowRef(true)
const errorMsg = shallowRef<string | null>(null)

const id = route.params.id as string

const hasCP = (d: CorporateDetail) => !!(d.cp_name || d.cp_phone_number || d.cp_mobile_number)

function goEdit() {
  router.push({ name: 'distribution-mustahiq-corporate-edit', params: { id } })
}

onMounted(async () => {
  try {
    detail.value = await api.get<CorporateDetail>(`/api/distribution/mustahiq/corporate/${id}`)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="max-w-3xl mx-auto space-y-4">
    <PageHeader title="Detail Mustahiq Lembaga" subtitle="Informasi penerima manfaat — organisasi / institusi">
      <template #actions>
        <div class="flex items-center gap-2">
          <Button variant="outline" size="sm" class="gap-1.5 h-8 text-xs" @click="router.back()">
            <ArrowLeft class="w-3.5 h-3.5" /> Kembali
          </Button>
          <Button size="sm" class="gap-1.5 h-8 text-xs" @click="goEdit">
            <Pencil class="w-3.5 h-3.5" /> Ubah
          </Button>
        </div>
      </template>
    </PageHeader>

    <div v-if="loading" class="rounded-xl border border-border bg-surface px-6 py-12 text-center text-muted-foreground text-sm">
      Memuat data...
    </div>

    <div v-else-if="errorMsg" class="rounded-xl border border-red-200 bg-red-50 dark:bg-red-900/10 px-4 py-3 text-sm text-red-700">
      {{ errorMsg }}
    </div>

    <template v-else-if="detail">
      <!-- Info Lembaga -->
      <div class="rounded-xl border border-border bg-surface overflow-hidden">
        <div class="px-5 py-3 border-b border-border bg-muted/30">
          <h3 class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Info Lembaga</h3>
        </div>
        <div class="px-5 py-4 grid grid-cols-2 gap-x-8 gap-y-3 text-sm">
          <div>
            <p class="text-xs text-muted-foreground mb-0.5">No. Mustahiq</p>
            <p class="font-mono">{{ detail.no_mustahiq || '—' }}</p>
          </div>
          <div>
            <p class="text-xs text-muted-foreground mb-0.5">Status</p>
            <span
              class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-semibold"
              :class="detail.status === 'A'
                ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300'
                : 'bg-zinc-100 text-zinc-500 dark:bg-zinc-800 dark:text-zinc-400'"
            >{{ detail.status === 'A' ? 'Aktif' : 'NonAktif' }}</span>
          </div>
          <div class="col-span-2">
            <p class="text-xs text-muted-foreground mb-0.5">Nama Lembaga</p>
            <p class="font-semibold text-base">{{ detail.name }}</p>
          </div>
          <div>
            <p class="text-xs text-muted-foreground mb-0.5">Alamat</p>
            <p>{{ detail.address || '—' }}</p>
          </div>
          <div>
            <p class="text-xs text-muted-foreground mb-0.5">Kelurahan</p>
            <p>{{ detail.address_kelurahan || '—' }}</p>
          </div>
          <div>
            <p class="text-xs text-muted-foreground mb-0.5">Kecamatan</p>
            <p>{{ detail.address_kecamatan || '—' }}</p>
          </div>
          <div>
            <p class="text-xs text-muted-foreground mb-0.5">Kode Pos</p>
            <p>{{ detail.postal_code || '—' }}</p>
          </div>
          <div>
            <p class="text-xs text-muted-foreground mb-0.5">Telepon</p>
            <p>{{ detail.phone_number || '—' }}</p>
          </div>
          <div>
            <p class="text-xs text-muted-foreground mb-0.5">Referensi</p>
            <p>{{ detail.reference_by || '—' }}</p>
          </div>
        </div>
      </div>

      <!-- Kontak Person -->
      <div class="rounded-xl border border-border bg-surface overflow-hidden">
        <div class="px-5 py-3 border-b border-border bg-muted/30">
          <h3 class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Kontak Person</h3>
        </div>
        <div class="px-5 py-4 text-sm">
          <p v-if="!hasCP(detail)" class="text-muted-foreground italic text-xs">Tidak ada kontak person.</p>
          <div v-else class="grid grid-cols-3 gap-x-8 gap-y-3">
            <div>
              <p class="text-xs text-muted-foreground mb-0.5">Nama Kontak</p>
              <p>{{ detail.cp_name || '—' }}</p>
            </div>
            <div>
              <p class="text-xs text-muted-foreground mb-0.5">Telepon</p>
              <p>{{ detail.cp_phone_number || '—' }}</p>
            </div>
            <div>
              <p class="text-xs text-muted-foreground mb-0.5">HP</p>
              <p>{{ detail.cp_mobile_number || '—' }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Rekening Bank -->
      <div class="rounded-xl border border-border bg-surface overflow-hidden">
        <div class="px-5 py-3 border-b border-border bg-muted/30">
          <h3 class="text-xs font-semibold text-muted-foreground uppercase tracking-wide">Rekening Bank</h3>
        </div>
        <div class="px-5 py-4">
          <p v-if="detail.bank_accounts.length === 0" class="text-xs text-muted-foreground italic">Tidak ada rekening bank.</p>
          <table v-else class="w-full text-sm">
            <thead>
              <tr class="text-xs text-muted-foreground border-b border-border">
                <th class="pb-2 text-left font-medium">No. Rekening</th>
                <th class="pb-2 text-left font-medium">Nama Rekening</th>
                <th class="pb-2 text-left font-medium">Bank</th>
                <th class="pb-2 text-center font-medium w-20">Default</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-border">
              <tr v-for="ba in detail.bank_accounts" :key="ba.bank_account_id">
                <td class="py-2">{{ ba.account_no || '—' }}</td>
                <td class="py-2">{{ ba.account_name || '—' }}</td>
                <td class="py-2">{{ ba.bank_code || '—' }}</td>
                <td class="py-2 text-center text-emerald-600 font-semibold">{{ ba.is_default === 'T' ? '✓' : '' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>
