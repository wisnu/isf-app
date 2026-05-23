<script setup lang="ts">
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'

import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'

interface AsnafItem {
  label: string
  value: number
}

const props = defineProps<{
  items: AsnafItem[]
  valueFormat?: 'currency' | 'count'
}>()

const PALETTE = [
  '#1976d2',
  '#0f766e',
  '#16a34a',
  '#d97706',
  '#9333ea',
  '#db2777',
  '#0891b2',
  '#ca8a04',
]

function formatValue(n: number): string {
  if (props.valueFormat === 'count') {
    return new Intl.NumberFormat('id-ID').format(n)
  }
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0,
  }).format(n)
}

const chartData = computed(() => ({
  labels: props.items.map((i) => i.label),
  datasets: [
    {
      data: props.items.map((i) => i.value),
      backgroundColor: PALETTE,
      borderWidth: 0,
      hoverOffset: 6,
    },
  ],
}))

const options = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  cutout: '62%',
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: {
        color: 'rgba(120, 120, 120, 0.9)',
        boxWidth: 10,
        boxHeight: 10,
        font: { size: 11 },
        usePointStyle: true,
        padding: 8,
      },
    },
    tooltip: {
      callbacks: {
        label: (ctx: { label?: string; parsed: number }) =>
          `${ctx.label}: ${formatValue(ctx.parsed)}`,
      },
    },
  },
}))
</script>

<template>
  <Card class="h-full">
    <CardHeader>
      <CardTitle>Distribusi Asnaf</CardTitle>
      <CardDescription>Penyaluran zakat per kategori</CardDescription>
    </CardHeader>
    <CardContent>
      <div class="h-72">
        <Doughnut :data="chartData" :options="options" />
      </div>
    </CardContent>
  </Card>
</template>
