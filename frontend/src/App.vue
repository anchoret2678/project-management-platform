<template>
  <div id="app" class="app-container">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { useAppStore } from '@/store/app'

const router = useRouter()
const userStore = useUserStore()
const appStore = useAppStore()

// 初始化应用
onMounted(async () => {
  try {
    // 恢复用户登录状态
    await userStore.restoreLogin()
    
    // 初始化应用配置
    appStore.initApp()
    
    // 设置页面标题
    document.title = '企业项目管理平台'
    
    // 添加favicon
    const link = document.querySelector("link[rel*='icon']") || document.createElement('link')
    link.type = 'image/x-icon'
    link.rel = 'shortcut icon'
    link.href = '/favicon.ico'
    document.getElementsByTagName('head')[0].appendChild(link)
    
  } catch (error) {
    console.error('应用初始化失败:', error)
  }
})
</script>

<style lang="scss">
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
  
  // 全局过渡效果
  .page-enter-active,
  .page-leave-active {
    transition: opacity 0.3s ease;
  }
  
  .page-enter-from,
  .page-leave-to {
    opacity: 0;
  }
  
  // 全局卡片悬停效果
  .hover-card {
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-lg);
    }
  }
  
  // 全局按钮样式增强
  .el-button {
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-1px);
    }
    
    &:active {
      transform: translateY(0);
    }
  }
  
  // 全局表格样式
  .el-table {
    background-color: transparent;
    
    th {
      background-color: var(--bg-secondary);
      color: var(--text-secondary);
      font-weight: 600;
    }
    
    tr {
      background-color: var(--bg-card);
      
      &:hover {
        background-color: var(--bg-hover);
      }
    }
    
    td {
      border-bottom: 1px solid var(--border-color);
    }
  }
  
  // 全局表单样式
  .el-form {
    .el-form-item {
      margin-bottom: 20px;
      
      &__label {
        color: var(--text-secondary);
        font-weight: 500;
      }
    }
    
    .el-input,
    .el-select,
    .el-date-editor {
      width: 100%;
    }
  }
  
  // 全局弹窗样式
  .el-dialog {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    
    &__header {
      border-bottom: 1px solid var(--border-color);
      padding: 20px;
      
      .el-dialog__title {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 18px;
      }
    }
    
    &__body {
      padding: 20px;
      color: var(--text-secondary);
    }
    
    &__footer {
      border-top: 1px solid var(--border-color);
      padding: 20px;
    }
  }
  
  // 全局消息提示样式
  .el-message {
    &--success {
      background-color: rgba(16, 185, 129, 0.1);
      border-color: rgba(16, 185, 129, 0.2);
    }
    
    &--warning {
      background-color: rgba(245, 158, 11, 0.1);
      border-color: rgba(245, 158, 11, 0.2);
    }
    
    &--error {
      background-color: rgba(239, 68, 68, 0.1);
      border-color: rgba(239, 68, 68, 0.2);
    }
    
    &--info {
      background-color: rgba(107, 114, 128, 0.1);
      border-color: rgba(107, 114, 128, 0.2);
    }
  }
  
  // 全局加载状态
  .loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(15, 23, 42, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
    
    .loading-content {
      text-align: center;
      color: var(--text-primary);
      
      .loading-text {
        margin-top: 16px;
        font-size: 16px;
      }
    }
  }
  
  // 响应式调整
  @media (max-width: 768px) {
    .el-dialog {
      width: 90% !important;
      margin: 20px auto !important;
    }
    
    .el-table {
      font-size: 14px;
    }
  }
}
</style>