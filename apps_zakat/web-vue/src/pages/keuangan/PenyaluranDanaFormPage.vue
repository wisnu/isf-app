<script setup lang="ts">
import { onMounted, ref, shallowRef, computed } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import DateField from '@/components/ui/DateField.vue'
import SearchSelect from '@/components/ui/SearchSelect.vue'
import { api } from '@/lib/api/client'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/lib/useToast'

interface RekeningOption {
  account_no: string
  account_name: string
  cash_code: string | null
  product_id: number | null
  account_interface: string | null
}

interface ProductOption {
  product_id: number
  product_name: string
  fund_category: string
  account_no: string
  fund_entity: number
}

interface AshnafOption {
  code: string
  name: string
}

interface FundAccountOption {
  account_no: string
  account_name: string
}

interface ItemRow {
  _id: number
  product_id: number | null
  product_name: string
  account_no: string
  fund_entity: number
  ashnaf: string
  amount: number | null
  description: string
  dist_item_account: string | null
  distribution_category: string | null
}

const router = useRouter()
const toast = useToast()
const auth = useAuthStore()

// ── Form header ──────────────────────────────────────────────────────────────
const actualDate = shallowRef(new Date().toISOString().slice(0, 10))
const referenceNo = shallowRef('')
const description = shallowRef('')
const paidTo = shallowRef('')
const receivedFrom = shallowRef(auth.user?.username ?? '')
const paymentType = shallowRef<'B' | 'C' | 'K' | 'A'>('B')
const paymentAccountNo = shallowRef<string | null>(null)
const fundAccountNo = shallowRef<string | null>(null)
const productBranchCode = shallowRef('001')
const rate = shallowRef(1.0)
const currencyCode = shallowRef('IDR')

// ── Items ────────────────────────────────────────────────────────────────────
let _idCtr = 1
const items = ref<ItemRow[]>([])

const totalAmount = computed(() => items.value.reduce((s, i) => s + (i.amount ?? 0), 0))
const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

// ── Lookup data ───────────────────────────────────────────────────────────────
const rekeningOptions = ref<RekeningOption[]>([])
const productOptions = ref<ProductOption[]>([])
const ashnafOptions = ref<AshnafOption[]>([])
const fundAccountOptions = ref<FundAccountOption[]>([])

const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

const paymentTabs = [
  { v: 'B', label: 'Bank' },
  { v: 'C', label: 'Kas Cabang' },
  { v: 'K', label: 'Kas Kecil' },
  { v: 'A', label: 'Aset/GL' },
] as const

async function loadLookups() {
  const [ashnaf, products] = await Promise.all([
    api.get<AshnafOption[]>('/api/penyaluran/lookup/ashnaf').catch(() => []),
    api.get<ProductOption[]>('/api/penyaluran/lookup/produk').catch(() => []),
  ])
  ashnafOptions.value = ashnaf
  productOptions.value = products
}

async function loadRekening() {
  const typeMap: Record<string, string> = { B: 'bank', K: 'petty', C: 'cabang', A: 'bank' }
  const rows = await api
    .get<RekeningOption[]>(`/api/penyaluran/lookup/rekening?type=${typeMap[paymentType.value]}`)
    .catch(() => [])
  rekeningOptions.value = rows
}

async function onBankSelected(accountNo: string) {
  paymentAccountNo.value = accountNo || null
  fundAccountNo.value = null
  fundAccountOptions.value = []
  if (!accountNo) return
  const rows = await api
    .get<FundAccountOption[]>(`/api/penyaluran/lookup/fund-product-account?bank_account_no=${accountNo}`)
    .catch(() => [])
  fundAccountOptions.value = rows
  if (rows.length === 1) fundAccountNo.value = rows[0].account_no
}

function onPaymentTypeChange(type: 'B' | 'C' | 'K' | 'A') {
  paymentType.value = type
  paymentAccountNo.value = null
  fundAccountNo.value = null
  fundAccountOptions.value = []
  loadRekening()
}

function addItem() {
  items.value.push({
    _id: _idCtr++,
    product_id: null,
    product_name: '',
    account_no: '',
    fund_entity: 2,
    ashnaf: 'L',
    amount: null,
    description: '',
    dist_item_account: null,
    distribution_category: null,
  })
}

function removeItem(id: number) {
  items.value = items.value.filter((i) => i._id !== id)
}

function onProductSelected(item: ItemRow, productId: string | number) {
  const p = productOptions.value.find((x) => x.product_id === Number(productId))
  if (!p) return
  item.product_id = p.product_id
  item.product_name = p.product_name
  item.account_no = p.account_no
  item.fund_entity = p.fund_entity
  item.ashnaf = p.fund_entity === 1 ? '' : 'L'
  item.description = p.product_name
}

function validate(): string | null {
  if (!actualDate.value) return 'Tanggal transaksi wajib diisi'
  if (items.value.length === 0) return 'Minimal satu item distribusi harus diisi'
  for (const item of items.value) {
    if (!item.product_id) return 'Semua item harus memiliki produk yang dipilih'
    if (!item.amount || item.amount <= 0) return 'Jumlah item harus lebih dari 0'
    if (item.fund_entity === 1 && (!item.ashnaf || item.ashnaf === 'L'))
      return 'Ashnaf wajib diisi untuk produk Zakat'
  }
  if (paymentType.value !== 'C' && !paymentAccountNo.value)
    return 'Rekening pembayaran wajib dipilih'
  if (!fundAccountNo.value) return 'Sumber dana penghimpunan wajib dipilih'
  return null
}

async function submit() {
  const validErr = validate()
  if (validErr) {
    toast.error(validErr)
    return
  }
  loading.value = true
  errorMsg.value = null
  try {
    const payload = {
      actual_date: actualDate.value,
      reference_no: referenceNo.value || null,
      description: description.value,
      paid_to: paidTo.value || null,
      received_from: receivedFrom.value || null,
      payment_type: paymentType.value,
      payment_account_no: paymentAccountNo.value,
      rate: rate.value,
      currency_code: currencyCode.value,
      fund_account_no: fundAccountNo.value,
      product_branch_code: productBranchCode.value,
      items: items.value.map((i) => ({
        product_id: i.product_id,
        account_no: i.account_no,
        ashnaf: i.fund_entity === 1 ? i.ashnaf : 'L',
        amount: i.amount,
        description: i.description || description.value,
        fund_entity: i.fund_entity,
        dist_item_account: i.dist_item_account,
        distribution_category: i.distribution_category,
      })),
    }
    const result = await api.post<{ transaction_id: number; transaction_no: string }>(
      '/api/penyaluran/',
      payload,
    )
    toast.success(`Transaksi ${result.transaction_no} berhasil dibuat`)
    router.push({ name: 'keuangan-transaksi-penyaluran' })
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
    toast.error('Gagal menyimpan transaksi')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadLookups()
  loadRekening()
})
</script>

<template>
  <!-- 1080p: 2-panel layout — left sticky 420px, right flex-1 -->
  <div class="w-full pb-6">

    <!-- Page header -->
    <header class="mb-4 flex items-center justify-between">
      <h1 class="text-2xl font-bold tracking-tight">Input Penyaluran Dana</h1>
      <Button variant="ghost" :disabled="loading" @click="router.back()">Kembali</Button>
    </header>

    <Alert v-if="errorMsg" variant="destructive" class="mb-4">{{ errorMsg }}</Alert>

    <!-- 2-panel body -->
    <div class="flex w-full flex-col gap-5 xl:flex-row xl:items-start">

      <!-- ── LEFT PANEL: sticky header + payment ────────────────────────── -->
      <div class="flex w-full shrink-0 flex-col gap-4 xl:w-[420px] xl:sticky xl:top-4">

        <!-- Informasi Transaksi -->
        <section class="space-y-3 rounded border bg-white p-5 dark:bg-zinc-900">
          <h2 class="text-sm font-semibold uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
            Informasi Transaksi
          </h2>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="mb-1 block text-sm font-medium">
                Tanggal <span class="text-red-500">*</span>
              </label>
              <DateField v-model="actualDate" />
            </div>
            <div>
              <label class="mb-1 block text-sm font-medium">No. Referensi</label>
              <input
                v-model="referenceNo"
                placeholder="Opsional"
                class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
              />
            </div>
            <div class="col-span-2">
              <label class="mb-1 block text-sm font-medium">
                Keterangan <span class="text-red-500">*</span>
              </label>
              <input
                v-model="description"
                placeholder="Keterangan transaksi"
                class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
              />
            </div>
            <div>
              <label class="mb-1 block text-sm font-medium">Dibayarkan Kepada</label>
              <input
                v-model="paidTo"
                class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
              />
            </div>
            <div>
              <label class="mb-1 block text-sm font-medium">Diterima Dari</label>
              <input
                v-model="receivedFrom"
                class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
              />
            </div>
          </div>
        </section>

        <!-- Jenis Pembayaran -->
        <section class="space-y-3 rounded border bg-white p-5 dark:bg-zinc-900">
          <h2 class="text-sm font-semibold uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
            Jenis Pembayaran
          </h2>
          <!-- Tabs -->
          <div class="flex gap-1.5">
            <button
              v-for="tab in paymentTabs"
              :key="tab.v"
              :class="[
                'flex-1 rounded border py-1.5 text-xs font-medium transition',
                paymentType === tab.v
                  ? 'border-primary bg-primary text-white'
                  : 'border-zinc-200 hover:bg-zinc-50 dark:border-zinc-700 dark:hover:bg-zinc-800',
              ]"
              @click="onPaymentTypeChange(tab.v)"
            >{{ tab.label }}</button>
          </div>

          <div class="space-y-3">
            <!-- Rekening Bank / Kas Kecil -->
            <div v-if="paymentType !== 'C' && paymentType !== 'A'">
              <label class="mb-1 block text-sm font-medium">
                {{ paymentType === 'B' ? 'Rekening Bank' : 'Rekening Kas Kecil' }}
                <span class="text-red-500">*</span>
              </label>
              <SearchSelect
                :options="rekeningOptions.map((r) => ({ value: r.account_no, label: `${r.account_name} (${r.account_no})` }))"
                :model-value="paymentAccountNo ?? ''"
                placeholder="Pilih rekening..."
                @update:model-value="onBankSelected($event as string)"
              />
            </div>
            <!-- Aset / GL -->
            <div v-if="paymentType === 'A'">
              <label class="mb-1 block text-sm font-medium">Kode Aset <span class="text-red-500">*</span></label>
              <input
                :value="paymentAccountNo ?? ''"
                placeholder="Kode akun GL aset"
                class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
                @input="paymentAccountNo = ($event.target as HTMLInputElement).value"
              />
            </div>
            <!-- Kas Cabang -->
            <div v-if="paymentType === 'C'" class="rounded border border-dashed p-3 text-xs text-zinc-500">
              Kas cabang dipilih otomatis berdasarkan cabang pengguna.
            </div>

            <!-- Sumber Dana -->
            <div>
              <label class="mb-1 block text-sm font-medium">
                Sumber Dana <span class="text-red-500">*</span>
              </label>
              <SearchSelect
                :options="fundAccountOptions.map((f) => ({ value: f.account_no, label: `${f.account_name} (${f.account_no})` }))"
                :model-value="fundAccountNo ?? ''"
                placeholder="Pilih sumber dana..."
                @update:model-value="fundAccountNo = $event as string || null"
              />
              <p v-if="paymentType === 'B' && !paymentAccountNo" class="mt-1 text-xs text-zinc-400">
                Pilih rekening bank terlebih dahulu.
              </p>
            </div>

            <!-- Cabang Produk -->
            <div>
              <label class="mb-1 block text-sm font-medium">Cabang Produk</label>
              <input
                v-model="productBranchCode"
                class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
              />
            </div>
          </div>
        </section>

        <!-- Action buttons (kiri bawah) -->
        <div class="flex gap-3">
          <Button variant="ghost" class="flex-1" :disabled="loading" @click="router.back()">Batal</Button>
          <Button class="flex-1" :disabled="loading || items.length === 0" @click="submit">
            {{ loading ? 'Menyimpan...' : 'Simpan Transaksi' }}
          </Button>
        </div>
      </div>

      <!-- ── RIGHT PANEL: Detail Distribusi (scrollable) ────────────────── -->
      <div class="flex-1 min-w-0">
        <section class="rounded border bg-white dark:bg-zinc-900">
          <!-- Header distribusi -->
          <div class="flex items-center justify-between border-b px-5 py-3">
            <div>
              <h2 class="font-semibold text-zinc-700 dark:text-zinc-300">Detail Distribusi</h2>
              <p class="text-xs text-zinc-400">{{ items.length }} item · Total:
                <span class="font-semibold text-zinc-700 dark:text-zinc-200">Rp {{ fmt(totalAmount) }}</span>
              </p>
            </div>
            <Button variant="secondary" size="sm" @click="addItem">+ Tambah Item</Button>
          </div>

          <!-- Empty state -->
          <div
            v-if="items.length === 0"
            class="py-16 text-center text-sm text-zinc-400"
          >
            Klik "+ Tambah Item" untuk menambah produk penyaluran.
          </div>

          <!-- Items table -->
          <div v-if="items.length > 0" class="divide-y">
            <!-- Table header -->
            <div class="grid grid-cols-[2fr_1fr_1fr_2fr_1.5fr_auto] gap-3 bg-zinc-50 px-5 py-2 text-xs font-semibold uppercase text-zinc-500 dark:bg-zinc-800">
              <span>Produk <span class="text-red-400">*</span></span>
              <span>Ashnaf</span>
              <span>Jumlah (Rp) <span class="text-red-400">*</span></span>
              <span>Keterangan</span>
              <span>Kode Anggaran</span>
              <span></span>
            </div>

            <!-- Item rows -->
            <div
              v-for="item in items"
              :key="item._id"
              class="grid grid-cols-[2fr_1fr_1fr_2fr_1.5fr_auto] gap-3 px-5 py-3 items-start hover:bg-zinc-50/50 dark:hover:bg-zinc-800/30"
            >
              <!-- Produk -->
              <div>
                <SearchSelect
                  :options="productOptions.map((p) => ({ value: p.product_id, label: `[${p.fund_category}] ${p.product_name}` }))"
                  :model-value="item.product_id ?? ''"
                  placeholder="Pilih produk..."
                  @update:model-value="onProductSelected(item, $event as string)"
                />
              </div>

              <!-- Ashnaf (hanya untuk Zakat) -->
              <div>
                <select
                  v-if="item.fund_entity === 1"
                  v-model="item.ashnaf"
                  class="h-9 w-full rounded border px-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
                >
                  <option value="">-- Pilih --</option>
                  <option v-for="a in ashnafOptions" :key="a.code" :value="a.code">{{ a.name }}</option>
                </select>
                <span v-else class="flex h-9 items-center text-xs text-zinc-400">—</span>
              </div>

              <!-- Jumlah -->
              <div>
                <input
                  v-model.number="item.amount"
                  type="number"
                  min="1"
                  placeholder="0"
                  class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
                />
              </div>

              <!-- Keterangan -->
              <div>
                <input
                  v-model="item.description"
                  placeholder="Opsional"
                  class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
                />
              </div>

              <!-- Kode Anggaran -->
              <div>
                <input
                  v-model="item.dist_item_account"
                  placeholder="Opsional"
                  class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
                />
              </div>

              <!-- Hapus -->
              <div class="flex h-9 items-center">
                <button
                  class="rounded p-1 text-zinc-400 hover:text-red-500"
                  title="Hapus item"
                  @click="removeItem(item._id)"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4h6v2"/></svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Hint: selalu tampil saat ada items -->
          <div
            v-if="items.length > 0"
            class="border-t px-5 py-2.5 text-xs italic text-zinc-400 dark:text-zinc-500"
          >
            Klik "+ Tambah Item" untuk menambah produk penyaluran.
          </div>

          <!-- Footer total -->
          <div v-if="items.length > 0" class="flex items-center justify-end gap-3 border-t bg-zinc-50 px-5 py-3 dark:bg-zinc-800">
            <span class="text-sm text-zinc-500">Total Penyaluran:</span>
            <span class="text-xl font-bold text-zinc-800 dark:text-zinc-100">Rp {{ fmt(totalAmount) }}</span>
          </div>
        </section>
      </div>

    </div>
  </div>
</template>
