import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { Quasar, Dark } from 'quasar'

import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/src/css/index.sass'

import App from '@/App.vue'
import router from '@/router'
import { useThemeStore } from '@/stores/theme'
import '@/styles.css'

const app = createApp(App)
app.use(createPinia())
app.use(Quasar, {
  plugins: { Dark },
  config: {},
})
app.use(router)

useThemeStore().init()

app.mount('#app')
