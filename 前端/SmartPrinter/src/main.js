import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'  // 用于PWA
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import router from './router'  // Vue Router路由
import ElementPlus from 'element-plus' // Element Plus 的组件库
import 'element-plus/dist/index.css'
import axios from "axios"
import VueAxios from 'vue-axios'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'  // Element Plus 的中文语言包

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.use(router)
app.use(ElementPlus, {
  locale: zhCn,
})
app.use(VueAxios,axios)
app.config.globalProperties.$http = axios
axios.defaults.baseURL='/';
app.mount('#app')

