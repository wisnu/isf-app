<script setup lang="ts">
import {
  TooltipContent,
  TooltipPortal,
  TooltipProvider,
  TooltipRoot,
  TooltipTrigger,
} from 'reka-ui'

import { cn } from '@/shared/utils/utils'

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
              'z-50 rounded-md bg-zinc-800 dark:bg-zinc-700 px-2.5 py-1.5 shadow-md',
              'text-white text-[11px] font-medium max-w-xs',
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
