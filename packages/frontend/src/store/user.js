// src/stores/user.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  // 状态
  const userInfo = ref({
    id: null,
    username: '',
    email: '',
    phone: '',
    avatar: ''
  })

  const access_token = ref(localStorage.getItem('access_token') || '')
  const refresh_token = ref(localStorage.getItem('refresh_token') || '')
  
  // 计算属性：是否已登录
  const isLoggedIn = computed(() => !!access_token.value)
  
  // 登录
  const login = (loginData) => {
    access_token.value = loginData.access_token
    refresh_token.value = loginData.refresh_token
    userInfo.value = {
      id: loginData.user_id,
      username: loginData.username,
      email: loginData.email,
      phone: loginData.phone,
      avatar: loginData.avatar
    }

    // 持久化存储
    localStorage.setItem('access_token', access_token.value)
    localStorage.setItem('refresh_token', refresh_token.value)
    localStorage.setItem('user_info', JSON.stringify(userInfo.value))
  }

  // 退出登录
  const logout = () => {
    access_token.value = ''
    refresh_token.value = ''
    userInfo.value = {
      id: null,
      username: '',
      email: '',
      phone: '',
      avatar: ''
    }

    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user_info')
  }

  // 更新用户信息
  const updateUserInfo = (info) => {
    userInfo.value = { ...userInfo.value, ...info }
    localStorage.setItem('user_info', JSON.stringify(userInfo.value))
  }

  // 从本地存储恢复用户信息
  const restoreUserInfo = () => {
    const savedUserInfo = localStorage.getItem('user_info')
    if (savedUserInfo) {
      try {
        userInfo.value = JSON.parse(savedUserInfo)
      } catch (error) {
        console.error('解析用户信息失败', error)
      }
    }
  }

  // 初始化时恢复用户信息
  restoreUserInfo()

  return {
    userInfo,
    access_token,
    refresh_token,
    isLoggedIn,
    login,
    logout,
    updateUserInfo,
    restoreUserInfo
  }
})