import { computed } from 'vue'
import { useAuthStore } from '@/app/stores/auth.store'

export function usePermission(menuKey: string) {
  const auth = useAuthStore()
  const actions = computed(() => auth.menuActions[menuKey] ?? [])
  return {
    canView:   computed(() => actions.value.includes('view')),
    canAdd:    computed(() => actions.value.includes('tambah')),
    canEdit:   computed(() => actions.value.includes('edit')),
    canDelete: computed(() => actions.value.includes('hapus')),
    canDetail: computed(() => actions.value.includes('detail')),
  }
}
