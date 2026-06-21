<script setup lang="ts">
import { cva, type VariantProps } from 'class-variance-authority'

import { cn } from '@/shared/utils/utils'

const alertVariants = cva(
  'relative w-full rounded-md border p-3 text-sm flex items-start gap-2',
  {
    variants: {
      variant: {
        default: 'bg-surface text-foreground border-border',
        destructive:
          'bg-destructive/10 text-destructive border-destructive/30 dark:bg-destructive/15',
      },
    },
    defaultVariants: { variant: 'default' },
  },
)

type AlertVariants = VariantProps<typeof alertVariants>

const props = defineProps<{
  variant?: AlertVariants['variant']
  class?: string
}>()
</script>

<template>
  <div
    role="alert"
    :class="cn(alertVariants({ variant: props.variant }), props.class)"
  >
    <slot />
  </div>
</template>
