<script setup lang="ts">
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'

const props = defineProps<{
  page: number
  totalPages: number
  total?: number
  loading?: boolean
  unit?: string
}>()

const emit = defineEmits<{
  prev: []
  next: []
}>()
</script>

<template>
  <div class="flex items-center gap-3">
    <span v-if="total !== undefined" class="text-[11px] text-muted tabular-nums">
      {{ total.toLocaleString('id-ID') }} {{ unit ?? 'baris' }}
    </span>
    <div class="flex items-center rounded-lg border border-border overflow-hidden text-[11px]">
      <button
        :disabled="page <= 1 || loading"
        class="px-2 py-1.5 border-r border-border text-muted disabled:opacity-30 hover:bg-muted/10 transition-colors"
        @click="emit('prev')"
      >
        <ChevronLeft class="w-3.5 h-3.5" />
      </button>
      <span class="px-3 py-1.5 tabular-nums select-none bg-background/50">
        {{ page }} / {{ totalPages }}
      </span>
      <button
        :disabled="page >= totalPages || loading"
        class="px-2 py-1.5 border-l border-border text-muted disabled:opacity-30 hover:bg-muted/10 transition-colors"
        @click="emit('next')"
      >
        <ChevronRight class="w-3.5 h-3.5" />
      </button>
    </div>
  </div>
</template>
