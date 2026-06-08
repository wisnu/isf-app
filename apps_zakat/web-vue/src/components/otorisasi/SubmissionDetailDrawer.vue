<script setup lang="ts">
import { ref, watch } from 'vue'
import { X, CheckCircle, XCircle } from 'lucide-vue-next'
import { api } from '@/lib/api/client'
import { dmy } from '@/lib/date'
import { useToast } from '@/lib/useToast'

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

function formatPayload(payload: Record<string, any>): { label: string; value: string }[] {
  const skip = ['items']
  return Object.entries(payload)
    .filter(([k]) => !skip.includes(k))
    .map(([k, v]) => ({
      label: k.replace(/_/g, ' '),
      value: typeof v === 'object' ? JSON.stringify(v) : String(v ?? '—'),
    }))
}
</script>

<template>
  <Teleport to="body">
    <Transition name="drawer">
      <div v-if="open && submission" class="fixed inset-0 z-50 flex justify-end">
        <div class="absolute inset-0 bg-black/30" @click="emit('close')" />
        <div class="relative w-full max-w-lg bg-white shadow-xl flex flex-col h-full overflow-y-auto">
          <!-- Header -->
          <div class="flex items-center justify-between px-6 py-4 border-b">
            <div>
              <p class="text-xs text-gray-500">{{ submission.entity_label }}</p>
              <h2 class="text-base font-semibold text-gray-800">Detail Submission #{{ submission.id }}</h2>
            </div>
            <button @click="emit('close')" class="text-gray-400 hover:text-gray-600">
              <X class="w-5 h-5" />
            </button>
          </div>

          <!-- Info -->
          <div class="px-6 py-4 space-y-3 border-b">
            <div class="grid grid-cols-2 gap-2 text-sm">
              <div>
                <p class="text-gray-400 text-xs">Inputer</p>
                <p class="font-medium">{{ submission.submitted_by }}</p>
              </div>
              <div>
                <p class="text-gray-400 text-xs">Cabang</p>
                <p class="font-medium">{{ submission.branch_code }}</p>
              </div>
              <div>
                <p class="text-gray-400 text-xs">Disubmit</p>
                <p class="font-medium">{{ submission.submitted_at ? dmy(submission.submitted_at) : '—' }}</p>
              </div>
              <div>
                <p class="text-gray-400 text-xs">Level</p>
                <p class="font-medium">{{ submission.level_current }}/{{ submission.level_required }}</p>
              </div>
            </div>
          </div>

          <!-- Payload -->
          <div class="px-6 py-4 border-b">
            <p class="text-xs font-medium text-gray-500 uppercase mb-3">Data Input</p>
            <dl class="space-y-2 text-sm">
              <div v-for="field in formatPayload(submission.payload)" :key="field.label"
                   class="flex justify-between gap-4">
                <dt class="text-gray-500 capitalize">{{ field.label }}</dt>
                <dd class="font-medium text-right">{{ field.value }}</dd>
              </div>
            </dl>
            <div v-if="submission.payload.items?.length" class="mt-3">
              <p class="text-xs font-medium text-gray-500 uppercase mb-2">Item ({{ submission.payload.items.length }})</p>
              <div v-for="(item, i) in submission.payload.items" :key="i"
                   class="text-xs bg-gray-50 rounded px-2 py-1 mb-1">
                {{ item.product_name || item.product_id }} — Rp {{ item.amount?.toLocaleString('id-ID') }}
              </div>
            </div>
          </div>

          <!-- Approval Log -->
          <div v-if="submission.approval_log?.length" class="px-6 py-4 border-b">
            <p class="text-xs font-medium text-gray-500 uppercase mb-3">Riwayat Otorisasi</p>
            <div v-for="log in submission.approval_log" :key="log.level"
                 class="flex items-start gap-3 text-sm mb-2">
              <span :class="log.status === 'APPROVED' ? 'text-green-500' : 'text-red-500'">
                <CheckCircle v-if="log.status === 'APPROVED'" class="w-4 h-4" />
                <XCircle v-else class="w-4 h-4" />
              </span>
              <div>
                <p class="font-medium">Level {{ log.level }} — {{ log.authorizer_id }}</p>
                <p v-if="log.notes" class="text-gray-500 text-xs">{{ log.notes }}</p>
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div v-if="submission.status === 'PENDING'" class="px-6 py-4 space-y-3 mt-auto border-t">
            <div v-if="!showRejectForm" class="flex gap-3">
              <button @click="approve" :disabled="loading"
                      class="flex-1 bg-green-600 text-white py-2 rounded font-medium hover:bg-green-700 disabled:opacity-50">
                Otorisasi
              </button>
              <button @click="showRejectForm = true"
                      class="flex-1 border border-red-500 text-red-600 py-2 rounded font-medium hover:bg-red-50">
                Tolak
              </button>
            </div>
            <div v-else class="space-y-2">
              <textarea v-model="rejectNotes" rows="3" placeholder="Alasan penolakan (wajib)"
                        class="w-full border rounded px-3 py-2 text-sm resize-none" />
              <div class="flex gap-2">
                <button @click="reject" :disabled="loading || !rejectNotes.trim()"
                        class="flex-1 bg-red-600 text-white py-2 rounded font-medium hover:bg-red-700 disabled:opacity-50">
                  Konfirmasi Tolak
                </button>
                <button @click="showRejectForm = false"
                        class="px-4 py-2 border rounded text-gray-600 hover:bg-gray-50">
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
