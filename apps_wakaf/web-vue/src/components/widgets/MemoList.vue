<script setup lang="ts">
import { Loader2 } from 'lucide-vue-next'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardContent from '@/components/ui/CardContent.vue'

interface MemoItem {
  memo_id: number
  memo_number: string | null
  subject: string | null
  amount: number | null
  memo_type: string
  memo_date: string | null
}

withDefaults(
  defineProps<{
    items: MemoItem[]
    loading?: boolean
  }>(),
  {
    loading: false,
  }
)

function typeBadge(type: string): { label: string; class: string } {
  if (type === 'R') return { label: 'Rutin', class: 'bg-blue-100 text-blue-700' }
  return { label: 'Non Rutin', class: 'bg-purple-100 text-purple-700' }
}

function formatIdr(v: number): string {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0,
  }).format(v)
}
</script>

<template>
  <Card>
    <CardHeader>
      <CardTitle>Memo Penyaluran Terbaru</CardTitle>
    </CardHeader>
    <CardContent>
      <div v-if="loading" class="flex justify-center py-8">
        <Loader2 class="w-5 h-5 animate-spin text-muted" />
      </div>
      <div v-else-if="items.length === 0" class="text-sm text-muted text-center py-4">
        Tidak ada memo terbaru
      </div>
      <ul v-else class="divide-y divide-border">
        <li v-for="item in items" :key="item.memo_id" class="py-3 first:pt-0 last:pb-0">
          <div class="flex items-start justify-between gap-2">
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-foreground truncate">
                {{ item.subject || item.memo_number || '(Tanpa subjek)' }}
              </p>
              <div class="flex items-center gap-2 mt-0.5 text-xs text-muted">
                <span v-if="item.memo_number">{{ item.memo_number }}</span>
                <span v-if="item.memo_date">{{ item.memo_date }}</span>
              </div>
              <p v-if="item.amount !== null" class="text-xs text-muted tabular-nums mt-0.5">
                {{ formatIdr(item.amount) }}
              </p>
            </div>
            <span
              class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium shrink-0"
              :class="typeBadge(item.memo_type).class"
            >
              {{ typeBadge(item.memo_type).label }}
            </span>
          </div>
        </li>
      </ul>
    </CardContent>
  </Card>
</template>
