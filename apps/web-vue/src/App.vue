<script setup lang="ts">
import { computed } from 'vue'

import AppHeader from '@/components/AppHeader.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const showHeader = computed(() => Boolean(auth.user))
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader v-if="showHeader" />
    <main class="flex-1 w-full max-w-screen-xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <router-view />
    </main>
  </div>
</template>
