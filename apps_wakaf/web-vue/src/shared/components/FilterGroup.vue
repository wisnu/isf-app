<script setup lang="ts">
defineProps<{ label: string }>()
</script>

<template>
  <div class="mb-3">
    <label class="text-[10px] uppercase tracking-widest text-muted font-semibold block mb-1.5">
      {{ label }}
    </label>
    <slot />
  </div>
</template>
