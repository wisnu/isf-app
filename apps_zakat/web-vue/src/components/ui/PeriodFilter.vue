<script setup lang="ts">
import { computed } from 'vue'
import { cn } from '@/lib/utils'

const props = defineProps<{
  bulan: number
  tahun: number
}>()

const emit = defineEmits<{
  'update:bulan': [number]
  'update:tahun': [number]
}>()

const months = [
  'Januari',
  'Februari',
  'Maret',
  'April',
  'Mei',
  'Juni',
  'Juli',
  'Agustus',
  'September',
  'Oktober',
  'November',
  'Desember',
]

const currentYear = new Date().getFullYear()
const years = computed(() => [currentYear - 2, currentYear - 1, currentYear])

const selectClass = cn(
  'h-10 rounded-md border border-border bg-surface px-3 py-2 text-sm text-foreground',
  'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary',
  'cursor-pointer',
)
</script>

<template>
  <div class="flex items-center gap-2">
    <label for="bulan" class="text-sm text-muted">Bulan:</label>
    <select
      id="bulan"
      :value="bulan"
      :class="selectClass"
      @change="emit('update:bulan', parseInt(($event.target as HTMLSelectElement).value))"
    >
      <option v-for="(month, index) in months" :key="index" :value="index + 1">
        {{ month }}
      </option>
    </select>

    <label for="tahun" class="text-sm text-muted">Tahun:</label>
    <select
      id="tahun"
      :value="tahun"
      :class="selectClass"
      @change="emit('update:tahun', parseInt(($event.target as HTMLSelectElement).value))"
    >
      <option v-for="year in years" :key="year" :value="year">
        {{ year }}
      </option>
    </select>
  </div>
</template>
