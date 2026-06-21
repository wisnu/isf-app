<script setup lang="ts">
import { CalendarDays } from 'lucide-vue-next'
import { shallowRef, useTemplateRef, watch } from 'vue'

// Input tanggal DD-MM-YYYY (tampilan) ↔ YYYY-MM-DD ISO (v-model).
//
// Keyboard typing:
//   - Ketik angka saja: "04062026" → auto-format ke "04-06-2026" saat blur/Enter
//   - Ketik dengan dash: "04-06-2026" → dash disisipkan otomatis di posisi ke-2 dan ke-4
//   - Karakter ke-10 yang valid langsung emit tanpa perlu blur
//   - Enter key meng-commit input (sama seperti blur)
//   - Input invalid saat blur → tampil ring merah 800ms, lalu revert ke nilai valid terakhir
//
// Calendar:
//   - Klik ikon kalender → native date picker
//   - Pilihan picker langsung update text + emit ISO (tidak menunggu watch)
//
// Props tambahan (backward-compatible — semua optional):
//   - disabled : nonaktifkan input + tombol kalender
//   - min / max: ISO YYYY-MM-DD — batas tanggal yang diterima (inclusive)

const props = defineProps<{
  modelValue: string
  disabled?: boolean
  /** ISO YYYY-MM-DD — tanggal minimum yang diterima (inclusive) */
  min?: string
  /** ISO YYYY-MM-DD — tanggal maksimum yang diterima (inclusive) */
  max?: string
}>()

const emit = defineEmits<{ 'update:modelValue': [string] }>()

// ─── Helpers ────────────────────────────────────────────────────────────────

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
  if (d.toISOString().slice(0, 10) !== iso) return null
  if (props.min && iso < props.min) return null
  if (props.max && iso > props.max) return null
  return iso
}

// ─── State ──────────────────────────────────────────────────────────────────

const text = shallowRef(isoToDisplay(props.modelValue))
const hasError = shallowRef(false)
const picker = useTemplateRef<HTMLInputElement>('picker')

// Sinkronisasi saat v-model berubah dari luar — hindari overwrite saat user sedang mengetik
watch(
  () => props.modelValue,
  (v) => {
    const display = isoToDisplay(v)
    if (display !== text.value) {
      text.value = display
      hasError.value = false
    }
  },
)

// ─── Keyboard typing ─────────────────────────────────────────────────────────

function onInput(e: Event) {
  const inp = e.target as HTMLInputElement
  const isDeleting = ((e as InputEvent).inputType ?? '').startsWith('delete')
  let val = inp.value

  // Buang karakter selain digit dan dash (handle paste "04/06/2026" atau "04.06.2026")
  const cleaned = val.replace(/[^\d-]/g, '')
  if (cleaned !== val) {
    val = cleaned
    inp.value = val
  }

  // Auto-insert dash setelah digit ke-2 dan ke-4 — hanya saat mengetik maju
  if (!isDeleting) {
    const digits = val.replace(/-/g, '')
    if (digits.length === 2 && val === digits) {
      val = digits + '-'
      inp.value = val
    } else if (digits.length === 4 && val.replace(/-/g, '') === digits) {
      val = `${digits.slice(0, 2)}-${digits.slice(2)}-`
      inp.value = val
    }
  }

  text.value = val
  hasError.value = false

  // Emit segera saat karakter ke-10 sudah valid
  if (val.length === 10) {
    const iso = displayToIso(val)
    if (iso) {
      emit('update:modelValue', iso)
    } else {
      hasError.value = true
    }
  }
}

function commit() {
  let iso = displayToIso(text.value)
  if (iso) {
    text.value = isoToDisplay(iso)
    hasError.value = false
    emit('update:modelValue', iso)
    return
  }

  // Fallback: 8 digit tanpa dash → format otomatis DD-MM-YYYY
  const digits = text.value.replace(/\D/g, '')
  if (digits.length === 8) {
    const formatted = `${digits.slice(0, 2)}-${digits.slice(2, 4)}-${digits.slice(4)}`
    iso = displayToIso(formatted)
    if (iso) {
      text.value = formatted
      hasError.value = false
      emit('update:modelValue', iso)
      return
    }
  }

  // Input kosong — biarkan, tidak perlu error
  if (!text.value.trim()) {
    text.value = ''
    return
  }

  // Input ada tapi tidak valid — tunjukkan ring merah lalu revert
  hasError.value = true
  setTimeout(() => {
    text.value = isoToDisplay(props.modelValue)
    hasError.value = false
  }, 800)
}

function onKeydown(e: KeyboardEvent) {
  if (e.key === 'Enter') {
    e.preventDefault()
    commit()
    ;(e.target as HTMLElement).blur()
  }
}

// ─── Calendar picker ─────────────────────────────────────────────────────────

function openPicker() {
  if (props.disabled) return
  const el = picker.value
  if (!el) return
  // @ts-expect-error showPicker belum di semua lib dom
  if (typeof el.showPicker === 'function') el.showPicker()
  else el.click()
}

function onPick(e: Event) {
  const v = (e.target as HTMLInputElement).value
  if (!v) return
  // Update text langsung agar tampilan segera sinkron (tidak menunggu watch)
  text.value = isoToDisplay(v)
  hasError.value = false
  emit('update:modelValue', v)
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
      :disabled="disabled"
      :class="[
        'h-9 w-36 rounded-lg border bg-surface pl-2 pr-8 text-sm focus:outline-none focus:ring-1',
        'disabled:cursor-not-allowed disabled:opacity-50',
        hasError
          ? 'border-red-400 focus:ring-red-400'
          : 'border-border focus:ring-primary',
      ]"
      @input="onInput"
      @blur="commit"
      @keydown="onKeydown"
    />
    <button
      type="button"
      :disabled="disabled"
      class="absolute right-1 h-7 w-7 grid place-items-center text-muted hover:text-foreground disabled:cursor-not-allowed disabled:opacity-50"
      title="Pilih tanggal"
      @click="openPicker"
    >
      <CalendarDays class="w-4 h-4" />
    </button>
    <input
      ref="picker"
      type="date"
      :value="modelValue"
      :min="min"
      :max="max"
      :disabled="disabled"
      class="sr-only absolute right-0 bottom-0"
      tabindex="-1"
      aria-hidden="true"
      @change="onPick"
    />
  </div>
</template>
