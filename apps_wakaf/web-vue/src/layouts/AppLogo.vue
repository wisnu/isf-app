<script setup lang="ts">
defineProps<{ class?: string }>()
</script>

<template>
  <img
    src="@/assets/logo.svg"
    alt="Logo Wakaf"
    :class="$props.class"
    aria-hidden="true"
    style="object-fit: contain;"
  />
</template>
