<script setup lang="ts">
import { AlertCircle, CheckCircle2, Info, X, AlertTriangle } from 'lucide-vue-next'
import { computed } from 'vue'

import { useToast } from '@/shared/composables/useToast'
import type { ToastType } from '@/shared/composables/useToast'

const { toasts, dismiss } = useToast()

const typeIcon = {
  success: CheckCircle2,
  error: AlertCircle,
  warning: AlertTriangle,
  info: Info,
} as const

const typeStyles = computed(() => ({
  success: {
    border: 'border-l-emerald-500',
    iconBox: 'bg-emerald-50 text-emerald-600',
  },
  error: {
    border: 'border-l-red-500',
    iconBox: 'bg-red-50 text-red-600',
  },
  warning: {
    border: 'border-l-amber-500',
    iconBox: 'bg-amber-50 text-amber-600',
  },
  info: {
    border: 'border-l-sky-500',
    iconBox: 'bg-sky-50 text-sky-600',
  },
} as Record<ToastType, { border: string; iconBox: string }>))
</script>

<template>
  <div class="fixed top-4 right-4 z-[9999] flex flex-col gap-2 max-w-sm">
    <transition-group name="toast">
      <div
        v-for="t in toasts"
        :key="t.id"
        :class="[
          'flex items-start gap-3 rounded-md bg-white shadow-lg border border-gray-200 border-l-4 p-3',
          typeStyles[t.type].border,
        ]"
      >
        <div
          :class="[
            'flex h-8 w-8 items-center justify-center rounded-md shrink-0',
            typeStyles[t.type].iconBox,
          ]"
        >
          <component :is="typeIcon[t.type]" class="h-5 w-5" />
        </div>
        <p class="flex-1 text-sm text-gray-800 whitespace-pre-line pt-1">
          {{ t.message }}
        </p>
        <button
          type="button"
          class="text-gray-400 hover:text-gray-600 transition-colors"
          aria-label="Dismiss"
          @click="dismiss(t.id)"
        >
          <X class="h-4 w-4" />
        </button>
      </div>
    </transition-group>
  </div>
</template>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 200ms ease-out;
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(20px);
}
.toast-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>
