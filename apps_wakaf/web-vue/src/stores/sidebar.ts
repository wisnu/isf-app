import { defineStore } from 'pinia'

const STORAGE_KEY = 'isf-sidebar-collapsed'

export const useSidebarStore = defineStore('sidebar', {
  state: () => ({ collapsed: false }),
  actions: {
    init() {
      this.collapsed = localStorage.getItem(STORAGE_KEY) === '1'
    },
    toggle() {
      this.collapsed = !this.collapsed
      localStorage.setItem(STORAGE_KEY, this.collapsed ? '1' : '0')
    },
  },
})
