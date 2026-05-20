<script setup lang="ts">
defineProps<{
  label: string
  amount: number
  period: string
  accent?: 'in' | 'out'
}>()

function formatIdr(n: number): string {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(n)
}
</script>

<template>
  <article class="widget card" :class="accent">
    <header class="widget-head">
      <span class="muted">{{ label }}</span>
      <span class="period">{{ period }}</span>
    </header>
    <p class="amount">{{ formatIdr(amount) }}</p>
  </article>
</template>

<style scoped>
.widget { display: flex; flex-direction: column; gap: 0.5rem; min-height: 130px; }
.widget-head { display: flex; justify-content: space-between; align-items: baseline; }
.muted { color: var(--color-text-muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.04em; }
.period { font-size: 0.75rem; color: var(--color-text-muted); }
.amount { font-size: 1.6rem; font-weight: 600; margin: 0; }
.widget.in .amount { color: var(--color-primary); }
.widget.out .amount { color: #ad6800; }
</style>
