<script setup lang="ts">
import { TrendingDown, TrendingUp } from 'lucide-vue-next'
import { computed } from 'vue'

import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'

const props = defineProps<{
  label: string
  amount: number
  deltaPct: number
  format?: 'currency' | 'count'
}>()

const formatted = computed(() => {
  if (props.format === 'count') {
    return new Intl.NumberFormat('id-ID').format(props.amount)
  }
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0,
  }).format(props.amount)
})

const positive = computed(() => props.deltaPct >= 0)
</script>

<template>
  <Card>
    <CardContent class="p-5 flex flex-col gap-2">
      <div class="text-xs uppercase tracking-wide text-muted">{{ label }}</div>
      <div class="text-2xl sm:text-3xl font-bold tabular-nums">{{ formatted }}</div>
      <div class="flex items-center gap-1 text-xs">
        <TrendingUp v-if="positive" class="w-3.5 h-3.5 text-positive" />
        <TrendingDown v-else class="w-3.5 h-3.5 text-destructive" />
        <span
          class="tabular-nums"
          :class="positive ? 'text-positive' : 'text-destructive'"
        >
          {{ positive ? '+' : '' }}{{ deltaPct.toFixed(1) }}%
        </span>
        <span class="text-muted">vs bulan lalu</span>
      </div>
    </CardContent>
  </Card>
</template>
