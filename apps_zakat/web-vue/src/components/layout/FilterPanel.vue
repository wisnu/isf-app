<script setup lang="ts">
import { shallowRef } from 'vue'
import { ChevronDown } from 'lucide-vue-next'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'

defineProps<{ hasFilters?: boolean }>()
defineEmits<{ reset: [] }>()

const tipsOpen = shallowRef(false)
</script>

<template>
  <Card>
    <CardContent class="p-4">

      <!-- Header -->
      <div class="flex items-center justify-between mb-3">
        <span class="font-semibold text-sm">Filter</span>
        <button
          v-if="hasFilters"
          type="button"
          class="text-xs font-medium text-primary hover:underline"
          @click="$emit('reset')"
        >
          Reset
        </button>
      </div>

      <!-- Filter fields (page-specific) -->
      <slot />

      <!-- Tips penggunaan — collapsible, konten via slot #tips -->
      <div v-if="$slots.tips" class="border-t border-border pt-2.5 mt-3">
        <button
          type="button"
          class="w-full flex items-center justify-between text-xs font-medium text-foreground hover:text-primary transition-colors"
          @click="tipsOpen = !tipsOpen"
        >
          <span>Tips penggunaan</span>
          <ChevronDown
            class="w-3.5 h-3.5 transition-transform duration-200 text-muted"
            :class="{ 'rotate-180': tipsOpen }"
          />
        </button>
        <div v-if="tipsOpen" class="mt-1.5 space-y-1 text-[11px] text-muted">
          <slot name="tips" />
        </div>
      </div>

    </CardContent>
  </Card>
</template>
