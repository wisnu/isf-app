import { acceptHMRUpdate, defineStore } from 'pinia'

const STORAGE_KEY = 'isf-notif-read'

export type NotificationKind = 'info' | 'success' | 'warning'

export interface AppNotification {
  id: string
  type: NotificationKind
  title: string
  body: string
  ts: string
  read: boolean
}

const DUMMY: AppNotification[] = [
  {
    id: 'n1',
    type: 'success',
    title: 'Penyaluran disetujui',
    body: 'Penyaluran Rp 50.000.000 ke Yayasan Cahaya disetujui',
    ts: '2026-05-19T10:30:00+07:00',
    read: false,
  },
  {
    id: 'n2',
    type: 'info',
    title: 'Donasi besar masuk',
    body: 'Donasi Rp 50.000.000 dari Yayasan Nurani · Wakaf Produktif',
    ts: '2026-05-19T09:15:00+07:00',
    read: false,
  },
  {
    id: 'n3',
    type: 'warning',
    title: 'Laporan periode Mei',
    body: 'Perlu finalisasi sebelum 25 Mei 2026',
    ts: '2026-05-18T16:00:00+07:00',
    read: false,
  },
  {
    id: 'n4',
    type: 'info',
    title: '142 donatur baru bulan ini',
    body: 'Naik 21.5% dibanding April',
    ts: '2026-05-18T08:00:00+07:00',
    read: true,
  },
  {
    id: 'n5',
    type: 'info',
    title: 'Tren penerimaan positif',
    body: 'Penerimaan bulan ini naik 12.4% YoY',
    ts: '2026-05-17T15:00:00+07:00',
    read: true,
  },
]

export const useNotificationsStore = defineStore('notifications', {
  state: () => ({ items: [...DUMMY] as AppNotification[] }),
  getters: {
    unreadCount(state): number {
      return state.items.filter((n) => !n.read).length
    },
  },
  actions: {
    init() {
      try {
        const raw = localStorage.getItem(STORAGE_KEY)
        if (!raw) return
        const readIds = new Set<string>(JSON.parse(raw))
        this.items.forEach((n) => {
          n.read = readIds.has(n.id)
        })
      } catch {
        // ignore
      }
    },
    persist() {
      const readIds = this.items.filter((n) => n.read).map((n) => n.id)
      localStorage.setItem(STORAGE_KEY, JSON.stringify(readIds))
    },
    markAllRead() {
      this.items.forEach((n) => {
        n.read = true
      })
      this.persist()
    },
    markRead(id: string) {
      const n = this.items.find((x) => x.id === id)
      if (n && !n.read) {
        n.read = true
        this.persist()
      }
    },
  },
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useNotificationsStore, import.meta.hot))
}
