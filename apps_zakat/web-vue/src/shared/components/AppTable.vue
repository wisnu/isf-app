<script setup lang="ts">
defineOptions({ inheritAttrs: false })
defineProps<{ sticky?: boolean }>()
</script>

<template>
  <div class="overflow-x-auto" v-bind="$attrs">
    <table class="w-full text-sm">
      <thead
        class="text-xs font-semibold text-zinc-600 dark:text-zinc-400 bg-zinc-50 dark:bg-zinc-800/50 border-b border-border"
        :class="sticky ? 'sticky top-0 z-10' : ''"
      >
        <slot name="head" />
      </thead>
      <tbody>
        <slot />
      </tbody>
    </table>
  </div>
</template>
