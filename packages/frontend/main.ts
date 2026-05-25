import { createApp } from 'vue'
import { createRouter,createWebHistory } from "vue-router";
import { createPinia } from "pinia";
import App from './src/App.vue'
import RegisterView from './src/views/RegisterView.vue'
import LoginView from './src/views/LoginView.vue'
import NoteView from './src/views/NoteView.vue'
import UserProView from './src/views/UserProView.vue'
import ShareNoteView from './src/views/ShareNoteView.vue'

const routes = [
    {path:"/",component:LoginView},
    {path:"/login",component:LoginView},
    {path:"/register",component:RegisterView},
    {path:"/notes",component:NoteView},
    {path:"/user",component:UserProView},
    {path:"/share",component:ShareNoteView}
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

let isPageVisible = true;

document.addEventListener('visibilitychange', () => {
  isPageVisible = !document.hidden;
});

window.addEventListener('beforeunload', () => {
  // 如果页面不可见，说明是关闭；否则可能是刷新
  if (isPageVisible) {
    return;
  }
  
  console.log('❌ 标签页关闭，清空登录状态');
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user_info');
});