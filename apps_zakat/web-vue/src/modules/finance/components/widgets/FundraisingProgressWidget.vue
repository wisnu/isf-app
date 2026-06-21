<script setup lang="ts">
import Card from '@/shared/components/Card.vue'
import CardContent from '@/shared/components/CardContent.vue'
import CardDescription from '@/shared/components/CardDescription.vue'
import CardHeader from '@/shared/components/CardHeader.vue'
import CardTitle from '@/shared/components/CardTitle.vue'

interface Channel {
  label: string
  actual: number
  target: number
}

defineProps<{ items: Channel[] }>()

function pct(actual: number, target: number): number {
  if (target <= 0) return 0
  return Math.min(150, Math.round((actual / target) * 100))
}

function clampWidth(actual: number, target: number): string {
  return Math.min(100, pct(actual, target)) + '%'
}

function formatIdr(n: number): string {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0,
  }).format(n)
}
</script>

<template>
  <Card class="h-full">
    <CardHeader>
      <CardTitle>Capaian Channel</CardTitle>
      <CardDescription>Realisasi vs target periode berjalan</CardDescription>
    </CardHeader>
    <CardContent class="space-y-4">
      <div v-for="ch in items" :key="ch.label" class="space-y-1.5">
        <div class="flex items-baseline justify-between gap-2">
          <span class="text-sm font-medium truncate">{{ ch.label }}</span>
          <span
            class="text-xs tabular-nums"
            :class="ch.actual >= ch.target ? 'text-positive font-medium' : 'text-muted'"
          >
            {{ pct(ch.actual, ch.target) }}%
          </span>
        </div>
        <div class="h-2 bg-background rounded-full overflow-hidden">
          <div
            class="h-full rounded-full transition-[width] duration-500"
            :class="ch.actual >= ch.target ? 'bg-positive' : 'bg-primary'"
            :style="{ width: clampWidth(ch.actual, ch.target) }"
          />
        </div>
        <div class="flex justify-between text-xs text-muted tabular-nums">
          <span>{{ formatIdr(ch.actual) }}</span>
          <span>target {{ formatIdr(ch.target) }}</span>
        </div>
      </div>
    </CardContent>
  </Card>
</template>
