<script setup lang="ts">
import { computed } from 'vue'

import AppHeader from '@/components/AppHeader.vue'
import AppSidebar from '@/components/AppSidebar.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const showShell = computed(() => Boolean(auth.user) && Boolean(auth.activeTenantId))
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader v-if="auth.user" />
    <div class="flex flex-1 min-h-0">
      <AppSidebar v-if="showShell" />
      <main class="flex-1 px-4 sm:px-6 lg:px-8 py-6 min-w-0">
        <div class="max-w-screen-xl mx-auto">
          <router-view />
        </div>
      </main>
    </div>
  </div>
</template>
