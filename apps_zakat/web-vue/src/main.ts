import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'

import App from '@/App.vue'
import '@/shared/utils/charts'
import router from '@/router'
import { useNotificationsStore } from '@/stores/notifications'
import { useSidebarStore } from '@/stores/sidebar'
import { useThemeStore } from '@/stores/theme'
import '@/styles.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(PrimeVue, { unstyled: true })

useThemeStore().init()
useSidebarStore().init()
useNotificationsStore().init()

app.mount('#app')
