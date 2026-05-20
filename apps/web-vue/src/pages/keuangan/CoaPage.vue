<script setup lang="ts">
import { Plus, Search } from 'lucide-vue-next'
import { computed, ref } from 'vue'

import Alert from '@/components/ui/Alert.vue'
import Button from '@/components/ui/Button.vue'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import Input from '@/components/ui/Input.vue'
import { formatIdr } from '@/lib/format'

interface CoaRow {
  code: string
  name: string
  type: 'Aset' | 'Kewajiban' | 'Modal' | 'Pendapatan' | 'Beban'
  parent: string | null
  balance: number
}

const rows: CoaRow[] = [
  { code: '1-1000', name: 'Kas', type: 'Aset', parent: null, balance: 357_500_000 },
  { code: '1-1100', name: 'Kas Kecil Operasional', type: 'Aset', parent: '1-1000', balance: 25_000_000 },
  { code: '1-1200', name: 'Kas Penyaluran', type: 'Aset', parent: '1-1000', balance: 320_000_000 },
  { code: '1-1300', name: 'Kas Booth Event', type: 'Aset', parent: '1-1000', balance: 12_500_000 },
  { code: '1-2000', name: 'Bank', type: 'Aset', parent: null, balance: 3_450_000_000 },
  { code: '1-2100', name: 'Bank Syariah Indonesia', type: 'Aset', parent: '1-2000', balance: 1_850_000_000 },
  { code: '1-2200', name: 'Bank Muamalat', type: 'Aset', parent: '1-2000', balance: 720_000_000 },
  { code: '1-2300', name: 'CIMB Niaga Syariah', type: 'Aset', parent: '1-2000', balance: 880_000_000 },
  { code: '2-1000', name: 'Kewajiban Jangka Pendek', type: 'Kewajiban', parent: null, balance: 18_500_000 },
  { code: '3-1000', name: 'Dana Zakat', type: 'Modal', parent: null, balance: 2_100_000_000 },
  { code: '3-2000', name: 'Dana Infaq & Sadaqah', type: 'Modal', parent: null, balance: 1_450_000_000 },
  { code: '3-3000', name: 'Dana Wakaf', type: 'Modal', parent: null, balance: 1_250_000_000 },
  { code: '3-4000', name: 'Dana Amil', type: 'Modal', parent: null, balance: 87_500_000 },
  { code: '4-1000', name: 'Penerimaan Zakat', type: 'Pendapatan', parent: null, balance: 1_250_000_000 },
  { code: '4-2000', name: 'Penerimaan Infaq', type: 'Pendapatan', parent: null, balance: 480_000_000 },
  { code: '4-3000', name: 'Penerimaan Wakaf', type: 'Pendapatan', parent: null, balance: 320_000_000 },
  { code: '5-1000', name: 'Penyaluran Zakat - Fakir', type: 'Beban', parent: null, balance: 245_000_000 },
  { code: '5-2000', name: 'Penyaluran Zakat - Miskin', type: 'Beban', parent: null, balance: 198_000_000 },
  { code: '5-3000', name: 'Beban Operasional Amil', type: 'Beban', parent: null, balance: 87_500_000 },
]

const search = ref('')

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return rows
  return rows.filter(
    (r) =>
      r.code.toLowerCase().includes(q) ||
      r.name.toLowerCase().includes(q) ||
      r.type.toLowerCase().includes(q),
  )
})

const stats = computed(() => {
  const byType = (t: CoaRow['type']) => rows.filter((r) => r.type === t).length
  return {
    total: rows.length,
    aset: byType('Aset'),
    modal: byType('Modal'),
    pendapatanBeban: byType('Pendapatan') + byType('Beban'),
  }
})

function typeColor(t: CoaRow['type']): string {
  switch (t) {
    case 'Aset':
      return 'bg-primary/10 text-primary'
    case 'Kewajiban':
      return 'bg-warning/15 text-warning'
    case 'Modal':
      return 'bg-accent/15 text-accent'
    case 'Pendapatan':
      return 'bg-positive/15 text-positive'
    case 'Beban':
      return 'bg-destructive/10 text-destructive'
  }
}
</script>

<template>
  <div class="space-y-6">
    <header class="flex flex-wrap items-start justify-between gap-3">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Chart of Accounts</h1>
        <p class="text-sm text-muted">
          Daftar akun perkiraan dan struktur kode akun ZISWAF.
        </p>
      </div>
      <Button class="gap-1.5" disabled title="Tersedia pada Fase 2">
        <Plus class="w-4 h-4" />
        Tambah Akun
      </Button>
    </header>

    <Alert>
      <span>
        <strong>Data dummy.</strong> Modul Keuangan akan terhubung ke existing DB pada Fase 2.
        Kode akun mengikuti standar PSAK 109 (Akuntansi Zakat & Infaq/Sedekah).
      </span>
    </Alert>

    <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
      <Card>
        <CardContent class="p-4">
          <p class="text-xs uppercase tracking-wide text-muted">Total Akun</p>
          <p class="text-2xl font-bold tabular-nums">{{ stats.total }}</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="p-4">
          <p class="text-xs uppercase tracking-wide text-muted">Aset</p>
          <p class="text-2xl font-bold tabular-nums text-primary">{{ stats.aset }}</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="p-4">
          <p class="text-xs uppercase tracking-wide text-muted">Dana / Modal</p>
          <p class="text-2xl font-bold tabular-nums text-accent">{{ stats.modal }}</p>
        </CardContent>
      </Card>
      <Card>
        <CardContent class="p-4">
          <p class="text-xs uppercase tracking-wide text-muted">Pendapatan + Beban</p>
          <p class="text-2xl font-bold tabular-nums">{{ stats.pendapatanBeban }}</p>
        </CardContent>
      </Card>
    </div>

    <Card>
      <CardContent class="p-0">
        <div class="px-4 py-3 border-b border-border flex items-center gap-2">
          <Search class="w-4 h-4 text-muted shrink-0" />
          <Input
            v-model="search"
            placeholder="Cari kode atau nama akun…"
            class="h-8 border-0 focus-visible:ring-0 focus-visible:ring-offset-0 bg-transparent p-0"
          />
          <span class="text-xs text-muted whitespace-nowrap">{{ filtered.length }} dari {{ rows.length }}</span>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="text-xs text-muted uppercase tracking-wide">
              <tr class="border-b border-border">
                <th class="text-left px-4 py-2 font-medium w-24">Kode</th>
                <th class="text-left px-4 py-2 font-medium">Nama Akun</th>
                <th class="text-left px-4 py-2 font-medium w-32">Tipe</th>
                <th class="text-left px-4 py-2 font-medium w-24 max-md:hidden">Parent</th>
                <th class="text-right px-4 py-2 font-medium">Saldo</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="r in filtered"
                :key="r.code"
                class="border-b border-border last:border-0 hover:bg-background/60"
              >
                <td class="px-4 py-2 font-mono text-xs tabular-nums whitespace-nowrap">{{ r.code }}</td>
                <td class="px-4 py-2">
                  <span :class="r.parent ? 'pl-4 text-foreground' : 'font-medium'">{{ r.name }}</span>
                </td>
                <td class="px-4 py-2">
                  <span
                    class="text-[10px] uppercase tracking-wide px-2 py-0.5 rounded font-medium"
                    :class="typeColor(r.type)"
                  >{{ r.type }}</span>
                </td>
                <td class="px-4 py-2 text-xs text-muted tabular-nums max-md:hidden">{{ r.parent ?? '—' }}</td>
                <td class="px-4 py-2 text-right font-medium tabular-nums whitespace-nowrap">
                  {{ formatIdr(r.balance) }}
                </td>
              </tr>
              <tr v-if="filtered.length === 0">
                <td colspan="5" class="px-4 py-8 text-center text-sm text-muted">
                  Tidak ada akun cocok dengan pencarian.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
