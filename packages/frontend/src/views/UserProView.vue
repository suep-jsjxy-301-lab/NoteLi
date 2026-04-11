<template>
  <div class="profile-container">
    <!-- 页面标题栏 -->
    <div class="page-header">
      <div class="header-left">
        <h1>个人中心</h1>
        <p class="subtitle">管理您的账户信息与安全设置</p>
      </div>
      <button class="logout-btn" @click="handlehome">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
          <path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/>
        </svg>
        <span>返回主页</span>
      </button>
    </div>

    <!-- 主要内容区域 -->
    <div class="profile-content">
      <!-- 左侧：头像与基础信息卡片 -->
      <div class="profile-sidebar">
        <div class="avatar-card">
          <div class="avatar-wrapper" @click="openAvatarUpload">
            <img 
              v-if="userInfo.avatar" 
              :src="userInfo.avatar" 
              :alt="userInfo.username"
              class="avatar-image"
            />
            <div v-else class="avatar-placeholder">
              {{ userInitial }}
            </div>
            <div class="avatar-overlay">
              <svg viewBox="0 0 24 24" width="20" height="20" fill="white">
                <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
              </svg>
              <span>更换头像</span>
            </div>
          </div>
          <h3 class="username">{{ userInfo.nickname || userInfo.username }}</h3>
          <p class="user-id">ID: {{ userInfo.id }}</p>
          
          <!-- 认证状态 -->
          <div class="verified-badge" :class="{ verified: userInfo.isVerified }">
            <svg v-if="userInfo.isVerified" viewBox="0 0 24 24" width="14" height="14" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
            <span>{{ userInfo.isVerified ? '已认证' : '未认证' }}</span>
          </div>
        </div>

        <!-- 隐藏的文件上传 input -->
        <input 
          ref="avatarInput"
          type="file" 
          accept="image/*"
          style="display: none"
          @change="handleAvatarChange"
        />
      </div>

      <!-- 右侧：详细信息与操作面板 -->
      <div class="profile-main">
        <!-- 基本信息面板 -->
        <div class="info-panel">
          <div class="panel-header">
            <h2>
              <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
              </svg>
              基本信息
            </h2>
          </div>
          
          <div class="info-grid">
            <div class="info-item">
              <div class="info-icon user-icon">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                  <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                </svg>
              </div>
              <div class="info-content">
                <span class="info-label">用户名</span>
                <span class="info-value">{{ userInfo.username }}</span>
              </div>
              <button class="edit-btn" @click="openModal('username')" title="修改用户名">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                  <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                </svg>
              </button>
            </div>

            <div class="info-item">
              <div class="info-icon email-icon">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                  <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                </svg>
              </div>
              <div class="info-content">
                <span class="info-label">邮箱</span>
                <span class="info-value" :class="{ empty: !userInfo.email }">
                  {{ userInfo.email || '未设置' }}
                </span>
              </div>
              <button class="edit-btn" @click="openModal('email')" title="修改邮箱">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                  <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                </svg>
              </button>
            </div>

            <div class="info-item">
              <div class="info-icon phone-icon">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                  <path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/>
                </svg>
              </div>
              <div class="info-content">
                <span class="info-label">电话</span>
                <span class="info-value" :class="{ empty: !userInfo.phone }">
                  {{ userInfo.phone || '未设置' }}
                </span>
              </div>
              <button class="edit-btn" @click="openModal('phone')" title="修改电话">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                  <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- 安全设置面板 -->
        <div class="security-panel">
          <h2>
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
              <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/>
            </svg>
            安全设置
          </h2>
          
          <div class="security-item" @click="openModal('password')">
            <div class="security-icon">
              <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor">
                <path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/>
              </svg>
            </div>
            <div class="security-content">
              <span class="security-title">修改密码</span>
              <span class="security-desc">定期更换密码可以保护账户安全</span>
            </div>
            <svg class="arrow-icon" viewBox="0 0 24 24" width="20" height="20" fill="#8c8c8c">
              <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
            </svg>
          </div>
        </div>

        <!-- 危险操作区域 -->
        <div class="danger-zone">
          <h2>
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
              <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
            </svg>
            危险操作
          </h2>
          <div class="danger-item" @click="openDeleteConfirm">
            <div class="danger-icon">
              <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
              </svg>
            </div>
            <div class="danger-content">
              <span class="danger-title">永久注销账户</span>
              <span class="danger-desc">注销后所有数据将被永久删除，无法恢复</span>
            </div>
            <svg class="arrow-icon" viewBox="0 0 24 24" width="20" height="20" fill="#e53e3e">
              <path d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z"/>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- 修改信息的弹窗 -->
    <div class="modal-overlay" :class="{ show: showModal }" @click="closeModal"></div>
    <div class="modal" :class="{ show: showModal }">
      <div class="modal-header">
        <h3>{{ modalTitle }}</h3>
        <button class="modal-close" @click="closeModal">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
            <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
          </svg>
        </button>
      </div>
      
      <div class="modal-body">
        <!-- 修改用户名 -->
        <div v-if="modalType === 'username'">
          <div class="form-group">
            <label>新用户名</label>
            <input 
              type="text" 
              v-model="formData.username"
              placeholder="请输入新的用户名"
              maxlength="20"
            />
          </div>
        </div>

        <!-- 修改邮箱 -->
        <div v-if="modalType === 'email'">
          <div class="form-group">
            <label>新邮箱地址</label>
            <input 
              type="email" 
              v-model="formData.email"
              placeholder="请输入新的邮箱"
            />
          </div>
        </div>

        <!-- 修改电话 -->
        <div v-if="modalType === 'phone'">
          <div class="form-group">
            <label>新电话号码</label>
            <input 
              type="tel" 
              v-model="formData.phone"
              placeholder="请输入新的电话号码（可选）"
            />
          </div>
        </div>

        <!-- 修改密码 -->
        <div v-if="modalType === 'password'">
          <div class="form-group">
            <label>当前密码</label>
            <input 
              type="password" 
              v-model="formData.currentPassword"
              placeholder="请输入当前密码"
            />
          </div>
          <div class="form-group">
            <label>新密码</label>
            <input 
              type="password" 
              v-model="formData.newPassword"
              placeholder="请输入新密码（至少6位）"
            />
          </div>
          <div class="form-group">
            <label>确认新密码</label>
            <input 
              type="password" 
              v-model="formData.confirmPassword"
              placeholder="请再次输入新密码"
            />
          </div>
        </div>

        <div v-if="message.text" class="modal-message" :class="message.type">
          {{ message.text }}
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="btn-cancel" @click="closeModal">取消</button>
        <button class="btn-confirm" @click="handleConfirm" :disabled="isLoading">
          {{ isLoading ? '处理中...' : '确认修改' }}
        </button>
      </div>
    </div>

    <!-- 注销确认弹窗 -->
    <div class="modal-overlay" :class="{ show: showDeleteModal }" @click="closeDeleteModal"></div>
    <div class="modal confirm-modal" :class="{ show: showDeleteModal }">
      <div class="modal-header">
        <h3>
          <svg viewBox="0 0 24 24" width="20" height="20" fill="#e53e3e">
            <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
          </svg>
          永久注销账户
        </h3>
      </div>
      <div class="modal-body">
        <p class="warning-text">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="#e53e3e">
            <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
          </svg>
          此操作不可逆转！您的所有笔记、分类、标签等数据将被永久删除。
        </p>
        <div class="form-group">
          <label>请输入您的密码以确认</label>
          <input 
            type="password" 
            v-model="deleteConfirmPassword"
            placeholder="请输入当前密码"
          />
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn-cancel" @click="closeDeleteModal">取消</button>
        <button class="btn-danger" @click="handleDeleteAccount" :disabled="deleteLoading">
          {{ deleteLoading ? '注销中...' : '确认注销' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../store/user'
import { verify_password, deleteMeApi, changePasswordApi, logoutApi } from '../api/auth'

const router = useRouter()
const userStore = useUserStore()

// ========== 用户信息（模拟数据） ==========
const userInfo = reactive({
  id: userStore.userInfo.id,
  username: userStore.userInfo.username,
  email: userStore.userInfo.email,
  phone: userStore.userInfo.phone || '',
  avatar: userStore.userInfo.avatar,
  isVerified: true
})

// 用户头像首字母
const userInitial = computed(() => {
  const name = userInfo.username
  return name ? name.charAt(0).toUpperCase() : 'U'
})

// ========== 弹窗状态 ==========
const showModal = ref(false)
const modalType = ref('') // 'username', 'email', 'phone', 'password'
const isLoading = ref(false)
const message = reactive({ text: '', type: 'success' })

// 表单数据
const formData = reactive({
  username: '',
  email: '',
  phone: '',
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// 模态框标题
const modalTitle = computed(() => {
  const titles = {
    username: '修改用户名',
    email: '修改邮箱',
    phone: '修改电话',
    password: '修改密码'
  }
  return titles[modalType.value] || ''
})

// ========== 头像上传 ==========
const avatarInput = ref(null)

const openAvatarUpload = () => {
  avatarInput.value?.click()
}

const handleAvatarChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      userInfo.avatar = e.target.result
      showMessage('头像已更新', 'success')
    }
    reader.readAsDataURL(file)
  }
}

// ========== 返回主页 ==========
const handlehome = () => {
  router.push('/notes')
}

// ========== 弹窗操作 ==========
const openModal = (type) => {
  modalType.value = type
  
  switch (type) {
    case 'username':
      formData.username = userInfo.username
      break
    case 'email':
      formData.email = userInfo.email
      break
    case 'phone':
      formData.phone = userInfo.phone
      break
    case 'password':
      formData.currentPassword = ''
      formData.newPassword = ''
      formData.confirmPassword = ''
      break
  }
  
  message.text = ''
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  modalType.value = ''
  message.text = ''
}

const showMessage = (text, type = 'success') => {
  message.text = text
  message.type = type
  setTimeout(() => {
    message.text = ''
  }, 3000)
}

// ========== 确认修改 ==========
const handleConfirm = async () => {
  isLoading.value = true
  
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    switch (modalType.value) {
      case 'username':
        if (!formData.username.trim()) {
          showMessage('用户名不能为空', 'error')
          isLoading.value = false
          return
        }
        userInfo.username = formData.username
        showMessage('用户名修改成功', 'success')
        break
        
      case 'email':
        if (!formData.email.trim()) {
          showMessage('邮箱不能为空', 'error')
          isLoading.value = false
          return
        }
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
          showMessage('请输入有效的邮箱地址', 'error')
          isLoading.value = false
          return
        }
        userInfo.email = formData.email
        showMessage('邮箱修改成功', 'success')
        break
        
      case 'phone':
        if (formData.phone && !/^1[3-9]\d{9}$/.test(formData.phone)) {
          showMessage('请输入有效的手机号', 'error')
          isLoading.value = false
          return
        }
        userInfo.phone = formData.phone || ''
        showMessage('电话修改成功', 'success')
        break
        
      case 'password':
        if (!formData.currentPassword) {
          showMessage('请输入当前密码', 'error')
          isLoading.value = false
          return
        }
        if (formData.newPassword.length < 6) {
          showMessage('新密码至少需要6位', 'error')
          isLoading.value = false
          return
        }
        if (formData.newPassword !== formData.confirmPassword) {
          showMessage('两次输入的密码不一致', 'error')
          isLoading.value = false
          return
        }
        const response = await verify_password(formData.currentPassword)
        if (response.data.success !== true) {
          showMessage('当前密码错误', 'error')
          isLoading.value = false
          return
        }
        const response2 = await changePasswordApi(formData.newPassword)
        if(response2.data.success !== true) {
          showMessage('密码修改失败，请稍后重试', 'error')
          isLoading.value = false
          return
        }
        showMessage('密码修改成功，请重新登录', 'success')
        await logoutApi(userStore.refresh_token, userStore.access_token)
        userStore.logout()
        router.push('/login')
        break
    }
    
    closeModal()
  } catch (error) {
    console.error('修改信息出错:', error)
    showMessage('操作失败，请稍后重试', 'error')
  } finally {
    isLoading.value = false
  }
}

// ========== 注销账户 ==========
const showDeleteModal = ref(false)
const deleteConfirmPassword = ref('')
const deleteLoading = ref(false)

const openDeleteConfirm = () => {
  deleteConfirmPassword.value = ''
  showDeleteModal.value = true
}

const closeDeleteModal = () => {
  showDeleteModal.value = false
  deleteConfirmPassword.value = ''
}

const handleDeleteAccount = async () => {
  if (!deleteConfirmPassword.value) {
    alert('请输入密码以确认注销')
    return
  }
  
  deleteLoading.value = true
  try {
    
    const response = await verify_password(deleteConfirmPassword.value)
    if (response.data.success !== true) {
      alert('密码错误，无法注销账户')
      deleteLoading.value = false
      return
    }
    
    await deleteMeApi();
    alert('账户已永久注销。')
    await logoutApi(userStore.refresh_token,userStore.access_token)
    userStore.logout()
    closeDeleteModal()
    router.push('/login')
  } catch (error) {
    alert('注销失败，请稍后重试')
  } finally {
    deleteLoading.value = false
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.profile-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 32px 24px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: #f5f7fa;
  min-height: 100vh;
}

/* ========== 页面标题栏 ========== */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e8e8e8;
}

.header-left h1 {
  font-size: 28px;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 6px;
}

.subtitle {
  color: #8c8c8c;
  font-size: 14px;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: white;
  border: 1.5px solid #e0e0e0;
  border-radius: 30px;
  color: #666;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  border-color: #e53e3e;
  color: #e53e3e;
  background: #fff5f5;
}

/* ========== 主内容区域 ========== */
.profile-content {
  display: flex;
  gap: 24px;
}

/* 左侧边栏 */
.profile-sidebar {
  width: 280px;
  flex-shrink: 0;
}

.avatar-card {
  background: white;
  border-radius: 24px;
  padding: 32px 24px;
  text-align: center;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
  border: 1px solid #f0f0f0;
}

.avatar-wrapper {
  width: 120px;
  height: 120px;
  margin: 0 auto 20px;
  border-radius: 50%;
  overflow: hidden;
  cursor: pointer;
  position: relative;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  font-weight: 600;
  color: white;
}

.avatar-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.5);
  padding: 8px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  color: white;
  font-size: 12px;
  transform: translateY(100%);
  transition: transform 0.2s;
}

.avatar-wrapper:hover .avatar-overlay {
  transform: translateY(0);
}

.username {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 8px;
}

.user-id {
  font-size: 13px;
  color: #8c8c8c;
  background: #f5f5f5;
  padding: 6px 12px;
  border-radius: 20px;
  display: inline-block;
  margin-bottom: 12px;
}

.verified-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  background: #f5f5f5;
  color: #8c8c8c;
}

.verified-badge.verified {
  background: #e8f5e9;
  color: #4caf50;
}

/* 右侧主区域 */
.profile-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.info-panel,
.security-panel,
.danger-zone {
  background: white;
  border-radius: 20px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
  border: 1px solid #f0f0f0;
}

.panel-header h2,
.security-panel h2,
.danger-zone h2 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 20px;
}

.panel-header h2 svg,
.security-panel h2 svg,
.danger-zone h2 svg {
  color: #667eea;
}

.danger-zone h2 svg {
  color: #e53e3e;
}

.info-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  align-items: center;
  padding: 14px 16px;
  background: #fafafa;
  border-radius: 16px;
  transition: all 0.2s;
}

.info-item:hover {
  background: #f5f5f5;
}

.info-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 14px;
}

.user-icon {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  color: #1976d2;
}

.email-icon {
  background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
  color: #7b1fa2;
}

.phone-icon {
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
  color: #388e3c;
}

.info-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 12px;
  color: #8c8c8c;
}

.info-value {
  font-size: 15px;
  font-weight: 500;
  color: #1a1a1a;
}

.info-value.empty {
  color: #b0b0b0;
  font-weight: normal;
}

.edit-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: white;
  border-radius: 10px;
  color: #8c8c8c;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
}

.edit-btn:hover {
  background: #667eea;
  color: white;
}

/* 安全设置 */
.security-item {
  display: flex;
  align-items: center;
  padding: 16px;
  background: #fafafa;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.2s;
}

.security-item:hover {
  background: #f0f0f0;
}

.security-item:hover .arrow-icon {
  transform: translateX(4px);
}

.security-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #f57c00;
  margin-right: 16px;
}

.security-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.security-title {
  font-size: 15px;
  font-weight: 500;
  color: #1a1a1a;
}

.security-desc {
  font-size: 13px;
  color: #8c8c8c;
}

.arrow-icon {
  transition: transform 0.2s;
}

/* 危险区域 */
.danger-item {
  display: flex;
  align-items: center;
  padding: 16px;
  background: #fff5f5;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid #ffebee;
}

.danger-item:hover {
  background: #ffebee;
}

.danger-item:hover .arrow-icon {
  transform: translateX(4px);
}

.danger-icon {
  width: 48px;
  height: 48px;
  background: #ffebee;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #e53e3e;
  margin-right: 16px;
}

.danger-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.danger-title {
  font-size: 15px;
  font-weight: 500;
  color: #c53030;
}

.danger-desc {
  font-size: 13px;
  color: #e53e3e;
}

/* ========== 弹窗 ========== */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s;
  z-index: 1000;
}

.modal-overlay.show {
  opacity: 1;
  visibility: visible;
}

.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(0.9);
  width: 90%;
  max-width: 420px;
  background: white;
  border-radius: 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s;
  z-index: 1001;
}

.modal.show {
  opacity: 1;
  visibility: visible;
  transform: translate(-50%, -50%) scale(1);
}

.confirm-modal {
  max-width: 400px;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #f0f0f0;
}

.modal-header h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
}

.modal-close {
  width: 32px;
  height: 32px;
  border: none;
  background: #f5f5f5;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8c8c8c;
  transition: all 0.2s;
}

.modal-close:hover {
  background: #e0e0e0;
}

.modal-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #4a4a4a;
}

.form-group input {
  width: 100%;
  padding: 14px 16px;
  border: 1.5px solid #e0e0e0;
  border-radius: 14px;
  font-size: 15px;
  transition: all 0.3s;
  background: #fafafa;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.warning-text {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #fff5f5;
  padding: 14px 16px;
  border-radius: 14px;
  color: #c53030;
  font-size: 14px;
  margin-bottom: 20px;
  border: 1px solid #ffebee;
}

.modal-message {
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  margin-top: 16px;
}

.modal-message.success {
  background: #f0fff4;
  color: #276749;
}

.modal-message.error {
  background: #fff5f5;
  color: #c53030;
}

.modal-footer {
  display: flex;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid #f0f0f0;
}

.btn-cancel,
.btn-confirm,
.btn-danger {
  flex: 1;
  padding: 14px;
  border-radius: 14px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn-cancel {
  background: #f5f5f5;
  color: #666;
}

.btn-cancel:hover {
  background: #e8e8e8;
}

.btn-confirm {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-confirm:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 12px rgba(102, 126, 234, 0.25);
}

.btn-confirm:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-danger {
  background: #e53e3e;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #c53030;
}

.btn-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ========== 响应式 ========== */
@media (max-width: 768px) {
  .profile-container {
    padding: 20px 16px;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .logout-btn {
    width: 100%;
    justify-content: center;
  }

  .profile-content {
    flex-direction: column;
  }
  
  .profile-sidebar {
    width: 100%;
  }
}
</style>