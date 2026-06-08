<script setup lang="ts">
defineProps<{ status: 'DRAFT' | 'PENDING' | 'AUTHORIZED' | 'REJECTED' }>()

const config = {
  DRAFT:      { label: 'Draft',        class: 'bg-gray-100 text-gray-600' },
  PENDING:    { label: 'Menunggu',     class: 'bg-yellow-100 text-yellow-700' },
  AUTHORIZED: { label: 'Terotorisasi', class: 'bg-green-100 text-green-700' },
  REJECTED:   { label: 'Ditolak',      class: 'bg-red-100 text-red-700' },
} as const
</script>

<template>
  <span :class="['inline-flex items-center px-2 py-0.5 rounded text-xs font-medium', config[status].class]">
    {{ config[status].label }}
  </span>
</template>
