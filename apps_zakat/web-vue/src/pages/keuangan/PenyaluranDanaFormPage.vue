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
  <div class="mx-auto max-w-4xl space-y-6 pb-10">
    <header class="flex items-center justify-between">
      <h1 class="text-2xl font-bold tracking-tight">Input Penyaluran Dana</h1>
      <Button variant="ghost" :disabled="loading" @click="router.back()">Kembali</Button>
    </header>

    <Alert v-if="errorMsg" variant="destructive">{{ errorMsg }}</Alert>

    <!-- Header Form -->
    <section class="space-y-4 rounded border bg-white p-6 dark:bg-zinc-900">
      <h2 class="font-semibold text-zinc-700 dark:text-zinc-300">Informasi Transaksi</h2>
      <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
        <div>
          <label class="mb-1 block text-sm font-medium">
            Tanggal Transaksi <span class="text-red-500">*</span>
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
        <div class="md:col-span-2">
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
    <section class="space-y-4 rounded border bg-white p-6 dark:bg-zinc-900">
      <h2 class="font-semibold text-zinc-700 dark:text-zinc-300">Jenis Pembayaran</h2>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="tab in paymentTabs"
          :key="tab.v"
          :class="[
            'rounded border px-4 py-1.5 text-sm font-medium transition',
            paymentType === tab.v
              ? 'border-primary bg-primary text-white'
              : 'border-zinc-200 hover:bg-zinc-50 dark:border-zinc-700 dark:hover:bg-zinc-800',
          ]"
          @click="onPaymentTypeChange(tab.v)"
        >
          {{ tab.label }}
        </button>
      </div>

      <div class="grid gap-4 md:grid-cols-2">
        <!-- Rekening pembayaran -->
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

        <div v-if="paymentType === 'A'">
          <label class="mb-1 block text-sm font-medium">Kode Aset <span class="text-red-500">*</span></label>
          <input
            :value="paymentAccountNo ?? ''"
            placeholder="Kode akun GL aset"
            class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
            @input="paymentAccountNo = ($event.target as HTMLInputElement).value"
          />
        </div>

        <div v-if="paymentType === 'C'" class="rounded border border-dashed p-3 text-sm text-zinc-500">
          Kas cabang dipilih otomatis oleh sistem berdasarkan cabang pengguna.
        </div>

        <!-- Sumber Dana -->
        <div>
          <label class="mb-1 block text-sm font-medium">
            Sumber Dana (Produk Penghimpunan) <span class="text-red-500">*</span>
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

        <div>
          <label class="mb-1 block text-sm font-medium">Cabang Produk</label>
          <input
            v-model="productBranchCode"
            class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
          />
        </div>
      </div>
    </section>

    <!-- Items -->
    <section class="space-y-4 rounded border bg-white p-6 dark:bg-zinc-900">
      <div class="flex items-center justify-between">
        <h2 class="font-semibold text-zinc-700 dark:text-zinc-300">Detail Distribusi</h2>
        <Button variant="secondary" size="sm" @click="addItem">+ Tambah Item</Button>
      </div>

      <div
        v-if="items.length === 0"
        class="rounded border border-dashed py-8 text-center text-sm text-zinc-400"
      >
        Klik "+ Tambah Item" untuk menambah produk penyaluran.
      </div>

      <div v-for="item in items" :key="item._id" class="space-y-3 rounded border p-4">
        <div class="flex items-center justify-between">
          <span class="text-sm font-medium text-zinc-600 dark:text-zinc-400">
            Item {{ item._id }}
            <span v-if="item.product_name" class="ml-2 text-zinc-400">— {{ item.product_name }}</span>
          </span>
          <button class="text-xs text-red-500 hover:underline" @click="removeItem(item._id)">
            Hapus
          </button>
        </div>
        <div class="grid gap-3 md:grid-cols-3">
          <div>
            <label class="mb-1 block text-xs font-medium">
              Produk <span class="text-red-500">*</span>
            </label>
            <SearchSelect
              :options="productOptions.map((p) => ({ value: p.product_id, label: `[${p.fund_category}] ${p.product_name}` }))"
              :model-value="item.product_id ?? ''"
              placeholder="Pilih produk..."
              @update:model-value="onProductSelected(item, $event as string)"
            />
          </div>
          <div v-if="item.fund_entity === 1">
            <label class="mb-1 block text-xs font-medium">
              Ashnaf <span class="text-red-500">*</span>
            </label>
            <select
              v-model="item.ashnaf"
              class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
            >
              <option value="">-- Pilih Ashnaf --</option>
              <option v-for="a in ashnafOptions" :key="a.code" :value="a.code">
                {{ a.name }}
              </option>
            </select>
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium">
              Jumlah (Rp) <span class="text-red-500">*</span>
            </label>
            <input
              v-model.number="item.amount"
              type="number"
              min="1"
              placeholder="0"
              class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
            />
          </div>
          <div class="md:col-span-2">
            <label class="mb-1 block text-xs font-medium">Keterangan Item</label>
            <input
              v-model="item.description"
              placeholder="Opsional"
              class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
            />
          </div>
          <div>
            <label class="mb-1 block text-xs font-medium">Kode Item Anggaran</label>
            <input
              v-model="item.dist_item_account"
              placeholder="Opsional"
              class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
            />
          </div>
        </div>
      </div>

      <div class="flex items-center justify-end gap-4 border-t pt-3">
        <span class="text-sm text-zinc-500">Total Penyaluran:</span>
        <span class="text-lg font-bold">Rp {{ fmt(totalAmount) }}</span>
      </div>
    </section>

    <!-- Actions -->
    <div class="flex justify-end gap-3">
      <Button variant="ghost" :disabled="loading" @click="router.back()">Batal</Button>
      <Button :disabled="loading || items.length === 0" @click="submit">
        {{ loading ? 'Menyimpan...' : 'Simpan Transaksi' }}
      </Button>
    </div>
  </div>
</template>
