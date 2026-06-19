<script setup lang="ts">
import { computed } from 'vue'

import AppHeader from '@/components/AppHeader.vue'
import AppSidebar from '@/components/AppSidebar.vue'
import Toast from '@/components/ui/Toast.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const showShell = computed(() => Boolean(auth.user) && Boolean(auth.activeTenantId))
</script>

<template>
  <div class="h-screen flex overflow-hidden">
    <AppSidebar v-if="showShell" />
    <div class="flex flex-col flex-1 min-w-0 overflow-hidden">
      <AppHeader v-if="auth.user" />
      <main class="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="max-w-screen-xl mx-auto">
          <router-view />
        </div>
      </main>
    </div>
  </div>
  <Toast />
</template>
