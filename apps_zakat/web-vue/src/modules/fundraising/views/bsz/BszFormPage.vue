<script setup lang="ts">
import { ArrowLeft, Search, RefreshCw, Save, Info } from 'lucide-vue-next'
import { computed, reactive, ref, shallowRef } from 'vue'
import { useRouter } from 'vue-router'

import Button from '@/shared/components/Button.vue'
import DateField from '@/shared/components/DateField.vue'
import PageHeader from '@/shared/components/PageHeader.vue'
import { api, ApiError } from '@/shared/api/client'
import { dmy } from '@/shared/utils/date'
import { useToast } from '@/shared/composables/useToast'

interface DonorOption {
  donor_id: number
  donor_no: string
  donor_name: string
}

interface ZakatObject {
  id: number
  code: string
  name: string
}

interface AvailableTransaction {
  transaction_item_id: number
  transaction_no: string
  transaction_date: string
  amount: number
  account_name: string
  description: string | null
  zakah_object: string
}

interface DetailItem {
  item: number
  zakat_object: string
  year: number
  percentage: number
  basic_value: number
  zakah_value: number
}

const router = useRouter()
const toast = useToast()

const idr = new Intl.NumberFormat('id-ID')
const fmtRp = (n: number) => 'Rp ' + idr.format(n)

// ── Donor selection ──────────────────────────────────────────────────────────
const donorSearch = shallowRef('')
const donorOptions = ref<DonorOption[]>([])
const selectedDonor = ref<DonorOption | null>(null)

async function searchDonors() {
  if (donorSearch.value.length < 2) { donorOptions.value = []; return }
  donorOptions.value = await api.get<DonorOption[]>(`/api/fundraising/bsz/lookup/donor?q=${encodeURIComponent(donorSearch.value)}`).catch(() => [])
}

function selectDonor(d: DonorOption) {
  selectedDonor.value = d
  donorOptions.value = []
  donorSearch.value = ''
  transactions.value = []
  detailItems.value = []
}

function clearDonor() {
  selectedDonor.value = null
  transactions.value = []
  detailItems.value = []
}

// ── Period ───────────────────────────────────────────────────────────────────
const periodBegin = shallowRef('')
const periodEnd = shallowRef('')

// ── Zakat objects ─────────────────────────────────────────────────────────────
const zakatObjects = ref<ZakatObject[]>([])

async function loadZakatObjects() {
  zakatObjects.value = await api.get<ZakatObject[]>('/api/fundraising/bsz/zakat-objects').catch(() => [])
}
loadZakatObjects()

// ── Transactions ─────────────────────────────────────────────────────────────
const transactions = ref<AvailableTransaction[]>([])
const transLoading = shallowRef(false)

async function loadTransactions() {
  if (!selectedDonor.value || !periodBegin.value || !periodEnd.value) {
    toast.warning('Pilih donatur dan periode terlebih dahulu')
    return
  }
  transLoading.value = true
  try {
    const rows = await api.get<AvailableTransaction[]>(
      `/api/fundraising/bsz/available-transactions?donor_id=${selectedDonor.value.donor_id}&begin_date=${periodBegin.value}&end_date=${periodEnd.value}`
    )
    transactions.value = rows
    buildDetailItems()
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal memuat transaksi')
  } finally {
    transLoading.value = false
  }
}

// ── Detail items (7 zakat objects) ───────────────────────────────────────────
const detailItems = ref<DetailItem[]>([])

function buildDetailItems() {
  const year = periodEnd.value ? parseInt(periodEnd.value.substring(0, 4)) : new Date().getFullYear()

  // Group transactions by zakah_object
  const amountByObj: Record<string, number> = {}
  for (const t of transactions.value) {
    const key = t.zakah_object || '1'
    amountByObj[key] = (amountByObj[key] || 0) + t.amount
  }

  detailItems.value = zakatObjects.value.map(zo => {
    const zakah_value = amountByObj[zo.code] || 0
    const percentage = 2.5
    const basic_value = zakah_value > 0 ? Math.round(zakah_value / (percentage / 100)) : 0
    return {
      item: zo.id,
      zakat_object: zo.name,
      year,
      percentage,
      basic_value,
      zakah_value,
    }
  })
}

// ── Transaction zakah_object assignment ──────────────────────────────────────
function updateTransactionZakahObject(tran: AvailableTransaction, newObj: string) {
  tran.zakah_object = newObj
  buildDetailItems()
}

// ── Totals ───────────────────────────────────────────────────────────────────
const totalTransactions = computed(() => transactions.value.reduce((s, t) => s + t.amount, 0))
const totalDetail = computed(() => detailItems.value.reduce((s, d) => s + d.zakah_value, 0))
const totalMatch = computed(() => Math.abs(totalTransactions.value - totalDetail.value) < 0.01)

// ── Save ─────────────────────────────────────────────────────────────────────
const saving = shallowRef(false)

async function save() {
  if (!selectedDonor.value) { toast.error('Donatur belum dipilih'); return }
  if (!periodBegin.value || !periodEnd.value) { toast.error('Periode belum diisi'); return }
  if (!transactions.value.length) { toast.error('Belum ada transaksi yang dimuat'); return }
  if (!totalMatch.value) { toast.error('Total detail tidak sama dengan total transaksi'); return }

  saving.value = true
  try {
    const body = {
      donor_id: selectedDonor.value.donor_id,
      period_begin: periodBegin.value,
      period_end: periodEnd.value,
      items: detailItems.value.filter(d => d.zakah_value > 0).map(d => ({
        item: d.item,
        year: d.year,
        percentage: d.percentage,
        basic_value: d.basic_value,
        zakah_value: d.zakah_value,
      })),
      transactions: transactions.value.map(t => ({
        transaction_item_id: t.transaction_item_id,
        zakah_object: t.zakah_object,
      })),
    }
    const result = await api.post<{ data: { bsz_id: number; bsz_number: string } }>('/api/fundraising/bsz', body)
    toast.success(`BSZ ${result.data.bsz_number} berhasil dibuat`)
    router.push({ name: 'fundraising-bsz-print', params: { id: result.data.bsz_id } })
  } catch (e) {
    toast.error(e instanceof ApiError ? e.message : 'Gagal menyimpan BSZ')
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="flex flex-col gap-4">
    <PageHeader title="Buat Bukti Setor Zakat" subtitle="Isi form untuk membuat BSZ baru">
      <template #actions>
        <Button variant="secondary" @click="router.push({ name: 'fundraising-bsz-list' })">
          <ArrowLeft class="w-4 h-4 mr-1" /> Kembali
        </Button>
      </template>
    </PageHeader>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
      <!-- Left: Form input -->
      <div class="lg:col-span-1 space-y-4">
        <!-- Card: Donor -->
        <div class="rounded-lg border border-slate-200 bg-white shadow-sm">
          <div class="border-b border-slate-100 px-4 py-3">
            <h3 class="text-sm font-semibold text-slate-700">Data Muzakki</h3>
          </div>
          <div class="p-4 space-y-3">
            <!-- Donor selected -->
            <div v-if="selectedDonor" class="rounded-lg bg-indigo-50 border border-indigo-200 p-3">
              <p class="font-semibold text-indigo-800">{{ selectedDonor.donor_name }}</p>
              <p class="text-xs text-indigo-600 mt-0.5">{{ selectedDonor.donor_no }}</p>
              <button class="mt-2 text-xs text-slate-500 hover:text-red-500" @click="clearDonor">Ganti donatur</button>
            </div>

            <!-- Donor search -->
            <div v-else>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Cari Donatur</label>
              <div class="relative">
                <input
                  v-model="donorSearch"
                  placeholder="Ketik nama atau no. donatur..."
                  class="w-full rounded border border-slate-200 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 pr-8"
                  @input="searchDonors"
                />
                <Search class="absolute right-2 top-1.5 w-4 h-4 text-slate-400" />
                <div v-if="donorOptions.length" class="absolute z-20 mt-1 w-full rounded border border-slate-200 bg-white shadow-lg max-h-48 overflow-y-auto">
                  <button
                    v-for="d in donorOptions"
                    :key="d.donor_id"
                    class="w-full text-left px-3 py-2 text-sm hover:bg-indigo-50"
                    @click="selectDonor(d)"
                  >
                    <span class="font-medium">{{ d.donor_name }}</span>
                    <span class="ml-2 text-xs text-slate-500">{{ d.donor_no }}</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Card: Periode -->
        <div class="rounded-lg border border-slate-200 bg-white shadow-sm">
          <div class="border-b border-slate-100 px-4 py-3">
            <h3 class="text-sm font-semibold text-slate-700">Periode Setoran</h3>
          </div>
          <div class="p-4 space-y-3">
            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Dari Tanggal</label>
              <DateField v-model="periodBegin" />
            </div>
            <div>
              <label class="mb-1 block text-xs font-semibold text-slate-500 uppercase tracking-wide">Sampai Tanggal</label>
              <DateField v-model="periodEnd" />
            </div>
            <Button
              variant="secondary"
              class="w-full"
              :loading="transLoading"
              :disabled="!selectedDonor || !periodBegin || !periodEnd"
              @click="loadTransactions"
            >
              <RefreshCw class="w-4 h-4 mr-1" />
              Muat Transaksi
            </Button>
          </div>
        </div>

        <!-- Summary card -->
        <div v-if="transactions.length" class="rounded-lg border bg-white shadow-sm"
          :class="totalMatch ? 'border-emerald-200' : 'border-amber-200'">
          <div class="border-b px-4 py-3" :class="totalMatch ? 'border-emerald-100' : 'border-amber-100'">
            <h3 class="text-sm font-semibold text-slate-700">Ringkasan</h3>
          </div>
          <div class="p-4 space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="text-slate-500">Total Transaksi</span>
              <span class="font-semibold">{{ fmtRp(totalTransactions) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-slate-500">Total Detail</span>
              <span class="font-semibold">{{ fmtRp(totalDetail) }}</span>
            </div>
            <div v-if="!totalMatch" class="flex items-center gap-1 text-amber-600 text-xs mt-1">
              <Info class="w-3.5 h-3.5" />
              Total tidak sesuai
            </div>
          </div>
          <div class="p-4 pt-0">
            <Button
              variant="primary"
              class="w-full"
              :loading="saving"
              :disabled="!totalMatch || !transactions.length"
              @click="save"
            >
              <Save class="w-4 h-4 mr-1" /> Simpan BSZ
            </Button>
          </div>
        </div>
      </div>

      <!-- Right: Transactions + Detail -->
      <div class="lg:col-span-2 space-y-4">
        <!-- Transactions table -->
        <div class="rounded-lg border border-slate-200 bg-white shadow-sm overflow-hidden">
          <div class="border-b border-slate-100 px-4 py-3 flex items-center justify-between">
            <h3 class="text-sm font-semibold text-slate-700">
              Daftar Transaksi
              <span v-if="transactions.length" class="ml-2 text-xs font-normal text-slate-500">({{ transactions.length }} item)</span>
            </h3>
          </div>

          <div v-if="!transactions.length" class="p-8 text-center text-slate-400 text-sm">
            Pilih donatur dan periode, lalu klik <strong>Muat Transaksi</strong>
          </div>

          <div v-else class="overflow-x-auto">
            <table class="w-full text-xs">
              <thead class="bg-slate-50 text-slate-500 uppercase tracking-wide font-semibold">
                <tr>
                  <th class="px-3 py-2 text-left">No. Transaksi</th>
                  <th class="px-3 py-2 text-left">Tanggal</th>
                  <th class="px-3 py-2 text-left">Rekening</th>
                  <th class="px-3 py-2 text-right">Jumlah</th>
                  <th class="px-3 py-2 text-left">Objek Zakat</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="t in transactions" :key="t.transaction_item_id" class="hover:bg-slate-50">
                  <td class="px-3 py-2 font-mono text-indigo-700">{{ t.transaction_no }}</td>
                  <td class="px-3 py-2">{{ dmy(t.transaction_date) }}</td>
                  <td class="px-3 py-2 text-slate-600 truncate max-w-[140px]" :title="t.account_name">{{ t.account_name }}</td>
                  <td class="px-3 py-2 text-right tabular-nums font-semibold">{{ fmtRp(t.amount) }}</td>
                  <td class="px-3 py-2">
                    <select
                      :value="t.zakah_object"
                      class="rounded border border-slate-200 px-2 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500"
                      @change="updateTransactionZakahObject(t, ($event.target as HTMLSelectElement).value)"
                    >
                      <option v-for="zo in zakatObjects" :key="zo.code" :value="zo.code">
                        {{ zo.id }}. {{ zo.name }}
                      </option>
                    </select>
                  </td>
                </tr>
              </tbody>
              <tfoot class="bg-slate-50 font-semibold text-xs">
                <tr>
                  <td colspan="3" class="px-3 py-2 text-right text-slate-500">Total Transaksi</td>
                  <td class="px-3 py-2 text-right tabular-nums">{{ fmtRp(totalTransactions) }}</td>
                  <td></td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>

        <!-- Detail items (7 zakat objects) -->
        <div v-if="detailItems.length" class="rounded-lg border border-slate-200 bg-white shadow-sm overflow-hidden">
          <div class="border-b border-slate-100 px-4 py-3">
            <h3 class="text-sm font-semibold text-slate-700">Rincian Objek Zakat</h3>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-xs">
              <thead class="bg-slate-50 text-slate-500 uppercase tracking-wide font-semibold">
                <tr>
                  <th class="px-3 py-2 text-left">No.</th>
                  <th class="px-3 py-2 text-left">Objek Zakat</th>
                  <th class="px-3 py-2 text-center">Tahun</th>
                  <th class="px-3 py-2 text-center">Kadar (%)</th>
                  <th class="px-3 py-2 text-right">Dasar Pengenaan</th>
                  <th class="px-3 py-2 text-right">Jumlah Zakat</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr v-for="d in detailItems" :key="d.item" class="hover:bg-slate-50">
                  <td class="px-3 py-2 text-slate-500">{{ d.item }}</td>
                  <td class="px-3 py-2">{{ d.zakat_object }}</td>
                  <td class="px-3 py-2 text-center">
                    <input
                      v-model.number="d.year"
                      type="number"
                      min="2000"
                      max="2099"
                      class="w-16 rounded border border-slate-200 px-2 py-0.5 text-center text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500"
                    />
                  </td>
                  <td class="px-3 py-2 text-center">{{ d.percentage }}</td>
                  <td class="px-3 py-2 text-right tabular-nums">{{ fmtRp(d.basic_value) }}</td>
                  <td class="px-3 py-2 text-right tabular-nums font-semibold"
                    :class="d.zakah_value > 0 ? 'text-emerald-700' : 'text-slate-300'">
                    {{ fmtRp(d.zakah_value) }}
                  </td>
                </tr>
              </tbody>
              <tfoot class="bg-slate-50 font-semibold text-xs">
                <tr>
                  <td colspan="5" class="px-3 py-2 text-right text-slate-500">Total</td>
                  <td class="px-3 py-2 text-right tabular-nums" :class="totalMatch ? 'text-emerald-700' : 'text-red-600'">
                    {{ fmtRp(totalDetail) }}
                  </td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
