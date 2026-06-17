<script setup lang="ts">
import { X } from 'lucide-vue-next'

defineProps<{
  maxWidth?: string
}>()

defineEmits<{ close: [] }>()
</script>

<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
    <div :class="['w-full bg-background rounded-xl shadow-xl border border-border overflow-hidden', maxWidth || 'max-w-2xl']">
      <!-- Header -->
      <div class="flex items-center justify-between px-6 py-4 border-b border-border">
        <div class="flex-1">
          <slot name="header" />
        </div>
        <button
          type="button"
          class="text-muted-foreground hover:text-foreground transition-colors ml-4"
          @click="$emit('close')"
        >
          <X class="w-4 h-4" />
        </button>
      </div>

      <!-- Body -->
      <div class="px-6 py-5">
        <slot />
      </div>

      <!-- Footer -->
      <div v-if="$slots.footer" class="px-6 py-3 border-t border-border bg-muted/30">
        <slot name="footer" />
      </div>
    </div>
  </div>
</template>
