import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from '@/App.vue'
import '@/lib/charts'
import router from '@/router'
import { useNotificationsStore } from '@/stores/notifications'
import { useSidebarStore } from '@/stores/sidebar'
import { useThemeStore } from '@/stores/theme'
import '@/styles.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)

useThemeStore().init()
useSidebarStore().init()
useNotificationsStore().init()

app.mount('#app')
