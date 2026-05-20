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
    <!-- Crescent moon -->
    <path d="M9.5 3.5 a 1.9 1.9 0 1 0 0 3.4 a 1.35 1.35 0 1 1 0 -3.4 z" />
    <!-- Star -->
    <path d="M14.4 3.2 L 14.7 4 L 15.5 4 L 14.85 4.5 L 15.15 5.3 L 14.4 4.85 L 13.65 5.3 L 13.95 4.5 L 13.3 4 L 14.1 4 Z" />
    <!-- Coin stack -->
    <ellipse cx="12" cy="9.6" rx="1.8" ry="0.5" />
    <rect x="10.2" y="9.6" width="3.6" height="1.1" />
    <ellipse cx="12" cy="10.7" rx="1.8" ry="0.5" />
    <rect x="10.2" y="10.7" width="3.6" height="1.1" />
    <ellipse cx="12" cy="11.8" rx="1.8" ry="0.5" />
    <!-- Left palm -->
    <path d="M6.5 10.5 C 5 11 4.5 12.4 4.5 13.8 C 4.5 15.2 4.9 16.6 5.7 18 C 6.2 18.7 7.1 18.9 7.7 18.3 C 8.1 17.9 8.2 17.3 8 16.7 L 7.8 11.4 C 7.7 10.8 7 10.4 6.5 10.5 Z" />
    <!-- Right palm -->
    <path d="M17.5 10.5 C 19 11 19.5 12.4 19.5 13.8 C 19.5 15.2 19.1 16.6 18.3 18 C 17.8 18.7 16.9 18.9 16.3 18.3 C 15.9 17.9 15.8 17.3 16 16.7 L 16.2 11.4 C 16.3 10.8 17 10.4 17.5 10.5 Z" />
  </svg>
</template>
