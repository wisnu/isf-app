<script setup lang="ts">
import { Calendar } from 'lucide-vue-next'
import { onMounted, onUnmounted, ref } from 'vue'

const now = ref(new Date())
let timer: ReturnType<typeof setInterval> | undefined

onMounted(() => {
  timer = setInterval(() => {
    now.value = new Date()
  }, 60_000)
})
onUnmounted(() => {
  if (timer) clearInterval(timer)
})

function format(d: Date): string {
  return new Intl.DateTimeFormat('id-ID', {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  }).format(d)
}

function formatLong(d: Date): string {
  return new Intl.DateTimeFormat('id-ID', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  }).format(d)
}
</script>

<template>
  <div
    class="flex items-center gap-2 text-xs opacity-90 max-md:hidden"
    :title="formatLong(now)"
  >
    <Calendar class="w-3.5 h-3.5" />
    <span class="tabular-nums">{{ format(now) }}</span>
  </div>
</template>
