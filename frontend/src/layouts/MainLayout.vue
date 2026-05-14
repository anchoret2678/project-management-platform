<template>
  <div class="main-layout">
    <!-- 侧边栏 -->
    <aside 
      class="sidebar" 
      :class="{ 'sidebar-collapsed': isSidebarCollapsed }"
      :style="{ width: sidebarWidth }"
    >
      <!-- 侧边栏头部 -->
      <div class="sidebar-header">
        <div class="logo" @click="router.push('/dashboard')">
          <el-icon size="28" color="#3b82f6">
            <DataBoard />
          </el-icon>
          <span v-show="!isSidebarCollapsed" class="logo-text">项目管理平台</span>
        </div>
        <el-tooltip 
          :content="isSidebarCollapsed ? '展开侧边栏' : '折叠侧边栏'" 
          placement="right"
        >
          <el-button 
            class="collapse-button" 
            :icon="isSidebarCollapsed ? Expand : Fold" 
            @click="toggleSidebar"
            size="small"
            circle
            plain
          />
        </el-tooltip>
      </div>
      
      <!-- 侧边栏菜单 -->
      <div class="sidebar-menu">
        <el-scrollbar>
          <el-menu
            :default-active="activeMenu"
            :collapse="isSidebarCollapsed"
            :collapse-transition="false"
            :unique-opened="true"
            :router="true"
            class="sidebar-menu-list"
            background-color="transparent"
            text-color="var(--text-secondary)"
            active-text-color="var(--primary-color)"
          >
            <!-- 仪表盘 -->
            <el-menu-item index="/dashboard">
              <el-icon><DataBoard /></el-icon>
              <template #title>仪表盘</template>
            </el-menu-item>
            
            <!-- 项目管理 -->
            <el-sub-menu index="projects">
              <template #title>
                <el-icon><Document /></el-icon>
                <span>项目管理</span>
              </template>
              <el-menu-item index="/projects">项目列表</el-menu-item>
              <el-menu-item 
                v-if="isAdmin" 
                index="/projects/create"
              >
                创建项目
              </el-menu-item>
            </el-sub-menu>
            
            <!-- 云资产管理 -->
            <el-sub-menu index="cloud-assets">
              <template #title>
                <el-icon><Cloudy /></el-icon>
                <span>云资产管理</span>
              </template>
              <el-menu-item index="/cloud-assets">资产列表</el-menu-item>
              <el-menu-item 
                v-if="isAdmin" 
                index="/cloud-assets/create"
              >
                创建资产
              </el-menu-item>
            </el-sub-menu>
            
            <!-- SOW管理 -->
            <el-sub-menu index="sows">
              <template #title>
                <el-icon><DocumentCopy /></el-icon>
                <span>SOW管理</span>
              </template>
              <el-menu-item index="/sows">SOW列表</el-menu-item>
              <el-menu-item 
                v-if="isAdmin" 
                index="/sows/create"
              >
                创建SOW
              </el-menu-item>
            </el-sub-menu>
            
            <!-- SLA管理 -->
            <el-sub-menu index="slas">
              <template #title>
                <el-icon><Setting /></el-icon>
                <span>SLA管理</span>
              </template>
              <el-menu-item index="/slas">SLA列表</el-menu-item>
              <el-menu-item 
                v-if="isAdmin" 
                index="/slas/create"
              >
                创建SLA
              </el-menu-item>
            </el-sub-menu>
            
            <!-- 知识库 -->
            <el-sub-menu index="knowledge">
              <template #title>
                <el-icon><Notebook /></el-icon>
                <span>知识库</span>
              </template>
              <el-menu-item index="/knowledge">文档列表</el-menu-item>
              <el-menu-item 
                v-if="isAdmin" 
                index="/knowledge/create"
              >
                创建文档
              </el-menu-item>
            </el-sub-menu>
            
            <!-- 用户管理（仅管理员） -->
            <el-menu-item 
              v-if="isAdmin" 
              index="/users"
            >
              <el-icon><User /></el-icon>
              <template #title>用户管理</template>
            </el-menu-item>
            
            <!-- 系统设置（仅管理员） -->
            <el-menu-item 
              v-if="isAdmin" 
              index="/settings"
            >
              <el-icon><Setting /></el-icon>
              <template #title>系统设置</template>
            </el-menu-item>
          </el-menu>
        </el-scrollbar>
      </div>
      
      <!-- 侧边栏底部 -->
      <div class="sidebar-footer">
        <div class="user-info" @click="router.push('/profile')">
          <el-avatar :size="isSidebarCollapsed ? 32 : 40" :src="userAvatar">
            {{ userStore.userInfo?.full_name?.charAt(0) || 'U' }}
          </el-avatar>
          <div v-show="!isSidebarCollapsed" class="user-details">
            <div class="user-name">{{ userStore.userInfo?.full_name || '用户' }}</div>
            <div class="user-role">{{ userRoleText }}</div>
          </div>
        </div>
      </div>
    </aside>
    
    <!-- 主内容区域 -->
    <div class="main-content" :style="{ marginLeft: sidebarWidth }">
      <!-- 顶部导航栏 -->
      <header class="header">
        <div class="header-left">
          <div class="breadcrumb">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/dashboard' }">
                <el-icon><HomeFilled /></el-icon>
                首页
              </el-breadcrumb-item>
              <el-breadcrumb-item 
                v-for="(item, index) in breadcrumbs" 
                :key="index"
                :to="item.path ? { path: item.path } : undefined"
              >
                {{ item.title }}
              </el-breadcrumb-item>
            </el-breadcrumb>
          </div>
        </div>
        
        <div class="header-right">
          <!-- 搜索框 -->
          <div class="search-box">
            <el-input
              v-model="searchKeyword"
              placeholder="搜索项目、文档..."
              :prefix-icon="Search"
              clearable
              @keyup.enter="handleSearch"
              @clear="handleSearchClear"
            />
          </div>
          
          <!-- 通知 -->
          <el-dropdown trigger="click" @command="handleNotificationCommand">
            <div class="header-action notification">
              <el-badge :value="unreadCount" :max="99" :hidden="unreadCount === 0">
                <el-icon size="20"><Bell /></el-icon>
              </el-badge>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item 
                  v-for="notification in notifications" 
                  :key="notification.id"
                  :class="`notification-item notification-${notification.type}`"
                >
                  <div class="notification-content">
                    <div class="notification-title">{{ notification.title }}</div>
                    <div class="notification-message">{{ notification.message }}</div>
                    <div class="notification-time">{{ formatTime(notification.timestamp) }}</div>
                  </div>
                </el-dropdown-item>
                <el-dropdown-item v-if="notifications.length === 0" disabled>
                  暂无通知
                </el-dropdown-item>
                <el-dropdown-item divided @click="clearNotifications">
                  <el-icon><Delete /></el-icon>
                  清空通知
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          
          <!-- 主题切换 -->
          <div class="header-action theme-toggle" @click="toggleTheme">
            <el-icon size="20">
              <Sunny v-if="isDark" />
              <Moon v-else />
            </el-icon>
          </div>
          
          <!-- 用户菜单 -->
          <el-dropdown trigger="click" @command="handleUserCommand">
            <div class="user-menu">
              <el-avatar :size="32" :src="userAvatar">
                {{ userStore.userInfo?.full_name?.charAt(0) || 'U' }}
              </el-avatar>
              <span class="user-name">{{ userStore.userInfo?.full_name || '用户' }}</span>
              <el-icon><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>
                  个人中心
                </el-dropdown-item>
                <el-dropdown-item command="settings">
                  <el-icon><Setting /></el-icon>
                  账户设置
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>
      
      <!-- 页面内容 -->
      <main class="content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
      
      <!-- 页脚 -->
      <footer class="footer">
        <div class="footer-content">
          <div class="footer-left">
            <span>© 2026 企业项目管理平台</span>
            <span class="divider">|</span>
            <span>版本: 1.0.0</span>
          </div>
          <div class="footer-right">
            <el-link :underline="'never'" type="info">帮助文档</el-link>
            <span class="divider">|</span>
            <el-link :underline="'never'" type="info">技术支持</el-link>
            <span class="divider">|</span>
            <el-link :underline="'never'" type="info">服务热线: 400-123-4567</el-link>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  DataBoard,
  Document,
  Cloudy,
  DocumentCopy,
  Setting,
  Notebook,
  User,
  HomeFilled,
  Search,
  Bell,
  Delete,
  Sunny,
  Moon,
  ArrowDown,
  SwitchButton,
  Expand,
  Fold
} from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { useAppStore } from '@/store/app'
import dayjs from 'dayjs'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const appStore = useAppStore()

// 搜索关键词
const searchKeyword = ref('')

// 通知数据
const notifications = ref([
  {
    id: '1',
    type: 'info',
    title: '系统通知',
    message: '欢迎使用企业项目管理平台',
    timestamp: new Date(),
    read: false
  },
  {
    id: '2',
    type: 'success',
    title: '项目更新',
    message: '项目"OA系统升级"已上线',
    timestamp: new Date(Date.now() - 3600000),
    read: false
  },
  {
    id: '3',
    type: 'warning',
    title: 'SLA提醒',
    message: 'SLA"客户服务协议"即将到期',
    timestamp: new Date(Date.now() - 7200000),
    read: true
  }
])

// 计算属性
const isSidebarCollapsed = computed(() => appStore.isSidebarCollapsed)
const sidebarWidth = computed(() => 
  isSidebarCollapsed.value ? `${appStore.layoutConfig.sidebarCollapsedWidth}px` : `${appStore.layoutConfig.sidebarWidth}px`
)
const isDark = computed(() => appStore.isDark)
const isAdmin = computed(() => userStore.isAdmin)
const userRoleText = computed(() => isAdmin.value ? '管理员' : '普通用户')
const userAvatar = computed(() => '') // 可以添加用户头像URL
const breadcrumbs = computed(() => appStore.breadcrumbs)
const activeMenu = computed(() => route.path)
const unreadCount = computed(() => notifications.value.filter(n => !n.read).length)

// 处理搜索
const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    // 根据当前路由决定搜索类型
    const currentPath = route.path
    if (currentPath.includes('/projects')) {
      router.push(`/projects?keyword=${encodeURIComponent(searchKeyword.value)}`)
    } else if (currentPath.includes('/knowledge')) {
      router.push(`/knowledge?keyword=${encodeURIComponent(searchKeyword.value)}`)
    } else {
      // 默认全局搜索
      ElMessage.info(`搜索: ${searchKeyword.value}`)
    }
  }
}

const handleSearchClear = () => {
  // 清除搜索条件
}

// 处理通知命令
const handleNotificationCommand = (command: string) => {
  if (command === 'clear') {
    clearNotifications()
  }
}

// 清除通知
const clearNotifications = () => {
  notifications.value = []
  ElMessage.success('通知已清空')
}

// 切换主题
const toggleTheme = () => {
  appStore.toggleTheme()
}

// 切换侧边栏
const toggleSidebar = () => {
  appStore.toggleSidebar()
}

// 处理用户命令
const handleUserCommand = async (command: string) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'settings':
      router.push('/settings')
      break
    case 'logout':
      await handleLogout()
      break
  }
}

// 处理退出登录
const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await userStore.logout()
  } catch (error) {
    // 用户取消退出
  }
}

// 格式化时间
const formatTime = (time: Date) => {
  return dayjs(time).fromNow()
}

// 键盘快捷键
const handleKeyDown = (event: KeyboardEvent) => {
  // Ctrl + B 切换侧边栏
  if (event.ctrlKey && event.key === 'b') {
    event.preventDefault()
    toggleSidebar()
  }
  
  // Ctrl + K 聚焦搜索框
  if (event.ctrlKey && event.key === 'k') {
    event.preventDefault()
    const searchInput = document.querySelector('.search-box input') as HTMLInputElement
    if (searchInput) {
      searchInput.focus()
    }
  }
  
  // Ctrl + D 切换主题
  if (event.ctrlKey && event.key === 'd') {
    event.preventDefault()
    toggleTheme()
  }
}

// 生命周期钩子
onMounted(() => {
  // 添加键盘事件监听
  document.addEventListener('keydown', handleKeyDown)
  
  // 初始化应用
  appStore.initApp()
})

onUnmounted(() => {
  // 移除键盘事件监听
  document.removeEventListener('keydown', handleKeyDown)
})
</script>

<style lang="scss" scoped>
.main-layout {
  display: flex;
  min-height: 100vh;
  background: var(--bg-primary);
}

// 侧边栏样式
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  background: var(--bg-card);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  z-index: 1000;
  transition: width var(--transition-normal);
  
  &-header {
    padding: 20px;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    justify-content: space-between;
    
    .logo {
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      user-select: none;
      
      .logo-text {
        font-size: 18px;
        font-weight: 600;
        color: var(--text-primary);
        white-space: nowrap;
      }
    }
    
    .collapse-button {
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      
      &:hover {
        background: var(--bg-hover);
        border-color: var(--primary-color);
      }
    }
  }
  
  &-menu {
    flex: 1;
    overflow: hidden;
    
    :deep(.el-scrollbar) {
      height: 100%;
    }
    
    .sidebar-menu-list {
      border: none;
      padding: 10px 0;
      
      :deep(.el-menu-item),
      :deep(.el-sub-menu__title) {
        height: 48px;
        line-height: 48px;
        margin: 4px 12px;
        border-radius: var(--radius-md);
        
        &:hover {
          background: var(--bg-hover);
        }
        
        &.is-active {
          background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-hover) 100%);
          color: white !important;
          
          .el-icon {
            color: white !important;
          }
        }
      }
      
      :deep(.el-sub-menu) {
        .el-menu {
          background: var(--bg-secondary);
        }
        
        .el-menu-item {
          margin: 2px 0;
          padding-left: 56px !important;
        }
      }
    }
  }
  
  &-footer {
    padding: 20px;
    border-top: 1px solid var(--border-color);
    
    .user-info {
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      padding: 8px;
      border-radius: var(--radius-md);
      transition: background var(--transition-fast);
      
      &:hover {
        background: var(--bg-hover);
      }
      
      .user-details {
        overflow: hidden;
        
        .user-name {
          font-weight: 500;
          color: var(--text-primary);
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        
        .user-role {
          font-size: 12px;
          color: var(--text-tertiary);
          margin-top: 2px;
        }
      }
    }
  }
  
  &.sidebar-collapsed {
    .logo-text,
    .user-details {
      display: none;
    }
    
    .sidebar-header {
      justify-content: center;
      padding: 20px 12px;
    }
    
    .sidebar-footer {
      padding: 20px 12px;
      display: flex;
      justify-content: center;
    }
  }
}

// 主内容区域
.main-content {
  flex: 1;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  transition: margin-left var(--transition-normal);
}

// 头部样式
.header {
  height: var(--header-height);
  background: var(--bg-card);
  border-bottom: 1px solid var(--border-color);
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 999;
  
  &-left {
    .breadcrumb {
      :deep(.el-breadcrumb) {
        .el-breadcrumb__item {
          .el-breadcrumb__inner {
            color: var(--text-secondary);
            
            &:hover {
              color: var(--primary-color);
            }
          }
          
          &:last-child {
            .el-breadcrumb__inner {
              color: var(--text-primary);
              font-weight: 500;
            }
          }
        }
      }
    }
  }
  
  &-right {
    display: flex;
    align-items: center;
    gap: 20px;
    
    .search-box {
      width: 240px;
      
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
    
    .header-action {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 36px;
      height: 36px;
      border-radius: var(--radius-md);
      cursor: pointer;
      color: var(--text-secondary);
      transition: all var(--transition-fast);
      
      &:hover {
        background: var(--bg-hover);
        color: var(--text-primary);
      }
      
      &.notification {
        position: relative;
        
        :deep(.el-badge__content) {
          border: 2px solid var(--bg-card);
        }
      }
      
      &.theme-toggle {
        .el-icon {
          transition: transform var(--transition-normal);
        }
        
        &:hover .el-icon {
          transform: rotate(30deg);
        }
      }
    }
    
    .user-menu {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 4px 8px;
      border-radius: var(--radius-md);
      cursor: pointer;
      transition: background var(--transition-fast);
      
      &:hover {
        background: var(--bg-hover);
      }
      
      .user-name {
        font-weight: 500;
        color: var(--text-primary);
        max-width: 120px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
      
      .el-icon {
        color: var(--text-tertiary);
        font-size: 12px;
      }
    }
  }
}

// 通知下拉菜单样式
:deep(.el-dropdown-menu) {
  .notification-item {
    padding: 12px 16px;
    min-width: 320px;
    
    .notification-content {
      .notification-title {
        font-weight: 500;
        color: var(--text-primary);
        margin-bottom: 4px;
      }
      
      .notification-message {
        font-size: 12px;
        color: var(--text-secondary);
        margin-bottom: 4px;
        line-height: 1.4;
      }
      
      .notification-time {
        font-size: 11px;
        color: var(--text-tertiary);
      }
    }
    
    &.notification-info {
      border-left: 3px solid var(--info-color);
    }
    
    &.notification-success {
      border-left: 3px solid var(--success-color);
    }
    
    &.notification-warning {
      border-left: 3px solid var(--warning-color);
    }
    
    &.notification-error {
      border-left: 3px solid var(--danger-color);
    }
  }
}

// 内容区域
.content {
  flex: 1;
  padding: 24px;
  overflow: auto;
  background: var(--bg-primary);
}

// 页脚样式
.footer {
  height: 48px;
  background: var(--bg-card);
  border-top: 1px solid var(--border-color);
  padding: 0 24px;
  
  .footer-content {
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: var(--text-tertiary);
    font-size: 12px;
    
    .footer-left,
    .footer-right {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    
    .divider {
      opacity: 0.5;
    }
    
    :deep(.el-link) {
      font-size: 12px;
    }
  }
}

// 过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--transition-normal);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

// 响应式调整
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    
    &.sidebar-collapsed {
      transform: translateX(0);
    }
  }
  
  .main-content {
    margin-left: 0 !important;
  }
  
  .header {
    padding: 0 16px;
    
    &-right {
      .search-box {
        display: none;
      }
      
      .user-menu .user-name {
        display: none;
      }
    }
  }
  
  .content {
    padding: 16px;
  }
  
  .footer {
    padding: 0 16px;
    
    .footer-content {
      flex-direction: column;
      justify-content: center;
      gap: 8px;
      text-align: center;
    }
  }
}

@media (max-width: 480px) {
  .header {
    &-left {
      .breadcrumb {
        display: none;
      }
    }
  }
}
</style>