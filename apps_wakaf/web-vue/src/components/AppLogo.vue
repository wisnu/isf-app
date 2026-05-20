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
    <!-- Tree foliage cluster -->
    <circle cx="7.5" cy="6.5" r="1.7" />
    <circle cx="10" cy="4.5" r="1.7" />
    <circle cx="12" cy="3.5" r="1.7" />
    <circle cx="14" cy="4.5" r="1.7" />
    <circle cx="16.5" cy="6.5" r="1.7" />
    <circle cx="10" cy="7" r="1.5" />
    <circle cx="14" cy="7" r="1.5" />
    <!-- Trunk -->
    <rect x="11.4" y="8" width="1.2" height="5" />
    <!-- Mosque dome -->
    <path d="M7.5 13 Q 12 8.5 16.5 13 Z" />
    <!-- Mosque body -->
    <rect x="7.5" y="13" width="9" height="4" />
    <!-- Roots -->
    <path
      d="M9 17 Q 7 19 5.5 20.5 M 9 17 Q 8 19.5 9.5 21 M 12 17 L 12 21 M 15 17 Q 17 19 18.5 20.5 M 15 17 Q 16 19.5 14.5 21"
      stroke="currentColor"
      stroke-width="0.6"
      fill="none"
      stroke-linecap="round"
    />
  </svg>
</template>
