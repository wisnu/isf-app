<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps<{
  modelValue: number | null
  placeholder?: string
  disabled?: boolean
  class?: string
}>()

const emit = defineEmits<{
  'update:modelValue': [value: number | null]
}>()

const fmt = new Intl.NumberFormat('id-ID', { maximumFractionDigits: 0 })

function toDisplay(n: number | null): string {
  return n !== null && n > 0 ? fmt.format(n) : ''
}

const display = ref(toDisplay(props.modelValue))

watch(
  () => props.modelValue,
  (val) => {
    const s = toDisplay(val)
    if (display.value !== s) display.value = s
  },
)

function onInput(e: Event) {
  const raw = (e.target as HTMLInputElement).value
  const digits = raw.replace(/\D/g, '')
  const num = digits ? parseInt(digits, 10) : null
  const formatted = toDisplay(num)
  display.value = formatted
  ;(e.target as HTMLInputElement).value = formatted
  emit('update:modelValue', num)
}
</script>

<template>
  <input
    :value="display"
    :placeholder="placeholder ?? '0'"
    :disabled="disabled"
    inputmode="numeric"
    :class="props.class ?? 'h-9 w-full rounded border px-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary dark:bg-zinc-800'"
    @input="onInput"
  />
</template>
