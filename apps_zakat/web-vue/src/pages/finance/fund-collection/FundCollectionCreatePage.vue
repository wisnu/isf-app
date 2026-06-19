<script setup lang="ts">
import { onMounted, onUnmounted, ref, shallowRef, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import AmountInput from '@/components/ui/AmountInput.vue'
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
}

interface ProductOption {
  product_id: number
  product_name: string
  fund_category: string
  account_no: string
  fund_entity: number
}

interface DonorOption {
  donor_id: number
  donor_no: string | null
  donor_name: string | null
  phone_number: string | null
  donor_type: string | null
}

interface ItemRow {
  _id: number
  product_id: number | null
  product_name: string
  account_no: string
  fund_entity: number
  amount: number | null
  description: string
  percentage_of_amil: number
}

const router = useRouter()
const route = useRoute()
const toast = useToast()
const auth = useAuthStore()

const editId = computed(() => {
  const p = route.params.id
  return p ? Number(p) : null
})
const isEditMode = computed(() => editId.value !== null)

const actualDate = shallowRef(new Date().toISOString().slice(0, 10))
const referenceNo = shallowRef('')
const description = shallowRef('')
const paidTo = shallowRef(auth.user?.username ?? '')
const donorId = shallowRef<number | null>(null)
const donorNo = shallowRef('')
const donorName = shallowRef('')
const paymentType = shallowRef<'B' | 'C' | 'K' | 'A'>('C')
const paymentAccountNo = shallowRef<string | null>(null)
const productBranchCode = shallowRef('001')
const rate = shallowRef(1.0)
const currencyCode = shallowRef('IDR')

let _idCtr = 1
const items = ref<ItemRow[]>([])

const totalAmount = computed(() => items.value.reduce((s, i) => s + (i.amount ?? 0), 0))
const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmt = (n: number) => idr.format(n)

const rekeningOptions = ref<RekeningOption[]>([])
const productOptions = ref<ProductOption[]>([])
const donorOptions = ref<DonorOption[]>([])
const donorQuery = shallowRef('')
const donorSearchLoading = shallowRef(false)

// Limit info
const nilaiLimit = shallowRef<number>(0)
const hasLimit = shallowRef<boolean>(false)
const limitLoading = shallowRef<boolean>(false)

const willBypass = computed(
  () => hasLimit.value && totalAmount.value > 0 && totalAmount.value <= nilaiLimit.value,
)
const fmtRp = (n: number) => 'Rp ' + idr.format(n)

const loading = shallowRef(false)
const errorMsg = shallowRef<string | null>(null)

const paymentTabs = [
  { v: 'C', label: 'Kas Cabang' },
  { v: 'B', label: 'Bank' },
  { v: 'K', label: 'Kas Kecil' },
  { v: 'A', label: 'Aset/GL' },
] as const

async function loadLookups() {
  productOptions.value = await api
    .get<ProductOption[]>(`/api/penghimpunan/lookup/produk?branch_code=${encodeURIComponent(productBranchCode.value)}`)
    .catch(() => [])
}

async function loadRekening() {
  const typeMap: Record<string, string> = { B: 'bank', K: 'petty', C: 'cabang', A: 'bank' }
  rekeningOptions.value = await api
    .get<RekeningOption[]>(`/api/penghimpunan/lookup/rekening?type=${typeMap[paymentType.value]}`)
    .catch(() => [])
}

async function searchDonor() {
  if (donorQuery.value.length < 2) return
  donorSearchLoading.value = true
  try {
    donorOptions.value = await api
      .get<DonorOption[]>(`/api/penghimpunan/lookup/donor?q=${encodeURIComponent(donorQuery.value)}`)
      .catch(() => [])
  } finally {
    donorSearchLoading.value = false
  }
}

function onDonorSelected(val: string | number) {
  const d = donorOptions.value.find((x) => x.donor_id === Number(val))
  if (!d) return
  donorId.value = d.donor_id
  donorNo.value = d.donor_no ?? ''
  donorName.value = d.donor_name ?? ''
}

function onPaymentTypeChange(type: 'B' | 'C' | 'K' | 'A') {
  paymentType.value = type
  paymentAccountNo.value = null
  loadRekening()
}

function addItem() {
  if (loading.value) return
  items.value.push({
    _id: _idCtr++,
    product_id: null,
    product_name: '',
    account_no: '',
    fund_entity: 2,
    amount: null,
    description: '',
    percentage_of_amil: 0,
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
  item.description = p.product_name
}

function validate(): string | null {
  if (!actualDate.value) return 'Tanggal transaksi wajib diisi'
  if (items.value.length === 0) return 'Minimal satu item produk harus diisi'
  for (const item of items.value) {
    if (!item.product_id) return 'Semua item harus memiliki produk yang dipilih'
    if (!item.amount || item.amount <= 0) return 'Jumlah item harus lebih dari 0'
  }
  if (paymentType.value !== 'C' && !paymentAccountNo.value)
    return 'Rekening pembayaran wajib dipilih'
  return null
}

async function loadSubmission(id: number) {
  try {
    const res = await api.get<{ id: number; payload: Record<string, any> }>(
      `/api/otorisasi/submission/${id}`,
    )
    const p = res.payload
    if (p.actual_date) actualDate.value = p.actual_date
    if (p.reference_no != null) referenceNo.value = p.reference_no ?? ''
    if (p.description != null) description.value = p.description ?? ''
    if (p.paid_to != null) paidTo.value = p.paid_to ?? ''
    if (p.donor_id != null) donorId.value = p.donor_id
    if (p.donor_no != null) donorNo.value = p.donor_no ?? ''
    if (p.donor_name != null) donorName.value = p.donor_name ?? ''
    if (p.payment_type) paymentType.value = p.payment_type
    if (p.payment_account_no != null) paymentAccountNo.value = p.payment_account_no
    if (p.product_branch_code) productBranchCode.value = p.product_branch_code
    if (p.rate != null) rate.value = p.rate
    if (p.currency_code) currencyCode.value = p.currency_code
    if (Array.isArray(p.items)) {
      items.value = p.items.map((i: any) => ({
        _id: _idCtr++,
        product_id: i.product_id,
        product_name: '',
        account_no: i.account_no ?? '',
        fund_entity: i.fund_entity ?? 2,
        amount: i.amount,
        description: i.description ?? '',
        percentage_of_amil: i.percentage_of_amil ?? 0,
      }))
    }
    await loadRekening()
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
    toast.error('Gagal memuat data submission')
  }
}

async function submit() {
  const validErr = validate()
  if (validErr) { toast.error(validErr); return }
  loading.value = true
  errorMsg.value = null
  try {
    const innerPayload = {
      actual_date: actualDate.value,
      reference_no: referenceNo.value || null,
      description: description.value,
      paid_to: paidTo.value || null,
      donor_id: donorId.value,
      donor_no: donorNo.value || null,
      donor_name: donorName.value || null,
      payment_type: paymentType.value,
      payment_account_no: paymentAccountNo.value,
      rate: rate.value,
      currency_code: currencyCode.value,
      product_branch_code: productBranchCode.value,
      items: items.value.map((i) => ({
        product_id: i.product_id,
        account_no: i.account_no,
        amount: i.amount,
        description: i.description || description.value,
        fund_entity: i.fund_entity,
        percentage_of_amil: i.percentage_of_amil,
      })),
    }

    let res: { status: string; bypassed_auth: boolean }

    if (isEditMode.value && editId.value !== null) {
      res = await api.put<{ status: string; bypassed_auth: boolean }>(
        `/api/otorisasi/save-and-submit/${editId.value}`,
        { payload: innerPayload },
      )
    } else {
      res = await api.post<{ status: string; bypassed_auth: boolean }>(
        '/api/otorisasi/save-and-submit/',
        { entity_type: 'penghimpunan', module: 'keuangan', payload: innerPayload },
      )
    }

    if (res.status === 'AUTHORIZED') {
      toast.success('Transaksi berhasil — langsung efektif')
    } else {
      toast.success('Transaksi dikirim — menunggu otorisasi')
    }
    router.push({ name: 'finance-transactions-fund-collection' })
  } catch (e: unknown) {
    errorMsg.value = e instanceof Error ? e.message : String(e)
    toast.error('Gagal menyimpan transaksi')
  } finally {
    loading.value = false
  }
}

async function fetchUserLimit() {
  if (isEditMode.value) return
  limitLoading.value = true
  try {
    const res = await api.get<{ nilai_limit: number; has_limit: boolean }>(
      '/api/otorisasi/user-limit/?entity_type=penghimpunan',
    )
    nilaiLimit.value = res.nilai_limit
    hasLimit.value = res.has_limit
  } catch {
    // silent fail — limit info not critical for UX
  } finally {
    limitLoading.value = false
  }
}

function onKeydown(e: KeyboardEvent) {
  if (e.altKey && e.key.toLowerCase() === 'n') {
    e.preventDefault()
    addItem()
  }
}

onMounted(async () => {
  await loadLookups()
  await loadRekening()
  if (isEditMode.value && editId.value !== null) {
    await loadSubmission(editId.value)
  }
  fetchUserLimit()
  window.addEventListener('keydown', onKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', onKeydown)
})
</script>

<template>
  <div class="w-full pb-6">
    <!-- Page header -->
    <header class="mb-4 flex items-center justify-between">
      <h1 class="text-2xl font-bold tracking-tight">
        {{ isEditMode ? 'Edit Draft Penghimpunan Dana' : 'Input Penghimpunan Dana' }}
      </h1>
      <Button variant="ghost" :disabled="loading" @click="router.back()">Kembali</Button>
    </header>

    <Alert v-if="errorMsg" variant="destructive" class="mb-4">{{ errorMsg }}</Alert>

    <!-- 2-panel body -->
    <div class="flex w-full flex-col gap-5 xl:flex-row xl:items-start">

      <!-- ── LEFT PANEL: sticky ─────────────────────────────────────── -->
      <div class="flex w-full shrink-0 flex-col gap-4 xl:w-[420px] xl:sticky xl:top-4">

        <!-- Info Transaksi -->
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
            <div class="col-span-2">
              <label class="mb-1 block text-sm font-medium">Disetor Oleh</label>
              <input
                v-model="paidTo"
                class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
              />
            </div>
          </div>
        </section>

        <!-- Info Donatur -->
        <section class="space-y-3 rounded border bg-white p-5 dark:bg-zinc-900">
          <h2 class="text-sm font-semibold uppercase tracking-wide text-zinc-500 dark:text-zinc-400">
            Info Donatur <span class="text-xs font-normal normal-case text-zinc-400">(opsional)</span>
          </h2>
          <div>
            <label class="mb-1 block text-sm font-medium">Cari Donatur</label>
            <div class="flex gap-2">
              <input
                v-model="donorQuery"
                placeholder="Ketik nama / no. donatur..."
                class="h-9 flex-1 rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
                @keyup.enter="searchDonor"
              />
              <Button variant="secondary" size="sm" :disabled="donorSearchLoading" @click="searchDonor">
                {{ donorSearchLoading ? '...' : 'Cari' }}
              </Button>
            </div>
            <div v-if="donorOptions.length > 0" class="mt-1">
              <SearchSelect
                :options="donorOptions.map((d) => ({ value: d.donor_id, label: `${d.donor_no} — ${d.donor_name}` }))"
                :model-value="donorId ?? ''"
                placeholder="Pilih hasil pencarian..."
                @update:model-value="onDonorSelected($event as number)"
              />
            </div>
          </div>
          <div v-if="donorName" class="rounded bg-zinc-50 px-3 py-2 dark:bg-zinc-800">
            <p class="text-xs text-zinc-500">Dipilih:</p>
            <p class="font-medium">{{ donorName }}</p>
            <p class="text-xs text-zinc-400">{{ donorNo }}</p>
          </div>
          <div v-else class="grid grid-cols-2 gap-3">
            <div>
              <label class="mb-1 block text-sm font-medium">No. Donatur</label>
              <input
                v-model="donorNo"
                placeholder="Manual"
                class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
              />
            </div>
            <div>
              <label class="mb-1 block text-sm font-medium">Nama Donatur</label>
              <input
                v-model="donorName"
                placeholder="Manual"
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
            <div v-if="paymentType === 'C'" class="rounded border border-dashed p-3 text-xs text-zinc-500">
              Kas cabang dipilih otomatis berdasarkan cabang pengguna.
            </div>
            <div v-else-if="paymentType === 'A'">
              <label class="mb-1 block text-sm font-medium">Kode Aset <span class="text-red-500">*</span></label>
              <input
                :value="paymentAccountNo ?? ''"
                placeholder="Kode akun GL aset"
                class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
                @input="paymentAccountNo = ($event.target as HTMLInputElement).value"
              />
            </div>
            <div v-else>
              <label class="mb-1 block text-sm font-medium">
                {{ paymentType === 'B' ? 'Rekening Bank' : 'Rekening Kas Kecil' }}
                <span class="text-red-500">*</span>
              </label>
              <SearchSelect
                :options="rekeningOptions.map((r) => ({ value: r.account_no, label: `${r.account_name} (${r.account_no})` }))"
                :model-value="paymentAccountNo ?? ''"
                placeholder="Pilih rekening..."
                @update:model-value="paymentAccountNo = $event as string || null"
              />
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

        <!-- Limit info -->
        <div v-if="!isEditMode && items.length > 0" class="rounded border px-4 py-3 text-sm space-y-1">
          <div class="flex justify-between font-medium">
            <span class="text-zinc-500">Total transaksi</span>
            <span>{{ fmtRp(totalAmount) }}</span>
          </div>
          <template v-if="!limitLoading">
            <div v-if="hasLimit" class="flex justify-between text-xs text-zinc-400">
              <span>Limit Anda</span>
              <span>{{ fmtRp(nilaiLimit) }}</span>
            </div>
            <div :class="['flex items-center gap-1.5 text-xs font-medium mt-1',
                          willBypass ? 'text-green-600' : 'text-amber-600']">
              <span>{{ willBypass ? '✓' : 'ⓘ' }}</span>
              <span>{{
                willBypass
                  ? 'Transaksi ini akan langsung efektif'
                  : hasLimit
                    ? 'Transaksi ini memerlukan otorisasi'
                    : 'Semua transaksi memerlukan otorisasi'
              }}</span>
            </div>
          </template>
        </div>

        <!-- Actions -->
        <div class="flex gap-3">
          <Button variant="ghost" class="flex-1" :disabled="loading" @click="router.back()">Batal</Button>
          <Button class="flex-1" :disabled="loading || items.length === 0" @click="submit">
            {{ loading ? 'Menyimpan...' : isEditMode ? 'Update & Submit' : 'Simpan & Submit' }}
          </Button>
        </div>
      </div>

      <!-- ── RIGHT PANEL: Item Produk ───────────────────────────────── -->
      <div class="flex-1 min-w-0">
        <section class="rounded border bg-white dark:bg-zinc-900">
          <div class="flex items-center justify-between border-b px-5 py-3">
            <div>
              <h2 class="font-semibold text-zinc-700 dark:text-zinc-300">Detail Produk Dana</h2>
              <p class="text-xs text-zinc-400">{{ items.length }} item · Total:
                <span class="font-semibold text-zinc-700 dark:text-zinc-200">Rp {{ fmt(totalAmount) }}</span>
              </p>
            </div>
            <Button variant="secondary" size="sm" @click="addItem">+ Tambah Item</Button>
          </div>

          <!-- Empty state -->
          <button
            v-if="items.length === 0"
            class="w-full py-16 text-center text-sm text-zinc-400 hover:text-primary hover:bg-zinc-50/60 dark:hover:bg-zinc-800/40 transition rounded"
            @click="addItem"
          >
            <span>Klik "+ Tambah Item" untuk menambah produk penghimpunan.</span>
            <kbd class="ml-2 rounded border border-zinc-200 bg-zinc-100 px-1.5 py-0.5 text-xs text-zinc-500 dark:border-zinc-700 dark:bg-zinc-800">Alt+N</kbd>
          </button>

          <!-- Items -->
          <div v-if="items.length > 0" class="divide-y">
            <div class="grid grid-cols-[2fr_1fr_2fr_auto] gap-3 bg-zinc-50 px-5 py-2 text-xs font-semibold uppercase text-zinc-500 dark:bg-zinc-800">
              <span>Produk <span class="text-red-400">*</span></span>
              <span>Jumlah (Rp) <span class="text-red-400">*</span></span>
              <span>Keterangan</span>
              <span></span>
            </div>

            <div
              v-for="item in items"
              :key="item._id"
              class="grid grid-cols-[2fr_1fr_2fr_auto] gap-3 px-5 py-3 items-start hover:bg-zinc-50/50 dark:hover:bg-zinc-800/30"
            >
              <div>
                <SearchSelect
                  :options="productOptions.map((p) => ({ value: p.product_id, label: `[${p.fund_category}] ${p.product_name}` }))"
                  :model-value="item.product_id ?? ''"
                  placeholder="Pilih produk..."
                  @update:model-value="onProductSelected(item, $event as string)"
                />
              </div>
              <div>
                <AmountInput
                  :model-value="item.amount"
                  @update:model-value="item.amount = $event"
                />
              </div>
              <div>
                <input
                  v-model="item.description"
                  placeholder="Opsional"
                  class="h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800"
                />
              </div>
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

          <!-- Hint tambah item -->
          <button
            v-if="items.length > 0"
            class="flex w-full items-center gap-2 border-t px-5 py-2.5 text-left text-xs italic text-zinc-400 hover:text-primary hover:bg-zinc-50/60 dark:text-zinc-500 dark:hover:bg-zinc-800/40 transition"
            @click="addItem"
          >
            <span>Klik "+ Tambah Item" untuk menambah produk penghimpunan.</span>
            <kbd class="rounded border border-zinc-200 bg-zinc-100 px-1.5 py-0.5 not-italic text-zinc-500 dark:border-zinc-700 dark:bg-zinc-800">Alt+N</kbd>
          </button>

          <!-- Footer total -->
          <div v-if="items.length > 0" class="flex items-center justify-end gap-3 border-t bg-zinc-50 px-5 py-3 dark:bg-zinc-800">
            <span class="text-sm text-zinc-500">Total Penghimpunan:</span>
            <span class="text-xl font-bold text-zinc-800 dark:text-zinc-100">Rp {{ fmt(totalAmount) }}</span>
          </div>
        </section>
      </div>

    </div>
  </div>
</template>
