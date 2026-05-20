<script setup lang="ts">
import { Calendar } from 'lucide-vue-next'
import { computed, onMounted, onUnmounted, ref } from 'vue'

const now = ref(new Date())
let timer: ReturnType<typeof setInterval> | undefined

onMounted(() => {
  timer = setInterval(() => {
    now.value = new Date()
  }, 30_000)
})
onUnmounted(() => {
  if (timer) clearInterval(timer)
})

const compact = computed(() => {
  const d = new Intl.DateTimeFormat('id-ID', {
    day: '2-digit',
    month: 'short',
  }).format(now.value)
  const t = new Intl.DateTimeFormat('id-ID', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  }).format(now.value)
  return `${d} · ${t}`
})

const long = computed(() =>
  new Intl.DateTimeFormat('id-ID', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(now.value),
)
</script>

<template>
  <div
    class="flex items-center gap-1.5 px-2 h-8 rounded-md bg-white/10 text-xs tabular-nums max-md:hidden"
    :title="long"
  >
    <Calendar class="w-3.5 h-3.5 opacity-90" />
    <span>{{ compact }}</span>
  </div>
</template>
