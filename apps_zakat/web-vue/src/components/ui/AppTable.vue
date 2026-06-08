<script setup lang="ts">
// Wrapper tabel standar isf-app — konsisten dengan gaya KasPage.
// Gunakan komponen ini sebagai container untuk semua native <table>.
defineProps<{ overflow?: boolean }>()
</script>

<template>
  <div class="overflow-x-auto">
    <table class="w-full text-[11px]">
      <slot />
    </table>
  </div>
</template>
