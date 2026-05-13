import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/store/user'
import { useAppStore } from '@/store/app'
import NProgress from 'nprogress'

// 路由配置
const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: {
      title: '登录',
      requiresAuth: false
    }
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/layouts/MainLayout.vue'),
    redirect: '/dashboard',
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: {
          title: '仪表盘',
          icon: 'DataBoard',
          requiresAuth: true
        }
      },
      {
        path: 'projects',
        name: 'Projects',
        component: () => import('@/views/projects/ProjectList.vue'),
        meta: {
          title: '项目管理',
          icon: 'Document',
          requiresAuth: true
        }
      },
      {
        path: 'projects/create',
        name: 'ProjectCreate',
        component: () => import('@/views/projects/ProjectForm.vue'),
        meta: {
          title: '创建项目',
          requiresAuth: true,
          requiresAdmin: true,
          breadcrumb: true
        }
      },
      {
        path: 'projects/:id/edit',
        name: 'ProjectEdit',
        component: () => import('@/views/projects/ProjectForm.vue'),
        meta: {
          title: '编辑项目',
          requiresAuth: true,
          requiresAdmin: true,
          breadcrumb: true
        }
      },
      {
        path: 'projects/:id',
        name: 'ProjectDetail',
        component: () => import('@/views/projects/ProjectDetail.vue'),
        meta: {
          title: '项目详情',
          requiresAuth: true,
          breadcrumb: true
        }
      },
      {
        path: 'cloud-assets',
        name: 'CloudAssets',
        component: () => import('@/views/cloud-assets/CloudAssetList.vue'),
        meta: {
          title: '云资产管理',
          icon: 'Cloudy',
          requiresAuth: true
        }
      },
      {
        path: 'cloud-assets/create',
        name: 'CloudAssetCreate',
        component: () => import('@/views/cloud-assets/CloudAssetForm.vue'),
        meta: {
          title: '创建云资产',
          requiresAuth: true,
          requiresAdmin: true,
          breadcrumb: true
        }
      },
      {
        path: 'cloud-assets/:id/edit',
        name: 'CloudAssetEdit',
        component: () => import('@/views/cloud-assets/CloudAssetForm.vue'),
        meta: {
          title: '编辑云资产',
          requiresAuth: true,
          requiresAdmin: true,
          breadcrumb: true
        }
      },
      {
        path: 'sows',
        name: 'SOWs',
        component: () => import('@/views/sows/SOWList.vue'),
        meta: {
          title: 'SOW管理',
          icon: 'DocumentCopy',
          requiresAuth: true
        }
      },
      {
        path: 'sows/create',
        name: 'SOWCreate',
        component: () => import('@/views/sows/SOWForm.vue'),
        meta: {
          title: '创建SOW',
          requiresAuth: true,
          requiresAdmin: true,
          breadcrumb: true
        }
      },
      {
        path: 'sows/:id/edit',
        name: 'SOWEdit',
        component: () => import('@/views/sows/SOWForm.vue'),
        meta: {
          title: '编辑SOW',
          requiresAuth: true,
          requiresAdmin: true,
          breadcrumb: true
        }
      },
      {
        path: 'slas',
        name: 'SLAs',
        component: () => import('@/views/slas/SLAList.vue'),
        meta: {
          title: 'SLA管理',
          icon: 'Setting',
          requiresAuth: true
        }
      },
      {
        path: 'slas/create',
        name: 'SLACreate',
        component: () => import('@/views/slas/SLAForm.vue'),
        meta: {
          title: '创建SLA',
          requiresAuth: true,
          requiresAdmin: true,
          breadcrumb: true
        }
      },
      {
        path: 'slas/:id/edit',
        name: 'SLAEdit',
        component: () => import('@/views/slas/SLAForm.vue'),
        meta: {
          title: '编辑SLA',
          requiresAuth: true,
          requiresAdmin: true,
          breadcrumb: true
        }
      },
      {
        path: 'knowledge',
        name: 'Knowledge',
        component: () => import('@/views/knowledge/KnowledgeList.vue'),
        meta: {
          title: '知识库',
          icon: 'Notebook',
          requiresAuth: true
        }
      },
      {
        path: 'knowledge/create',
        name: 'KnowledgeCreate',
        component: () => import('@/views/knowledge/KnowledgeForm.vue'),
        meta: {
          title: '创建文档',
          requiresAuth: true,
          requiresAdmin: true,
          breadcrumb: true
        }
      },
      {
        path: 'knowledge/:id/edit',
        name: 'KnowledgeEdit',
        component: () => import('@/views/knowledge/KnowledgeForm.vue'),
        meta: {
          title: '编辑文档',
          requiresAuth: true,
          requiresAdmin: true,
          breadcrumb: true
        }
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/views/users/UserList.vue'),
        meta: {
          title: '用户管理',
          icon: 'User',
          requiresAuth: true,
          requiresAdmin: true
        }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/users/Profile.vue'),
        meta: {
          title: '个人中心',
          icon: 'UserFilled',
          requiresAuth: true
        }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/Settings.vue'),
        meta: {
          title: '系统设置',
          icon: 'Setting',
          requiresAuth: true,
          requiresAdmin: true
        }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: {
      title: '页面不存在',
      requiresAuth: false
    }
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 路由守卫 - 全局前置守卫
router.beforeEach(async (to, from, next) => {
  // 开始进度条
  NProgress.start()
  
  const userStore = useUserStore()
  const appStore = useAppStore()
  
  // 设置页面标题
  if (to.meta.title) {
    appStore.setPageTitle(to.meta.title as string)
  }
  
  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    // 检查是否已登录
    if (!userStore.isLoggedIn) {
      // 未登录，重定向到登录页
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
      return
    }
    
    // 检查是否需要管理员权限
    if (to.meta.requiresAdmin && !userStore.isAdmin) {
      // 权限不足，重定向到首页
      next({ path: '/dashboard' })
      return
    }
  }
  
  // 如果已登录且访问登录页，重定向到首页
  if (to.path === '/login' && userStore.isLoggedIn) {
    next({ path: '/' })
    return
  }
  
  next()
})

// 路由守卫 - 全局后置守卫
router.afterEach((to) => {
  // 完成进度条
  NProgress.done()
  
  // 设置面包屑导航
  const appStore = useAppStore()
  const breadcrumbs: Array<{ title: string; path?: string }> = []
  
  // 添加首页
  breadcrumbs.push({ title: '首页', path: '/dashboard' })
  
  // 添加当前路由的面包屑
  if (to.meta.breadcrumb && to.meta.title) {
    breadcrumbs.push({ title: to.meta.title as string, path: to.path })
  }
  
  appStore.setBreadcrumbs(breadcrumbs)
})

// 错误处理
router.onError((error) => {
  console.error('路由错误:', error)
  NProgress.done()
})

export default router