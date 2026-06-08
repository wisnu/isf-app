<script setup lang="ts">
import { Landmark, Plus, RefreshCw } from 'lucide-vue-next'
import { computed, onMounted, reactive, ref, shallowRef } from 'vue'

import StatusBadge from '@/components/otorisasi/StatusBadge.vue'
import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import { api } from '@/lib/api/client'
import { formatDate, formatIdr } from '@/lib/format'
import { useToast } from '@/lib/useToast'

interface BankAccount {
  id: string
  bankName: string
  branch: string
  accountNumber: string
  accountHolder: string
  balance: number
  primary: boolean
  updatedAt: string
}

const accounts: BankAccount[] = [
  {
    id: 'bk-1',
    bankName: 'Bank Syariah Indonesia',
    branch: 'KCP Tendean Jakarta',
    accountNumber: '7012345678',
    accountHolder: 'Lembaga ZISWAF',
    balance: 1_850_000_000,
    primary: true,
    updatedAt: '2026-05-19',
  },
  {
    id: 'bk-2',
    bankName: 'Bank Muamalat',
    branch: 'KC Salemba Jakarta',
    accountNumber: '4011223344',
    accountHolder: 'Lembaga ZISWAF',
    balance: 720_000_000,
    primary: false,
    updatedAt: '2026-05-19',
  },
  {
    id: 'bk-3',
    bankName: 'CIMB Niaga Syariah',
    branch: 'KCP Cipinang Jakarta',
    accountNumber: '8055667788',
    accountHolder: 'Lembaga ZISWAF',
    balance: 880_000_000,
    primary: false,
    updatedAt: '2026-05-18',
  },
  {
    id: 'bk-4',
    bankName: 'Bank Mandiri',
    branch: 'KCU Sudirman Jakarta',
    accountNumber: '1230009988',
    accountHolder: 'Lembaga ZISWAF · Dana Wakaf',
    balance: 425_000_000,
    primary: false,
    updatedAt: '2026-05-17',
  },
  {
    id: 'bk-5',
    bankName: 'BCA Syariah',
    branch: 'KCP Cikini Jakarta',
    accountNumber: '0091122334',
    accountHolder: 'Lembaga ZISWAF · Operasional',
    balance: 132_000_000,
    primary: false,
    updatedAt: '2026-05-15',
  },
]

const stats = computed(() => {
  const total = accounts.reduce((s, a) => s + a.balance, 0)
  const banks = new Set(accounts.map((a) => a.bankName)).size
  const lastUpdate = accounts
    .map((a) => a.updatedAt)
    .sort()
    .at(-1) as string
  return { total, accounts: accounts.length, banks, lastUpdate }
})

interface BankSubmission {
  id: number
  status: 'DRAFT' | 'PENDING' | 'AUTHORIZED' | 'REJECTED'
  payload: {
    bank_name?: string
    account_number?: string
    account_holder?: string
    branch?: string | null
  }
}

const toast = useToast()
const submissions = ref<BankSubmission[]>([])
const showAddModal = shallowRef(false)
const submitting = shallowRef(false)
const newBank = reactive({ bank_name: '', account_number: '', account_holder: '', branch: '' })

async function loadSubmissions() {
  try {
    const res = await api.get<{ rows: BankSubmission[] }>(
      '/api/otorisasi/my-submissions/?entity_type=bank',
    )
    submissions.value = res.rows ?? []
  } catch {
    // silent
  }
}

async function submitNewBank() {
  if (!newBank.bank_name || !newBank.account_number || !newBank.account_holder) {
    toast.error('Nama bank, nomor rekening, dan nama pemilik wajib diisi')
    return
  }
  submitting.value = true
  try {
    await api.post('/api/otorisasi/submission/', {
      entity_type: 'bank',
      module: 'keuangan',
      payload: {
        bank_name: newBank.bank_name,
        account_number: newBank.account_number,
        account_holder: newBank.account_holder,
        branch: newBank.branch || null,
      },
    })
    toast.success('Permintaan tambah rekening bank disubmit untuk otorisasi')
    showAddModal.value = false
    newBank.bank_name = ''
    newBank.account_number = ''
    newBank.account_holder = ''
    newBank.branch = ''
    await loadSubmissions()
  } catch (e: unknown) {
    toast.error(e instanceof Error ? e.message : 'Gagal mengirim submission')
  } finally {
    submitting.value = false
  }
}

onMounted(loadSubmissions)
</script>

<template>
  <div class="space-y-6">
    <header class="flex flex-wrap items-start justify-between gap-3">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Manajemen Bank</h1>
        <p class="text-sm text-muted">
          Daftar rekening bank dengan saldo dan informasi rekonsiliasi.
        </p>
      </div>
      <div class="flex gap-2">
        <Button variant="outline" class="gap-1.5" disabled title="Tersedia pada Fase 2">
          <RefreshCw class="w-4 h-4" />
          Sinkron
        </Button>
        <Button class="gap-1.5" @click="showAddModal = true">
          <Plus class="w-4 h-4" />
          Tambah Rekening
        </Button>
      </div>
    </header>

    <Alert>
      <span>
        <strong>Data dummy.</strong> Sinkronisasi saldo dengan H2H bank / open banking API akan
        diintegrasikan di Fase 2.
      </span>
    </Alert>

    <!-- Pending submissions -->
    <div v-if="submissions.length > 0" class="rounded-lg border border-amber-200 bg-amber-50 dark:bg-amber-900/10 dark:border-amber-800 p-3">
      <p class="mb-2 text-xs font-semibold uppercase tracking-wide text-amber-700 dark:text-amber-400">
        Permintaan Tambah Rekening Bank ({{ submissions.length }})
      </p>
      <div class="space-y-1">
        <div
          v-for="sub in submissions"
          :key="sub.id"
          class="flex items-center gap-3 rounded bg-white dark:bg-zinc-900 px-3 py-1.5 text-[11px] border border-border"
        >
          <span class="font-mono text-muted">#{{ sub.id }}</span>
          <span class="font-semibold">{{ sub.payload.bank_name }}</span>
          <span class="font-mono text-muted">{{ sub.payload.account_number }}</span>
          <span class="text-muted truncate flex-1">{{ sub.payload.account_holder }}</span>
          <StatusBadge :status="sub.status" />
        </div>
      </div>
    </div>

    <!-- Add Bank modal -->
    <Teleport to="body">
      <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
        <div class="w-full max-w-md rounded-xl border border-border bg-surface p-6 shadow-xl">
          <h2 class="mb-4 text-base font-semibold">Permintaan Tambah Rekening Bank</h2>
          <div class="space-y-3">
            <div>
              <label class="mb-1 block text-xs font-medium">Nama Bank <span class="text-red-500">*</span></label>
              <input
                v-model="newBank.bank_name"
                placeholder="mis. Bank Syariah Indonesia"
                class="h-8 w-full rounded border border-border bg-background px-2 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
            <div>
              <label class="mb-1 block text-xs font-medium">Nomor Rekening <span class="text-red-500">*</span></label>
              <input
                v-model="newBank.account_number"
                placeholder="Nomor rekening bank"
                class="h-8 w-full rounded border border-border bg-background px-2 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
            <div>
              <label class="mb-1 block text-xs font-medium">Nama Pemilik Rekening <span class="text-red-500">*</span></label>
              <input
                v-model="newBank.account_holder"
                placeholder="a.n. ..."
                class="h-8 w-full rounded border border-border bg-background px-2 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
            <div>
              <label class="mb-1 block text-xs font-medium">Cabang Bank</label>
              <input
                v-model="newBank.branch"
                placeholder="Cabang / KCP (opsional)"
                class="h-8 w-full rounded border border-border bg-background px-2 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
          </div>
          <p class="mt-3 text-[10px] text-muted">
            Permintaan ini disubmit ke sistem otorisasi. Rekening aktif setelah disetujui supervisor.
          </p>
          <div class="mt-4 flex justify-end gap-2">
            <Button variant="outline" size="sm" :disabled="submitting" @click="showAddModal = false">Batal</Button>
            <Button size="sm" :disabled="submitting" @click="submitNewBank">
              {{ submitting ? 'Mengirim...' : 'Submit Otorisasi' }}
            </Button>
          </div>
        </div>
      </div>
    </Teleport>

    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
      <Card>
        <CardContent class="p-4">
          <p class="text-xs uppercase tracking-wide text-muted">Total Saldo Bank</p>
          <p class="text-2xl font-bold tabular-nums text-positive">{{ formatIdr(stats.total) }}</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="p-4">
          <p class="text-xs uppercase tracking-wide text-muted">Jumlah Rekening</p>
          <p class="text-2xl font-bold tabular-nums">{{ stats.accounts }}</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="p-4">
          <p class="text-xs uppercase tracking-wide text-muted">Jumlah Bank</p>
          <p class="text-2xl font-bold tabular-nums">{{ stats.banks }}</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="p-4">
          <p class="text-xs uppercase tracking-wide text-muted">Update Terakhir</p>
          <p class="text-base font-semibold mt-1">{{ formatDate(stats.lastUpdate) }}</p>
        </CardContent>
      </Card>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <Card v-for="a in accounts" :key="a.id" class="overflow-hidden">
        <CardContent class="p-4 flex items-start gap-3">
          <div
            class="w-11 h-11 rounded-lg bg-primary/10 text-primary grid place-items-center shrink-0"
          >
            <Landmark class="w-5 h-5" />
          </div>
          <div class="min-w-0 flex-1">
            <div class="flex items-baseline gap-2">
              <h3 class="font-semibold text-foreground truncate">{{ a.bankName }}</h3>
              <span
                v-if="a.primary"
                class="text-[10px] uppercase tracking-wide bg-primary text-primary-foreground px-1.5 py-0.5 rounded font-medium shrink-0"
              >Utama</span>
            </div>
            <p class="text-xs text-muted truncate">{{ a.branch }}</p>
            <p class="text-sm font-mono tabular-nums mt-1">{{ a.accountNumber }}</p>
            <p class="text-xs text-muted truncate">a.n. {{ a.accountHolder }}</p>
          </div>
          <div class="text-right shrink-0">
            <p class="text-[10px] uppercase tracking-wide text-muted">Saldo</p>
            <p class="text-base font-bold tabular-nums whitespace-nowrap">{{ formatIdr(a.balance) }}</p>
            <p class="text-[10px] text-muted mt-1">{{ formatDate(a.updatedAt) }}</p>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
