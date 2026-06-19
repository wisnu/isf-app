import { shallowRef } from 'vue'
import { defineStore } from 'pinia'

const STORAGE_KEY = 'isf-sidebar-collapsed'

export const useSidebarStore = defineStore('sidebar', () => {
  const collapsed = shallowRef(false)

  function init() {
    collapsed.value = localStorage.getItem(STORAGE_KEY) === '1'
  }

  function toggle() {
    collapsed.value = !collapsed.value
    localStorage.setItem(STORAGE_KEY, collapsed.value ? '1' : '0')
  }

  return { collapsed, init, toggle }
})
