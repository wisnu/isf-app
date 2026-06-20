import { acceptHMRUpdate, defineStore } from 'pinia'

const STORAGE_KEY = 'isf-theme'

type Mode = 'light' | 'dark'

function readStored(): Mode {
  return localStorage.getItem(STORAGE_KEY) === 'dark' ? 'dark' : 'light'
}

function applyDom(mode: Mode) {
  document.documentElement.classList.toggle('dark', mode === 'dark')
}

export const useThemeStore = defineStore('theme', {
  state: () => ({ mode: 'light' as Mode }),
  getters: {
    isDark: (state): boolean => state.mode === 'dark',
  },
  actions: {
    init() {
      this.mode = readStored()
      applyDom(this.mode)
    },
    setMode(mode: Mode) {
      this.mode = mode
      applyDom(mode)
      localStorage.setItem(STORAGE_KEY, mode)
    },
    toggle() {
      this.setMode(this.mode === 'dark' ? 'light' : 'dark')
    },
  },
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useThemeStore, import.meta.hot))
}
