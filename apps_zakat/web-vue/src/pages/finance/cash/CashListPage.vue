<script setup lang="ts">
import { Banknote, Plus } from 'lucide-vue-next'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import PageHeader from '@/components/layout/PageHeader.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import { formatIdr } from '@/shared/utils/format'
import { dmy } from '@/shared/utils/date'

interface KasAccount {
  id: string
  code: string
  name: string
  holder: string
  balance: number
  updatedAt: string
  active: boolean
}

const accounts: KasAccount[] = [
  {
    id: 'kas-1',
    code: '1-1100',
    name: 'Kas Kecil Operasional',
    holder: 'Bendahara · Siti Aminah',
    balance: 25_000_000,
    updatedAt: '2026-05-19',
    active: true,
  },
  {
    id: 'kas-2',
    code: '1-1200',
    name: 'Kas Penyaluran Asnaf',
    holder: 'Tim Penyaluran · Ahmad Faisal',
    balance: 320_000_000,
    updatedAt: '2026-05-18',
    active: true,
  },
  {
    id: 'kas-3',
    code: '1-1300',
    name: 'Kas Booth Event Ramadhan',
    holder: 'Tim Penghimpunan · Rina Wijaya',
    balance: 12_500_000,
    updatedAt: '2026-05-19',
    active: true,
  },
  {
    id: 'kas-4',
    code: '1-1400',
    name: 'Kas Program Wakaf Produktif',
    holder: 'Tim Wakaf · Budi Setiawan',
    balance: 8_750_000,
    updatedAt: '2026-05-17',
    active: true,
  },
  {
    id: 'kas-5',
    code: '1-1500',
    name: 'Kas Cadangan Lebaran 2026',
    holder: 'Bendahara · Siti Aminah',
    balance: 0,
    updatedAt: '2026-04-30',
    active: false,
  },
]

const router = useRouter()

const stats = computed(() => ({
  totalBalance: accounts.filter((a) => a.active).reduce((s, a) => s + a.balance, 0),
  totalAccounts: accounts.length,
  active: accounts.filter((a) => a.active).length,
}))
</script>

<template>
  <div class="space-y-6">
    <PageHeader title="Manajemen Kas" subtitle="Daftar brankas/kas fisik beserta saldo, pemegang, dan tanggal mutasi terakhir.">
      <template #actions>
        <Button size="sm" class="gap-1.5 h-8 text-xs" @click="router.push({ name: 'finance-cash-create' })">
          <Plus class="w-3.5 h-3.5" />
          Tambah Kas
        </Button>
      </template>
    </PageHeader>

    <Alert>
      <span>
        <strong>Data dummy.</strong> Mutasi kas (input/output) akan terhubung ke modul transaksi
        keuangan di Fase 2.
      </span>
    </Alert>

    <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
      <Card>
        <CardContent class="p-4">
          <p class="text-xs uppercase tracking-wide text-muted">Total Saldo Kas</p>
          <p class="text-2xl font-bold tabular-nums text-positive">{{ formatIdr(stats.totalBalance) }}</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="p-4">
          <p class="text-xs uppercase tracking-wide text-muted">Brankas Aktif</p>
          <p class="text-2xl font-bold tabular-nums">{{ stats.active }} / {{ stats.totalAccounts }}</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="p-4 flex items-center gap-3">
          <div
            class="w-10 h-10 rounded-full bg-primary/10 text-primary grid place-items-center shrink-0"
          >
            <Banknote class="w-5 h-5" />
          </div>
          <div>
            <p class="text-xs uppercase tracking-wide text-muted">Mata Uang</p>
            <p class="text-base font-semibold">Rupiah (IDR)</p>
          </div>
        </CardContent>
      </Card>
    </div>

    <Card>
      <CardContent class="p-0">
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border">
              <tr class="border-b border-border">
                <th class="text-left px-4 py-2 font-medium w-24">Kode</th>
                <th class="text-left px-4 py-2 font-medium">Nama Kas</th>
                <th class="text-left px-4 py-2 font-medium max-md:hidden">Pemegang</th>
                <th class="text-right px-4 py-2 font-medium">Saldo</th>
                <th class="text-left px-4 py-2 font-medium max-md:hidden whitespace-nowrap">Update Terakhir</th>
                <th class="text-center px-4 py-2 font-medium w-20">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="a in accounts"
                :key="a.id"
                class="border-b border-border last:border-0 hover:bg-background/60"
                :class="{ 'opacity-60': !a.active }"
              >
                <td class="px-4 py-1 font-mono text-[11px] tabular-nums whitespace-nowrap">{{ a.code }}</td>
                <td class="px-4 py-1 font-medium text-[11px]">{{ a.name }}</td>
                <td class="px-4 py-1 text-muted text-[11px] max-md:hidden">{{ a.holder }}</td>
                <td class="px-4 py-1 text-right font-medium tabular-nums whitespace-nowrap">
                  {{ formatIdr(a.balance) }}
                </td>
                <td class="px-4 py-1 text-muted text-[11px] max-md:hidden whitespace-nowrap">
                  {{ dmy(a.updatedAt) }}
                </td>
                <td class="px-4 py-1 text-center">
                  <span
                    class="text-[10px] uppercase tracking-wide px-2 py-0.5 rounded font-medium"
                    :class="
                      a.active
                        ? 'bg-positive/15 text-positive'
                        : 'bg-background text-muted border border-border'
                    "
                  >{{ a.active ? 'Aktif' : 'Non-aktif' }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
