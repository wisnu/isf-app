<script setup lang="ts">
import { CalendarDays } from 'lucide-vue-next'
import { ref, watch } from 'vue'

// Input tanggal format DD-MM-YYYY (tampilan) yang tetap mengikat nilai ISO
// 'YYYY-MM-DD' via v-model. Dilengkapi date-picker native (tombol kalender).
const props = defineProps<{ modelValue: string }>()
const emit = defineEmits<{ 'update:modelValue': [string] }>()

function isoToDisplay(iso: string): string {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || '')
  return m ? `${m[3]}-${m[2]}-${m[1]}` : (iso || '')
}
function displayToIso(s: string): string | null {
  const m = /^(\d{2})-(\d{2})-(\d{4})$/.exec((s || '').trim())
  if (!m) return null
  const iso = `${m[3]}-${m[2]}-${m[1]}`
  const d = new Date(iso + 'T00:00:00')
  if (isNaN(d.getTime())) return null
  // pastikan komponen valid (mis. 31-02 ditolak)
  return d.toISOString().slice(0, 10) === iso ? iso : null
}

const text = ref(isoToDisplay(props.modelValue))
const picker = ref<HTMLInputElement | null>(null)

watch(() => props.modelValue, (v) => { text.value = isoToDisplay(v) })

function onInput(e: Event) {
  // auto-mask: hanya digit, sisipkan '-' jadi DD-MM-YYYY
  const raw = (e.target as HTMLInputElement).value.replace(/\D/g, '').slice(0, 8)
  let out = raw
  if (raw.length > 4) out = `${raw.slice(0, 2)}-${raw.slice(2, 4)}-${raw.slice(4)}`
  else if (raw.length > 2) out = `${raw.slice(0, 2)}-${raw.slice(2)}`
  text.value = out
  // auto-commit begitu format lengkap (DD-MM-YYYY) agar tak perlu blur
  if (out.length === 10) {
    const iso = displayToIso(out)
    if (iso) emit('update:modelValue', iso)
  }
}
function commit() {
  const iso = displayToIso(text.value)
  if (iso) emit('update:modelValue', iso)
  else text.value = isoToDisplay(props.modelValue) // revert invalid
}
function openPicker() {
  const el = picker.value
  if (!el) return
  // showPicker() bila tersedia, else fokus (klik) input native
  // @ts-expect-error showPicker belum di semua lib dom
  if (typeof el.showPicker === 'function') el.showPicker()
  else el.click()
}
function onPick(e: Event) {
  const v = (e.target as HTMLInputElement).value
  if (v) emit('update:modelValue', v)
}
</script>

<template>
  <div class="relative inline-flex items-center">
    <input
      :value="text"
      type="text"
      inputmode="numeric"
      placeholder="DD-MM-YYYY"
      maxlength="10"
      class="h-9 w-36 rounded-lg border border-border bg-surface pl-2 pr-8 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
      @input="onInput"
      @change="commit"
      @blur="commit"
    />
    <button
      type="button"
      class="absolute right-1 h-7 w-7 grid place-items-center text-muted hover:text-foreground"
      title="Pilih tanggal"
      @click="openPicker"
    >
      <CalendarDays class="w-4 h-4" />
    </button>
    <input
      ref="picker"
      type="date"
      :value="modelValue"
      class="sr-only absolute right-0 bottom-0"
      tabindex="-1"
      aria-hidden="true"
      @change="onPick"
    />
  </div>
</template>
