<script setup lang="ts">
import { shallowRef } from 'vue'

import PeriodFilter from '@/shared/components/PeriodFilter.vue'
import Card from '@/shared/components/Card.vue'
import CardHeader from '@/shared/components/CardHeader.vue'
import CardTitle from '@/shared/components/CardTitle.vue'
import CardContent from '@/shared/components/CardContent.vue'
import KpiCard from '@/modules/finance/components/widgets/KpiCardWidget.vue'
import TrendChart from '@/modules/finance/components/widgets/TrendChartWidget.vue'

const bulan = shallowRef(new Date().getMonth() + 1)
const tahun = shallowRef(new Date().getFullYear())

// KPI cards
const kpis = {
  realization: 1_250_000_000,
  target: 1_500_000_000,
  pctTarget: 83.3,
  donaturAktif: 342,
  donaturBaru: 28,
  donaturHC: 156,
  konfirmasiPending: 7,
}

// Trend 6 bulan: realization vs target
const trendLabels = ['2025-12', '2026-01', '2026-02', '2026-03', '2026-04', '2026-05']
const trendRealisasi = [980_000_000, 1_050_000_000, 1_100_000_000, 1_180_000_000, 1_200_000_000, 1_250_000_000]
const trendTarget = [1_200_000_000, 1_200_000_000, 1_200_000_000, 1_500_000_000, 1_500_000_000, 1_500_000_000]

// Top donatur
const topDonatur = [
  { nama: 'PT Maju Bersama', jenis: 'Korporat', produk: 'Zakat Maal', nominal: 150_000_000 },
  { nama: 'Ahmad Fauzi', jenis: 'Individu', produk: 'Zakat Maal', nominal: 85_000_000 },
  { nama: 'Yayasan Harapan', jenis: 'Korporat', produk: 'Infaq', nominal: 60_000_000 },
  { nama: 'Siti Rahayu', jenis: 'Individu', produk: 'Sedekah', nominal: 45_000_000 },
  { nama: 'CV Berkah Jaya', jenis: 'Korporat', produk: 'Zakat Maal', nominal: 40_000_000 },
]

function formatIdr(v: number): string {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(v)
}
</script>

<template>
  <div class="space-y-6">
    <!-- Header + period filter -->
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Dashboard Penghimpunan ZIS</h1>
        <p class="text-sm text-muted">Periode {{ tahun }}-{{ String(bulan).padStart(2, '0') }} · Data simulasi</p>
      </div>
      <PeriodFilter v-model:bulan="bulan" v-model:tahun="tahun" />
    </div>

    <!-- Row 1: 4 KPI cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <KpiCard
        label="Realisasi Penghimpunan"
        :amount="kpis.realization"
        :delta-pct="kpis.pctTarget"
        format="currency"
      />
      <KpiCard
        label="Total Donatur Aktif"
        :amount="kpis.donaturAktif"
        :delta-pct="0"
        format="count"
      />
      <KpiCard
        label="Donatur HC/Payroll"
        :amount="kpis.donaturHC"
        :delta-pct="0"
        format="count"
      />
      <KpiCard
        label="Konfirmasi Pending"
        :amount="kpis.konfirmasiPending"
        :delta-pct="0"
        format="count"
      />
    </div>

    <!-- Row 2: Trend realization vs target (full width) -->
    <TrendChart
      :labels="trendLabels"
      :collection="trendRealisasi"
      :distribution="trendTarget"
    />

    <!-- Row 3: Top Donatur -->
    <Card>
      <CardHeader class="pb-2">
        <CardTitle>Top Donatur Bulan Ini</CardTitle>
      </CardHeader>
      <CardContent class="p-5 pt-0">
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <tbody class="divide-y divide-border">
              <tr v-for="d in topDonatur" :key="d.nama">
                <td class="py-2 pr-3 font-medium text-foreground">{{ d.nama }}</td>
                <td class="py-2 pr-3">
                  <span
                    class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
                    :class="d.jenis === 'Korporat' ? 'bg-purple-100 text-purple-700' : 'bg-blue-100 text-blue-700'"
                  >
                    {{ d.jenis }}
                  </span>
                </td>
                <td class="py-2 pr-3 text-muted text-xs">{{ d.produk }}</td>
                <td class="py-2 text-right tabular-nums font-medium">{{ formatIdr(d.nominal) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  </div>
</template>
