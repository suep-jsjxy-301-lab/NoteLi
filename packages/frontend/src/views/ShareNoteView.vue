<template>
  <div class="shared-docs-app">
    <!-- 侧边栏（共享笔记专用，简化版） -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2>📡 共享笔记</h2>
      </div>
      
      <!-- 操作按钮组 -->
      <div class="action-buttons">
        <button class="new-shared-btn" @click="createNewSharedDoc">
          <span>+</span> 新建共享笔记
        </button>
        <button class="join-shared-btn" @click="openJoinDialog">
          <span>🔗</span> 加入共享笔记
        </button>
        <button class="back-home-btn" @click="goBackToNote">
          <span>🏠</span> 返回主页面
        </button>
      </div>
    </aside>
    
    <!-- 主内容区：笔记编辑器/查看器 -->
    <main class="main-content">
      <header class="content-header">
        <div class="doc-info" v-if="currentDoc">
          <h2 class="doc-title">
            <input 
              v-if="isEditingTitle && canEdit"
              v-model="currentDoc.title"
              @blur="saveDocTitle"
              @keyup.enter="saveDocTitle"
              class="title-edit-input"
              autofocus
            />
            <span v-else class="title-display" @click="startEditTitleIfCan">{{ currentDoc.title || '无标题' }}</span>
            <button 
              v-if="canEdit && !isEditingTitle"
              class="edit-title-btn"
              @click="startEditTitleIfCan"
              title="编辑标题"
            >
              ✏️
            </button>
          </h2>
          <div class="doc-meta">
            <span class="doc-owner">创建者：{{ currentDoc.owner_name }}</span>
            <span class="doc-role-badge" :class="{ owner: currentDoc.role === 'owner', collaborator: currentDoc.role === 'collaborator' }">
              {{ currentDoc.role === 'owner' ? '创建者' : '协作者' }}
            </span>
            <span class="doc-updated">更新于 {{ formatDate(currentDoc.updated_at) }}</span>
          </div>
        </div>
        
        <div class="header-toolbar" v-if="currentDoc && canEdit">
          <button class="save-btn-header" @click="saveContent" :disabled="saving">
            {{ saving ? '保存中...' : '保存' }}
          </button>
          <button class="share-btn-header" @click="openShareDialog" title="分享笔记">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
              <path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.05 4.11c-.05.23-.09.46-.09.7 0 1.66 1.34 3 3 3s3-1.34 3-3-1.34-3-3-3z"/>
            </svg>
            分享
          </button>
        </div>
        
        <div class="empty-header" v-else-if="!currentDoc">
          <p>👈 选择或创建一个共享笔记开始协作</p>
        </div>
      </header>
      
      <!-- 笔记内容编辑器（富文本简化版） -->
      <div class="editor-container" v-if="currentDoc">
        <div class="editor-toolbar" v-if="canEdit">
          <button type="button" @click="execCmd('bold')" title="加粗"><strong>B</strong></button>
          <button type="button" @click="execCmd('italic')" title="斜体"><em>I</em></button>
          <button type="button" @click="execCmd('underline')" title="下划线"><u>U</u></button>
          <span class="toolbar-sep"></span>
          <button type="button" @click="execCmd('insertUnorderedList')" title="无序列表">• 列表</button>
          <button type="button" @click="execCmd('insertOrderedList')" title="有序列表">1. 列表</button>
          <span class="toolbar-sep"></span>
          <button type="button" @click="execCmd('justifyLeft')" title="左对齐">左</button>
          <button type="button" @click="execCmd('justifyCenter')" title="居中">中</button>
          <button type="button" @click="execCmd('justifyRight')" title="右对齐">右</button>
          <span class="toolbar-sep"></span>
          <button type="button" @click="insertLink" title="插入链接">🔗 链接</button>
          <button type="button" @click="insertImage" title="插入图片">🖼️ 图片</button>
        </div>
        <div 
          ref="editorRef"
          class="document-editor"
          :contenteditable="canEdit"
          @input="onContentInput"
          @keydown="onEditorKeydown"
          v-html="currentDoc.content"
        ></div>
        <div v-if="!canEdit" class="readonly-overlay">
          <span>📖 只读模式 - 您只有查看权限</span>
        </div>
      </div>
      
      <div class="empty-editor" v-else>
        <div class="empty-icon">📭</div>
        <p>点击左侧"新建共享笔记"或加入现有笔记开始协作</p>
      </div>
    </main>
    
    <!-- 加入笔记弹窗 -->
    <div class="modal-overlay" :class="{ show: showJoinModal }" @click="closeJoinDialog"></div>
    <div class="join-modal" :class="{ show: showJoinModal }">
      <div class="modal-header">
        <h3>🔗 加入共享笔记</h3>
        <button class="close-btn" @click="closeJoinDialog">✕</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label>笔记分享码 / 链接ID</label>
          <input 
            type="text" 
            v-model="joinDocId"
            placeholder="请输入笔记ID或分享码"
            class="join-input"
            @keyup.enter="joinSharedDoc"
          />
        </div>
        <p class="help-text">💡 提示：从笔记创建者处获取分享码或笔记ID</p>
      </div>
      <div class="modal-footer">
        <button class="cancel-btn" @click="closeJoinDialog">取消</button>
        <button class="join-btn" @click="joinSharedDoc">加入笔记</button>
      </div>
    </div>
    
    <!-- 分享笔记弹窗 -->
    <div class="modal-overlay" :class="{ show: showShareModal }" @click="closeShareDialog"></div>
    <div class="share-modal" :class="{ show: showShareModal }">
      <div class="modal-header">
        <h3>📤 分享笔记</h3>
        <button class="close-btn" @click="closeShareDialog">✕</button>
      </div>
      <div class="modal-body" v-if="currentDoc">
        <div class="form-group">
          <label>笔记ID（分享码）</label>
          <div class="share-code">
            <input type="text" readonly :value="currentDoc.id || ''" class="share-code-input" />
            <button class="copy-btn" @click="copyShareCode">复制</button>
          </div>
        </div>
        <div class="form-group">
          <label>邀请链接</label>
          <div class="share-link">
            <input type="text" readonly :value="shareLink" class="share-link-input" />
            <button class="copy-btn" @click="copyShareLink">复制链接</button>
          </div>
        </div>
        <div class="share-settings">
          <label class="checkbox-label">
            <input type="checkbox" v-model="currentDoc.is_public" @change="togglePublic" />
            <span>允许任何人通过链接加入（设为公开）</span>
          </label>
        </div>
        <p class="help-text">💡 协作者可通过笔记ID或链接加入，创建者拥有编辑和分享权限</p>
      </div>
      <div class="modal-body" v-else>
        <p class="help-text">请先选择一个笔记</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import Api from '@/api/api'

const router = useRouter()
const userStore = useUserStore()

// ========== 数据定义 ==========
const mySharedDocs = ref([])        // 我参与的笔记列表
const activeDocId = ref(null)       // 当前选中的笔记ID
const currentDoc = ref(null)        // 当前打开的笔记详情
const canEdit = ref(false)          // 当前用户是否有编辑权限

// UI 状态
const showJoinModal = ref(false)
const showShareModal = ref(false)
const joinDocId = ref('')
const saving = ref(false)
const isEditingTitle = ref(false)

// 编辑器 DOM 引用
const editorRef = ref(null)

// 当前用户信息
const userInfo = ref({
  id: userStore.userInfo?.id || null,
  username: userStore.userInfo?.username || '用户',
})

// ========== 路由跳转 ==========
const goBackToNote = () => {
  router.push('/notes')
}

// ========== 共享笔记 API 调用（模拟/对接） ==========
// 获取我参与的共享笔记列表
const fetchMySharedDocs = async () => {
  try {
    const resp = await Api.sharedDocs.getMySharedDocsApi?.() || await fakeGetMyDocs()
    mySharedDocs.value = resp?.data?.data || []
  } catch (e) {
    console.error('获取共享笔记列表失败:', e)
    mySharedDocs.value = []
  }
}

// 新建共享笔记
const createNewSharedDoc = async () => {
  try {
    const resp = await Api.sharedDocs.createSharedDocApi?.({
      title: '无标题笔记',
      content: '<p>欢迎开始协作编辑～</p>'
    }) || await fakeCreateDoc()
    const newDoc = resp?.data?.data
    if (newDoc) {
      mySharedDocs.value.unshift(newDoc)
      await selectSharedDoc(newDoc)
    }
  } catch (e) {
    console.error('新建共享笔记失败:', e)
    alert('创建失败，请稍后重试')
  }
}

// 通过ID加入笔记
const joinSharedDoc = async () => {
  const docId = joinDocId.value.trim()
  if (!docId) {
    alert('请输入笔记ID')
    return
  }
  try {
    const resp = await Api.sharedDocs.joinSharedDocApi?.({ doc_id: docId }) || await fakeJoinDoc(docId)
    if (resp?.success === false) {
      alert(resp?.message || '加入失败，请检查笔记ID')
      return
    }
    const doc = resp?.data?.data
    if (doc && !mySharedDocs.value.find(d => d.id === doc.id)) {
      mySharedDocs.value.unshift(doc)
    }
    await selectSharedDoc(doc)
    closeJoinDialog()
    alert('加入成功！')
  } catch (e) {
    console.error('加入共享笔记失败:', e)
    alert('加入失败，请检查笔记ID或网络')
  }
}

// 打开笔记详情（含权限）
const selectSharedDoc = async (doc) => {
  if (!doc?.id) return
  activeDocId.value = doc.id
  try {
    const resp = await Api.sharedDocs.getSharedDocApi?.({ doc_id: doc.id }) || await fakeGetDocDetail(doc.id)
    const docDetail = resp?.data?.data
    if (!docDetail) return
    
    currentDoc.value = {
      ...docDetail,
      role: docDetail.role || (docDetail.owner_id === userInfo.value.id ? 'owner' : 'collaborator'),
      is_public: docDetail.is_public ?? false  // 确保 is_public 有默认值
    }
    canEdit.value = currentDoc.value.role === 'owner' || currentDoc.value.can_edit === true
    
    // 同步更新列表中的标题等信息
    const idx = mySharedDocs.value.findIndex(d => d.id === doc.id)
    if (idx !== -1) {
      mySharedDocs.value[idx].title = currentDoc.value.title
    }
    
    // 渲染内容到编辑器
    await nextTick()
    if (editorRef.value) {
      editorRef.value.innerHTML = currentDoc.value.content || '<p></p>'
    }
  } catch (e) {
    console.error('获取笔记详情失败:', e)
    alert('打开笔记失败')
  }
}

// 保存笔记内容
const saveContent = async () => {
  if (!currentDoc.value || !canEdit.value) return
  saving.value = true
  try {
    const content = editorRef.value?.innerHTML || ''
    const resp = await Api.sharedDocs.updateSharedDocApi?.({
      doc_id: currentDoc.value.id,
      content: content,
      title: currentDoc.value.title
    }) || await fakeUpdateDoc(currentDoc.value.id, { content, title: currentDoc.value.title })
    
    if (resp?.success !== false) {
      currentDoc.value.content = content
      currentDoc.value.updated_at = new Date().toISOString()
      const idx = mySharedDocs.value.findIndex(d => d.id === currentDoc.value.id)
      if (idx !== -1) mySharedDocs.value[idx].updated_at = currentDoc.value.updated_at
    } else {
      alert('保存失败：' + (resp?.message || '未知错误'))
    }
  } catch (e) {
    console.error('保存失败:', e)
    alert('保存失败，请重试')
  } finally {
    saving.value = false
  }
}

// 保存标题
const saveDocTitle = async () => {
  if (!currentDoc.value || !canEdit.value) {
    isEditingTitle.value = false
    return
  }
  isEditingTitle.value = false
  try {
    await Api.sharedDocs.updateSharedDocApi?.({
      doc_id: currentDoc.value.id,
      title: currentDoc.value.title
    }) || await fakeUpdateDoc(currentDoc.value.id, { title: currentDoc.value.title })
    const idx = mySharedDocs.value.findIndex(d => d.id === currentDoc.value.id)
    if (idx !== -1) mySharedDocs.value[idx].title = currentDoc.value.title
  } catch (e) {
    console.error('更新标题失败:', e)
  }
}

// 切换公开状态
const togglePublic = async () => {
  if (!currentDoc.value || currentDoc.value.role !== 'owner') return
  const originalValue = currentDoc.value.is_public
  try {
    await Api.sharedDocs.setPublicApi?.({
      doc_id: currentDoc.value.id,
      is_public: currentDoc.value.is_public
    })
  } catch (e) {
    console.error('设置公开失败:', e)
    currentDoc.value.is_public = originalValue
  }
}

// ========== 编辑器操作方法 ==========
const execCmd = (command, value = null) => {
  document.execCommand(command, false, value)
  editorRef.value?.focus()
  onContentInput()
}

const insertLink = () => {
  const url = prompt('请输入链接地址:', 'https://')
  if (url) execCmd('createLink', url)
}

const insertImage = () => {
  const url = prompt('请输入图片地址:', 'https://')
  if (url) execCmd('insertImage', url)
}

let autoSaveTimer = null
const onContentInput = () => {
  if (!canEdit.value) return
  if (autoSaveTimer) clearTimeout(autoSaveTimer)
  autoSaveTimer = setTimeout(() => {
    saveContent()
  }, 1000)
}

const onEditorKeydown = () => {
  // 预留
}

const startEditTitleIfCan = () => {
  if (canEdit.value && !isEditingTitle.value) {
    isEditingTitle.value = true
  }
}

// ========== 弹窗控制 ==========
const openJoinDialog = () => {
  joinDocId.value = ''
  showJoinModal.value = true
}
const closeJoinDialog = () => {
  showJoinModal.value = false
}
const openShareDialog = () => {
  if (!currentDoc.value) return
  showShareModal.value = true
}
const closeShareDialog = () => {
  showShareModal.value = false
}

// 分享链接
const shareLink = computed(() => {
  if (!currentDoc.value) return ''
  return `${window.location.origin}/shared/${currentDoc.value.id}`
})

const copyShareCode = () => {
  if (!currentDoc.value) return
  navigator.clipboard.writeText(currentDoc.value.id)
  alert('笔记ID已复制')
}

const copyShareLink = () => {
  if (!shareLink.value) return
  navigator.clipboard.writeText(shareLink.value)
  alert('链接已复制')
}

// 加入公开笔记
const joinPublicDoc = async (doc) => {
  if (!doc?.id) return
  joinDocId.value = doc.id
  await joinSharedDoc()
}

// ========== 辅助函数 ==========
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

// ========== 模拟数据（可删除，对接真实API后替换） ==========
const fakeGetMyDocs = async () => {
  return { data: { data: [] } }
}
const fakeGetPublicDocs = async () => {
  return { data: { data: [] } }
}
const fakeCreateDoc = async () => {
  const newId = Date.now()
  return {
    data: {
      data: {
        id: newId,
        title: '无标题笔记',
        content: '<p>欢迎开始协作编辑～</p>',
        owner_id: userInfo.value.id,
        owner_name: userInfo.value.username,
        role: 'owner',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        is_public: false
      }
    }
  }
}
const fakeJoinDoc = async (docId) => {
  return {
    data: {
      data: {
        id: docId,
        title: '示例共享笔记',
        content: '<p>这是协作笔记内容</p>',
        owner_id: 1,
        owner_name: '笔记主人',
        role: 'collaborator',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        is_public: false
      }
    }
  }
}
const fakeGetDocDetail = async (docId) => {
  // 尝试从已有列表中查找
  const existing = mySharedDocs.value.find(d => d.id === docId)
  if (existing) {
    return {
      data: {
        data: {
          ...existing,
          is_public: existing.is_public ?? false
        }
      }
    }
  }
  return {
    data: {
      data: {
        id: docId,
        title: '示例笔记',
        content: '<p>笔记正文内容</p>',
        owner_id: 1,
        owner_name: '创建者',
        role: userInfo.value.id === 1 ? 'owner' : 'collaborator',
        is_public: false,
        updated_at: new Date().toISOString()
      }
    }
  }
}
const fakeUpdateDoc = async (docId, data) => {
  return { success: true }
}

// ========== 初始化 ==========
onMounted(() => {
  fetchMySharedDocs()
})

onUnmounted(() => {
  if (autoSaveTimer) clearTimeout(autoSaveTimer)
})
</script>

<style scoped>
/* 样式保持不变，与之前相同 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.shared-docs-app {
  display: flex;
  height: 100vh;
  background: #f5f7fa;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.sidebar {
  width: 280px;
  background: white;
  border-right: 1px solid #e8e8e8;
  display: flex;
  flex-direction: column;
  padding: 20px;
  overflow-y: auto;
}

.sidebar-header h2 {
  font-size: 22px;
  color: #1a1a1a;
  font-weight: 600;
  margin-bottom: 20px;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 28px;
}

.new-shared-btn,
.join-shared-btn,
.back-home-btn {
  width: 100%;
  padding: 12px 14px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
  border: none;
}

.new-shared-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}
.new-shared-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(102, 126, 234, 0.3);
}

.join-shared-btn {
  background: #f0f0f0;
  color: #4a4a4a;
}
.join-shared-btn:hover {
  background: #e8deff;
  color: #667eea;
}

.back-home-btn {
  background: white;
  border: 1px solid #e0e0e0;
  color: #666;
}
.back-home-btn:hover {
  background: #f5f5f5;
  border-color: #ccc;
}

.sidebar-section {
  margin-bottom: 28px;
}
.section-header h3 {
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #8c8c8c;
  margin-bottom: 12px;
  font-weight: 600;
}
.shared-list {
  list-style: none;
}
.shared-list li {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: #4a4a4a;
  margin-bottom: 4px;
  gap: 8px;
}
.shared-list li:hover {
  background: #f0f0f0;
}
.shared-list li.active {
  background: linear-gradient(135deg, #f0e7ff 0%, #e8deff 100%);
  color: #667eea;
  font-weight: 500;
}
.doc-icon {
  font-size: 18px;
}
.doc-name {
  flex: 1;
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.doc-role, .doc-author {
  font-size: 11px;
  background: #e8e8e8;
  padding: 2px 8px;
  border-radius: 12px;
  color: #666;
}
.empty-tip {
  color: #b0b0b0;
  text-align: center;
  padding: 16px;
  font-size: 13px;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fafbfc;
  overflow: hidden;
}

.content-header {
  padding: 20px 28px;
  background: white;
  border-bottom: 1px solid #e8e8e8;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

.doc-info {
  flex: 1;
}
.doc-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}
.title-display {
  font-size: 22px;
  font-weight: 600;
  color: #1a1a1a;
  cursor: pointer;
  border-bottom: 1px dashed transparent;
}
.title-display:hover {
  border-bottom-color: #667eea;
}
.title-edit-input {
  font-size: 22px;
  font-weight: 600;
  padding: 4px 8px;
  border: 1.5px solid #667eea;
  border-radius: 8px;
  width: 300px;
  background: white;
}
.edit-title-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  opacity: 0.6;
}
.edit-title-btn:hover {
  opacity: 1;
}
.doc-meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: #8c8c8c;
}
.doc-role-badge {
  background: #e8e8e8;
  padding: 2px 10px;
  border-radius: 20px;
}
.doc-role-badge.owner {
  background: #e8f5e9;
  color: #2e7d32;
}
.doc-role-badge.collaborator {
  background: #e3f2fd;
  color: #1565c0;
}

.header-toolbar {
  display: flex;
  gap: 12px;
}
.save-btn-header, .share-btn-header {
  padding: 8px 20px;
  border-radius: 24px;
  border: none;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}
.save-btn-header {
  background: #667eea;
  color: white;
}
.save-btn-header:hover:not(:disabled) {
  background: #5a67d8;
}
.save-btn-header:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.share-btn-header {
  background: #f0f0f0;
  color: #4a4a4a;
  display: flex;
  align-items: center;
  gap: 6px;
}
.share-btn-header:hover {
  background: #e8deff;
  color: #667eea;
}

.empty-header {
  padding: 8px 0;
  color: #b0b0b0;
}

.editor-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  margin: 20px 28px;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  overflow: hidden;
  position: relative;
}
.editor-toolbar {
  padding: 12px 16px;
  background: #fafafa;
  border-bottom: 1px solid #e8e8e8;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.editor-toolbar button {
  background: white;
  border: 1px solid #e0e0e0;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
}
.editor-toolbar button:hover {
  background: #f0f0f0;
  border-color: #667eea;
}
.toolbar-sep {
  width: 1px;
  background: #e0e0e0;
  margin: 0 4px;
}
.document-editor {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  outline: none;
  line-height: 1.6;
  font-size: 15px;
  min-height: 300px;
}
.document-editor:focus {
  background: #fff;
}
.readonly-overlay {
  position: absolute;
  bottom: 16px;
  right: 20px;
  background: rgba(0,0,0,0.6);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  pointer-events: none;
}
.empty-editor {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #b0b0b0;
}
.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s;
  z-index: 1000;
}
.modal-overlay.show {
  opacity: 1;
  visibility: visible;
}
.join-modal, .share-modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(0.9);
  width: 90%;
  max-width: 460px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s;
  z-index: 1001;
}
.join-modal.show, .share-modal.show {
  opacity: 1;
  visibility: visible;
  transform: translate(-50%, -50%) scale(1);
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e8e8e8;
}
.modal-header h3 {
  font-size: 18px;
  font-weight: 600;
}
.close-btn {
  width: 32px;
  height: 32px;
  background: #f0f0f0;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
.modal-body {
  padding: 24px;
}
.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #e8e8e8;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}
.join-input, .share-code-input, .share-link-input {
  width: 100%;
  padding: 12px 14px;
  border: 1.5px solid #e0e0e0;
  border-radius: 10px;
  font-size: 14px;
}
.share-code, .share-link {
  display: flex;
  gap: 8px;
}
.copy-btn {
  padding: 0 16px;
  background: #f0f0f0;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}
.copy-btn:hover {
  background: #e0e0e0;
}
.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}
.help-text {
  margin-top: 12px;
  font-size: 12px;
  color: #8c8c8c;
}
.join-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 10px;
  cursor: pointer;
}
.cancel-btn {
  background: #f0f0f0;
  border: none;
  padding: 10px 20px;
  border-radius: 10px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .sidebar {
    display: none;
  }
  .main-content {
    padding: 0;
  }
  .editor-container {
    margin: 12px;
  }
  .doc-title .title-edit-input {
    width: 180px;
    font-size: 18px;
  }
}
</style>