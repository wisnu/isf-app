<script setup lang="ts">
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
  <q-card flat bordered class="summary-widget">
    <q-card-section>
      <div class="row items-baseline justify-between">
        <div class="text-overline text-grey">{{ label }}</div>
        <div class="text-caption text-grey">{{ period }}</div>
      </div>
      <div
        class="text-h5 q-mt-sm text-weight-bold"
        :class="accent === 'in' ? 'text-positive' : accent === 'out' ? 'text-warning' : ''"
      >
        {{ formatIdr(amount) }}
      </div>
    </q-card-section>
  </q-card>
</template>

<style scoped>
.summary-widget {
  min-height: 120px;
}
</style>
