<script setup lang="ts">
import { computed } from 'vue'

import AppHeader from '@/layouts/AppHeader.vue'
import AppDomainRail from '@/layouts/AppDomainRail.vue'
import AppSidebar from '@/layouts/AppSidebar.vue'
import Toast from '@/shared/components/Toast.vue'
import { useAuthStore } from '@/app/stores/auth.store'

const auth = useAuthStore()
const showShell = computed(() => Boolean(auth.user) && Boolean(auth.activeTenantId))
</script>

<template>
  <div class="h-screen flex overflow-hidden">
    <!-- Navigation shell: domain rail + sidebar (always side by side) -->
    <template v-if="showShell">
      <AppDomainRail />
      <AppSidebar />
    </template>

    <!-- Main content column -->
    <div class="flex flex-col flex-1 min-w-0 overflow-hidden">
      <AppHeader v-if="auth.user" />
      <main class="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8 py-6 bg-[#eef0f5]">
        <div class="max-w-screen-xl mx-auto">
          <router-view />
        </div>
      </main>
    </div>
  </div>
  <Toast />
</template>
