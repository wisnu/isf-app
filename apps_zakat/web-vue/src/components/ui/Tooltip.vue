<script setup lang="ts">
import {
  TooltipContent,
  TooltipPortal,
  TooltipProvider,
  TooltipRoot,
  TooltipTrigger,
} from 'reka-ui'

import { cn } from '@/lib/utils'

const props = defineProps<{
  side?: 'top' | 'bottom' | 'left' | 'right'
  align?: 'start' | 'center' | 'end'
  delay?: number
  contentClass?: string
}>()
</script>

<template>
  <TooltipProvider :delay-duration="delay ?? 200">
    <TooltipRoot>
      <TooltipTrigger as-child>
        <slot name="trigger" />
      </TooltipTrigger>
      <TooltipPortal>
        <TooltipContent
          :side="side ?? 'bottom'"
          :align="align ?? 'center'"
          :side-offset="6"
          :class="
            cn(
              'z-50 rounded-md border border-border bg-surface px-3 py-2 shadow-md',
              'text-foreground text-xs max-w-sm',
              'data-[state=delayed-open]:animate-in data-[state=closed]:animate-out',
              props.contentClass,
            )
          "
        >
          <slot />
        </TooltipContent>
      </TooltipPortal>
    </TooltipRoot>
  </TooltipProvider>
</template>
