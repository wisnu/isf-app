<script setup lang="ts">
import { Loader2, Search } from 'lucide-vue-next'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'

defineProps<{
  title: string
  rowCount?: number
  total?: number
  loading?: boolean
  isEmpty?: boolean
}>()
</script>

<template>
  <Card>
    <CardContent class="p-0">

      <!-- Panel header: judul + count + controls -->
      <div class="px-4 py-2.5 border-b border-border flex flex-wrap items-center justify-between gap-2 rounded-t-2xl">
        <div class="flex items-center gap-3">
          <h2 class="font-semibold text-xs">{{ title }}</h2>
          <p v-if="total !== undefined" class="text-[11px] text-muted">
            {{ rowCount ?? 0 }} dari {{ total }} data
          </p>
        </div>
        <div class="flex items-center gap-1.5">
          <slot name="controls" />
        </div>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="flex justify-center py-10">
        <Loader2 class="w-5 h-5 animate-spin text-primary" />
      </div>

      <!-- Empty state -->
      <div v-else-if="isEmpty" class="flex flex-col items-center gap-1.5 py-10 text-muted">
        <Search class="w-6 h-6 opacity-30" />
        <p class="text-xs">
          <slot name="empty">Tidak ada data yang sesuai filter</slot>
        </p>
      </div>

      <!-- Table / konten utama -->
      <slot v-else />

      <!-- Pagination footer -->
      <slot name="pagination" />

    </CardContent>
  </Card>
</template>
