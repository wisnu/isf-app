<script setup lang="ts">
import Card from '@/components/ui/Card.vue'
import CardContent from '@/components/ui/CardContent.vue'
import CardDescription from '@/components/ui/CardDescription.vue'
import CardHeader from '@/components/ui/CardHeader.vue'
import CardTitle from '@/components/ui/CardTitle.vue'
import { dmy } from '@/lib/date'
import { formatIdr } from '@/lib/format'

interface Transaction {
  id: string
  date: string
  type: string
  channel: string
  amount: number
  donor: string
}

defineProps<{ items: Transaction[] }>()
</script>

<template>
  <Card class="h-full">
    <CardHeader>
      <CardTitle>Transaksi Terbaru</CardTitle>
      <CardDescription>10 transaksi terakhir</CardDescription>
    </CardHeader>
    <CardContent class="p-0">
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="text-xs text-muted uppercase tracking-wide">
            <tr class="border-b border-border">
              <th class="text-left px-6 py-2 font-medium">Tanggal</th>
              <th class="text-left px-6 py-2 font-medium">Jenis</th>
              <th class="text-left px-6 py-2 font-medium max-md:hidden">Channel</th>
              <th class="text-left px-6 py-2 font-medium">Donatur</th>
              <th class="text-right px-6 py-2 font-medium">Nominal</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="tx in items"
              :key="tx.id"
              class="border-b border-border last:border-0 hover:bg-background/60"
            >
              <td class="px-6 py-2 text-muted tabular-nums whitespace-nowrap">
                {{ dmy(tx.date) }}
              </td>
              <td class="px-6 py-2 whitespace-nowrap">{{ tx.type }}</td>
              <td class="px-6 py-2 max-md:hidden text-muted whitespace-nowrap">
                {{ tx.channel }}
              </td>
              <td class="px-6 py-2 truncate max-w-[180px]">{{ tx.donor }}</td>
              <td class="px-6 py-2 text-right font-medium tabular-nums whitespace-nowrap">
                {{ formatIdr(tx.amount) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </CardContent>
  </Card>
</template>
