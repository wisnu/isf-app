import { defineStore } from 'pinia'
import { Dark } from 'quasar'

const STORAGE_KEY = 'isf-theme'

type Mode = 'light' | 'dark'

function readStored(): Mode {
  return localStorage.getItem(STORAGE_KEY) === 'dark' ? 'dark' : 'light'
}

export const useThemeStore = defineStore('theme', {
  state: () => ({ mode: 'light' as Mode }),
  getters: {
    isDark: (state): boolean => state.mode === 'dark',
  },
  actions: {
    init() {
      this.mode = readStored()
      Dark.set(this.mode === 'dark')
    },
    setMode(mode: Mode) {
      this.mode = mode
      Dark.set(mode === 'dark')
      localStorage.setItem(STORAGE_KEY, mode)
    },
    toggle() {
      this.setMode(this.mode === 'dark' ? 'light' : 'dark')
    },
  },
})
