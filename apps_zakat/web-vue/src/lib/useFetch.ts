import { shallowRef } from 'vue'

import { ApiError } from '@/lib/api/client'

/**
 * Composable untuk fetch endpoint async dengan state loading/error/data.
 * Cocok untuk per-chart fetching di dashboard — tiap section punya state
 * sendiri, gagal di satu section tidak menggagalkan section lain.
 */
export function useFetch<T>(fetcher: () => Promise<T>) {
  const loading = shallowRef(false)
  const error = shallowRef<string | null>(null)
  const data = shallowRef<T | null>(null)

  async function load() {
    loading.value = true
    error.value = null
    try {
      data.value = (await fetcher()) as T
    } catch (e) {
      if (e instanceof ApiError) {
        error.value = e.message || 'Gagal memuat data'
      } else {
        error.value = 'Gagal memuat data'
      }
      data.value = null
    } finally {
      loading.value = false
    }
  }

  return { loading, error, data, load }
}
