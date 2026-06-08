<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { CheckCircle, XCircle, X } from 'lucide-vue-next'
import { api } from '@/lib/api/client'
import { dmyt, dmy } from '@/lib/date'
import { useToast } from '@/lib/useToast'
import StatusBadge from '@/components/otorisasi/StatusBadge.vue'

interface ApprovalLog {
  level: number
  authorizer_id: string
  status: 'APPROVED' | 'REJECTED'
  notes: string | null
  logged_at: string
}

interface Submission {
  id: number
  entity_type: string
  entity_label: string
  branch_code: string
  payload: Record<string, any>
  status: string
  level_current: number
  level_required: number
  submitted_by: string
  submitted_at: string | null
  approval_log: ApprovalLog[]
}

const props = defineProps<{ submission: Submission | null; open: boolean }>()
const emit = defineEmits<{
  (e: 'close'): void
  (e: 'approved', id: number): void
  (e: 'rejected', id: number): void
}>()

const toast = useToast()
const rejectNotes = ref('')
const showRejectForm = ref(false)
const loading = ref(false)

// ── Lookup resolver (untuk kode → nama saat payload tidak menyertakan nama) ──
const bankMap = ref<Record<string, string>>({})
const branchMap = ref<Record<string, string>>({})
let lookupLoaded = false

async function loadBankLookups() {
  if (lookupLoaded) return
  try {
    const [banks, branches] = await Promise.all([
      api.get<{ data: { bank_code: string; bank_short_name: string | null; bank_name: string | null }[] }>('/api/bank/lookup/banks'),
      api.get<{ data: { branch_code: string; branch_name: string | null }[] }>('/api/bank/lookup/branches'),
    ])
    for (const b of banks.data ?? []) bankMap.value[b.bank_code] = b.bank_short_name ?? b.bank_name ?? b.bank_code
    for (const b of branches.data ?? []) branchMap.value[b.branch_code] = b.branch_name ?? b.branch_code
    lookupLoaded = true
  } catch { /* silent */ }
}

watch(() => props.submission, (sub) => {
  if (sub?.entity_type === 'bank') loadBankLookups()
}, { immediate: true })

watch(() => props.open, (val) => {
  if (!val) { rejectNotes.value = ''; showRejectForm.value = false }
})

async function approve() {
  if (!props.submission) return
  loading.value = true
  try {
    await api.post(`/api/otorisasi/submission/${props.submission.id}/approve`, { notes: null })
    toast.success('Submission diotorisasi')
    emit('approved', props.submission.id)
    emit('close')
  } catch {
    toast.error('Otorisasi gagal')
  } finally {
    loading.value = false
  }
}

async function reject() {
  if (!props.submission || !rejectNotes.value.trim()) return
  loading.value = true
  try {
    await api.post(`/api/otorisasi/submission/${props.submission.id}/reject`, { notes: rejectNotes.value })
    toast.warning('Submission ditolak')
    emit('rejected', props.submission.id)
    emit('close')
  } catch {
    toast.error('Penolakan gagal')
  } finally {
    loading.value = false
  }
}

// ── Helpers ───────────────────────────────────────────────────────────────────

const p = computed<Record<string, any>>(() => {
  const raw = props.submission?.payload
  if (!raw) return {}
  if (typeof raw === 'string') { try { return JSON.parse(raw) } catch { return {} } }
  return raw as Record<string, any>
})

const PAYMENT: Record<string, string> = {
  K: 'Kas Kecil', C: 'Kas Cabang', B: 'Bank', A: 'Aset/GL',
}
const ASHNAF: Record<string, string> = {
  F: 'Fakir', M: 'Miskin', A: 'Amil', R: 'Riqab',
  G: 'Gharimin', S: 'Sabilillah', I: 'Ibnu Sabil', L: 'Lainnya',
}
const FUND_ENTITY: Record<number, string> = {
  1: 'Zakat', 2: 'Infaq', 3: 'Wakaf', 4: 'Amil', 5: 'Non-Halal',
}

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmtRp = (n: number | string | undefined) => 'Rp ' + idr.format(Number(n) || 0)
const v = (val: unknown, fallback = '—') =>
  val === null || val === undefined || val === '' ? fallback : String(val)

const items = computed<any[]>(() => p.value.items ?? [])
const totalAmount = computed(() =>
  items.value.reduce((s, i) => s + (Number(i.amount) || 0), 0)
)

// ── Per entity_type sections ──────────────────────────────────────────────────

type FieldRow = { label: string; value: string; wide?: boolean }
type Section = { title: string; fields: FieldRow[] }

const sections = computed<Section[]>(() => {
  const et = props.submission?.entity_type
  if (!et || !p.value) return []

  if (et === 'penghimpunan') {
    const secs: Section[] = []
    if (p.value.donor_name || p.value.donor_no) {
      secs.push({
        title: 'Informasi Donatur',
        fields: [
          { label: 'Nama Donatur', value: v(p.value.donor_name) },
          { label: 'No. Donatur',  value: v(p.value.donor_no) },
        ],
      })
    }
    secs.push({
      title: 'Detail Transaksi',
      fields: [
        { label: 'Tanggal',        value: dmy(p.value.actual_date) },
        { label: 'Jenis Bayar',    value: PAYMENT[p.value.payment_type] ?? v(p.value.payment_type) },
        { label: 'Rekening',       value: v(p.value.payment_account_no) },
        { label: 'No. Referensi',  value: v(p.value.reference_no) },
        { label: 'Keterangan',     value: v(p.value.description), wide: true },
        { label: 'Mata Uang',      value: v(p.value.currency_code) },
        { label: 'Cabang Produk',  value: v(p.value.product_branch_code) },
      ].filter(f => f.value !== '—'),
    })
    return secs
  }

  if (et === 'penyaluran') {
    return [{
      title: 'Detail Transaksi',
      fields: [
        { label: 'Tanggal',        value: dmy(p.value.actual_date) },
        { label: 'Jenis Bayar',    value: PAYMENT[p.value.payment_type] ?? v(p.value.payment_type) },
        { label: 'Rekening Bayar', value: v(p.value.payment_account_no) },
        { label: 'Sumber Dana',    value: v(p.value.fund_account_no) },
        { label: 'No. Referensi',  value: v(p.value.reference_no) },
        { label: 'Keterangan',     value: v(p.value.description), wide: true },
        { label: 'Dibayarkan Kpd', value: v(p.value.paid_to) },
        { label: 'Cabang Produk',  value: v(p.value.product_branch_code) },
      ].filter(f => f.value !== '—'),
    }]
  }

  if (et === 'upload_penghimpunan') {
    return [{
      title: 'Info Upload',
      fields: [
        { label: 'File',         value: v(p.value.filename) },
        { label: 'Total Baris',  value: v(p.value.total_rows ?? p.value.rows?.length) },
        { label: 'Total Jumlah', value: p.value.total_amount != null ? fmtRp(p.value.total_amount) : '—' },
        { label: 'Cabang',       value: v(p.value.branch_code) },
      ].filter(f => f.value !== '—'),
    }]
  }

  if (et === 'coa') {
    return [{
      title: 'Detail Akun',
      fields: [
        { label: 'Kode Akun',   value: v(p.value.account_no) },
        { label: 'Nama Akun',   value: v(p.value.account_name) },
        { label: 'Tipe',        value: v(p.value.account_type) },
        { label: 'Parent',      value: v(p.value.parent_no) },
        { label: 'Level Akhir', value: p.value.is_detail ? 'Ya' : 'Tidak' },
      ].filter(f => f.value !== '—'),
    }]
  }

  if (et === 'kas') {
    return [{
      title: 'Detail Kas',
      fields: [
        { label: 'Nama',  value: v(p.value.account_name ?? p.value.name) },
        { label: 'Kode',  value: v(p.value.code ?? p.value.account_no) },
      ].filter(f => f.value !== '—'),
    }]
  }

  if (et === 'bank') {
    return [{
      title: 'Detail Rekening Bank',
      fields: [
        { label: 'Aksi',          value: v(p.value.action ? String(p.value.action).toUpperCase() : null) },
        { label: 'Kode Rekening', value: v(p.value.account_no) },
        { label: 'Nama Rekening', value: v(p.value.account_name) },
        { label: 'No. Rekening',  value: v(p.value.bank_account_no) },
        { label: 'Bank',    value: v(p.value.bank_name ?? (p.value.bank_code ? `${p.value.bank_code} — ${bankMap.value[p.value.bank_code] ?? p.value.bank_code}` : null)) },
        { label: 'Cabang',  value: v(p.value.branch_name ?? (p.value.branch_code ? `${p.value.branch_code} — ${branchMap.value[p.value.branch_code] ?? p.value.branch_code}` : null)) },
        { label: 'Valuta',        value: v(p.value.currency_code) },
        { label: 'GL Interface',  value: v(p.value.account_interface) },
        { label: 'Tgl Buka',      value: v(p.value.opening_date) },
        { label: 'Rek. Amil',     value: p.value.is_amil_account === true ? 'Ya' : p.value.is_amil_account === false ? 'Tidak' : '—' },
      ].filter(f => f.value !== '—'),
    }]
  }

  // Fallback: generic key-value
  return [{
    title: 'Data Input',
    fields: Object.entries(p.value)
      .filter(([k, v]) => k !== 'items' && v !== null && v !== undefined && v !== '')
      .map(([k, v]) => ({
        label: k.replace(/_/g, ' '),
        value: typeof v === 'object' ? JSON.stringify(v) : String(v),
      })),
  }]
})

// Items table columns per entity
const hasAshnaf = computed(() => items.value.some(i => i.ashnaf && i.ashnaf !== 'L'))
const hasAmil   = computed(() => items.value.some(i => i.percentage_of_amil != null && i.percentage_of_amil > 0))
const hasDesc   = computed(() => items.value.some(i => i.description))
</script>

<template>
  <Teleport to="body">
    <Transition name="drawer">
      <div v-if="open && submission" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/40" @click="emit('close')" />

        <!-- Panel -->
        <div class="relative flex flex-col w-full max-w-2xl max-h-[90vh] rounded-xl bg-white shadow-2xl">

          <!-- ── Header (sticky) ──────────────────────────────────────── -->
          <div class="shrink-0 border-b bg-white px-6 py-4">
            <div class="flex items-start justify-between gap-3">
              <div class="min-w-0">
                <div class="flex flex-wrap items-center gap-2 mb-1">
                  <span class="rounded-full bg-zinc-100 px-2.5 py-0.5 text-xs font-medium text-zinc-600">
                    {{ submission.entity_label }}
                  </span>
                  <StatusBadge :status="(submission.status as any)" />
                </div>
                <h2 class="text-lg font-bold text-zinc-900">Submission #{{ submission.id }}</h2>
              </div>
              <button @click="emit('close')"
                      class="shrink-0 rounded-md p-1.5 text-zinc-400 hover:bg-zinc-100 hover:text-zinc-600 transition">
                <X class="w-5 h-5" />
              </button>
            </div>

            <!-- Meta: 4 kolom -->
            <div class="mt-3 grid grid-cols-4 gap-3 rounded-lg bg-zinc-50 px-4 py-3 text-xs">
              <div>
                <p class="text-zinc-400 mb-0.5">Inputer</p>
                <p class="font-semibold text-zinc-800">{{ submission.submitted_by }}</p>
              </div>
              <div>
                <p class="text-zinc-400 mb-0.5">Cabang</p>
                <p class="font-semibold text-zinc-800">{{ submission.branch_code }}</p>
              </div>
              <div class="col-span-2">
                <p class="text-zinc-400 mb-0.5">Disubmit</p>
                <p class="font-semibold text-zinc-800">
                  {{ submission.submitted_at ? dmyt(submission.submitted_at) : '—' }}
                </p>
              </div>
            </div>
          </div>

          <!-- ── Scrollable body ──────────────────────────────────────── -->
          <div class="flex-1 overflow-y-auto divide-y divide-zinc-100">

            <!-- Sections (entity-specific fields) -->
            <div v-for="sec in sections" :key="sec.title" class="px-6 py-5">
              <p class="text-[10px] font-semibold uppercase tracking-wider text-zinc-400 mb-3">
                {{ sec.title }}
              </p>
              <dl class="grid grid-cols-2 gap-x-8 gap-y-3">
                <div v-for="f in sec.fields" :key="f.label"
                     :class="f.wide ? 'col-span-2' : ''">
                  <dt class="text-[11px] text-zinc-400 capitalize mb-0.5">{{ f.label }}</dt>
                  <dd class="text-sm font-medium text-zinc-800 break-words">{{ f.value }}</dd>
                </div>
              </dl>
            </div>

            <!-- Items (penghimpunan / penyaluran) -->
            <div v-if="items.length" class="px-6 py-5">
              <div class="flex items-center justify-between mb-3">
                <p class="text-[10px] font-semibold uppercase tracking-wider text-zinc-400">
                  Item Transaksi ({{ items.length }})
                </p>
                <span class="text-sm font-bold text-zinc-800">{{ fmtRp(totalAmount) }}</span>
              </div>
              <div class="overflow-x-auto rounded-lg border border-zinc-100">
                <table class="w-full text-xs">
                  <thead class="bg-zinc-50 text-zinc-400 font-semibold">
                    <tr>
                      <th class="px-3 py-2 text-left w-7">#</th>
                      <th class="px-3 py-2 text-left">Produk / Rekening</th>
                      <th v-if="submission.entity_type === 'penghimpunan'" class="px-3 py-2 text-left">Jenis Dana</th>
                      <th v-if="hasAshnaf" class="px-3 py-2 text-left">Ashnaf</th>
                      <th v-if="hasAmil" class="px-3 py-2 text-right">% Amil</th>
                      <th class="px-3 py-2 text-right">Jumlah</th>
                      <th v-if="hasDesc" class="px-3 py-2 text-left">Ket.</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(item, i) in items" :key="i"
                        class="border-t border-zinc-100 hover:bg-zinc-50/60">
                      <td class="px-3 py-2 text-zinc-400">{{ i + 1 }}</td>
                      <td class="px-3 py-2">
                        <p class="font-medium text-zinc-800">
                          {{ item.product_name || `Produk #${item.product_id}` }}
                        </p>
                        <p v-if="item.account_no" class="text-zinc-400">{{ item.account_no }}</p>
                      </td>
                      <td v-if="submission.entity_type === 'penghimpunan'" class="px-3 py-2 text-zinc-500">
                        {{ FUND_ENTITY[item.fund_entity] ?? item.fund_entity ?? '—' }}
                      </td>
                      <td v-if="hasAshnaf" class="px-3 py-2 text-zinc-500">
                        {{ item.ashnaf ? (ASHNAF[item.ashnaf] ?? item.ashnaf) : '—' }}
                      </td>
                      <td v-if="hasAmil" class="px-3 py-2 text-right text-zinc-500">
                        {{ item.percentage_of_amil ? item.percentage_of_amil + '%' : '—' }}
                      </td>
                      <td class="px-3 py-2 text-right font-semibold text-zinc-800 whitespace-nowrap">
                        {{ fmtRp(item.amount) }}
                      </td>
                      <td v-if="hasDesc" class="px-3 py-2 text-zinc-500 max-w-[140px] truncate">
                        {{ item.description || '—' }}
                      </td>
                    </tr>
                    <!-- Total row -->
                    <tr class="border-t-2 border-zinc-200 bg-zinc-50">
                      <td :colspan="2 + (submission.entity_type === 'penghimpunan' ? 1 : 0) + (hasAshnaf ? 1 : 0) + (hasAmil ? 1 : 0)"
                          class="px-3 py-2.5 text-right text-xs font-semibold text-zinc-500">Total</td>
                      <td class="px-3 py-2.5 text-right text-sm font-bold text-zinc-900 whitespace-nowrap">
                        {{ fmtRp(totalAmount) }}
                      </td>
                      <td v-if="hasDesc" />
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Approval Log -->
            <div v-if="submission.approval_log?.length" class="px-6 py-5">
              <p class="text-[10px] font-semibold uppercase tracking-wider text-zinc-400 mb-3">
                Riwayat Otorisasi
              </p>
              <div class="space-y-2">
                <div v-for="log in submission.approval_log" :key="log.level"
                     class="flex items-start gap-3 rounded-lg border px-4 py-3"
                     :class="log.status === 'APPROVED'
                       ? 'border-green-100 bg-green-50'
                       : 'border-red-100 bg-red-50'">
                  <span class="mt-0.5 shrink-0"
                        :class="log.status === 'APPROVED' ? 'text-green-500' : 'text-red-500'">
                    <CheckCircle v-if="log.status === 'APPROVED'" class="w-4 h-4" />
                    <XCircle v-else class="w-4 h-4" />
                  </span>
                  <div class="min-w-0 flex-1">
                    <div class="flex items-center justify-between gap-2 flex-wrap">
                      <p class="text-sm font-medium text-zinc-800">
                        {{ log.authorizer_id === 'SYSTEM_AUTO' ? 'Sistem (dalam limit)' : log.authorizer_id }}
                        <span class="ml-1 text-xs text-zinc-400 font-normal">· Level {{ log.level }}</span>
                      </p>
                      <span class="text-xs text-zinc-400 shrink-0">{{ dmyt(log.logged_at) }}</span>
                    </div>
                    <p v-if="log.notes" class="mt-0.5 text-xs text-zinc-600">{{ log.notes }}</p>
                  </div>
                </div>
              </div>
            </div>

          </div>

          <!-- ── Actions (sticky bottom) ─────────────────────────────── -->
          <div v-if="submission.status === 'PENDING'" class="shrink-0 border-t bg-white px-6 py-4">
            <div v-if="!showRejectForm" class="flex gap-3">
              <button @click="approve" :disabled="loading"
                      class="flex-1 rounded-lg bg-green-600 py-2.5 text-sm font-semibold text-white hover:bg-green-700 disabled:opacity-50 transition">
                Otorisasi
              </button>
              <button @click="showRejectForm = true"
                      class="flex-1 rounded-lg border border-red-400 py-2.5 text-sm font-semibold text-red-600 hover:bg-red-50 transition">
                Tolak
              </button>
            </div>
            <div v-else class="space-y-2">
              <textarea v-model="rejectNotes" rows="3" placeholder="Alasan penolakan (wajib)"
                        class="w-full rounded-lg border px-3 py-2 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-red-400" />
              <div class="flex gap-2">
                <button @click="reject" :disabled="loading || !rejectNotes.trim()"
                        class="flex-1 rounded-lg bg-red-600 py-2.5 text-sm font-semibold text-white hover:bg-red-700 disabled:opacity-50 transition">
                  Konfirmasi Tolak
                </button>
                <button @click="showRejectForm = false"
                        class="rounded-lg border px-5 py-2.5 text-sm text-zinc-600 hover:bg-zinc-50 transition">
                  Batal
                </button>
              </div>
            </div>
          </div>

        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.drawer-enter-active, .drawer-leave-active { transition: opacity 0.2s ease; }
.drawer-enter-from, .drawer-leave-to { opacity: 0; }
</style>
