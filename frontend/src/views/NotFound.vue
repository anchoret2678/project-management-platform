<template>
  <div class="not-found-container">
    <!-- 背景装饰 -->
    <div class="background-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
    </div>
    
    <!-- 错误内容 -->
    <div class="error-content">
      <!-- 错误代码 -->
      <div class="error-code">
        <span class="code-number">4</span>
        <el-icon class="code-icon"><WarningFilled /></el-icon>
        <span class="code-number">4</span>
      </div>
      
      <!-- 错误标题 -->
      <h1 class="error-title">页面未找到</h1>
      
      <!-- 错误描述 -->
      <p class="error-description">
        抱歉，您访问的页面不存在或已被移除。<br>
        请检查URL是否正确，或返回首页继续浏览。
      </p>
      
      <!-- 操作按钮 -->
      <div class="action-buttons">
        <el-button
          type="primary"
          size="large"
          :icon="HomeFilled"
          @click="goToHome"
          class="home-button"
        >
          返回首页
        </el-button>
        
        <el-button
          size="large"
          :icon="Refresh"
          @click="goBack"
          class="back-button"
        >
          返回上一页
        </el-button>
      </div>
      
      <!-- 额外信息 -->
      <div class="extra-info">
        <div class="info-item">
          <el-icon><Clock /></el-icon>
          <span>当前时间: {{ currentTime }}</span>
        </div>
        <div class="info-item">
          <el-icon><Link /></el-icon>
          <span>请求路径: {{ currentPath }}</span>
        </div>
      </div>
      
      <!-- 技术支持 -->
      <div class="support-info">
        <p>如需帮助，请联系技术支持:</p>
        <div class="contact-info">
          <el-icon><Phone /></el-icon>
          <span>服务热线: 400-123-4567</span>
        </div>
        <div class="contact-info">
          <el-icon><Message /></el-icon>
          <span>邮箱: support@company.com</span>
        </div>
      </div>
    </div>
    
    <!-- 页脚 -->
    <div class="not-found-footer">
      <p>© 2026 企业项目管理平台. 保留所有权利.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  WarningFilled,
  HomeFilled,
  Refresh,
  Clock,
  Link,
  Phone,
  Message
} from '@element-plus/icons-vue'
import { useAppStore } from '@/store/app'

const router = useRouter()
const appStore = useAppStore()

// 当前时间
const currentTime = ref('')
const currentPath = ref('')

// 更新时间
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  })
}

// 返回首页
const goToHome = () => {
  router.push('/dashboard')
}

// 返回上一页
const goBack = () => {
  if (window.history.length > 1) {
    router.back()
  } else {
    goToHome()
  }
}

// 生命周期钩子
onMounted(() => {
  // 设置页面标题
  appStore.setPageTitle('页面未找到')
  
  // 获取当前路径
  currentPath.value = window.location.pathname
  
  // 初始化时间
  updateTime()
  
  // 设置定时器更新时间
  const timer = setInterval(updateTime, 1000)
  
  // 清理定时器
  onUnmounted(() => {
    clearInterval(timer)
  })
})
</script>

<style lang="scss" scoped>
.not-found-container {
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

.background-shapes {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  
  .shape {
    position: absolute;
    border-radius: 50%;
    opacity: 0.05;
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%);
    
    &.shape-1 {
      width: 400px;
      height: 400px;
      top: -200px;
      right: -200px;
    }
    
    &.shape-2 {
      width: 300px;
      height: 300px;
      bottom: -150px;
      left: -150px;
    }
    
    &.shape-3 {
      width: 200px;
      height: 200px;
      top: 50%;
      left: 10%;
    }
  }
}

.error-content {
  text-align: center;
  max-width: 600px;
  z-index: 1;
  animation: fadeIn 0.6s ease-out;
}

.error-code {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 30px;
  
  .code-number {
    font-size: 120px;
    font-weight: 800;
    color: var(--primary-color);
    line-height: 1;
    text-shadow: 0 4px 20px rgba(59, 130, 246, 0.3);
    
    @media (max-width: 768px) {
      font-size: 80px;
    }
  }
  
  .code-icon {
    font-size: 80px;
    color: var(--warning-color);
    margin: 0 20px;
    animation: pulse 2s infinite;
    
    @media (max-width: 768px) {
      font-size: 60px;
      margin: 0 15px;
    }
  }
}

.error-title {
  font-size: 32px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 16px;
  line-height: 1.3;
  
  @media (max-width: 768px) {
    font-size: 24px;
  }
}

.error-description {
  font-size: 16px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 40px;
  
  @media (max-width: 768px) {
    font-size: 14px;
  }
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 40px;
  
  @media (max-width: 768px) {
    flex-direction: column;
    gap: 12px;
  }
  
  .home-button {
    padding: 12px 32px;
    font-size: 16px;
    font-weight: 500;
    border-radius: var(--radius-lg);
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%);
    border: none;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-lg);
    }
    
    &:active {
      transform: translateY(0);
    }
  }
  
  .back-button {
    padding: 12px 32px;
    font-size: 16px;
    font-weight: 500;
    border-radius: var(--radius-lg);
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    
    &:hover {
      background: var(--bg-hover);
      border-color: var(--primary-color);
      color: var(--primary-color);
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
    }
    
    &:active {
      transform: translateY(0);
    }
  }
}

.extra-info {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 20px;
  margin-bottom: 30px;
  
  .info-item {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-bottom: 10px;
    font-size: 14px;
    color: var(--text-secondary);
    
    &:last-child {
      margin-bottom: 0;
    }
    
    .el-icon {
      color: var(--text-tertiary);
      font-size: 16px;
    }
  }
}

.support-info {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 24px;
  margin-bottom: 30px;
  
  p {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 16px;
  }
  
  .contact-info {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-bottom: 8px;
    font-size: 14px;
    color: var(--text-primary);
    
    &:last-child {
      margin-bottom: 0;
    }
    
    .el-icon {
      color: var(--primary-color);
      font-size: 16px;
    }
  }
}

.not-found-footer {
  margin-top: 30px;
  text-align: center;
  color: var(--text-tertiary);
  font-size: 12px;
  z-index: 1;
  
  p {
    margin: 0;
    opacity: 0.8;
  }
}

// 动画
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

// 响应式调整
@media (max-width: 768px) {
  .not-found-container {
    padding: 10px;
  }
  
  .error-code {
    margin-bottom: 20px;
  }
  
  .error-title {
    margin-bottom: 12px;
  }
  
  .error-description {
    margin-bottom: 30px;
  }
  
  .extra-info,
  .support-info {
    padding: 16px;
  }
}
</style>