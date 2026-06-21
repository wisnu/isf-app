import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import '@/shared/utils/charts'
import router from '@/router'
import { useNotificationsStore } from '@/app/stores/notification.store'
import { useSidebarStore } from '@/app/stores/sidebar.store'
import { useThemeStore } from '@/app/stores/theme.store'
import '@/styles.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)

useThemeStore().init()
useSidebarStore().init()
useNotificationsStore().init()

app.mount('#app')
