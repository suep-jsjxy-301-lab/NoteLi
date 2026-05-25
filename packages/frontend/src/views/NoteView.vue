<template>
  <div class="note-app">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2>📝 笔记管理</h2>
      </div>
      
      <!-- 新建笔记按钮 -->
      <button class="new-note-btn" @click="createNewNote">
        <span>+</span> 新建笔记
      </button>

      <button class="sharenote-btn" @click="router.push('/share')">
        <span>📡</span> 共享笔记
      </button>

      <button class="ai-helper-btn" @click="openAIManage">
        <span>🤖</span> AI助手
      </button>

      <!-- 分类筛选（含管理功能） -->
      <div class="sidebar-section">
        <div class="section-header">
          <h3>分类</h3>
          <button class="manage-btn" @click="openCategoryManage" title="管理分类">
            ⚙️
          </button>
        </div>
        <ul class="category-list">
          <li 
            v-for="cat in categories" 
            :key="cat.category_name"
            :class="{ active: activeCategory === cat.category_name }"
            @click="activeCategory = cat.category_name"
          >
            <span class="category-icon">{{ getCategoryIcon(cat.category_name) }}</span>
            <span class="category-name">{{ cat.category_name }}</span>
            <span class="category-count">{{ getCategoryCount(cat.category_name) }}</span>
          </li>
        </ul>
      </div>
      
      <!-- 标签云 -->
      <div class="sidebar-section">
        <h3>热门标签</h3>
        <div class="tags-cloud">
          <span 
            v-for="tag in popularTags" 
            :key="tag"
            class="tag"
            :class="{ active: activeTag === tag }"
            @click="activeTag = activeTag === tag ? '' : tag"
          >
            {{ tag }}
          </span>
        </div>
      </div>
    </aside>
    
    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 顶部搜索栏 -->
      <header class="content-header">
        <div class="search-box">
          <input 
            type="text" 
            v-model="searchKeyword"
            placeholder="搜索笔记标题或内容..."
            class="search-input"
          />
        </div>
        
        <!-- 右侧工具栏：视图切换 + 用户头像 -->
        <div class="header-toolbar">
          <!-- 视图切换按钮 -->
          <div class="view-options">
            <button 
              :class="{ active: viewMode === 'grid' }"
              @click="viewMode = 'grid'"
              title="网格视图"
            >
              <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                <path d="M3 3h7v7H3zm11 0h7v7h-7zm0 11h7v7h-7zM3 14h7v7H3z"/>
              </svg>
            </button>
            <button 
              :class="{ active: viewMode === 'list' }"
              @click="viewMode = 'list'"
              title="列表视图"
            >
              <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                <path d="M3 13h2v-2H3v2zm0 4h2v-2H3v2zm0-8h2V7H3v2zm4 4h14v-2H7v2zm0 4h14v-2H7v2zm0-8h14V7H7v2z"/>
              </svg>
            </button>
          </div>
          
          <!-- 分隔线 -->
          <div class="divider"></div>
          
          <!-- 用户头像下拉菜单 -->
          <div class="user-menu" ref="userMenuRef">
            <button 
              class="user-avatar-btn"
              @click="toggleUserMenu"
              :class="{ active: showUserMenu }"
            >
              <div class="avatar">
                <img 
                  v-if="userInfo.avatar" 
                  :src="userInfo.avatar" 
                  :alt="userInfo.username"
                />
                <span v-else class="avatar-placeholder">
                  {{ userInitial }}
                </span>
              </div>
              <span class="username">{{ userInfo.username }}</span>
              <svg 
                class="dropdown-icon" 
                :class="{ rotate: showUserMenu }"
                viewBox="0 0 24 24" 
                width="16" 
                height="16" 
                fill="currentColor"
              >
                <path d="M7 10l5 5 5-5z"/>
              </svg>
            </button>
            
            <!-- 下拉菜单 -->
            <transition name="dropdown-fade">
              <div v-if="showUserMenu" class="user-dropdown">
                <div class="dropdown-header">
                  <div class="dropdown-avatar">
                    <img 
                      v-if="userInfo.avatar" 
                      :src="userInfo.avatar" 
                      :alt="userInfo.username"
                    />
                    <span v-else class="avatar-placeholder large">
                      {{ userInitial }}
                    </span>
                  </div>
                  <div class="dropdown-user-info">
                    <div class="dropdown-username">{{ userInfo.username }}</div>
                    <div class="dropdown-email">{{ userInfo.email }}</div>
                  </div>
                </div>
                
                <div class="dropdown-divider"></div>
                
                <div class="dropdown-menu-items">
                  <button class="dropdown-item" @click="goToProfile">
                    <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                      <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                    </svg>
                    个人中心
                  </button>
                  
                  <!--
                  <button class="dropdown-item" @click="goToSettings">
                    <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                      <path d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.33-.02-.64-.06-.94l2.02-1.58c.18-.14.23-.38.12-.56l-1.89-3.28c-.12-.19-.36-.26-.56-.18l-2.38.96c-.5-.38-1.06-.68-1.66-.88L14.45 3.5c-.04-.2-.2-.34-.4-.34h-3.78c-.2 0-.36.14-.4.34l-.3 2.52c-.6.2-1.16.5-1.66.88l-2.38-.96c-.2-.08-.44-.01-.56.18l-1.89 3.28c-.12.19-.07.42.12.56l2.02 1.58c-.04.3-.06.61-.06.94 0 .33.02.64.06.94l-2.02 1.58c-.18.14-.23.38-.12.56l1.89 3.28c.12.19.36.26.56.18l2.38-.96c.5.38 1.06.68 1.66.88l.3 2.52c.04.2.2.34.4.34h3.78c.2 0 .36-.14.4-.34l.3-2.52c.6-.2 1.16-.5 1.66-.88l2.38.96c.2.08.44.01.56-.18l1.89-3.28c.12-.19.07-.42-.12-.56l-2.02-1.58zM12 15c-1.66 0-3-1.34-3-3s1.34-3 3-3 3 1.34 3 3-1.34 3-3 3z"/>
                    </svg>
                    账号设置
                  </button>
                  -->
                </div>
                
                <div class="dropdown-divider"></div>
                
                <div class="dropdown-menu-items">
                  <button class="dropdown-item danger" @click="handleLogout">
                    <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                      <path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/>
                    </svg>
                    退出登录
                  </button>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </header>
      
      <!-- 统计卡片 -->
      <div class="stats-cards">
        <div class="stat-card">
          <div class="stat-icon">📄</div>
          <div class="stat-info">
            <span class="stat-value">{{ notes.length }}</span>
            <span class="stat-label">总笔记数</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">⭐</div>
          <div class="stat-info">
            <span class="stat-value">{{ starredNotesCount }}</span>
            <span class="stat-label">收藏笔记</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📂</div>
          <div class="stat-info">
            <span class="stat-value">{{ categories.length }}</span>
            <span class="stat-label">分类数量</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🏷️</div>
          <div class="stat-info">
            <span class="stat-value">{{ allTags.length }}</span>
            <span class="stat-label">标签总数</span>
          </div>
        </div>
      </div>
      
      <!-- 笔记列表/网格 -->
      <div class="notes-container">
        <div v-if="filteredNotes.length === 0" class="empty-state">
          <div class="empty-icon">📭</div>
          <p>暂无笔记，点击"新建笔记"开始记录吧！</p>
        </div>
        
        <div 
          v-else
          :class="['notes-wrapper', viewMode === 'grid' ? 'grid-view' : 'list-view']"
        >
          <div 
            v-for="note in filteredNotes" 
            :key="note.id"
            class="note-card"
            :class="{ starred: note.starred }"
            @click="selectNote(note)"
          >
            <div class="note-header">
              <h4 class="note-title">{{ note.title || '无标题' }}</h4>
              <div class="note-actions" @click.stop>
                <button 
                  class="star-btn" 
                  :class="{ active: note.starred }"
                  @click="toggleStar(note)"
                  title="收藏"
                >
                  {{ note.starred ? '⭐' : '☆' }}
                </button>
                <button class="delete-btn" @click="deleteNote(note)" title="删除">
                  🗑️
                </button>
              </div>
            </div>
            
            <div class="note-preview" v-html="getPreviewContent(note.content)"></div>
            
            <div class="note-footer">
              <span class="note-category">
                <span class="cat-icon">{{ getCategoryIcon(note.category_name) }}</span>
                {{ note.category_name }}
              </span>
              <div class="note-tags" v-if="note.tags && note.tags.length">
                <span 
                  v-for="tag in note.tags.slice(0, 3)" 
                  :key="tag"
                  class="note-tag"
                  @click.stop="activeTag = tag"
                >
                  #{{ tag }}
                </span>
                <span v-if="note.tags.length > 3" class="more-tag">
                  +{{ note.tags.length - 3 }}
                </span>
              </div>
              <span class="note-date">{{ formatDate(note.updatedAt) }}</span>
            </div>
          </div>
        </div>
      </div>
    </main>
    
    <!-- 笔记编辑抽屉 -->
    <div class="drawer-overlay" :class="{ show: showDrawer }" @click="closeDrawer"></div>
    <aside class="note-drawer" :class="{ show: showDrawer }">
      <div class="drawer-header">
        <h3>{{ editingNote?.id ? '编辑笔记' : '新建笔记' }}</h3>
        <button class="close-btn" @click="closeDrawer">✕</button>
      </div>
      
      <div class="drawer-body">
        <div class="form-group">
          <input 
            type="text" 
            v-model="editingNote.title"
            placeholder="笔记标题"
            class="title-input"
          />
        </div>
        
        <div class="form-group">
          <select v-model="editingNote.category_id" class="category-select">
            <option v-for="cat in selectableCategories" :key="cat.id" :value="cat.id">
              {{ getCategoryIcon(cat.category_name) }} {{ cat.category_name }}
            </option>
          </select>
        </div>
        
        <div class="form-group">
          <textarea 
            v-model="editingNote.content"
            placeholder="写下你的笔记内容..."
            class="content-textarea"
            rows="10"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label>标签（用逗号分隔）</label>
          <input 
            type="text" 
            v-model="tagInput"
            placeholder="例如：工作, 重要, 待办"
            class="tag-input"
          />
        </div>
      </div>
      
      <div class="drawer-footer">
        <button class="cancel-btn" @click="closeDrawer">取消</button>
        <button class="save-btn" @click="saveNote">保存</button>
      </div>
    </aside>
    
    <!-- 分类管理弹窗 -->
    <div class="modal-overlay" :class="{ show: showCategoryModal }" @click="closeCategoryManage"></div>
    <div class="category-modal" :class="{ show: showCategoryModal }">
      <div class="modal-header">
        <h3>📂 管理分类</h3>
        <button class="close-btn" @click="closeCategoryManage">✕</button>
      </div>
      
      <div class="modal-body">
        <!-- 添加新分类 -->
        <div class="add-category-section">
          <h4>添加新分类</h4>
          <div class="add-form">
            <div class="icon-selector">
              <label>选择图标</label>
              <div class="icon-grid">
                <span 
                  v-for="icon in iconOptions" 
                  :key="icon"
                  :class="{ active: newCategory.category_icon === icon }"
                  @click="newCategory.category_icon = icon"
                >
                  {{ icon }}
                </span>
              </div>
            </div>
            <div class="name-input">
              <label>分类名称</label>
              <input 
                type="text" 
                v-model="newCategory.category_name" 
                placeholder="例如：旅行"
                maxlength="10"
                @keyup.enter="addCategory"
              />
            </div>
            <button class="add-btn" @click="addCategory" :disabled="!newCategory.category_name.trim()">
              + 添加分类
            </button>
          </div>
        </div>
        
        <!-- 已有分类列表（可编辑） -->
        <div class="existing-categories">
          <h4>已有分类</h4>
          <div v-if="editableCategories.length === 0" class="empty-tip">
            暂无自定义分类，点击上方添加
          </div>
          <ul class="editable-category-list">
            <li v-for="cat in editableCategories" :key="cat.category_name">
              <span class="category-icon">
                <select v-model="editingCopies[cat.category_name].category_icon" class="icon-select">
                  <option v-for="(icon, index) in iconOptions" :key="icon" :value="index+1">
                    {{ icon }}
                  </option>
                </select>
              </span>
              <input 
                type="text" 
                v-model="editingCopies[cat.category_name].category_name" 
                class="category-name-input"
                maxlength="10"
              />
              <div class="category-actions">
                <button class="save-btn-small" @click="updateCategory(cat, editingCopies[cat.category_name])" title="保存修改">
                  💾
                </button>
                <button 
                  class="delete-btn-small" 
                  @click="deleteCategory(cat)" 
                  title="删除分类"
                  :disabled="getCategoryCount(cat.category_name) > 0"
                >
                  🗑️
                </button>
              </div>
            </li>
          </ul>
          <p class="help-text">
            💡 提示：系统默认分类不可删除，自定义分类删除前需确保没有笔记
          </p>
        </div>
      </div>
    </div>

    <AIAssistantDrawer 
    :visible="showAIDrawer"
    :current-note="currentSelectedNote"
    :all-notes="notes"
    :categories="categories"
    :init_notes="init_notes"
    :init_Categories="init_Categories"
    @close="closeAIDrawer"
    @action="handleAIAction"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import Api from '@/api/api'
import AIAssistantDrawer from '@/views/AIAssistantDrawer.vue'

const router = useRouter()
const userStore = useUserStore()

// ========== 图标选项 ==========
const iconOptions = [
  '📋', '💼', '🏠', '📚', '💡', '✅', 
  '🎯', '🎨', '🎵', '🏃', '🍔', '✈️',
  '📷', '🎮', '❤️', '🌟', '🔥', '💻',
  '📝', '🔧', '🎓', '🏆', '💎', '🌍'
]

// ========== 分类数据 ==========
// 系统默认分类（不可删除）
const defaultCategories = [
  { id:1, category_name: '全部笔记', category_icon: 1, isDefault: true },
  { id:2, category_name: '工作', category_icon: 2, isDefault: true },
  { id:3, category_name: '个人', category_icon: 3, isDefault: true },
  { id:4, category_name: '学习', category_icon: 4, isDefault: true },
  { id:5, category_name: '想法', category_icon: 5, isDefault: true },
  { id:6, category_name: '待办', category_icon: 6, isDefault: true }
]
// 自定义分类（用户可增删改）
const customCategories = ref([])

// 合并所有分类
const categories = computed(() => {
  return [...defaultCategories, ...customCategories.value]
})

// 可选分类（用于下拉选择，排除"全部笔记"）
const selectableCategories = computed(() => {
  return categories.value.filter(c => c.category_name !== '全部笔记')
})

// 可编辑的分类（排除系统默认分类）
const editableCategories = computed(() => {
  return customCategories.value
})

// 副本数据（独立于原始数据）
const editingCopies = reactive({})

const initCopies = () => {
  // 清空旧数据
  Object.keys(editingCopies).forEach(key => {
    delete editingCopies[key]
  })
  
  // 重新填充，以 category_name 为键
  editableCategories.value.forEach(cat => {
    editingCopies[cat.category_name] = {
      category_name: cat.category_name,
      category_icon: cat.category_icon
    }
  })
}

watch(editableCategories, () => {
  initCopies()
}, { deep: true })

// ========== 笔记数据 ==========
const notes = ref([])

const init_notes = async () =>{
  try {
    const resp = await Api.note.listNotesApi()
    const list = resp?.data?.data ?? []
    notes.value = list.map(n => ({
      id: n.id,
      title: n.title,
      content: n.content,
      category_id: n.category_id,
      category_name: n.category_name,
      tags: n.tags ?? [],
      starred: !!n.starred,
      createdAt: n.created_at,
      updatedAt: n.updated_at
    }))
  } catch (e) {
    console.error('获取笔记列表失败:', e)
    const status = e?.response?.status
    const detail = e?.response?.data?.message || e?.response?.data?.detail
    alert(`获取笔记列表失败${status ? `（HTTP ${status}）` : ''}${detail ? `：${detail}` : ''}`)
  }
}

onMounted(() => {
  init_notes()
})

const editingNote = ref({
  id: null,
  title: '',
  content: '',
  category_name: '全部笔记',
  tags: []
})
const tagInput = ref('')
// ========== 状态管理 ==========
const activeCategory = ref('全部笔记')
const activeTag = ref('')
const searchKeyword = ref('')
const viewMode = ref('grid')
const showDrawer = ref(false)
const showCategoryModal = ref(false)
const showAIDrawer = ref(false)
const currentSelectedNote = ref(null)

const userInfo = reactive({
  username: userStore.userInfo.username,
  email: userStore.userInfo.email,
  avatar: userStore.userInfo.avatar
})

// 用户头像首字母
const userInitial = computed(() => {
  return userInfo.username.charAt(0).toUpperCase()
})

// 用户菜单显示状态
const showUserMenu = ref(false)
const userMenuRef = ref(null)

// 切换用户菜单
const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

// 关闭用户菜单
const closeUserMenu = () => {
  showUserMenu.value = false
}

// 跳转到个人中心（占位函数）
const goToProfile = () => {
  closeUserMenu()
  router.push('/user')
}

// 跳转到账号设置（占位函数）
const goToSettings = () => {
  closeUserMenu()
  console.log('跳转到账号设置')
  alert('跳转到账号设置（功能待实现）')
}

// 退出登录（占位函数）
const handleLogout = () => {
  closeUserMenu()
  console.log('退出登录')
  if (confirm('确定要退出登录吗？')) {
    alert('已退出登录')
    Api.user.logoutApi(userStore.refresh_token, userStore.access_token)
    userStore.logout()
    router.push('/login')
  }
}

// 点击外部关闭菜单
const handleClickOutside = (event) => {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target)) {
    closeUserMenu()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// 新分类表单
const newCategory = reactive({
  category_name: '',
  category_icon: '📄'
})

// ========== 计算属性 ==========
const starredNotesCount = computed(() => {
  return notes.value.filter(n => n.starred).length
})

const allTags = computed(() => {
  const tags = new Set()
  notes.value.forEach(note => {
    note.tags?.forEach(tag => tags.add(tag))
  })
  return Array.from(tags)
})

const popularTags = computed(() => {
  const tagCount = {}
  notes.value.forEach(note => {
    note.tags?.forEach(tag => {
      tagCount[tag] = (tagCount[tag] || 0) + 1
    })
  })
  return Object.entries(tagCount)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([tag]) => tag)
})

const filteredNotes = computed(() => {
  let result = notes.value
  
  if (activeCategory.value !== '全部笔记') {
    result = result.filter(n => n.category_name === activeCategory.value)
  }
  
  if (activeTag.value) {
    result = result.filter(n => n.tags?.includes(activeTag.value))
  }
  
  if (searchKeyword.value.trim()) {
    const keyword = searchKeyword.value.trim().toLowerCase()
    result = result.filter(n => 
      n.title.toLowerCase().includes(keyword) || 
      n.content.toLowerCase().includes(keyword)
    )
  }
  
  return result.sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt))
})

// ========== AI助手相关方法 ==========
// 打开 AI 助手
const openAIManage = () => {
  showAIDrawer.value = true
}

// 关闭 AI 助手
const closeAIDrawer = () => {
  showAIDrawer.value = false
}

// 处理 AI 操作
const handleAIAction = (action) => {
  console.log('AI 执行操作:', action)
  
  switch (action.type) {
    case 'addTags':
      // 添加标签到当前笔记
      if (editingNote.value && action.tags) {
        const existingTags = editingNote.value.tags || []
        const newTags = [...new Set([...existingTags, ...action.tags])]
        editingNote.value.tags = newTags
        tagInput.value = newTags.join(', ')
        // 保存笔记
        saveNote()
      }
      break
      
    case 'optimize':
      // 优化当前笔记内容
      if (editingNote.value && action.content) {
        editingNote.value.content = action.content
        // 保存笔记
        saveNote()
      }
      break
      
    default:
      break
  }
}

// 监听笔记选中，更新当前选中的笔记
watch(editingNote, (newNote) => {
  currentSelectedNote.value = newNote
}, { deep: true })

// ========== 分类相关方法 ==========
const getCategoryIcon = (category_name) => {
  const category = categories.value.find(c => c.category_name === category_name)
  return category ? iconOptions[category.category_icon-1] : '📄'
}

const getCategoryCount = (category_name) => {
  if (category_name === '全部笔记') return notes.value.length
  return notes.value.filter(n => n.category_name === category_name).length
}

const openCategoryManage = () => {
  showCategoryModal.value = true
}

const closeCategoryManage = () => {
  showCategoryModal.value = false
  newCategory.category_name = ''
  newCategory.category_icon = '📄'
}

const getCategoryList = async () => {
  return await Api.category.getCategoriesApi()
}

const init_Categories = async () => {
  try {
    const response = await getCategoryList()
    const categoryList = response?.data?.data;
    customCategories.value = categoryList.map(cat => ({
      id: cat.id,
      category_name: cat.category_name,
      category_icon: cat.category_id,
      isDefault: false
    }))
  } catch (error) {
    console.error('获取分类列表失败:', error)
    alert('获取分类列表失败，请稍后重试')
  }
}

init_Categories()

const addCategory = async () => {
  const category_name = newCategory.category_name.trim()
  if (!category_name) return
  
  const exists = categories.value.some(
    cat => cat.category_name.toLowerCase() === category_name.toLowerCase()
  )
  if (exists) {
    alert('分类名称已存在')
    return
  }

  const categoryData = {
    category_id: iconOptions.findIndex(icon => icon === newCategory.category_icon)+1,
    category_name: newCategory.category_name
  }

  const response = await Api.category.createCategoryApi(categoryData)
  if(response.success === false) {
    alert('分类添加失败，请稍后重试')
  } else {
    customCategories.value.push({
      id: response?.data?.data.id,
      category_name: categoryData.category_name,
      category_icon: categoryData.category_id,
      isDefault: false
    })
    alert('分类添加成功')
  }
  newCategory.category_name = ''
  newCategory.category_icon = '📄'
}

const updateCategory = async (categoryId, categoryData) => {
  console.log(categoryId)
  if (!categoryData.category_name) {
    alert('分类名称不能为空')
    return
  }
  
  const category = {
    category_id: categoryData.category_icon,
    category_name: categoryData.category_name.trim()
  }

  const exists = categories.value.some(
    cat => cat.category_name.toLowerCase() === categoryData.category_name.toLowerCase()
  )
  if (exists) {
    alert('分类名称已存在')
    return
  }
  const response = await Api.category.updateCategoryApi(categoryId.id, category)
  if(response.success === false) {
    alert('分类更新失败，请稍后重试')
    return
  }
  const index = customCategories.value.findIndex(c => c.id === categoryId.id)
  if (index !== -1) {
    customCategories.value[index].category_name = response?.data?.data.category_name
    customCategories.value[index].category_icon = response?.data?.data.category_id
  }
  alert('分类已更新')
}

const deleteCategory = async (category) => {
  const noteCount = getCategoryCount(category.category_name)
  if (noteCount > 0) {
    alert(`无法删除：该分类下还有 ${noteCount} 篇笔记，请先移动或删除这些笔记`)
    return
  }
  
  if (confirm(`确定要删除分类"${category.category_name}"吗？`)) {
    const response =await Api.category.deleteCategoryApi(category.id)
    if(response.success === false) {
      alert('分类删除失败，请稍后重试')
      return
    }
    const index = customCategories.value.findIndex(c => c.category_name === category.category_name)
    if (index !== -1) {
      customCategories.value.splice(index, 1)
      
      if (activeCategory.value === category.category_name) {
        activeCategory.value = '全部笔记'
      }
    }
  }
}

// ========== 笔记相关方法 ==========
const getPreviewContent = (content) => {
  if (!content) return '<span class="empty-content">暂无内容</span>'
  const plainText = content.replace(/<[^>]+>/g, '')
  return plainText.length > 120 ? plainText.slice(0, 120) + '...' : plainText
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  
  return date.toLocaleDateString('zh-CN', { month: 'numeric', day: 'numeric' })
}

const createNewNote = async () => {
  const defaultCategoryId = selectableCategories.value[0].id

  try {
    // 点击“新建笔记”即在后端创建一条草稿，拿到 note.id
    const resp = await Api.note.createNoteApi({
      category_id: defaultCategoryId,
      title: '',
      content: '',
      tags: [],
      starred: false
    })
    const created = resp?.data?.data

    editingNote.value = {
      id: created?.id ?? null,
      title: created?.title ?? '',
      content: created?.content ?? '',
      category_id: defaultCategoryId,
      tags: created?.tags ?? []
    }

    // 让列表也立刻出现这条新笔记（用后端 id）
    const now = new Date().toISOString()
    notes.value.unshift({
      id: created?.id ?? Date.now(),
      title: '',
      content: '',
      category_name: created?.category_name ?? (selectableCategories.value[0]?.category_name ?? ''),
      tags: [],
      starred: false,
      createdAt: created?.created_at ?? now,
      updatedAt: created?.updated_at ?? now
    })

    tagInput.value = ''
    showDrawer.value = true
  } catch (e) {
    console.error('新建笔记失败:', e)
    const status = e?.response?.status
    const detail = e?.response?.data?.message || e?.response?.data?.detail
    alert(`新建笔记失败${status ? `（HTTP ${status}）` : ''}${detail ? `：${detail}` : ''}`)
  }
}

const selectNote = (note) => {
  editingNote.value = {
    id: note.id ?? null,
    title: note.title ?? '',
    content: note.content ?? '',
    category_id: note.category_id ?? (categories.value.find(c => c.category_name === note.category_name)?.id ?? 2),
    tags: note.tags ?? []
  }
  tagInput.value = note.tags?.join(', ') || ''
  showDrawer.value = true
}

const closeDrawer = () => {
  showDrawer.value = false
  editingNote.value = {
    id: null,
    title: '',
    content: '',
    category_id: 2,
    tags: []
  }
  tagInput.value = ''
}

const saveNote = async () => {
  const now = new Date().toISOString()
  const tags = tagInput.value
    .split(/[，,]/)
    .map(t => t.trim())
    .filter(t => t)
  
  try {
    if (!editingNote.value.id) {
      // 理论上 createNewNote 已经会创建草稿；兜底再创建一次
      const resp = await Api.note.createNoteApi({
        category_id: editingNote.value.category_id || 2,
        title: editingNote.value.title ?? '',
        content: editingNote.value.content ?? '',
        tags,
        starred: false
      })
      editingNote.value.id = resp?.data?.data?.id ?? null
    }
    const response = await Api.note.updateNoteApi({
      id: editingNote.value.id,
      category_id: editingNote.value.category_id || 2,
      title: editingNote.value.title ?? '',
      content: editingNote.value.content ?? '',
      tags,
      starred: false
    })
    const Date = response?.data?.data
    // 同步本地列表展示
    const index = notes.value.findIndex(n => n.id === Date.id)
    if (index !== -1) {
      notes.value[index].title = Date.title
      notes.value[index].content = Date.content
      notes.value[index].category_id = Date.category_id
      notes.value[index].category_name = Date.category_name
      notes.value[index].tags = Date.tags
      notes.value[index].updatedAt = Date.updated_at
    } else {
      // 如果列表里没有（理论上不应该发生），就加进去
      notes.value.unshift({
        id: Date.id,
        title: Date.title,
        content: Date.content,
        category_name: Date.category_name,
        tags: Date.tags,
        starred: false,
        createdAt: Date.created_at,
        updatedAt: Date.updated_at
      })
    }

    closeDrawer()
  } catch (e) {
    console.error('保存笔记失败:', e)
    const status = e?.response?.status
    const detail = e?.response?.data?.message || e?.response?.data?.detail
    alert(`保存失败${status ? `（HTTP ${status}）` : ''}${detail ? `：${detail}` : ''}`)
  }
}

const toggleStar = (note) => {
  note.starred = !note.starred
  const response = Api.note.updateNoteStarredApi({ id: note.id })
  if(response.success === false) {
    alert('操作失败，请稍后重试')
    note.starred = !note.starred // 回退状态
  }
}

const deleteNote = async (note) => {
  if (!confirm(`确定要删除笔记"${note.title || '无标题'}"吗？`)) return

  // 没落库的临时笔记（防御性处理）直接本地删除
  if (!note?.id || typeof note.id !== 'number') {
    const index = notes.value.findIndex(n => n.id === note.id)
    if (index !== -1) notes.value.splice(index, 1)
    return
  }

  try {
    await Api.note.deleteNoteApi(note.id)
    const index = notes.value.findIndex(n => n.id === note.id)
    if (index !== -1) notes.value.splice(index, 1)

    if (editingNote.value?.id === note.id) {
      closeDrawer()
    }
  } catch (e) {
    console.error('删除笔记失败:', e)
    const status = e?.response?.status
    const detail = e?.response?.data?.message || e?.response?.data?.detail
    alert(`删除失败${status ? `（HTTP ${status}）` : ''}${detail ? `：${detail}` : ''}`)
  }
}

</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.note-app {
  display: flex;
  height: 100vh;
  background: #f5f7fa;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

/* ========== 侧边栏 ========== */
.sidebar {
  width: 280px;
  background: white;
  border-right: 1px solid #e8e8e8;
  display: flex;
  flex-direction: column;
  padding: 20px;
  overflow-y: auto;
}

.sidebar-header {
  margin-bottom: 20px;
}

.sidebar-header h2 {
  font-size: 22px;
  color: #1a1a1a;
  font-weight: 600;
}

.new-note-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
  margin-bottom: 24px;
}

.new-note-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

.new-note-btn span {
  font-size: 20px;
  font-weight: 300;
}

.sharenote-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
  margin-bottom: 24px;
}

.sharenote-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

.sharenote-btn span {
  font-size: 20px;
  font-weight: 300;
}

.ai-helper-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s;
  margin-bottom: 24px;
}

.ai-helper-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

.ai-helper-btn span {
  font-size: 20px;
  font-weight: 300;
}

.sidebar-section {
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.section-header h3 {
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #8c8c8c;
  margin-bottom: 0;
  font-weight: 600;
}

.manage-btn {
  width: 28px;
  height: 28px;
  border: none;
  background: #f0f0f0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.manage-btn:hover {
  background: #e0e0e0;
}

.sidebar-section h3 {
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #8c8c8c;
  margin-bottom: 12px;
  font-weight: 600;
}

.category-list {
  list-style: none;
}

.category-list li {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: #4a4a4a;
  margin-bottom: 4px;
}

.category-list li:hover {
  background: #f0f0f0;
}

.category-list li.active {
  background: linear-gradient(135deg, #f0e7ff 0%, #e8deff 100%);
  color: #667eea;
  font-weight: 500;
}

.category-icon {
  font-size: 18px;
  margin-right: 10px;
}

.category-name {
  flex: 1;
  font-size: 14px;
}

.category-count {
  background: #e8e8e8;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  color: #666;
}

.category-list li.active .category-count {
  background: #d4c5f9;
  color: #667eea;
}

.tags-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  padding: 6px 12px;
  background: #f0f0f0;
  border-radius: 20px;
  font-size: 13px;
  color: #4a4a4a;
  cursor: pointer;
  transition: all 0.2s;
}

.tag:hover {
  background: #e0e0e0;
}

.tag.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

/* ========== 主内容区 ========== */
.main-content {
  flex: 1;
  padding: 24px 32px;
  overflow-y: auto;
}

.content-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.header-toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: 16px;
}

.divider {
  width: 1px;
  height: 28px;
  background: #e0e0e0;
}

.search-box {
  flex: 1;
  max-width: 500px;
}

.search-input {
  width: 100%;
  padding: 14px 18px;
  border: 1.5px solid #e0e0e0;
  border-radius: 12px;
  font-size: 15px;
  transition: all 0.3s;
  background: white;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.view-options {
  display: flex;
  gap: 8px;
}

.view-options button {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1.5px solid #e0e0e0;
  border-radius: 10px;
  background: white;
  color: #8c8c8c;
  cursor: pointer;
  transition: all 0.2s;
}

.view-options button:hover {
  border-color: #667eea;
  color: #667eea;
}

.view-options button.active {
  background: #667eea;
  border-color: #667eea;
  color: white;
}

.user-menu {
  position: relative;
}

.user-avatar-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px 6px 8px;
  background: white;
  border: 1.5px solid #e0e0e0;
  border-radius: 40px;
  cursor: pointer;
  transition: all 0.2s;
}

.user-avatar-btn:hover {
  border-color: #667eea;
  background: #fafaff;
}

.user-avatar-btn.active {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  color: white;
  font-weight: 600;
  font-size: 14px;
}

.avatar-placeholder.large {
  font-size: 20px;
}

.username {
  font-size: 14px;
  font-weight: 500;
  color: #1a1a1a;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropdown-icon {
  color: #8c8c8c;
  transition: transform 0.2s;
}

.dropdown-icon.rotate {
  transform: rotate(180deg);
}

/* 下拉菜单 */
.user-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 240px;
  background: white;
  border-radius: 14px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  border: 1px solid #f0f0f0;
  overflow: hidden;
  z-index: 100;
}

.dropdown-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
}

.dropdown-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.dropdown-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.dropdown-user-info {
  flex: 1;
  min-width: 0;
}

.dropdown-username {
  font-size: 15px;
  font-weight: 600;
  color: #1a1a1a;
  margin-bottom: 4px;
}

.dropdown-email {
  font-size: 12px;
  color: #8c8c8c;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropdown-divider {
  height: 1px;
  background: #f0f0f0;
  margin: 4px 0;
}

.dropdown-menu-items {
  padding: 8px;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 10px 12px;
  border: none;
  background: transparent;
  border-radius: 8px;
  font-size: 14px;
  color: #4a4a4a;
  cursor: pointer;
  transition: all 0.15s;
  text-align: left;
}

.dropdown-item:hover {
  background: #f5f5f5;
}

.dropdown-item.danger {
  color: #e53e3e;
}

.dropdown-item.danger:hover {
  background: #fee2e2;
}

/* 下拉菜单动画 */
.dropdown-fade-enter-active,
.dropdown-fade-leave-active {
  transition: all 0.2s;
}

.dropdown-fade-enter-from,
.dropdown-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* 统计卡片 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 28px;
}

.stat-card {
  background: white;
  border-radius: 14px;
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 14px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 1px solid #f0f0f0;
}

.stat-icon {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #f5f0ff 0%, #ede4ff 100%);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 26px;
  font-weight: 700;
  color: #1a1a1a;
  line-height: 1.2;
}

.stat-label {
  font-size: 13px;
  color: #8c8c8c;
}

/* 笔记容器 */
.notes-container {
  min-height: 400px;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: #b0b0b0;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.notes-wrapper {
  display: grid;
  gap: 18px;
}

.grid-view {
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
}

.list-view {
  grid-template-columns: 1fr;
}

.note-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 1px solid #f0f0f0;
  cursor: pointer;
  transition: all 0.25s;
}

.note-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
  border-color: #e0d4ff;
}

.note-card.starred {
  border-left: 4px solid #f5b342;
}

.note-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 12px;
}

.note-title {
  font-size: 17px;
  font-weight: 600;
  color: #1a1a1a;
  line-height: 1.4;
  flex: 1;
  margin-right: 8px;
}

.note-actions {
  display: flex;
  gap: 6px;
  opacity: 0;
  transition: opacity 0.2s;
}

.note-card:hover .note-actions {
  opacity: 1;
}

.star-btn,
.delete-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: #f5f5f5;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.star-btn:hover {
  background: #fef3c7;
}

.star-btn.active {
  background: #fef3c7;
  color: #f5b342;
}

.delete-btn:hover {
  background: #fee2e2;
  color: #ef4444;
}

.note-preview {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 16px;
  max-height: 80px;
  overflow: hidden;
}

.note-footer {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px 12px;
  font-size: 12px;
  color: #8c8c8c;
  border-top: 1px solid #f0f0f0;
  padding-top: 14px;
}

.note-category {
  display: flex;
  align-items: center;
  gap: 4px;
  background: #f5f5f5;
  padding: 4px 10px;
  border-radius: 20px;
}

.note-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  flex: 1;
}

.note-tag {
  background: #f0f0f0;
  padding: 4px 10px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.note-tag:hover {
  background: #667eea;
  color: white;
}

.more-tag {
  background: #f0f0f0;
  padding: 4px 10px;
  border-radius: 20px;
}

.note-date {
  margin-left: auto;
}

/* ========== 编辑抽屉 ========== */
.drawer-overlay {
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

.drawer-overlay.show {
  opacity: 1;
  visibility: visible;
}

.note-drawer {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  max-width: 600px;
  background: white;
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.1);
  transform: translateX(100%);
  transition: transform 0.3s ease;
  z-index: 1001;
  display: flex;
  flex-direction: column;
}

.note-drawer.show {
  transform: translateX(0);
}

.drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 28px;
  border-bottom: 1px solid #e8e8e8;
}

.drawer-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: #1a1a1a;
}

.close-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: #f0f0f0;
  border-radius: 10px;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #e0e0e0;
}

.drawer-body {
  flex: 1;
  padding: 28px;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 22px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #4a4a4a;
}

.title-input {
  width: 100%;
  padding: 14px 16px;
  border: 1.5px solid #e0e0e0;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 500;
  transition: all 0.3s;
}

.title-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.category-select {
  width: 100%;
  padding: 12px 16px;
  border: 1.5px solid #e0e0e0;
  border-radius: 12px;
  font-size: 15px;
  background: white;
  cursor: pointer;
}

.content-textarea {
  width: 100%;
  padding: 16px;
  border: 1.5px solid #e0e0e0;
  border-radius: 12px;
  font-size: 15px;
  line-height: 1.6;
  resize: vertical;
  font-family: inherit;
}

.content-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.tag-input {
  width: 100%;
  padding: 14px 16px;
  border: 1.5px solid #e0e0e0;
  border-radius: 12px;
  font-size: 15px;
}

.drawer-footer {
  display: flex;
  gap: 12px;
  padding: 20px 28px;
  border-top: 1px solid #e8e8e8;
}

.cancel-btn,
.save-btn {
  flex: 1;
  padding: 14px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.cancel-btn {
  background: #f5f5f5;
  border: none;
  color: #666;
}

.cancel-btn:hover {
  background: #e8e8e8;
}

.save-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
}

.save-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 12px rgba(102, 126, 234, 0.25);
}

/* ========== 分类管理弹窗 ========== */
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
  z-index: 2000;
}

.modal-overlay.show {
  opacity: 1;
  visibility: visible;
}

.category-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(0.9);
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s;
  z-index: 2001;
  display: flex;
  flex-direction: column;
}

.category-modal.show {
  opacity: 1;
  visibility: visible;
  transform: translate(-50%, -50%) scale(1);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #e8e8e8;
}

.modal-header h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
}

.add-category-section {
  margin-bottom: 28px;
}

.add-category-section h4,
.existing-categories h4 {
  font-size: 15px;
  font-weight: 600;
  color: #4a4a4a;
  margin-bottom: 16px;
}

.add-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.icon-selector label,
.name-input label {
  display: block;
  font-size: 13px;
  color: #8c8c8c;
  margin-bottom: 8px;
}

.icon-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  max-height: 150px;
  overflow-y: auto;
  padding: 4px;
}

.icon-grid span {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 10px;
  font-size: 22px;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s;
}

.icon-grid span:hover {
  background: #e8deff;
  transform: scale(1.05);
}

.icon-grid span.active {
  border-color: #667eea;
  background: #f0e7ff;
}

.name-input input {
  width: 100%;
  padding: 12px 14px;
  border: 1.5px solid #e0e0e0;
  border-radius: 10px;
  font-size: 15px;
  transition: all 0.3s;
}

.name-input input:focus {
  outline: none;
  border-color: #667eea;
}

.add-btn {
  padding: 12px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.add-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 12px rgba(102, 126, 234, 0.25);
}

.add-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.existing-categories {
  border-top: 1px solid #e8e8e8;
  padding-top: 20px;
}

.empty-tip {
  color: #b0b0b0;
  text-align: center;
  padding: 20px;
  font-size: 14px;
}

.editable-category-list {
  list-style: none;
  max-height: 250px;
  overflow-y: auto;
}

.editable-category-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 10px;
  background: #fafafa;
  margin-bottom: 8px;
}

.icon-select {
  width: 55px;
  padding: 6px;
  border: 1.5px solid #e0e0e0;
  border-radius: 8px;
  font-size: 18px;
  text-align: center;
  background: white;
  cursor: pointer;
}

.category-name-input {
  flex: 1;
  padding: 8px 12px;
  border: 1.5px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  background: white;
}

.category-name-input:focus {
  outline: none;
  border-color: #667eea;
}

.category-actions {
  display: flex;
  gap: 6px;
}

.save-btn-small,
.delete-btn-small {
  width: 34px;
  height: 34px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.save-btn-small {
  background: #e8f5e9;
  color: #4caf50;
}

.save-btn-small:hover {
  background: #c8e6c9;
}

.delete-btn-small {
  background: #ffebee;
  color: #f44336;
}

.delete-btn-small:hover:not(:disabled) {
  background: #ffcdd2;
}

.delete-btn-small:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.help-text {
  margin-top: 16px;
  font-size: 12px;
  color: #8c8c8c;
  text-align: center;
}

/* ========== 响应式 ========== */
@media (max-width: 900px) {
  .stats-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .sidebar {
    display: none;
  }
  
  .main-content {
    padding: 16px;
  }
  
  .note-drawer {
    max-width: 100%;
  }
  
  .category-modal {
    width: 95%;
  }
}
</style>