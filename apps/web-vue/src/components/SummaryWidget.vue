<script setup lang="ts">
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardHeader from '@/components/ui/CardHeader.vue'

defineProps<{
  label: string
  amount: number
  period: string
  accent?: 'in' | 'out'
}>()

function formatIdr(n: number): string {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0,
  }).format(n)
}
</script>

<template>
  <Card>
    <CardHeader class="pb-2">
      <div class="flex items-baseline justify-between gap-2">
        <CardDescription class="uppercase tracking-wide text-xs">
          {{ label }}
        </CardDescription>
        <span class="text-xs text-muted">{{ period }}</span>
      </div>
    </CardHeader>
    <CardContent>
      <div
        class="text-2xl sm:text-3xl font-bold tabular-nums"
        :class="accent === 'in' ? 'text-positive' : accent === 'out' ? 'text-warning' : ''"
      >
        {{ formatIdr(amount) }}
      </div>
    </CardContent>
  </Card>
</template>
