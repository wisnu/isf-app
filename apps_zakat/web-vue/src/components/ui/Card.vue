<script setup lang="ts">
import { cn } from '@/lib/utils'

const props = defineProps<{ class?: string }>()
</script>

<template>
  <div
    :class="cn('rounded-2xl border border-border bg-surface text-foreground shadow-sm', props.class)"
  >
    <slot />
  </div>
</template>
