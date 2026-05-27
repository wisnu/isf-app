import { ref } from 'vue'

export type ToastType = 'success' | 'error' | 'warning' | 'info'

export interface ToastItem {
  id: number
  type: ToastType
  message: string
}

const toasts = ref<ToastItem[]>([])
let nextId = 1

function push(type: ToastType, message: string, timeoutMs = 4000) {
  const id = nextId++
  toasts.value.push({ id, type, message })
  if (timeoutMs > 0) {
    setTimeout(() => dismiss(id), timeoutMs)
  }
  return id
}

function dismiss(id: number) {
  toasts.value = toasts.value.filter((t) => t.id !== id)
}

export function useToast() {
  return {
    toasts,
    success: (message: string, timeoutMs?: number) => push('success', message, timeoutMs),
    error: (message: string, timeoutMs?: number) => push('error', message, timeoutMs),
    warning: (message: string, timeoutMs?: number) => push('warning', message, timeoutMs),
    info: (message: string, timeoutMs?: number) => push('info', message, timeoutMs),
    dismiss,
  }
}
