<script setup lang="ts">
import {
  DropdownMenuContent,
  DropdownMenuPortal,
  DropdownMenuRoot,
  DropdownMenuTrigger,
} from 'reka-ui'

import { cn } from '@/lib/utils'

const props = defineProps<{ contentClass?: string }>()
</script>

<template>
  <DropdownMenuRoot>
    <DropdownMenuTrigger as-child>
      <slot name="trigger" />
    </DropdownMenuTrigger>
    <DropdownMenuPortal>
      <DropdownMenuContent
        :class="
          cn(
            'z-50 min-w-[220px] overflow-hidden rounded-md border border-border bg-surface p-1 text-foreground shadow-md',
            'data-[state=open]:animate-in data-[state=closed]:animate-out',
            props.contentClass,
          )
        "
        :side-offset="6"
        align="end"
      >
        <slot />
      </DropdownMenuContent>
    </DropdownMenuPortal>
  </DropdownMenuRoot>
</template>
