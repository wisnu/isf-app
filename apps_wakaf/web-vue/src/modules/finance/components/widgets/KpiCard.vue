<script setup lang="ts">
import { AlertTriangle, Loader2, TrendingDown, TrendingUp } from 'lucide-vue-next'
import { computed } from 'vue'

import Card from '@/shared/components/Card.vue'
import CardContent from '@/shared/components/CardContent.vue'

const props = withDefaults(
  defineProps<{
    label: string
    amount: number
    deltaPct: number
    format?: 'currency' | 'count'
    loading?: boolean
    error?: boolean
    errorMessage?: string
  }>(),
  { loading: false, error: false },
)

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
    <CardContent class="p-5 flex flex-col gap-2 min-h-[7rem]">
      <div class="text-xs uppercase tracking-wide text-muted">{{ label }}</div>
      <template v-if="loading">
        <div class="flex items-center gap-2 text-muted text-sm py-2">
          <Loader2 class="w-4 h-4 animate-spin" />
          Memuat...
        </div>
      </template>
      <template v-else-if="error">
        <div class="flex items-start gap-2 text-destructive text-sm py-2">
          <AlertTriangle class="w-4 h-4 mt-0.5 shrink-0" />
          <div class="min-w-0">
            <p class="font-medium">Gagal memuat</p>
            <p v-if="errorMessage" class="text-xs text-muted truncate" :title="errorMessage">
              {{ errorMessage }}
            </p>
          </div>
        </div>
        <div class="text-2xl sm:text-3xl font-bold tabular-nums text-muted">—</div>
      </template>
      <template v-else>
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
      </template>
    </CardContent>
  </Card>
</template>
