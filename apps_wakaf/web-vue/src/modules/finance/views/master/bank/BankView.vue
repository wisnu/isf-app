<script setup lang="ts">
import { Landmark, Plus, RefreshCw } from 'lucide-vue-next'
import { computed } from 'vue'

import Alert from '@/shared/components/Alert.vue'
import Button from '@/shared/components/Button.vue'
import Card from '@/shared/components/Card.vue'
import CardContent from '@/shared/components/CardContent.vue'
import { formatDate, formatIdr } from '@/shared/utils/format'

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
        <Button class="gap-1.5" disabled title="Tersedia pada Fase 2">
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
