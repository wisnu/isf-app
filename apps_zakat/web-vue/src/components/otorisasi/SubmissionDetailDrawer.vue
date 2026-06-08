<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { CheckCircle, XCircle, X } from 'lucide-vue-next'
import { api } from '@/lib/api/client'
import { dmyt } from '@/lib/date'
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

// ── Payload parsing ────────────────────────────────────────────────────────────

const parsedPayload = computed<Record<string, any>>(() => {
  const raw = props.submission?.payload
  if (!raw) return {}
  if (typeof raw === 'string') { try { return JSON.parse(raw) } catch { return {} } }
  return raw as Record<string, any>
})

const PAYMENT_LABEL: Record<string, string> = {
  K: 'Kas Kecil', C: 'Kas Cabang', B: 'Bank', A: 'Aset/GL',
}

const FIELD_LABEL: Record<string, string> = {
  actual_date: 'Tanggal',
  reference_no: 'No. Referensi',
  description: 'Keterangan',
  paid_to: 'Dibayarkan Kepada',
  payment_type: 'Jenis Bayar',
  payment_account_no: 'Rekening Bayar',
  fund_account_no: 'Sumber Dana',
  product_branch_code: 'Cabang Produk',
  rate: 'Kurs',
  currency_code: 'Mata Uang',
  donor_name: 'Donatur',
  donor_no: 'No. Donatur',
  account_no: 'No. Rekening',
  account_name: 'Nama Rekening',
  bank_name: 'Bank',
  account_number: 'No. Rekening',
  account_holder: 'Atas Nama',
}

const SKIP_FIELDS = new Set(['items', 'donor_id', 'marketer_id', 'sponsor_id', 'volunteer_id', 'asset_code', 'asset_currency'])

function formatValue(key: string, value: unknown): string {
  if (value === null || value === undefined || value === '') return '—'
  if (key === 'payment_type') return PAYMENT_LABEL[String(value)] ?? String(value)
  if (key === 'actual_date') {
    const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(String(value))
    return m ? `${m[3]}-${m[2]}-${m[1]}` : String(value)
  }
  if (key === 'rate' && Number(value) === 1) return 'IDR 1 : 1'
  if (typeof value === 'number') return value.toLocaleString('id-ID')
  if (typeof value === 'boolean') return value ? 'Ya' : 'Tidak'
  if (typeof value === 'object') return JSON.stringify(value)
  return String(value)
}

const mainFields = computed(() =>
  Object.entries(parsedPayload.value)
    .filter(([k, v]) => !SKIP_FIELDS.has(k) && v !== null && v !== undefined && v !== '')
    .map(([k, v]) => ({ key: k, label: FIELD_LABEL[k] ?? k.replace(/_/g, ' '), value: formatValue(k, v) }))
)

const items = computed<any[]>(() => parsedPayload.value.items ?? [])

const idr = new Intl.NumberFormat('id-ID', { minimumFractionDigits: 0 })
const fmtRp = (n: number) => 'Rp ' + idr.format(n)

const totalAmount = computed(() =>
  items.value.reduce((s, i) => s + (Number(i.amount) || 0), 0)
)

const ASHNAF_LABEL: Record<string, string> = {
  F: 'Fakir', M: 'Miskin', A: 'Amil', R: 'Riqab',
  G: 'Gharimin', S: 'Sabilillah', I: 'Ibnu Sabil', L: 'Lainnya',
}
</script>

<template>
  <Teleport to="body">
    <Transition name="drawer">
      <div v-if="open && submission" class="fixed inset-0 z-50 flex justify-end">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-black/40" @click="emit('close')" />

        <!-- Panel -->
        <div class="relative flex flex-col h-full w-full max-w-2xl bg-white shadow-2xl">

          <!-- ── Header (sticky) ──────────────────────────────────────── -->
          <div class="shrink-0 border-b bg-white px-6 py-4">
            <div class="flex items-start justify-between gap-3">
              <div class="min-w-0">
                <div class="flex items-center gap-2 mb-1">
                  <span class="inline-flex items-center rounded-full bg-zinc-100 px-2.5 py-0.5 text-xs font-medium text-zinc-600">
                    {{ submission.entity_label }}
                  </span>
                  <StatusBadge :status="(submission.status as any)" />
                </div>
                <h2 class="text-lg font-bold text-zinc-900">
                  Submission #{{ submission.id }}
                </h2>
              </div>
              <button @click="emit('close')"
                      class="shrink-0 rounded-md p-1.5 text-zinc-400 hover:bg-zinc-100 hover:text-zinc-600 transition">
                <X class="w-5 h-5" />
              </button>
            </div>

            <!-- Meta info — 4 kolom -->
            <div class="mt-3 grid grid-cols-4 gap-3 rounded-lg bg-zinc-50 px-4 py-3 text-xs">
              <div>
                <p class="text-zinc-400 mb-0.5">Inputer</p>
                <p class="font-semibold text-zinc-800">{{ submission.submitted_by }}</p>
              </div>
              <div>
                <p class="text-zinc-400 mb-0.5">Cabang</p>
                <p class="font-semibold text-zinc-800">{{ submission.branch_code }}</p>
              </div>
              <div>
                <p class="text-zinc-400 mb-0.5">Disubmit</p>
                <p class="font-semibold text-zinc-800">{{ submission.submitted_at ? dmyt(submission.submitted_at) : '—' }}</p>
              </div>
              <div>
                <p class="text-zinc-400 mb-0.5">Level</p>
                <p class="font-semibold text-zinc-800">{{ submission.level_current }}/{{ submission.level_required }}</p>
              </div>
            </div>
          </div>

          <!-- ── Scrollable content ───────────────────────────────────── -->
          <div class="flex-1 overflow-y-auto">

            <!-- Data Input -->
            <div class="px-6 py-5 border-b">
              <p class="text-[10px] font-semibold uppercase tracking-wider text-zinc-400 mb-3">Data Input</p>
              <dl class="grid grid-cols-2 gap-x-8 gap-y-3">
                <div v-for="f in mainFields" :key="f.key">
                  <dt class="text-[11px] text-zinc-400 capitalize mb-0.5">{{ f.label }}</dt>
                  <dd class="text-sm font-medium text-zinc-800 break-words">{{ f.value }}</dd>
                </div>
              </dl>
            </div>

            <!-- Items -->
            <div v-if="items.length" class="px-6 py-5 border-b">
              <div class="flex items-center justify-between mb-3">
                <p class="text-[10px] font-semibold uppercase tracking-wider text-zinc-400">
                  Item Transaksi ({{ items.length }})
                </p>
                <span class="text-sm font-bold text-zinc-800">{{ fmtRp(totalAmount) }}</span>
              </div>
              <div class="overflow-x-auto rounded-lg border border-zinc-100">
                <table class="w-full text-xs">
                  <thead class="bg-zinc-50 text-zinc-400 font-semibold uppercase">
                    <tr>
                      <th class="px-3 py-2 text-left w-8">#</th>
                      <th class="px-3 py-2 text-left">Produk</th>
                      <th class="px-3 py-2 text-right">Jumlah</th>
                      <th v-if="items.some(i => i.ashnaf)" class="px-3 py-2 text-left">Ashnaf</th>
                      <th v-if="items.some(i => i.description)" class="px-3 py-2 text-left">Keterangan</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(item, i) in items" :key="i"
                        class="border-t border-zinc-100 hover:bg-zinc-50">
                      <td class="px-3 py-2 text-zinc-400">{{ i + 1 }}</td>
                      <td class="px-3 py-2 text-zinc-700">
                        {{ item.product_name || `#${item.product_id}` || '—' }}
                        <span v-if="item.account_no" class="block text-zinc-400 font-normal">{{ item.account_no }}</span>
                      </td>
                      <td class="px-3 py-2 text-right font-semibold text-zinc-800">
                        {{ fmtRp(Number(item.amount) || 0) }}
                      </td>
                      <td v-if="items.some(i => i.ashnaf)" class="px-3 py-2 text-zinc-500">
                        {{ item.ashnaf ? (ASHNAF_LABEL[item.ashnaf] ?? item.ashnaf) : '—' }}
                      </td>
                      <td v-if="items.some(i => i.description)" class="px-3 py-2 text-zinc-500 max-w-[180px] truncate">
                        {{ item.description || '—' }}
                      </td>
                    </tr>
                    <!-- Subtotal row -->
                    <tr class="border-t-2 border-zinc-200 bg-zinc-50">
                      <td colspan="2" class="px-3 py-2 text-right text-zinc-500 font-medium">Total</td>
                      <td class="px-3 py-2 text-right font-bold text-zinc-900">{{ fmtRp(totalAmount) }}</td>
                      <td v-if="items.some(i => i.ashnaf)" />
                      <td v-if="items.some(i => i.description)" />
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Approval Log -->
            <div v-if="submission.approval_log?.length" class="px-6 py-5">
              <p class="text-[10px] font-semibold uppercase tracking-wider text-zinc-400 mb-3">Riwayat Otorisasi</p>
              <div class="space-y-2">
                <div v-for="log in submission.approval_log" :key="log.level"
                     class="flex items-start gap-3 rounded-lg border px-4 py-3 text-sm"
                     :class="log.status === 'APPROVED' ? 'border-green-100 bg-green-50' : 'border-red-100 bg-red-50'">
                  <span class="mt-0.5 shrink-0"
                        :class="log.status === 'APPROVED' ? 'text-green-500' : 'text-red-500'">
                    <CheckCircle v-if="log.status === 'APPROVED'" class="w-4 h-4" />
                    <XCircle v-else class="w-4 h-4" />
                  </span>
                  <div class="min-w-0 flex-1">
                    <div class="flex items-center justify-between gap-2">
                      <p class="font-medium text-zinc-800">
                        {{ log.authorizer_id === 'SYSTEM_AUTO' ? 'Sistem (dalam limit)' : log.authorizer_id }}
                        <span class="ml-1 text-xs text-zinc-400 font-normal">· Level {{ log.level }}</span>
                      </p>
                      <span class="shrink-0 text-xs text-zinc-400">{{ dmyt(log.logged_at) }}</span>
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
.drawer-enter-active, .drawer-leave-active { transition: transform 0.25s ease; }
.drawer-enter-from, .drawer-leave-to { transform: translateX(100%); }
</style>
