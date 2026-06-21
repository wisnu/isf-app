<script setup lang="ts">
import { cn } from '@/shared/utils/utils'

const props = defineProps<{ class?: string }>()
</script>

<template>
  <p :class="cn('text-sm text-muted', props.class)">
    <slot />
  </p>
</template>
