<script setup lang="ts">
import { DropdownMenuItem as RekaDropdownMenuItem } from 'reka-ui'

import { cn } from '@/lib/utils'

const props = defineProps<{ class?: string; disabled?: boolean }>()
</script>

<template>
  <RekaDropdownMenuItem
    :disabled="disabled"
    :class="
      cn(
        'relative flex cursor-pointer select-none items-center gap-2 rounded-sm px-2 py-1.5 text-sm outline-none',
        'data-[highlighted]:bg-background data-[highlighted]:text-foreground',
        'data-[disabled]:pointer-events-none data-[disabled]:opacity-50',
        props.class,
      )
    "
  >
    <slot />
  </RekaDropdownMenuItem>
</template>
