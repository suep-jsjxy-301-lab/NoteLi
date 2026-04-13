<template>
    <div class="register-card">
        <h2>📝 账号注册</h2>
        <p class="subtitle">填写以下信息，创建您的账户</p>

        <form @submit.prevent="handleRegister">
            <!-- 用户名 -->
            <div class="form-group">
                <label for="username">
                    用户名 <span class="required">*</span>
                </label>
                <input type="text" id="username" v-model="form.username" placeholder="请输入用户名（3-20个字符）"
                    autocomplete="off" :class="{ 'input-error': validationErrors.username }" />
                <span v-if="validationErrors.username" class="error-message">
                    {{ validationErrors.username }}
                </span>
            </div>

            <!-- 邮箱 -->
            <div class="form-group">
                <label for="email">
                    邮箱 <span class="required">*</span>
                </label>
                <input type="email" id="email" v-model="form.email" placeholder="请输入邮箱地址" autocomplete="off"
                    :class="{ 'input-error': validationErrors.email }" />
                <span v-if="validationErrors.email" class="error-message">
                    {{ validationErrors.email }}
                </span>
            </div>

            <!-- 手机号（可选） -->
            <div class="form-group">
                <label for="phone">手机号 <span class="optional">(可选)</span></label>
                <input type="tel" id="phone" v-model="form.phone" placeholder="请输入手机号" autocomplete="off"
                    :class="{ 'input-error': validationErrors.phone }" />
                <span v-if="validationErrors.phone" class="error-message">
                    {{ validationErrors.phone }}
                </span>
            </div>

            <!-- 密码 -->
            <div class="form-group">
                <label for="password">
                    密码 <span class="required">*</span>
                </label>
                <input type="password" id="password" v-model="form.password" placeholder="请输入密码（至少6位）"
                    autocomplete="off" :class="{ 'input-error': validationErrors.password }" />
                <span v-if="validationErrors.password" class="error-message">
                    {{ validationErrors.password }}
                </span>
                <!-- 密码强度提示 -->
                <div v-if="form.password" class="password-strength">
                    <div class="strength-bar">
                        <div class="strength-fill" :style="{ width: passwordStrength.percentage + '%' }"
                            :class="passwordStrength.class"></div>
                    </div>
                    <span class="strength-text" :class="passwordStrength.class">
                        {{ passwordStrength.text }}
                    </span>
                </div>
            </div>

            <!-- 确认密码 -->
            <div class="form-group">
                <label for="confirmPassword">
                    确认密码 <span class="required">*</span>
                </label>
                <input type="password" id="confirmPassword" v-model="form.confirmPassword" placeholder="请再次输入密码"
                    autocomplete="off" :class="{ 'input-error': validationErrors.confirmPassword }" />
                <span v-if="validationErrors.confirmPassword" class="error-message">
                    {{ validationErrors.confirmPassword }}
                </span>
            </div>

            <!-- 同意条款 -->
            <div class="form-group checkbox-group">
                <label class="checkbox-label">
                    <input type="checkbox" v-model="form.agreement" />
                    <span class="checkbox-text">
                        我已阅读并同意
                        <a href="#" @click.prevent="showTerms">《服务条款》</a>
                        和
                        <a href="#" @click.prevent="showPrivacy">《隐私政策》</a>
                    </span>
                </label>
                <span v-if="validationErrors.agreement" class="error-message">
                    {{ validationErrors.agreement }}
                </span>
            </div>
            <div class="form-group">
            <div class="register-link">
            <label class="login-label">
    已有账号？ <router-link to="/login">立即登录</router-link>
</label>
          </div></div>
            <!-- 提交按钮 -->
            <button type="submit" class="register-btn" :disabled="isLoading || !isFormValid">
                <span v-if="!isLoading">注 册</span>
                <span v-else class="loading">
                    <i class="loading-spinner"></i>
                    注册中...
                </span>
            </button>
        </form>

        <!-- 提示消息 -->
        <transition name="fade">
            <div v-if="message.text" class="message" :class="message.type">
                {{ message.text }}
            </div>
        </transition>
        
    </div>
</template>

<script setup>
import { reactive, ref, computed, watch, onUnmounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import Api from '@/api/api'

const router = useRouter()
let redirectTimerId = null

// 表单数据
const form = reactive({
    username: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
    agreement: false
})

// 加载状态
const isLoading = ref(false)

// 提示消息
const message = reactive({
    text: '',
    type: 'success' // 'success' 或 'error'
})

// 表单是否被提交过（用于控制错误显示时机）
const isSubmitted = ref(false)

// 密码强度计算
const passwordStrength = computed(() => {
    const pwd = form.password
    if (!pwd) {
        return { text: '', percentage: 0, class: '' }
    }

    let strength = 0
    // 长度得分
    if (pwd.length >= 6) strength += 20
    if (pwd.length >= 8) strength += 10
    // 字符类型得分
    if (/[a-z]/.test(pwd)) strength += 15
    if (/[A-Z]/.test(pwd)) strength += 15
    if (/[0-9]/.test(pwd)) strength += 20
    if (/[^a-zA-Z0-9]/.test(pwd)) strength += 20

    let text = ''
    let className = ''
    if (strength < 30) {
        text = '弱'
        className = 'weak'
    } else if (strength < 60) {
        text = '中'
        className = 'medium'
    } else {
        text = '强'
        className = 'strong'
    }

    return {
        text,
        percentage: Math.min(strength, 100),
        class: className
    }
})

// 验证规则
const validationErrors = computed(() => {
    const errors = {}

    // 只在表单提交后或字段有值时进行验证
    if (isSubmitted.value || form.username) {
        if (!form.username) {
            errors.username = '用户名不能为空'
        } else if (form.username.length < 3 || form.username.length > 20) {
            errors.username = '用户名长度应为 3-20 个字符'
        } else if (!/^[a-zA-Z0-9_\u4e00-\u9fa5]+$/.test(form.username)) {
            errors.username = '用户名只能包含字母、数字、下划线和中文'
        }
    }

    if (isSubmitted.value || form.email) {
        if (!form.email) {
            errors.email = '邮箱不能为空'
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
            errors.email = '请输入有效的邮箱地址'
        }
    }

    if (form.phone && (isSubmitted.value || form.phone)) {
        if (!/^1[3-9]\d{9}$/.test(form.phone)) {
            errors.phone = '请输入有效的手机号'
        }
    }

    if (isSubmitted.value || form.password) {
        if (!form.password) {
            errors.password = '密码不能为空'
        } else if (form.password.length < 6) {
            errors.password = '密码长度至少为 6 位'
        }
    }

    if (isSubmitted.value || form.confirmPassword) {
        if (!form.confirmPassword) {
            errors.confirmPassword = '请再次输入密码'
        } else if (form.confirmPassword !== form.password) {
            errors.confirmPassword = '两次输入的密码不一致'
        }
    }

    if (isSubmitted.value) {
        if (!form.agreement) {
            errors.agreement = '请阅读并同意服务条款和隐私政策'
        }
    }

    return errors
})

// 表单整体是否有效
const isFormValid = computed(() => {
    return Object.keys(validationErrors.value).length === 0
})

// 清空消息（当用户开始修改表单时）
watch(
    () => form,
    () => {
        if (message.text) {
            message.text = ''
        }
    },
    { deep: true }
)

// 处理注册
const handleRegister = async () => {
    isSubmitted.value = true
    message.text = ''

    // 验证表单
    if (!isFormValid.value) {
        message.text = '❌ 请正确填写所有必填项'
        message.type = 'error'
        return
    }

    isLoading.value = true

    try {
        const response = await Api.user.registerApi({
            username: form.username.trim(),
            password: form.password,
            email: form.email.trim(),
            phone: form.phone.trim() || null
        })
        const ok = response?.data?.success
        if (!ok) {
            message.text = `❌ ${response?.data?.message || '注册失败'}`
            message.type = 'error'
            return
        }

        message.text = '✅ 注册成功！1.5 秒后自动前往登录页…'
        message.type = 'success'
        if (redirectTimerId) {
            clearTimeout(redirectTimerId)
        }
        redirectTimerId = setTimeout(() => {
            redirectTimerId = null
            resetForm()
            router.push('/login')
        }, 1500)
    } catch (error) {
        const backendMsg = error?.response?.data?.message
        message.text = `❌ ${backendMsg || '网络错误，请稍后再试'}`
        message.type = 'error'
        console.error('注册出错:', error)
    } finally {
        isLoading.value = false
    }
}

const resetForm = () => {
    form.username = ''
    form.email = ''
    form.phone = ''
    form.password = ''
    form.confirmPassword = ''
    form.agreement = false
    isSubmitted.value = false
}

// 显示条款（模拟弹窗）
const showTerms = () => {
    alert('《服务条款》内容：这是一个演示页面，条款内容可自行替换。')
}

const showPrivacy = () => {
    alert('《隐私政策》内容：我们重视您的隐私，数据仅用于演示。')
}

onUnmounted(() => {
    if (redirectTimerId) {
        clearTimeout(redirectTimerId)
    }
})
</script>

<style scoped>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

.register-card {
    width: 100%;
    max-width: 460px;
    background: white;
    border-radius: 16px;
    padding: 40px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

h2 {
    text-align: center;
    color: #2d3748;
    margin-bottom: 8px;
    font-size: 28px;
}

.subtitle {
    text-align: center;
    color: #718096;
    margin-bottom: 30px;
    font-size: 14px;
}

.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 6px;
    color: #4a5568;
    font-size: 14px;
    font-weight: 500;
}

.required {
    color: #e53e3e;
    margin-left: 2px;
}

.optional {
    color: #a0aec0;
    font-weight: normal;
    font-size: 12px;
}

input[type='text'],
input[type='email'],
input[type='tel'],
input[type='password'] {
    width: 100%;
    padding: 12px 14px;
    border: 1.5px solid #e2e8f0;
    border-radius: 8px;
    font-size: 15px;
    transition: all 0.3s ease;
    background: #fafafa;
}

input:focus {
    outline: none;
    border-color: #667eea;
    background: white;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.input-error {
    border-color: #fc8181 !important;
    background: #fff5f5 !important;
}

.error-message {
    display: block;
    color: #e53e3e;
    font-size: 12px;
    margin-top: 4px;
}

/* 密码强度指示器 */
.password-strength {
    margin-top: 8px;
}

.strength-bar {
    height: 4px;
    background: #e2e8f0;
    border-radius: 2px;
    overflow: hidden;
    margin-bottom: 4px;
}

.strength-fill {
    height: 100%;
    transition: width 0.3s ease;
}

.strength-fill.weak {
    background: #fc8181;
}

.strength-fill.medium {
    background: #f6ad55;
}

.strength-fill.strong {
    background: #68d391;
}

.strength-text {
    font-size: 12px;
}

.strength-text.weak {
    color: #e53e3e;
}

.strength-text.medium {
    color: #dd6b20;
}

.strength-text.strong {
    color: #38a169;
}

/* 复选框 */
.checkbox-group {
    margin-top: 5px;
}

.checkbox-label {
    display: flex;
    align-items: flex-start;
    cursor: pointer;
    font-weight: normal;
}

.checkbox-label input[type='checkbox'] {
    width: 18px;
    height: 18px;
    margin-right: 10px;
    margin-top: 2px;
    cursor: pointer;
    accent-color: #667eea;
}

.checkbox-text {
    color: #4a5568;
    font-size: 14px;
    line-height: 1.5;
}

.checkbox-text a {
    color: #667eea;
    text-decoration: none;
    font-weight: 500;
}

.checkbox-text a:hover {
    text-decoration: underline;
}

.login-label {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    cursor: pointer;
    font-weight: normal;
}
/* 注册按钮 */
.register-btn {
    width: 100%;
    padding: 14px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 10px;
}

.register-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.register-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.loading {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.loading-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    display: inline-block;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

/* 消息提示 */
.message {
    margin-top: 20px;
    padding: 12px 16px;
    border-radius: 8px;
    text-align: center;
    font-size: 14px;
    font-weight: 500;
}

.message.success {
    background: #f0fff4;
    color: #276749;
    border: 1px solid #9ae6b4;
}

.message.error {
    background: #fff5f5;
    color: #c53030;
    border: 1px solid #feb2b2;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

/* 移动端适配 */
@media (max-width: 480px) {
    .register-card {
        padding: 30px 20px;
    }

    h2 {
        font-size: 24px;
    }
}
</style>