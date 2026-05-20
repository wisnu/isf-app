<script setup lang="ts">
import { computed } from 'vue'

import AppHeader from '@/components/AppHeader.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const showHeader = computed(() => Boolean(auth.user))
</script>

<template>
  <q-layout view="hHh lpr fFf">
    <AppHeader v-if="showHeader" />
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>
