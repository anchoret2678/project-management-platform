<template>
  <div class="login-container">
    <!-- 背景装饰 -->
    <div class="login-background">
      <div class="background-shapes">
        <div class="shape shape-1"></div>
        <div class="shape shape-2"></div>
        <div class="shape shape-3"></div>
        <div class="shape shape-4"></div>
      </div>
    </div>
    
    <!-- 登录卡片 -->
    <div class="login-card">
      <!-- 左侧品牌区域 -->
      <div class="login-brand">
        <div class="brand-logo">
          <el-icon size="48" color="#3b82f6">
            <DataBoard />
          </el-icon>
        </div>
        <div class="brand-content">
          <h1 class="brand-title">企业项目管理平台</h1>
          <p class="brand-subtitle">统一管理项目全生命周期信息</p>
          <div class="brand-features">
            <div class="feature-item">
              <el-icon color="#10b981"><Check /></el-icon>
              <span>项目全生命周期管理</span>
            </div>
            <div class="feature-item">
              <el-icon color="#10b981"><Check /></el-icon>
              <span>云平台资产管理</span>
            </div>
            <div class="feature-item">
              <el-icon color="#10b981"><Check /></el-icon>
              <span>SOW/SLA文档管理</span>
            </div>
            <div class="feature-item">
              <el-icon color="#10b981"><Check /></el-icon>
              <span>项目知识库</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 右侧登录表单 -->
      <div class="login-form">
        <div class="form-header">
          <h2 class="form-title">欢迎登录</h2>
          <p class="form-subtitle">请输入您的账号信息</p>
        </div>
        
        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          class="login-form-content"
          @keyup.enter="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              size="large"
              :prefix-icon="User"
              clearable
            />
          </el-form-item>
          
          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              :prefix-icon="Lock"
              show-password
              clearable
            />
          </el-form-item>
          
          <el-form-item>
            <div class="form-options">
              <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
              <el-link type="primary" :underline="false">忘记密码？</el-link>
            </div>
          </el-form-item>
          
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              @click="handleLogin"
              class="login-button"
            >
              {{ loading ? '登录中...' : '登录' }}
            </el-button>
          </el-form-item>
          
          <div class="form-footer">
            <div class="demo-accounts">
              <p class="demo-title">演示账号：</p>
              <div class="account-item">
                <span class="account-role">管理员</span>
                <span class="account-info">用户名: admin / 密码: admin123</span>
              </div>
              <div class="account-item">
                <span class="account-role">普通用户</span>
                <span class="account-info">用户名: user1 / 密码: admin123</span>
              </div>
            </div>
            
            <div class="version-info">
              <el-icon><InfoFilled /></el-icon>
              <span>版本: 1.0.0</span>
            </div>
          </div>
        </el-form>
      </div>
    </div>
    
    <!-- 页脚 -->
    <div class="login-footer">
      <p>© 2026 企业项目管理平台. 保留所有权利.</p>
      <p>技术支持: IT部门 | 服务热线: 400-123-4567</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { User, Lock, Check, DataBoard, InfoFilled } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { useAppStore } from '@/store/app'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const appStore = useAppStore()

// 表单引用
const loginFormRef = ref<FormInstance>()

// 表单数据
const loginForm = reactive({
  username: '',
  password: '',
  remember: false
})

// 加载状态
const loading = ref(false)

// 表单验证规则
const loginRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在 6 到 20 个字符', trigger: 'blur' }
  ]
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    // 验证表单
    await loginFormRef.value.validate()
    
    // 设置加载状态
    loading.value = true
    
    // 调用登录接口
    const success = await userStore.login({
      username: loginForm.username,
      password: loginForm.password
    })
    
    if (success) {
      // 登录成功，跳转到目标页面或首页
      const redirect = route.query.redirect as string
      router.push(redirect || '/dashboard')
    }
  } catch (error) {
    console.error('登录错误:', error)
  } finally {
    loading.value = false
  }
}

// 初始化演示账号
const initDemoAccounts = () => {
  // 可以根据需要预填充演示账号
  // loginForm.username = 'admin'
  // loginForm.password = 'admin123'
}

// 键盘事件监听
const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Enter' && !loading.value) {
    handleLogin()
  }
}

// 生命周期钩子
onMounted(() => {
  // 初始化演示账号
  initDemoAccounts()
  
  // 添加键盘事件监听
  document.addEventListener('keydown', handleKeyDown)
  
  // 设置应用主题
  appStore.applyTheme()
})

onUnmounted(() => {
  // 移除键盘事件监听
  document.removeEventListener('keydown', handleKeyDown)
})
</script>

<style lang="scss" scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.login-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  
  .background-shapes {
    position: relative;
    width: 100%;
    height: 100%;
    
    .shape {
      position: absolute;
      border-radius: 50%;
      opacity: 0.1;
      background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%);
      
      &.shape-1 {
        width: 300px;
        height: 300px;
        top: -150px;
        right: -150px;
      }
      
      &.shape-2 {
        width: 200px;
        height: 200px;
        bottom: -100px;
        left: -100px;
      }
      
      &.shape-3 {
        width: 150px;
        height: 150px;
        top: 50%;
        left: 10%;
      }
      
      &.shape-4 {
        width: 100px;
        height: 100px;
        bottom: 20%;
        right: 15%;
      }
    }
  }
}

.login-card {
  display: flex;
  max-width: 1000px;
  width: 100%;
  background: var(--bg-card);
  border-radius: var(--radius-xl);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  z-index: 1;
  min-height: 600px;
  
  @media (max-width: 768px) {
    flex-direction: column;
    max-width: 400px;
  }
}

.login-brand {
  flex: 1;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%);
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: white;
  
  @media (max-width: 768px) {
    padding: 30px;
    text-align: center;
  }
  
  .brand-logo {
    margin-bottom: 30px;
    
    .el-icon {
      background: rgba(255, 255, 255, 0.1);
      padding: 12px;
      border-radius: var(--radius-lg);
    }
  }
  
  .brand-content {
    .brand-title {
      font-size: 28px;
      font-weight: 700;
      margin-bottom: 10px;
      line-height: 1.3;
    }
    
    .brand-subtitle {
      font-size: 16px;
      opacity: 0.9;
      margin-bottom: 30px;
    }
    
    .brand-features {
      .feature-item {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
        font-size: 14px;
        
        .el-icon {
          margin-right: 10px;
          font-size: 16px;
        }
        
        span {
          opacity: 0.9;
        }
      }
    }
  }
}

.login-form {
  flex: 1;
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  
  @media (max-width: 768px) {
    padding: 30px;
  }
  
  .form-header {
    margin-bottom: 40px;
    text-align: center;
    
    .form-title {
      font-size: 24px;
      font-weight: 600;
      color: var(--text-primary);
      margin-bottom: 8px;
    }
    
    .form-subtitle {
      font-size: 14px;
      color: var(--text-tertiary);
    }
  }
  
  .login-form-content {
    .el-form-item {
      margin-bottom: 24px;
      
      :deep(.el-input__wrapper) {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        
        &:hover {
          border-color: var(--primary-color);
        }
        
        &.is-focus {
          border-color: var(--primary-color);
          box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
        }
      }
    }
    
    .form-options {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      
      :deep(.el-checkbox__label) {
        color: var(--text-secondary);
      }
    }
    
    .login-button {
      width: 100%;
      height: 48px;
      font-size: 16px;
      font-weight: 500;
      border-radius: var(--radius-lg);
      background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%);
      border: none;
      
      &:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
      }
      
      &:active {
        transform: translateY(0);
      }
    }
    
    .form-footer {
      margin-top: 30px;
      padding-top: 20px;
      border-top: 1px solid var(--border-color);
      
      .demo-accounts {
        margin-bottom: 20px;
        
        .demo-title {
          font-size: 12px;
          color: var(--text-tertiary);
          margin-bottom: 8px;
          text-transform: uppercase;
          letter-spacing: 0.5px;
        }
        
        .account-item {
          display: flex;
          align-items: center;
          margin-bottom: 6px;
          font-size: 12px;
          
          .account-role {
            color: var(--primary-color);
            font-weight: 500;
            margin-right: 8px;
            min-width: 60px;
          }
          
          .account-info {
            color: var(--text-secondary);
          }
        }
      }
      
      .version-info {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        color: var(--text-tertiary);
        
        .el-icon {
          margin-right: 6px;
          font-size: 14px;
        }
      }
    }
  }
}

.login-footer {
  margin-top: 30px;
  text-align: center;
  color: var(--text-tertiary);
  font-size: 12px;
  z-index: 1;
  
  p {
    margin: 4px 0;
    opacity: 0.8;
  }
}

// 动画效果
.login-card {
  animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

// 响应式调整
@media (max-width: 768px) {
  .login-container {
    padding: 10px;
  }
  
  .login-card {
    min-height: auto;
  }
  
  .login-brand {
    .brand-title {
      font-size: 24px;
    }
    
    .brand-subtitle {
      font-size: 14px;
    }
  }
  
  .login-form {
    .form-title {
      font-size: 20px;
    }
  }
}

@media (max-width: 480px) {
  .login-brand {
    padding: 20px;
    
    .brand-title {
      font-size: 20px;
    }
  }
  
  .login-form {
    padding: 20px;
  }
}
</style>