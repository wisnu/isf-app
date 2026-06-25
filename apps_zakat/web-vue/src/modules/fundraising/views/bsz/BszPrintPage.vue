<script setup lang="ts">
import { ArrowLeft, Printer } from 'lucide-vue-next'
import { onMounted, ref, shallowRef } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import Button from '@/shared/components/Button.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'

interface BszDetailItem {
  item: number
  zakat_object: string
  year: number
  percentage: number
  basic_value: number
  zakah_value: number
}

interface BszTransactionItem {
  transaction_item_id: number
  transaction_no: string
  transaction_date: string
  amount: number
  account_name: string
  description: string | null
  zakah_object: string
}

interface BszDetail {
  bsz_id: number
  bsz_number: string
  donor_id: number
  donor_name: string
  donor_no: string
  npwz: string | null
  npwp: string | null
  address: string | null
  bsz_date: string
  period_begin: string
  period_end: string
  items: BszDetailItem[]
  transactions: BszTransactionItem[]
}

const route = useRoute()
const router = useRouter()

const bsz = ref<BszDetail | null>(null)
const loading = shallowRef(true)
const errorMsg = shallowRef<string | null>(null)

const idr = new Intl.NumberFormat('id-ID')
const fmtRp = (n: number) => 'Rp ' + idr.format(n)

const totalZakat = ref(0)

async function loadBsz() {
  loading.value = true
  try {
    const res = await api.get<{ data: BszDetail }>(`/api/fundraising/bsz/${route.params.id}`)
    bsz.value = res.data
    totalZakat.value = res.data.items.reduce((s, i) => s + i.zakah_value, 0)
  } catch (e) {
    errorMsg.value = e instanceof ApiError ? e.message : 'Gagal memuat data BSZ'
  } finally {
    loading.value = false
  }
}

function print() {
  window.print()
}

onMounted(loadBsz)
</script>

<template>
  <div>
    <!-- Screen toolbar — hidden when printing -->
    <div class="print:hidden flex items-center justify-between mb-4 gap-3">
      <Button variant="secondary" @click="router.push({ name: 'fundraising-bsz-list' })">
        <ArrowLeft class="w-4 h-4 mr-1" /> Kembali ke Daftar
      </Button>
      <Button v-if="bsz" variant="primary" @click="print">
        <Printer class="w-4 h-4 mr-1" /> Cetak BSZ
      </Button>
    </div>

    <!-- Loading / Error -->
    <div v-if="loading" class="p-8 text-center text-sm text-slate-500 print:hidden">Memuat data...</div>
    <div v-else-if="errorMsg" class="p-4 text-sm text-red-600 bg-red-50 rounded-lg print:hidden">{{ errorMsg }}</div>

    <!-- Print document -->
    <div v-else-if="bsz" class="bg-white rounded-lg border border-slate-200 shadow-sm p-8 print:border-0 print:shadow-none print:p-0 max-w-3xl mx-auto">

      <!-- Header -->
      <div class="text-center mb-6">
        <h1 class="text-xl font-bold uppercase tracking-widest text-slate-900">BUKTI SETOR ZAKAT</h1>
        <p class="text-sm text-slate-500 mt-1">BADAN PENGELOLA ZAKAT INFAQ DAN SHADAQAH</p>
      </div>

      <!-- BSZ Info -->
      <div class="mb-6 grid grid-cols-2 gap-3 text-sm">
        <div class="space-y-2">
          <div class="flex gap-2">
            <span class="w-32 text-slate-500">No. BSZ</span>
            <span class="font-bold font-mono text-indigo-800">{{ bsz.bsz_number }}</span>
          </div>
          <div class="flex gap-2">
            <span class="w-32 text-slate-500">Tanggal</span>
            <span>{{ dmy(bsz.bsz_date) }}</span>
          </div>
          <div class="flex gap-2">
            <span class="w-32 text-slate-500">Periode</span>
            <span>{{ dmy(bsz.period_begin) }} s/d {{ dmy(bsz.period_end) }}</span>
          </div>
        </div>
        <div class="space-y-2">
          <div class="flex gap-2">
            <span class="w-32 text-slate-500">Nama Muzakki</span>
            <span class="font-semibold">{{ bsz.donor_name }}</span>
          </div>
          <div class="flex gap-2">
            <span class="w-32 text-slate-500">No. Muzakki</span>
            <span>{{ bsz.donor_no || '—' }}</span>
          </div>
          <div class="flex gap-2">
            <span class="w-32 text-slate-500">NPWZ</span>
            <span>{{ bsz.npwz || '—' }}</span>
          </div>
          <div class="flex gap-2">
            <span class="w-32 text-slate-500">NPWP</span>
            <span>{{ bsz.npwp || '—' }}</span>
          </div>
          <div class="flex gap-2">
            <span class="w-32 text-slate-500">Alamat</span>
            <span class="flex-1">{{ bsz.address || '—' }}</span>
          </div>
        </div>
      </div>

      <hr class="border-slate-300 mb-6" />

      <!-- Detail table -->
      <div class="mb-6">
        <h2 class="text-sm font-bold uppercase tracking-wide text-slate-700 mb-3">Rincian Objek Zakat</h2>
        <table class="w-full text-sm border border-slate-300">
          <thead>
            <tr class="bg-slate-100">
              <th class="border border-slate-300 px-3 py-2 text-left text-xs font-semibold uppercase">No.</th>
              <th class="border border-slate-300 px-3 py-2 text-left text-xs font-semibold uppercase">Objek Zakat</th>
              <th class="border border-slate-300 px-3 py-2 text-center text-xs font-semibold uppercase">Thn. Perolehan</th>
              <th class="border border-slate-300 px-3 py-2 text-center text-xs font-semibold uppercase">Kadar (%)</th>
              <th class="border border-slate-300 px-3 py-2 text-right text-xs font-semibold uppercase">Dasar Pengenaan (Rp)</th>
              <th class="border border-slate-300 px-3 py-2 text-right text-xs font-semibold uppercase">Jumlah Zakat (Rp)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in bsz.items" :key="item.item" class="hover:bg-slate-50">
              <td class="border border-slate-300 px-3 py-2 text-center">{{ item.item }}</td>
              <td class="border border-slate-300 px-3 py-2">{{ item.zakat_object }}</td>
              <td class="border border-slate-300 px-3 py-2 text-center">{{ item.year || '—' }}</td>
              <td class="border border-slate-300 px-3 py-2 text-center">{{ item.percentage }}</td>
              <td class="border border-slate-300 px-3 py-2 text-right tabular-nums">
                {{ item.basic_value > 0 ? idr.format(item.basic_value) : '—' }}
              </td>
              <td class="border border-slate-300 px-3 py-2 text-right tabular-nums font-semibold"
                :class="item.zakah_value > 0 ? 'text-emerald-800' : 'text-slate-300'">
                {{ item.zakah_value > 0 ? idr.format(item.zakah_value) : '—' }}
              </td>
            </tr>
          </tbody>
          <tfoot>
            <tr class="bg-slate-100 font-bold">
              <td colspan="5" class="border border-slate-300 px-3 py-2 text-right text-sm uppercase tracking-wide">
                Jumlah Total Zakat
              </td>
              <td class="border border-slate-300 px-3 py-2 text-right tabular-nums text-emerald-800">
                {{ idr.format(totalZakat) }}
              </td>
            </tr>
          </tfoot>
        </table>
      </div>

      <!-- Transactions list -->
      <div v-if="bsz.transactions.length" class="mb-6">
        <h2 class="text-sm font-bold uppercase tracking-wide text-slate-700 mb-3">Transaksi yang Terhubung</h2>
        <table class="w-full text-xs border border-slate-300">
          <thead>
            <tr class="bg-slate-100">
              <th class="border border-slate-300 px-3 py-2 text-left font-semibold uppercase">No. Transaksi</th>
              <th class="border border-slate-300 px-3 py-2 text-left font-semibold uppercase">Tanggal</th>
              <th class="border border-slate-300 px-3 py-2 text-left font-semibold uppercase">Rekening</th>
              <th class="border border-slate-300 px-3 py-2 text-right font-semibold uppercase">Jumlah (Rp)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="t in bsz.transactions" :key="t.transaction_item_id">
              <td class="border border-slate-300 px-3 py-1.5 font-mono">{{ t.transaction_no }}</td>
              <td class="border border-slate-300 px-3 py-1.5">{{ dmy(t.transaction_date) }}</td>
              <td class="border border-slate-300 px-3 py-1.5">{{ t.account_name }}</td>
              <td class="border border-slate-300 px-3 py-1.5 text-right tabular-nums">{{ idr.format(t.amount) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Signature area -->
      <div class="mt-10 grid grid-cols-2 gap-8 text-sm text-center">
        <div>
          <p class="text-slate-500 mb-16">Muzakki,</p>
          <div class="border-t border-slate-400 pt-2">
            <p class="font-semibold">{{ bsz.donor_name }}</p>
          </div>
        </div>
        <div>
          <p class="text-slate-500 mb-16">Petugas BPZIS,</p>
          <div class="border-t border-slate-400 pt-2">
            <p class="font-semibold">___________________</p>
          </div>
        </div>
      </div>

      <!-- Footer note -->
      <div class="mt-8 text-xs text-slate-400 text-center border-t border-slate-200 pt-4">
        <p>Bukti Setor Zakat ini sah sebagai bukti pembayaran zakat resmi.</p>
        <p>{{ bsz.bsz_number }} | Dicetak: {{ dmy(new Date().toISOString()) }}</p>
      </div>
    </div>
  </div>
</template>

<style>
@media print {
  body { font-size: 12px; }
  @page { margin: 1.5cm; size: A4; }
}
</style>
