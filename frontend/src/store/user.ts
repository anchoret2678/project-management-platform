import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { User, LoginForm, RegisterForm } from '@/types/user'
import { authApi } from '@/api/auth'
import { setToken, removeToken, getToken } from '@/utils/auth'

// 用户状态存储
export const useUserStore = defineStore('user', () => {
  const router = useRouter()

  // 状态
  const user = ref<User | null>(null)
  const token = ref<string>('')
  const permissions = ref<string[]>([])
  const roles = ref<string[]>([])

  // 计算属性
  const isLoggedIn = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => roles.value.includes('admin'))
  const isUser = computed(() => roles.value.includes('user'))
  const userInfo = computed(() => user.value)
  const userPermissions = computed(() => permissions.value)
  const userRoles = computed(() => roles.value)

  // 动作 - 用户登录
  const login = async (form: LoginForm) => {
    try {
      const response = await authApi.login(form)
      
      if (response.code === 200 && response.data) {
        const { access_token, user: userData } = response.data
        
        // 保存用户信息和token
        user.value = userData
        token.value = access_token
        roles.value = [userData.role]
        
        // 根据角色设置权限
        if (userData.role === 'admin') {
          permissions.value = ['*'] // 管理员拥有所有权限
        } else {
          permissions.value = ['read'] // 普通用户只有读权限
        }
        
        // 保存token到本地存储
        setToken(access_token)
        
        // 显示登录成功消息
        ElMessage.success('登录成功')
        
        // 跳转到首页
        router.push('/dashboard')
        
        return true
      } else {
        ElMessage.error(response.message || '登录失败')
        return false
      }
    } catch (error: any) {
      console.error('登录错误:', error)
      ElMessage.error(error.response?.data?.message || '登录失败，请检查网络连接')
      return false
    }
  }

  // 动作 - 用户注册（仅管理员）
  const register = async (form: RegisterForm) => {
    try {
      const response = await authApi.register(form)
      
      if (response.code === 200) {
        ElMessage.success('用户注册成功')
        return true
      } else {
        ElMessage.error(response.message || '注册失败')
        return false
      }
    } catch (error: any) {
      console.error('注册错误:', error)
      ElMessage.error(error.response?.data?.message || '注册失败')
      return false
    }
  }

  // 动作 - 用户注销
  const logout = async () => {
    try {
      // 调用注销API（如果有）
      // await authApi.logout()
      
      // 清除本地存储
      removeToken()
      
      // 重置状态
      user.value = null
      token.value = ''
      permissions.value = []
      roles.value = []
      
      // 显示注销消息
      ElMessage.success('已安全退出')
      
      // 跳转到登录页
      router.push('/login')
    } catch (error) {
      console.error('注销错误:', error)
      // 即使API调用失败，也清除本地状态
      removeToken()
      user.value = null
      token.value = ''
      permissions.value = []
      roles.value = []
      router.push('/login')
    }
  }

  // 动作 - 获取当前用户信息
  const fetchUserInfo = async () => {
    try {
      const response = await authApi.getCurrentUser()
      
      if (response.code === 200 && response.data) {
        user.value = response.data
        roles.value = [response.data.role]
        
        // 根据角色设置权限
        if (response.data.role === 'admin') {
          permissions.value = ['*']
        } else {
          permissions.value = ['read']
        }
        
        return true
      } else {
        // 如果获取用户信息失败，清除登录状态
        logout()
        return false
      }
    } catch (error) {
      console.error('获取用户信息错误:', error)
      // 如果获取失败，清除登录状态
      logout()
      return false
    }
  }

  // 动作 - 恢复登录状态
  const restoreLogin = async () => {
    const savedToken = getToken()
    
    if (savedToken) {
      token.value = savedToken
      
      // 尝试获取用户信息
      try {
        await fetchUserInfo()
        return true
      } catch (error) {
        console.error('恢复登录状态失败:', error)
        // 如果获取用户信息失败，清除token
        removeToken()
        token.value = ''
        return false
      }
    }
    
    return false
  }

  // 动作 - 更新用户信息
  const updateUserInfo = async (userData: Partial<User>) => {
    try {
      const response = await authApi.updateUser(user.value?.id || 0, userData)
      
      if (response.code === 200 && response.data) {
        user.value = { ...user.value, ...response.data } as User
        ElMessage.success('用户信息更新成功')
        return true
      } else {
        ElMessage.error(response.message || '更新失败')
        return false
      }
    } catch (error: any) {
      console.error('更新用户信息错误:', error)
      ElMessage.error(error.response?.data?.message || '更新失败')
      return false
    }
  }

  // 动作 - 修改密码
  const changePassword = async (oldPassword: string, newPassword: string) => {
    try {
      const response = await authApi.changePassword({
        current_password: oldPassword,
        new_password: newPassword
      })
      
      if (response.code === 200) {
        ElMessage.success('密码修改成功')
        return true
      } else {
        ElMessage.error(response.message || '密码修改失败')
        return false
      }
    } catch (error: any) {
      console.error('修改密码错误:', error)
      ElMessage.error(error.response?.data?.message || '密码修改失败')
      return false
    }
  }

  // 动作 - 检查权限
  const hasPermission = (permission: string): boolean => {
    if (!permissions.value.length) return false
    
    // 管理员拥有所有权限
    if (isAdmin.value) return true
    
    // 检查具体权限
    return permissions.value.includes(permission) || permissions.value.includes('*')
  }

  // 动作 - 检查角色
  const hasRole = (role: string): boolean => {
    return roles.value.includes(role)
  }

  // 动作 - 重置用户状态
  const resetUser = () => {
    user.value = null
    token.value = ''
    permissions.value = []
    roles.value = []
    removeToken()
  }

  return {
    // 状态
    user,
    token,
    permissions,
    roles,
    
    // 计算属性
    isLoggedIn,
    isAdmin,
    isUser,
    userInfo,
    userPermissions,
    userRoles,
    
    // 动作
    login,
    register,
    logout,
    fetchUserInfo,
    restoreLogin,
    updateUserInfo,
    changePassword,
    hasPermission,
    hasRole,
    resetUser
  }
})