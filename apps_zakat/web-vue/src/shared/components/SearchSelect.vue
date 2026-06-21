<script setup lang="ts">
import { ChevronDown, X } from 'lucide-vue-next'
import { computed, nextTick, onUnmounted, shallowRef, useTemplateRef } from 'vue'

// Combobox dropdown yang bisa diketik untuk search. Bind value via v-model.
// Dropdown di-teleport ke body dengan position:fixed agar tidak terpotong
// oleh parent yang punya overflow:hidden/auto (mis. modal dengan scroll).
interface Option { value: string; label: string }
const props = defineProps<{
  modelValue: string
  options: Option[]
  allLabel?: string // teks opsi "semua" (value '')
  placeholder?: string
}>()
const emit = defineEmits<{ 'update:modelValue': [string] }>()

const open = shallowRef(false)
const query = shallowRef('')
const inputEl = useTemplateRef<HTMLInputElement>('inputEl')
const wrapEl = useTemplateRef<HTMLDivElement>('wrapEl')
const activeIdx = shallowRef(0)

// posisi dropdown (fixed, relatif terhadap viewport)
const dropStyle = shallowRef<{ top: string; left: string; width: string }>({
  top: '0px', left: '0px', width: '200px',
})

function calcDropPosition() {
  const el = wrapEl.value
  if (!el) return
  const rect = el.getBoundingClientRect()
  const spaceBelow = window.innerHeight - rect.bottom
  const dropH = Math.min(288, items.value.length * 36 + 8) // max-h-72 = 288px
  const top = spaceBelow >= dropH
    ? rect.bottom + 4
    : rect.top - dropH - 4
  dropStyle.value = {
    top: `${top}px`,
    left: `${rect.left}px`,
    width: `${rect.width}px`,
  }
}

const selectedLabel = computed(() => {
  if (!props.modelValue) return props.allLabel ?? ''
  return props.options.find((o) => o.value === props.modelValue)?.label ?? props.modelValue
})

// daftar opsi terfilter (+ opsi "semua" di atas bila ada)
const items = computed<Option[]>(() => {
  const q = query.value.trim().toLowerCase()
  const base = props.options.filter(
    (o) => !q || o.label.toLowerCase().includes(q) || o.value.toLowerCase().includes(q),
  )
  return props.allLabel !== undefined ? [{ value: '', label: props.allLabel }, ...base] : base
})

function openList() {
  open.value = true
  query.value = ''
  activeIdx.value = 0
  nextTick(calcDropPosition)
}
function pick(v: string) {
  emit('update:modelValue', v)
  open.value = false
  query.value = ''
}
function onInput(e: Event) {
  query.value = (e.target as HTMLInputElement).value
  if (!open.value) {
    open.value = true
    nextTick(calcDropPosition)
  }
  activeIdx.value = 0
}
function onBlur() {
  setTimeout(() => { open.value = false }, 150)
}
function move(d: number) {
  if (!open.value) { open.value = true; nextTick(calcDropPosition); return }
  const n = items.value.length
  if (!n) return
  activeIdx.value = (activeIdx.value + d + n) % n
}
function enter() {
  if (open.value && items.value[activeIdx.value]) pick(items.value[activeIdx.value].value)
}
async function clearSel() {
  emit('update:modelValue', '')
  query.value = ''
  await nextTick()
  inputEl.value?.focus()
}

// tutup dropdown saat scroll/resize
function closeOnScroll() { if (open.value) open.value = false }
window.addEventListener('scroll', closeOnScroll, true)
window.addEventListener('resize', closeOnScroll)
onUnmounted(() => {
  window.removeEventListener('scroll', closeOnScroll, true)
  window.removeEventListener('resize', closeOnScroll)
})
</script>

<template>
  <div ref="wrapEl" class="relative">
    <input
      ref="inputEl"
      :value="open ? query : selectedLabel"
      :placeholder="placeholder ?? 'Cari…'"
      type="text"
      autocomplete="off"
      class="h-9 w-full rounded-lg border border-border bg-surface pl-2 pr-14 text-sm focus:outline-none focus:ring-1 focus:ring-primary"
      @focus="openList"
      @input="onInput"
      @blur="onBlur"
      @keydown.down.prevent="move(1)"
      @keydown.up.prevent="move(-1)"
      @keydown.enter.prevent="enter"
      @keydown.esc="open = false"
    />
    <button
      v-if="modelValue"
      type="button"
      class="absolute right-7 top-0 h-9 w-6 grid place-items-center text-muted hover:text-foreground"
      title="Hapus pilihan"
      @mousedown.prevent="clearSel"
    >
      <X class="w-3.5 h-3.5" />
    </button>
    <ChevronDown class="absolute right-2 top-2.5 w-4 h-4 text-muted pointer-events-none" />

    <!-- Dropdown di-teleport ke body agar tidak terpotong overflow modal -->
    <Teleport to="body">
      <ul
        v-if="open"
        :style="dropStyle"
        class="fixed z-[9998] max-h-72 overflow-auto rounded-lg border border-border bg-surface shadow-lg text-sm"
      >
        <li
          v-for="(o, i) in items"
          :key="o.value || '__all__'"
          class="px-3 py-1.5 cursor-pointer"
          :class="[
            i === activeIdx ? 'bg-primary/10 text-primary' : 'hover:bg-background',
            o.value === modelValue && i !== activeIdx ? 'font-medium' : '',
          ]"
          @mousedown.prevent="pick(o.value)"
          @mousemove="activeIdx = i"
        >{{ o.label }}</li>
        <li v-if="!items.length" class="px-3 py-1.5 text-muted italic">Tidak ada hasil</li>
      </ul>
    </Teleport>
  </div>
</template>
