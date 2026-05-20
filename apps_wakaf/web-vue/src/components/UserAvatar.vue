<script setup lang="ts">
import { computed } from 'vue'

import { cn } from '@/lib/utils'

const props = defineProps<{
  name: string
  size?: 'sm' | 'md' | 'lg'
  class?: string
}>()

const initials = computed(() => {
  const parts = props.name.trim().split(/\s+/).filter(Boolean)
  if (parts.length === 0) return '?'
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase()
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
})

const sizeClass = computed(() => {
  if (props.size === 'sm') return 'w-7 h-7 text-[10px]'
  if (props.size === 'lg') return 'w-12 h-12 text-base'
  return 'w-8 h-8 text-xs'
})
</script>

<template>
  <div
    :class="
      cn(
        'rounded-full grid place-items-center bg-white text-primary font-semibold shrink-0 select-none',
        sizeClass,
        props.class,
      )
    "
    :title="name"
    aria-hidden="true"
  >
    {{ initials }}
  </div>
</template>
