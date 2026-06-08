<script setup lang="ts">
import DataTable from 'primevue/datatable'
import { computed } from 'vue'

defineOptions({ inheritAttrs: false })

const props = defineProps<{ compact?: boolean }>()

const pt = computed(() => ({
  root: { class: 'overflow-x-auto relative' },
  table: { class: 'w-full text-[11px]' },
  thead: { class: 'text-[10px] text-muted uppercase tracking-widest border-b border-border' },
  headerRow: { class: '' },
  headerCell: { class: 'text-left px-4 py-2 font-medium whitespace-nowrap' },
  tbody: { class: '' },
  row: { class: 'border-b border-border last:border-0 hover:bg-background/60 transition-colors' },
  bodyCell: { class: `px-4 ${props.compact ? 'py-1' : 'py-1.5'} overflow-hidden` },
  emptyMessageCell: { class: 'p-10 text-center text-sm text-muted italic' },
  loadingOverlay: { class: 'absolute inset-0 flex items-center justify-center bg-surface/80 z-10' },
  loadingIcon: { class: 'w-7 h-7 animate-spin text-primary' },
  // Column filter popup
  filterOverlay: { class: 'z-50 bg-surface border border-border rounded-xl shadow-xl p-3 min-w-[180px] text-[11px]' },
  filterConstraint: { class: 'flex flex-col gap-2' },
  filterInput: { class: 'w-full rounded-lg border border-border bg-surface px-2 py-1.5 text-[11px] focus:outline-none focus:ring-1 focus:ring-primary' },
  filterButtonbar: { class: 'flex items-center justify-end gap-2 mt-2 pt-2 border-t border-border' },
  pcFilterClearButton: {
    root: { class: 'text-[10px] text-muted hover:text-foreground px-2 py-1 rounded border border-border transition-colors cursor-pointer' },
  },
  pcFilterApplyButton: {
    root: { class: 'text-[10px] bg-primary text-primary-foreground px-2 py-1 rounded transition-colors cursor-pointer' },
  },
  // Filter icon button in column header
  pcColumnFilterButton: {
    root: { class: 'ml-1 p-0.5 rounded text-muted/50 hover:text-primary transition-colors cursor-pointer inline-flex items-center' },
  },
  columnFilterButtonIcon: { class: 'w-2.5 h-2.5' },
}))
</script>

<template>
  <DataTable v-bind="$attrs" :pt="pt">
    <slot />
    <template v-if="$slots.empty" #empty>
      <slot name="empty" />
    </template>
    <template v-if="$slots.footer" #footer>
      <slot name="footer" />
    </template>
  </DataTable>
</template>
