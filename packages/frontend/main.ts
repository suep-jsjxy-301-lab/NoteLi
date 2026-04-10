import { createApp } from 'vue'
import { createRouter,createWebHistory } from "vue-router";
import { createPinia } from "pinia";
import App from './src/App.vue'
import RegisterView from './src/views/RegisterView.vue'
import LoginView from './src/views/LoginView.vue'
import NoteView from './src/views/NoteView.vue'
import UserProView from './src/views/UserProView.vue'

const routes = [
    {path:"/",component:LoginView},
    {path:"/login",component:LoginView},
    {path:"/register",component:RegisterView},
    {path:"/notes",component:NoteView},
    {path:"/user",component:UserProView}
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.mount('#app')