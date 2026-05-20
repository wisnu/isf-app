<script setup lang="ts">
defineProps<{ class?: string }>()
</script>

<template>
  <svg
    viewBox="0 0 24 24"
    fill="currentColor"
    xmlns="http://www.w3.org/2000/svg"
    :class="$props.class"
    aria-hidden="true"
  >
    <path
      d="M12 21 C 5.5 16 4 13 4 10.5 C 4 8.3 5.8 6.5 8 6.5 C 9.3 6.5 10.4 7.1 11.1 8 C 11.4 8.4 11.6 8.4 11.9 8 C 12.6 7.1 13.7 6.5 15 6.5 C 17.2 6.5 19 8.3 19 10.5 C 19 13 17.5 16 12 21 Z"
    />
  </svg>
</template>
