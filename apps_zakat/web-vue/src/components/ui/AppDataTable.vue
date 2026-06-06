<script setup lang="ts">
import DataTable from 'primevue/datatable'

defineOptions({ inheritAttrs: false })

const pt = {
  root: { class: 'overflow-x-auto' },
  table: { class: 'w-full text-[11px]' },
  thead: { class: 'text-[10px] text-muted uppercase tracking-widest border-b border-border bg-background/50' },
  headerRow: { class: '' },
  headerCell: { class: 'text-left px-3 py-1 font-semibold whitespace-nowrap' },
  tbody: { class: '' },
  row: { class: 'border-b border-border/40 hover:bg-muted/5 transition-colors' },
  bodyCell: { class: 'px-3 py-1' },
  emptyMessageCell: { class: 'p-10 text-center text-sm text-muted italic' },
  loadingOverlay: { class: 'absolute inset-0 flex items-center justify-center bg-surface/80 z-10' },
  loadingIcon: { class: 'w-7 h-7 animate-spin text-primary' },
}
</script>

<template>
  <DataTable v-bind="$attrs" :pt="pt">
    <slot />
    <template v-if="$slots.empty" #empty>
      <slot name="empty" />
    </template>
  </DataTable>
</template>
