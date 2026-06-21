<script setup lang="ts">
import { AlertTriangle, Bell, CheckCircle2, Info } from 'lucide-vue-next'
import { computed } from 'vue'

import DropdownMenu from '@/components/ui/DropdownMenu.vue'
import { cn } from '@/shared/utils/utils'
import { useNotificationsStore, type NotificationKind } from '@/stores/notifications'

const notifications = useNotificationsStore()
const items = computed(() => notifications.items)
const unread = computed(() => notifications.unreadCount)

function iconFor(kind: NotificationKind) {
  if (kind === 'success') return CheckCircle2
  if (kind === 'warning') return AlertTriangle
  return Info
}

function colorFor(kind: NotificationKind): string {
  if (kind === 'success') return 'text-positive'
  if (kind === 'warning') return 'text-warning'
  return 'text-primary'
}

function relativeTime(ts: string): string {
  const then = new Date(ts).getTime()
  const now = Date.now()
  const diffMin = Math.round((now - then) / 60000)
  if (Math.abs(diffMin) < 1) return 'baru saja'
  if (Math.abs(diffMin) < 60) return `${diffMin} mnt lalu`
  const diffHr = Math.round(diffMin / 60)
  if (Math.abs(diffHr) < 24) return `${diffHr} jam lalu`
  const diffDay = Math.round(diffHr / 24)
  if (Math.abs(diffDay) < 7) return `${diffDay} hari lalu`
  return new Intl.DateTimeFormat('id-ID', {
    day: 'numeric',
    month: 'short',
  }).format(new Date(ts))
}
</script>

<template>
  <DropdownMenu content-class="w-[22rem] p-0">
    <template #trigger>
      <button
        type="button"
        :class="
          cn(
            'relative h-8 w-8 inline-flex items-center justify-center rounded-md text-primary-foreground',
            'hover:bg-white/15 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/40',
          )
        "
        title="Notifikasi"
      >
        <Bell class="w-4 h-4" />
        <span
          v-if="unread > 0"
          class="absolute -top-1 -right-1 bg-destructive text-destructive-foreground text-[10px] font-semibold rounded-full min-w-[16px] h-4 px-1 grid place-items-center leading-none"
        >{{ unread > 9 ? '9+' : unread }}</span>
      </button>
    </template>

    <div class="px-3 py-2.5 border-b border-border flex items-center justify-between gap-2">
      <span class="text-sm font-medium text-foreground">
        Notifikasi
        <span v-if="unread > 0" class="text-xs text-muted font-normal">({{ unread }} baru)</span>
      </span>
      <button
        v-if="unread > 0"
        type="button"
        class="text-xs text-primary hover:underline"
        @click="notifications.markAllRead()"
      >
        Tandai semua dibaca
      </button>
    </div>

    <div class="max-h-80 overflow-y-auto">
      <div
        v-for="n in items"
        :key="n.id"
        class="flex items-start gap-2 px-3 py-2 hover:bg-background/60 border-b border-border last:border-0 cursor-default"
        @click="notifications.markRead(n.id)"
      >
        <component
          :is="iconFor(n.type)"
          class="w-4 h-4 mt-0.5 shrink-0"
          :class="colorFor(n.type)"
        />
        <div class="min-w-0 flex-1">
          <p class="text-sm text-foreground" :class="{ 'font-medium': !n.read }">
            {{ n.title }}
          </p>
          <p class="text-xs text-muted">{{ n.body }}</p>
          <p class="text-[10px] text-muted mt-0.5">{{ relativeTime(n.ts) }}</p>
        </div>
        <span
          v-if="!n.read"
          class="w-2 h-2 rounded-full bg-primary mt-1.5 shrink-0"
          aria-label="belum dibaca"
        />
      </div>

      <div
        v-if="items.length === 0"
        class="px-3 py-8 text-sm text-muted text-center"
      >
        Tidak ada notifikasi
      </div>
    </div>
  </DropdownMenu>
</template>
