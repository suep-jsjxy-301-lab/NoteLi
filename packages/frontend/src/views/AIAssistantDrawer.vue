<template>
  <div class="ai-drawer-overlay" :class="{ show: visible }" @click="close"></div>
  <aside class="ai-drawer" :class="{ show: visible }">
    <div class="drawer-header">
      <div class="header-left">
        <span class="ai-icon">🤖</span>
        <h3>AI 助手</h3>
      </div>
      <button class="close-btn" @click="close">✕</button>
    </div>
    
    <div class="drawer-body">
      <!-- 对话历史区域 -->
      <div class="chat-messages" ref="messagesContainer">
        <div 
          v-for="(message, index) in messages" 
          :key="index"
          :class="['message', message.role]"
        >
          <div class="message-avatar">
            {{ message.role === 'user' ? '👤' : '🤖' }}
          </div>
          <div class="message-content">
            <div class="message-text">{{ message.content }}</div>
            <div class="message-time">{{ message.time }}</div>
          </div>
        </div>
        
        <!-- 加载状态 -->
        <div v-if="isLoading" class="message assistant">
          <div class="message-avatar">🤖</div>
          <div class="message-content">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="drawer-footer">
      <!-- 快捷操作 -->
      <div class="quick-actions">
        <button 
          v-for="action in quickActions" 
          :key="action.text"
          class="quick-action-btn"
          @click="sendQuickAction(action.text)"
        >
          {{ action.icon }} {{ action.text }}
        </button>
      </div>
      
      <!-- 输入区域 -->
      <div class="input-area">
        <textarea 
          v-model="inputText"
          placeholder="输入你的问题，AI 会帮你处理笔记..."
          @keydown.enter.prevent="sendMessage"
          class="ai-input"
          rows="2"
        ></textarea>
        <button 
          class="send-btn" 
          @click="sendMessage"
          :disabled="!inputText.trim() || isLoading"
        >
          <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
          </svg>
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import Api from '@/api/api'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  currentNote: {
    type: Object,
    default: null
  },
  allNotes: {
    type: Array,
    default: () => []
  },
  categories: {
    type: Array,
    default: () => []
  },
  init_notes: {
    type: Function,
    required: true
  },
  init_Categories: {
    type: Function,
    required: true
  }
})

const emit = defineEmits(['close', 'action'])

const messages = ref([
  {
    role: 'assistant',
    content: '你好！我是你的 AI 笔记助手 🎯\n\n我可以帮你：\n• 总结和整理笔记内容\n• 生成笔记标题\n• 提取笔记标签\n• 优化文字表达\n• 回答笔记相关问题\n\n有什么我可以帮你的吗？',
    time: getCurrentTime()
  }
])
const inputText = ref('')
const isLoading = ref(false)
const messagesContainer = ref(null)

// 快捷操作
const quickActions = [
  { icon: '📝', text: '总结当前笔记' },
  { icon: '🏷️', text: '生成标签' },
  { icon: '✏️', text: '优化表达' },
  { icon: '📊', text: '笔记统计' }
]

// 获取当前时间
function getCurrentTime() {
  const now = new Date()
  return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`
}

// 滚动到底部
async function scrollToBottom() {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 发送快捷操作
async function sendQuickAction(actionText) {
  inputText.value = actionText
  await sendMessage()
}

// 发送消息
async function sendMessage() {
  if (!inputText.value.trim() || isLoading.value) return
  
  const userMessage = inputText.value.trim()
  inputText.value = ''
  
  // 添加用户消息
  messages.value.push({
    role: 'user',
    content: userMessage,
    time: getCurrentTime()
  })
  await scrollToBottom()
  
  // 开始加载
  isLoading.value = true
  
  try {
    // 调用 AI 接口
    const response = await processWithAI(userMessage)

    // 添加 AI 回复
    messages.value.push({
      role: 'assistant',
      content: response.message,
      time: getCurrentTime()
    })
    
    // 如果有操作指令，触发父组件执行
    if (response.actions && response.actions.length > 0) {
      response.actions.forEach(action => {
        emit('action', action)
      })
    }
    
    await scrollToBottom()
  } catch (error) {
    console.error('AI 处理失败:', error)
    messages.value.push({
      role: 'assistant',
      content: '抱歉，我遇到了一些问题，请稍后再试。',
      time: getCurrentTime()
    })
    await scrollToBottom()
  } finally {
    isLoading.value = false
    props.init_notes()
    props.init_Categories()
  }
}

// AI 处理函数
async function processWithAI(userMessage) {
  // 这里调用你的后端 AI 接口
  
  const lowerMessage = userMessage.toLowerCase()
  
  const response = await Api.agent.processMessageApi(lowerMessage)
  
  return {
    message: response?.data?.data ?? "请求失败，请稍后再试。",
    actions: []
  }
  
  // 通用回复
  return {
    message: getGeneralResponse(userMessage),
    actions: []
  }
}

// 生成摘要
function generateSummary(content) {
  if (!content) return '暂无内容'
  const plainText = content.replace(/<[^>]+>/g, '')
  return plainText.length > 200 ? plainText.substring(0, 200) + '...' : plainText
}

// 生成标签
function generateTags(content) {
  const tags = []
  const lowerContent = content.toLowerCase()
  
  if (lowerContent.includes('工作') || lowerContent.includes('项目') || lowerContent.includes('会议')) {
    tags.push('工作')
  }
  if (lowerContent.includes('学习') || lowerContent.includes('课程') || lowerContent.includes('知识')) {
    tags.push('学习')
  }
  if (lowerContent.includes('想法') || lowerContent.includes('灵感') || lowerContent.includes('创意')) {
    tags.push('灵感')
  }
  if (lowerContent.includes('待办') || lowerContent.includes('任务') || lowerContent.includes('计划')) {
    tags.push('待办')
  }
  if (lowerContent.includes('重要') || lowerContent.includes('紧急')) {
    tags.push('重要')
  }
  
  return tags.length ? tags : ['笔记', '记录']
}

// 优化内容
function optimizeContent(content) {
  // 简单的优化示例，实际可以使用 AI 接口
  let optimized = content
  optimized = optimized.replace(/  +/g, ' ')
  optimized = optimized.replace(/^\s+|\s+$/g, '')
  return optimized
}

// 获取笔记统计
function getNoteStats() {
  const notes = props.allNotes
  let totalWords = 0
  notes.forEach(note => {
    const plainText = note.content?.replace(/<[^>]+>/g, '') || ''
    totalWords += plainText.length
  })
  
  return {
    totalNotes: notes.length,
    totalWords,
    avgWords: notes.length ? Math.round(totalWords / notes.length) : 0,
    categoryCount: props.categories.length,
    tagCount: new Set(notes.flatMap(n => n.tags || [])).size
  }
}

// 获取通用回复
function getGeneralResponse(message) {
  if (message.includes('你好') || message.includes('hi')) {
    return '你好！有什么可以帮你的吗？'
  }
  if (message.includes('谢谢')) {
    return '不客气！随时为你服务 😊'
  }
  if (message.includes('帮助')) {
    return '我可以帮你处理笔记相关的事情，比如总结内容、生成标签、优化表达等。试试发送"总结当前笔记"或"生成标签"吧！'
  }
  return `收到你的问题："${message}"\n\n我目前还在学习阶段，你可以尝试以下功能：\n• 总结当前笔记\n• 生成标签\n• 优化表达\n• 笔记统计`
}

// 监听消息变化滚动
watch(messages, () => {
  scrollToBottom()
})

// 关闭抽屉
const close = () => {
  emit('close')
}
</script>

<style scoped>
.ai-drawer-overlay {
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

.ai-drawer-overlay.show {
  opacity: 1;
  visibility: visible;
}

.ai-drawer {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  max-width: 480px;
  background: white;
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.1);
  transform: translateX(100%);
  transition: transform 0.3s ease;
  z-index: 1001;
  display: flex;
  flex-direction: column;
}

.ai-drawer.show {
  transform: translateX(0);
}

.drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #e8e8e8;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.ai-icon {
  font-size: 28px;
}

.drawer-header h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: white;
}

.close-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  color: white;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.drawer-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f8f9fa;
}

.chat-messages {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  display: flex;
  gap: 12px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
  background: #e0e0e0;
}

.message.user .message-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.message.assistant .message-avatar {
  background: #e8e8e8;
}

.message-content {
  flex: 1;
  max-width: 80%;
}

.message.user .message-content {
  text-align: right;
}

.message-text {
  background: white;
  padding: 12px 16px;
  border-radius: 16px;
  font-size: 14px;
  line-height: 1.6;
  color: #333;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  white-space: pre-wrap;
  word-wrap: break-word;
}

.message.user .message-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.message-time {
  font-size: 11px;
  color: #999;
  margin-top: 4px;
  padding: 0 4px;
}

/* 打字动画 */
.typing-indicator {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  background: white;
  border-radius: 16px;
  width: fit-content;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #999;
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.4;
  }
  30% {
    transform: translateY(-8px);
    opacity: 1;
  }
}

.drawer-footer {
  padding: 16px 20px 20px;
  border-top: 1px solid #e8e8e8;
  background: white;
}

.quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.quick-action-btn {
  padding: 6px 12px;
  background: #f0f0f0;
  border: none;
  border-radius: 20px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
  color: #666;
}

.quick-action-btn:hover {
  background: #e0e0e0;
  transform: translateY(-1px);
}

.input-area {
  display: flex;
  gap: 12px;
  align-items: flex-end;
}

.ai-input {
  flex: 1;
  padding: 12px 16px;
  border: 1.5px solid #e0e0e0;
  border-radius: 12px;
  font-size: 14px;
  resize: none;
  font-family: inherit;
  transition: all 0.3s;
}

.ai-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.send-btn {
  width: 40px;
  height: 40px;
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  color: white;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 响应式 */
@media (max-width: 600px) {
  .ai-drawer {
    max-width: 100%;
  }
  
  .message-content {
    max-width: 85%;
  }
  
  .quick-actions {
    gap: 6px;
  }
  
  .quick-action-btn {
    font-size: 11px;
    padding: 4px 10px;
  }
}
</style>