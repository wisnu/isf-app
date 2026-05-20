<script setup lang="ts">
import { computed } from 'vue'

import AppHeader from '@/components/AppHeader.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const showHeader = computed(() => Boolean(auth.user))
</script>

<template>
  <AppHeader v-if="showHeader" />
  <main class="main">
    <router-view />
  </main>
</template>

<style scoped>
.main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}
</style>
