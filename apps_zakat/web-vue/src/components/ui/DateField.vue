<script setup lang="ts">
import { CalendarDays } from 'lucide-vue-next'
import { shallowRef, useTemplateRef, watch } from 'vue'

// Input tanggal DD-MM-YYYY (tampilan) ↔ YYYY-MM-DD ISO (v-model).
// Mendukung input manual bebas: user bisa ketik "04-06-2026" atau "04062026".
// Dashes disisipkan otomatis saat panjang digit menyentuh posisi 2 dan 4.
// Format final (DD-MM-YYYY) divalidasi saat blur/commit.
const props = defineProps<{ modelValue: string }>()
const emit = defineEmits<{ 'update:modelValue': [string] }>()

function isoToDisplay(iso: string): string {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || '')
  return m ? `${m[3]}-${m[2]}-${m[1]}` : ''
}
function displayToIso(s: string): string | null {
  const m = /^(\d{2})-(\d{2})-(\d{4})$/.exec((s || '').trim())
  if (!m) return null
  const iso = `${m[3]}-${m[2]}-${m[1]}`
  const d = new Date(iso + 'T00:00:00')
  if (isNaN(d.getTime())) return null
  return d.toISOString().slice(0, 10) === iso ? iso : null
}

const text = shallowRef(isoToDisplay(props.modelValue))
const picker = useTemplateRef<HTMLInputElement>('picker')

watch(() => props.modelValue, (v) => {
  text.value = isoToDisplay(v)
})

function onInput(e: Event) {
  const inp = e.target as HTMLInputElement
  const isDeleting = ((e as InputEvent).inputType ?? '').startsWith('delete')
  let val = inp.value

  // Auto-insert dash setelah digit ke-2 dan ke-4 — hanya saat mengetik maju,
  // tidak saat menghapus agar dash tidak "bounce back" saat backspace.
  if (!isDeleting) {
    const digits = val.replace(/\D/g, '')
    if (digits.length === 2 && val === digits) {
      val = digits + '-'
      inp.value = val
    } else if (digits.length === 4 && val.replace(/-/g, '') === digits) {
      val = `${digits.slice(0, 2)}-${digits.slice(2)}-`
      inp.value = val
    }
  }

  text.value = val

  // Emit langsung jika sudah 10 karakter valid
  if (val.length === 10) {
    const iso = displayToIso(val)
    if (iso) emit('update:modelValue', iso)
  }
}

function commit() {
  // Coba parse DD-MM-YYYY
  let iso = displayToIso(text.value)
  if (iso) {
    text.value = isoToDisplay(iso)
    emit('update:modelValue', iso)
    return
  }
  // Fallback: 8 digit tanpa strip → format otomatis
  const digits = text.value.replace(/\D/g, '')
  if (digits.length === 8) {
    const formatted = `${digits.slice(0, 2)}-${digits.slice(2, 4)}-${digits.slice(4)}`
    iso = displayToIso(formatted)
    if (iso) {
      text.value = formatted
      emit('update:modelValue', iso)
      return
    }
  }
  // Invalid — revert ke nilai terakhir yang valid
  text.value = isoToDisplay(props.modelValue)
}

function openPicker() {
  const el = picker.value
  if (!el) return
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
