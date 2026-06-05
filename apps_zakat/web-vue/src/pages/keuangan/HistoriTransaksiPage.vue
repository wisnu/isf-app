<script setup lang="ts">
import { Download, History, Search } from 'lucide-vue-next'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import { BASE_URL } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useAuthStore } from '@/stores/auth'

interface TransaksiRow {
  transactionid: number
  transactionno: string | null
  transactiondate: string
  actualdate: string
  amount: number
  donorno: string | null
  donorname: string | null
  referenceno: string | null
  description: string | null
  inputer: string | null
  authstatus: string | null
  isposted: string | null
  authoperationmode: string | null
  branchcode: string | null
  channelname: string | null
  exttransactionid: number | null
}

const router = useRouter()
const auth = useAuthStore()
const today = new Date().toISOString().slice(0, 10)
const begin = ref(today)
const end = ref(today)
const dateType = ref('actual')
const sortBy = ref('actual_date')
const searchCategory = ref('none')
const searchText = ref('')
const cashAccountNo = ref('')
const limitRows = ref(50)

const rows = ref<TransaksiRow[]>([])
const loading = ref(false)
const exporting = ref(false)
const errorMsg = ref<string | null>(null)
const hasLoaded = ref(false)

const deleteConfirmId = ref<number | null>(null)
const deleteMsg = ref<string | null>(null)
const deleting = ref(false)

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

function canDelete(row: TransaksiRow): boolean {
  if (row.exttransactionid != null) return false
  if (row.authstatus === 'F' && row.authoperationmode === 'D') return false
  return true
}

function authChip(s: string | null) {
  return s === 'T' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
}
function authLabel(s: string | null) {
  return s === 'T' ? 'Terotorisasi' : 'Pending'
}
function postedChip(s: string | null) {
  return s === 'T' ? 'bg-blue-100 text-blue-800' : 'bg-gray-100 text-gray-600'
}

function buildParams(extra: Record<string, string> = {}): string {
  const p = new URLSearchParams({
    begin: begin.value, end: end.value,
    date_type: dateType.value, sort_by: sortBy.value,
    search_category: searchCategory.value,
    limit: String(limitRows.value),
    ...extra,
  })
  if (searchCategory.value !== 'none' && searchText.value)
    p.set('search_text', searchText.value)
  if (cashAccountNo.value)
    p.set('cash_account_no', cashAccountNo.value)
  return p.toString()
}

async function load() {
  loading.value = true
  errorMsg.value = null
  try {
    const res = await fetch(`${BASE_URL}/api/transaksi-histori/search?${buildParams()}`, {
      credentials: 'include',
    })
    const payload = await res.json()
    if (!res.ok) throw new Error(payload?.error?.message ?? 'Gagal memuat data')
    rows.value = payload.data
    hasLoaded.value = true
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
  } finally {
    loading.value = false
  }
}

async function exportXlsx() {
  exporting.value = true
  try {
    const res = await fetch(
      `${BASE_URL}/api/transaksi-histori/search/export.xlsx?${buildParams()}`,
      { credentials: 'include' },
    )
    if (!res.ok) throw new Error('Export gagal')
    const disp = res.headers.get('Content-Disposition') ?? ''
    const match = /filename\s*=\s*"?([^";]+)"?/i.exec(disp)
    const filename = match?.[1] ?? `histori-transaksi-${begin.value}-${end.value}.xlsx`
    const blob = await res.blob()
    const a = document.createElement('a')
    a.href = URL.createObjectURL(blob)
    a.download = filename
    a.click()
    setTimeout(() => URL.revokeObjectURL(a.href), 1000)
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
  } finally {
    exporting.value = false
  }
}

async function confirmDelete() {
  if (!deleteConfirmId.value) return
  deleting.value = true
  deleteMsg.value = null
  try {
    const res = await fetch(
      `${BASE_URL}/api/transaksi-histori/transactions/${deleteConfirmId.value}/delete`,
      {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: '{}',
      },
    )
    const payload = await res.json()
    if (!res.ok) throw new Error(payload?.error?.message ?? 'Hapus gagal')
    const result = payload.data
    deleteConfirmId.value = null
    if (result.deleted) {
      rows.value = rows.value.filter((r) => r.transactionid !== deleteConfirmId.value)
      await load()
    } else {
      await load()
    }
  } catch (e: unknown) {
    deleteMsg.value = e instanceof Error ? e.message : String(e)
  } finally {
    deleting.value = false
  }
}
</script>

<template>
  <div class="p-6">
    <div class="mb-4 flex items-center gap-3">
      <History class="h-5 w-5 text-primary" />
      <h1 class="text-lg font-semibold">Histori Transaksi</h1>
    </div>

    <!-- Filter bar -->
    <div class="mb-4 flex flex-wrap items-end gap-3">
      <div class="flex flex-col gap-1">
        <label class="text-xs text-muted">Dari</label>
        <DateField v-model="begin" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs text-muted">Sampai</label>
        <DateField v-model="end" />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs text-muted">Tipe Tanggal</label>
        <select v-model="dateType" class="rounded border border-border bg-background px-2 py-1.5 text-sm">
          <option value="actual">Aktual</option>
          <option value="transaction">Transaksi</option>
        </select>
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs text-muted">Urut</label>
        <select v-model="sortBy" class="rounded border border-border bg-background px-2 py-1.5 text-sm">
          <option value="actual_date">Tgl Aktual</option>
          <option value="transaction_date">Tgl Transaksi</option>
          <option value="transaction_no">No Transaksi</option>
          <option value="donor_no">No Donatur</option>
          <option value="donor_name">Nama Donatur</option>
          <option value="channel_name">Rekening</option>
        </select>
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs text-muted">Cari</label>
        <div class="flex gap-1">
          <select v-model="searchCategory" class="rounded border border-border bg-background px-2 py-1.5 text-sm">
            <option value="none">(Semua)</option>
            <option value="transno">No Transaksi</option>
            <option value="donorno">No Donatur</option>
            <option value="donorname">Nama Donatur</option>
            <option value="description">Keterangan</option>
            <option value="refno">No Referensi</option>
          </select>
          <input
            v-model="searchText"
            :disabled="searchCategory === 'none'"
            placeholder="Teks cari..."
            class="rounded border border-border bg-background px-2 py-1.5 text-sm w-36 disabled:opacity-50"
          />
        </div>
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs text-muted">Rekening</label>
        <input
          v-model="cashAccountNo"
          placeholder="Opsional"
          class="rounded border border-border bg-background px-2 py-1.5 text-sm w-28"
        />
      </div>
      <div class="flex flex-col gap-1">
        <label class="text-xs text-muted">Max Baris</label>
        <input
          v-model.number="limitRows"
          type="number"
          min="1"
          max="500"
          class="rounded border border-border bg-background px-2 py-1.5 text-sm w-20"
        />
      </div>
      <Button :disabled="loading" @click="load">
        <Search class="mr-1 h-3.5 w-3.5" />
        {{ loading ? 'Memuat...' : 'Tampilkan' }}
      </Button>
      <Button
        v-if="hasLoaded && rows.length"
        variant="outline"
        :disabled="exporting"
        @click="exportXlsx"
      >
        <Download class="mr-1 h-3.5 w-3.5" />
        {{ exporting ? 'Mengekspor...' : 'Export XLSX' }}
      </Button>
    </div>

    <Alert v-if="errorMsg" variant="error" :message="errorMsg" class="mb-3" />

    <div v-if="hasLoaded" class="overflow-x-auto rounded-lg border border-border">
      <table v-if="rows.length" class="w-full text-xs">
        <thead class="bg-surface">
          <tr>
            <th class="px-2 py-1.5 text-left">No</th>
            <th class="px-2 py-1.5 text-left">No Transaksi</th>
            <th class="px-2 py-1.5 text-left">Rekening</th>
            <th class="px-2 py-1.5 text-left whitespace-nowrap">Tgl Aktual</th>
            <th class="px-2 py-1.5 text-left whitespace-nowrap">Tgl Transaksi</th>
            <th class="px-2 py-1.5 text-right">Nominal</th>
            <th class="px-2 py-1.5 text-left">No Donatur</th>
            <th class="px-2 py-1.5 text-left min-w-[120px]">Nama Donatur</th>
            <th class="px-2 py-1.5 text-left">No Ref</th>
            <th class="px-2 py-1.5 text-left min-w-[140px]">Keterangan</th>
            <th class="px-2 py-1.5 text-left">Inputer</th>
            <th class="px-2 py-1.5 text-left">Status</th>
            <th class="px-2 py-1.5 text-left">Posted</th>
            <th class="px-2 py-1.5 text-left">Cabang</th>
            <th class="px-2 py-1.5 text-left">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(row, i) in rows"
            :key="row.transactionid"
            class="border-t border-border hover:bg-background cursor-pointer"
            @click="router.push(`/keuangan/transaksi/histori/${row.transactionid}`)"
          >
            <td class="px-2 py-1 text-center">{{ i + 1 }}</td>
            <td class="px-2 py-1 font-mono text-[10px]">{{ row.transactionno ?? '—' }}</td>
            <td class="px-2 py-1 max-w-[100px] truncate" :title="row.channelname ?? ''">
              {{ row.channelname ?? row.transactionno }}
            </td>
            <td class="px-2 py-1 whitespace-nowrap">{{ dmy(row.actualdate) }}</td>
            <td class="px-2 py-1 whitespace-nowrap">{{ dmy(row.transactiondate) }}</td>
            <td class="px-2 py-1 text-right">{{ fmt(row.amount) }}</td>
            <td class="px-2 py-1">{{ row.donorno ?? '' }}</td>
            <td class="px-2 py-1 max-w-[140px] truncate" :title="row.donorname ?? ''">
              {{ row.donorname ?? '' }}
            </td>
            <td class="px-2 py-1">{{ row.referenceno ?? '' }}</td>
            <td class="px-2 py-1 max-w-[160px] truncate" :title="row.description ?? ''">
              {{ row.description ?? '' }}
            </td>
            <td class="px-2 py-1">{{ row.inputer ?? '' }}</td>
            <td class="px-2 py-1">
              <span :class="['rounded px-1 py-0.5 text-[9px] font-medium uppercase', authChip(row.authstatus)]">
                {{ authLabel(row.authstatus) }}
              </span>
            </td>
            <td class="px-2 py-1">
              <span :class="['rounded px-1 py-0.5 text-[9px] font-medium', postedChip(row.isposted)]">
                {{ row.isposted === 'T' ? 'Posted' : 'Belum' }}
              </span>
            </td>
            <td class="px-2 py-1">{{ row.branchcode ?? '' }}</td>
            <td class="px-2 py-1" @click.stop>
              <Button
                v-if="canDelete(row)"
                size="sm"
                variant="outline"
                class="text-red-600 hover:bg-red-50 border-red-200 text-[10px] px-1.5 py-0.5"
                @click="deleteConfirmId = row.transactionid; deleteMsg = null"
              >Hapus</Button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="p-6 text-center text-sm text-muted">Tidak ada transaksi ditemukan.</div>
    </div>
    <div v-else-if="!loading" class="text-sm text-muted">Klik "Tampilkan" untuk memuat data.</div>

    <!-- Delete confirm dialog -->
    <div
      v-if="deleteConfirmId !== null"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
    >
      <div class="mx-4 w-full max-w-sm rounded-xl bg-white p-6 shadow-xl">
        <h2 class="mb-2 font-semibold">Konfirmasi Hapus Transaksi</h2>
        <p class="mb-4 text-sm text-muted">
          Transaksi #{{ deleteConfirmId }} akan dihapus. Jika sudah terotorisasi, akan masuk antrean
          approval supervisor. Lanjutkan?
        </p>
        <Alert v-if="deleteMsg" variant="error" :message="deleteMsg" class="mb-3" />
        <div class="flex justify-end gap-3">
          <Button variant="outline" :disabled="deleting" @click="deleteConfirmId = null">Batal</Button>
          <Button
            class="bg-red-600 hover:bg-red-700 text-white"
            :disabled="deleting"
            @click="confirmDelete"
          >
            {{ deleting ? 'Memproses...' : 'Ya, Hapus' }}
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>
