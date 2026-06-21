<script setup lang="ts">
defineProps<{
  title: string
  subtitle?: string
  statusCode?: string  // ditampilkan sebagai <code> inline dengan dot hijau
}>()
</script>

<template>
  <header class="flex flex-wrap items-center justify-between gap-2">
    <div>
      <div class="flex items-center gap-2">
        <h1 class="text-lg font-bold tracking-tight">{{ title }}</h1>
        <slot name="status">
          <span v-if="statusCode" class="inline-flex items-center gap-1 text-[10px] font-medium text-muted">
            <span class="w-1.5 h-1.5 rounded-full bg-positive shrink-0"></span>
            <code class="font-mono">{{ statusCode }}</code>
          </span>
        </slot>
      </div>
      <p v-if="subtitle" class="text-xs text-muted">{{ subtitle }}</p>
    </div>
    <div class="flex flex-wrap gap-1.5">
      <slot name="actions" />
    </div>
  </header>
</template>
