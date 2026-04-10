<template>
    <div class="login-container">
        <h2>🔐 账号登录</h2>
        <form @submit.prevent="handleLogin">
            <div class="form-group">
                <label for="username">用户名</label>
                <input type="text" id="username" v-model="form.username" placeholder="请输入用户名" autocomplete="off"
                    required>
            </div>

            <div class="form-group">
                <label for="password">密码</label>
                <input type="password" id="password" v-model="form.password" placeholder="请输入密码" autocomplete="off"
                    required>
            </div>

            <button type="submit" :disabled="isLoading">
                {{ isLoading ? '登录中...' : '登 录' }}
            </button>
        </form>
        <div v-if="message.text" class="message" :class="message.type">
            {{ message.text }}
        </div>
        <div class="register-link">
            还没有账号？ <RouterLink to="/register">立即注册</RouterLink>
        </div>
    </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { loginApi, getMeApi } from '@/api/auth'

const router = useRouter()
const userStore = useUserStore()

const form = reactive({ username: '', password: '' })
const isLoading = ref(false)
const message = reactive({ text: '', type: 'success' })

const handleLogin = async () => {
    if (!form.username.trim() || !form.password.trim()) {
        message.text = '❌ 用户名和密码不能为空';
        message.type = 'error';
        return;
    }

    isLoading.value = true;
    message.text = '';

    try {
        const response = await loginApi(form.username, form.password);
        const tokenData = response?.data?.data;
        const access_token = tokenData?.access_token;
        const refresh_token = tokenData?.refresh_token;

        if (!access_token || !refresh_token) {
            throw new Error('登录响应缺少 token 信息');
        }
        
        const meResponse = await getMeApi(access_token);
        const me = meResponse?.data?.data || {};
        userStore.login({
            access_token: access_token,
            refresh_token: refresh_token,
            user_id: me.id ?? null,
            username: me.username ?? form.username,
            email: me.email ?? '',
            phone: me.phone ?? '',
            avatar: ''
        })
        
        router.push('/notes'); // 登录成功后跳转到笔记页面
    } catch (error) {
        if (error?.response?.status === 401) {
            message.text = '用户名或密码错误';
        } else {
            message.text = '登录请求失败，请检查后端服务是否启动';
        }
        message.type = 'error';
        console.error('登录出错:', error);
    } finally {
        isLoading.value = false;
    }
}
</script>

<style scoped>
.login-container {
    background: white;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

h2 {
    text-align: center;
    color: #333;
    margin-bottom: 30px;
}

.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 8px;
    color: #555;
    font-weight: 500;
}

input {
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    box-sizing: border-box;
    font-size: 16px;
    transition: border-color 0.3s;
}

input:focus {
    outline: none;
    border-color: #42b983;
    box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
}

button {
    width: 100%;
    padding: 14px;
    background-color: #42b983;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s;
}

button:hover {
    background-color: #369f6e;
}

button:disabled {
    background-color: #a0c0b0;
    cursor: not-allowed;
}

.message {
    margin-top: 20px;
    padding: 12px;
    border-radius: 6px;
    text-align: center;
    font-weight: 500;
}

.success {
    background-color: #e6f7e6;
    color: #2e7d32;
    border: 1px solid #a5d6a5;
}

.error {
    background-color: #fdeded;
    color: #d32f2f;
    border: 1px solid #f5c6c6;
}

.register-link {
    text-align: center;
    margin-top: 20px;
    color: #666;
}

.register-link a {
    color: #42b983;
    text-decoration: none;
    cursor: pointer;
}

.register-link a:hover {
    text-decoration: underline;
}
</style>