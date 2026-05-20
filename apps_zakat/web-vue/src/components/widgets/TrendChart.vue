<script setup lang="ts">
import { computed } from 'vue'
import { Line } from 'vue-chartjs'

import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'

const props = defineProps<{
  labels: string[]
  penerimaan: number[]
  penyaluran: number[]
}>()

function formatIdr(n: number): string {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0,
  }).format(n)
}

function formatShortIdr(n: number): string {
  if (n >= 1e9) return 'Rp ' + (n / 1e9).toFixed(1) + ' M'
  if (n >= 1e6) return 'Rp ' + (n / 1e6).toFixed(0) + ' jt'
  if (n >= 1e3) return 'Rp ' + (n / 1e3).toFixed(0) + ' rb'
  return 'Rp ' + n
}

const chartData = computed(() => ({
  labels: props.labels,
  datasets: [
    {
      label: 'Penerimaan',
      data: props.penerimaan,
      borderColor: '#1976d2',
      backgroundColor: 'rgba(25, 118, 210, 0.10)',
      fill: true,
      tension: 0.35,
      pointRadius: 3,
      pointHoverRadius: 5,
      borderWidth: 2,
    },
    {
      label: 'Penyaluran',
      data: props.penyaluran,
      borderColor: '#d97706',
      backgroundColor: 'rgba(217, 119, 6, 0.08)',
      fill: true,
      tension: 0.35,
      pointRadius: 3,
      pointHoverRadius: 5,
      borderWidth: 2,
    },
  ],
}))

const options = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index' as const, intersect: false },
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: {
        color: 'rgba(120, 120, 120, 0.9)',
        boxWidth: 12,
        boxHeight: 12,
        usePointStyle: true,
      },
    },
    tooltip: {
      callbacks: {
        label: (ctx: { dataset: { label?: string }; parsed: { y: number } }) =>
          `${ctx.dataset.label}: ${formatIdr(ctx.parsed.y)}`,
      },
    },
  },
  scales: {
    x: {
      grid: { color: 'rgba(128, 128, 128, 0.12)' },
      ticks: { color: 'rgba(120, 120, 120, 0.9)' },
    },
    y: {
      grid: { color: 'rgba(128, 128, 128, 0.12)' },
      ticks: {
        color: 'rgba(120, 120, 120, 0.9)',
        callback: (v: string | number) => formatShortIdr(Number(v)),
      },
    },
  },
}))
</script>

<template>
  <Card class="h-full">
    <CardHeader>
      <CardTitle>Tren 6 Bulan</CardTitle>
      <CardDescription>Penerimaan vs Penyaluran</CardDescription>
    </CardHeader>
    <CardContent>
      <div class="h-64">
        <Line :data="chartData" :options="options" />
      </div>
    </CardContent>
  </Card>
</template>
