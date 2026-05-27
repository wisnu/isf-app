<script setup lang="ts">
import { computed } from 'vue'
import { AlertTriangle, Loader2 } from 'lucide-vue-next'
import Card from '@/components/ui/Card.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import CardContent from '@/components/ui/CardContent.vue'

interface RekeningItem {
  account_no: string
  account_name: string
  account_type: string
  bank_name: string | null
  balance: number
}

const props = withDefaults(
  defineProps<{
    items: RekeningItem[]
    loading?: boolean
    error?: boolean
    errorMessage?: string
  }>(),
  {
    loading: false,
    error: false,
  },
)

function typeBadgeClass(type: string): string {
  if (type === 'Bank') return 'bg-blue-100 text-blue-700'
  if (type === 'Kas Besar') return 'bg-emerald-100 text-emerald-700'
  if (type === 'Kas Kecil') return 'bg-amber-100 text-amber-700'
  return 'bg-gray-100 text-gray-600'
}

function formatIdr(v: number): string {
  return new Intl.NumberFormat('id-ID', {
    style: 'currency',
    currency: 'IDR',
    maximumFractionDigits: 0,
  }).format(v)
}

const totalSaldo = computed(() =>
  props.items.reduce((sum, r) => sum + r.balance, 0),
)
</script>

<template>
  <Card>
    <CardHeader>
      <CardTitle>Saldo Kas/Bank</CardTitle>
    </CardHeader>
    <CardContent>
      <div v-if="loading" class="flex items-center justify-center gap-2 text-muted text-sm py-8">
        <Loader2 class="w-4 h-4 animate-spin" />
        Memuat rekening...
      </div>
      <div v-else-if="error" class="flex flex-col items-center gap-1 text-destructive text-sm py-8 text-center px-4">
        <AlertTriangle class="w-5 h-5 mb-1" />
        <span class="font-medium">Gagal memuat rekening</span>
        <span v-if="errorMessage" class="text-xs text-muted">{{ errorMessage }}</span>
      </div>
      <div v-else-if="items.length === 0" class="text-sm text-muted text-center py-8 italic">
        Tidak ada rekening aktif.
      </div>
      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <tbody class="divide-y divide-border">
            <tr v-for="item in items" :key="item.account_no">
              <td class="py-2 pr-3">
                <div class="font-medium text-foreground truncate">{{ item.account_name }}</div>
                <div v-if="item.bank_name" class="text-xs text-muted">{{ item.bank_name }}</div>
              </td>
              <td class="py-2 pr-3">
                <span
                  class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium"
                  :class="typeBadgeClass(item.account_type)"
                >
                  {{ item.account_type }}
                </span>
              </td>
              <td class="py-2 text-right tabular-nums font-medium">{{ formatIdr(item.balance) }}</td>
            </tr>
          </tbody>
          <tfoot>
            <tr class="border-t-2 border-border">
              <td class="pt-2 font-bold text-foreground">Total</td>
              <td></td>
              <td class="pt-2 text-right tabular-nums font-bold">{{ formatIdr(totalSaldo) }}</td>
            </tr>
          </tfoot>
        </table>
      </div>
    </CardContent>
  </Card>
</template>
