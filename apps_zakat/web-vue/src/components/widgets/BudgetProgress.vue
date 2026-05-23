<script setup lang="ts">
import { Loader2 } from 'lucide-vue-next'
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'

interface AnggaranItem {
  owner_id: number
  owner_name: string
  anggaran: number
  realisasi: number
  pct: number
}

withDefaults(
  defineProps<{
    items: AnggaranItem[]
    loading?: boolean
  }>(),
  {
    loading: false
  }
)

function progressColor(pct: number): string {
  if (pct > 95) return 'bg-red-500'
  if (pct > 80) return 'bg-amber-500'
  if (pct > 50) return 'bg-blue-600'
  return 'bg-blue-400'
}

function displayPct(pct: number): string {
  return pct >= 999 ? '999+' : pct.toFixed(1)
}
</script>

<template>
  <Card>
    <CardHeader class="pb-2">
      <CardTitle>Realisasi Anggaran</CardTitle>
    </CardHeader>
    <CardContent class="p-5 pt-0">
      <div v-if="loading" class="flex justify-center py-8">
        <Loader2 class="w-5 h-5 animate-spin text-muted" />
      </div>
      <div v-else-if="items.length === 0" class="text-sm text-muted text-center py-4">
        Tidak ada data anggaran
      </div>
      <div v-else class="space-y-3">
        <div v-for="item in items" :key="item.owner_id">
          <div class="flex justify-between text-sm mb-1">
            <span class="text-foreground truncate">{{ item.owner_name }}</span>
            <span class="text-muted tabular-nums ml-2">{{ displayPct(item.pct) }}%</span>
          </div>
          <div class="w-full h-2 rounded-full bg-border overflow-hidden">
            <div
              class="h-full rounded-full transition-all"
              :class="progressColor(item.pct)"
              :style="{ width: `${Math.min(item.pct, 100)}%` }"
            />
          </div>
        </div>
      </div>
    </CardContent>
  </Card>
</template>
