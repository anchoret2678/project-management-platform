import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { AppState, ThemeConfig, LayoutConfig } from '@/types/app'

// 应用状态存储
export const useAppStore = defineStore('app', () => {
  // 状态
  const state = ref<AppState>({
    theme: 'dark',
    layout: 'vertical',
    sidebarCollapsed: false,
    loading: false,
    pageTitle: '企业项目管理平台',
    breadcrumbs: [],
    notifications: []
  })

  // 主题配置
  const themeConfig = ref<ThemeConfig>({
    primaryColor: '#3b82f6',
    backgroundColor: '#0f172a',
    textColor: '#f8fafc',
    borderRadius: '0.5rem'
  })

  // 布局配置
  const layoutConfig = ref<LayoutConfig>({
    headerHeight: 64,
    sidebarWidth: 240,
    sidebarCollapsedWidth: 64,
    footerHeight: 48,
    contentPadding: '1.5rem'
  })

  // 计算属性
  const isDark = computed(() => state.value.theme === 'dark')
  const isLight = computed(() => state.value.theme === 'light')
  const isSidebarCollapsed = computed(() => state.value.sidebarCollapsed)
  const isLoading = computed(() => state.value.loading)
  const pageTitle = computed(() => state.value.pageTitle)
  const breadcrumbs = computed(() => state.value.breadcrumbs)
  const notifications = computed(() => state.value.notifications)

  // 动作
  const toggleTheme = () => {
    state.value.theme = state.value.theme === 'dark' ? 'light' : 'dark'
    applyTheme()
  }

  const toggleSidebar = () => {
    state.value.sidebarCollapsed = !state.value.sidebarCollapsed
  }

  const setLoading = (loading: boolean) => {
    state.value.loading = loading
  }

  const setPageTitle = (title: string) => {
    state.value.pageTitle = title
    document.title = `${title} - 企业项目管理平台`
  }

  const setBreadcrumbs = (items: Array<{ title: string; path?: string }>) => {
    state.value.breadcrumbs = items
  }

  const addNotification = (notification: {
    id: string
    type: 'success' | 'warning' | 'error' | 'info'
    title: string
    message: string
    duration?: number
  }) => {
    state.value.notifications.push(notification)
    
    // 自动移除通知
    if (notification.duration) {
      setTimeout(() => {
        removeNotification(notification.id)
      }, notification.duration)
    }
  }

  const removeNotification = (id: string) => {
    state.value.notifications = state.value.notifications.filter(n => n.id !== id)
  }

  const clearNotifications = () => {
    state.value.notifications = []
  }

  // 初始化应用
  const initApp = () => {
    // 从本地存储恢复设置
    const savedTheme = localStorage.getItem('app-theme')
    if (savedTheme) {
      state.value.theme = savedTheme as 'dark' | 'light'
    }

    const savedSidebarState = localStorage.getItem('sidebar-collapsed')
    if (savedSidebarState) {
      state.value.sidebarCollapsed = JSON.parse(savedSidebarState)
    }

    // 应用主题
    applyTheme()
    
    // 设置默认页面标题
    setPageTitle('仪表盘')
  }

  // 应用主题
  const applyTheme = () => {
    const html = document.documentElement
    
    if (state.value.theme === 'dark') {
      html.classList.add('dark')
      html.classList.remove('light')
    } else {
      html.classList.add('light')
      html.classList.remove('dark')
    }
    
    // 保存到本地存储
    localStorage.setItem('app-theme', state.value.theme)
    localStorage.setItem('sidebar-collapsed', JSON.stringify(state.value.sidebarCollapsed))
  }

  // 重置应用状态
  const resetApp = () => {
    state.value = {
      theme: 'dark',
      layout: 'vertical',
      sidebarCollapsed: false,
      loading: false,
      pageTitle: '企业项目管理平台',
      breadcrumbs: [],
      notifications: []
    }
    
    applyTheme()
  }

  return {
    // 状态
    state,
    themeConfig,
    layoutConfig,
    
    // 计算属性
    isDark,
    isLight,
    isSidebarCollapsed,
    isLoading,
    pageTitle,
    breadcrumbs,
    notifications,
    
    // 动作
    toggleTheme,
    toggleSidebar,
    setLoading,
    setPageTitle,
    setBreadcrumbs,
    addNotification,
    removeNotification,
    clearNotifications,
    initApp,
    applyTheme,
    resetApp
  }
})