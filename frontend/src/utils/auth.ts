import Cookies from 'js-cookie'

// Token键名
const TOKEN_KEY = 'pmp_token'
const USER_KEY = 'pmp_user'
const PERMISSIONS_KEY = 'pmp_permissions'
const ROLES_KEY = 'pmp_roles'

// 获取Token
export function getToken(): string {
  return Cookies.get(TOKEN_KEY) || localStorage.getItem(TOKEN_KEY) || ''
}

// 设置Token
export function setToken(token: string, remember = false): void {
  if (remember) {
    // 记住登录状态，保存7天
    Cookies.set(TOKEN_KEY, token, { expires: 7 })
  } else {
    // 会话级别存储
    Cookies.set(TOKEN_KEY, token)
  }
  localStorage.setItem(TOKEN_KEY, token)
}

// 移除Token
export function removeToken(): void {
  Cookies.remove(TOKEN_KEY)
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(USER_KEY)
  localStorage.removeItem(PERMISSIONS_KEY)
  localStorage.removeItem(ROLES_KEY)
}

// 获取用户信息
export function getUser(): any {
  const userStr = localStorage.getItem(USER_KEY)
  return userStr ? JSON.parse(userStr) : null
}

// 设置用户信息
export function setUser(user: any): void {
  localStorage.setItem(USER_KEY, JSON.stringify(user))
}

// 移除用户信息
export function removeUser(): void {
  localStorage.removeItem(USER_KEY)
}

// 获取权限
export function getPermissions(): string[] {
  const permissionsStr = localStorage.getItem(PERMISSIONS_KEY)
  return permissionsStr ? JSON.parse(permissionsStr) : []
}

// 设置权限
export function setPermissions(permissions: string[]): void {
  localStorage.setItem(PERMISSIONS_KEY, JSON.stringify(permissions))
}

// 获取角色
export function getRoles(): string[] {
  const rolesStr = localStorage.getItem(ROLES_KEY)
  return rolesStr ? JSON.parse(rolesStr) : []
}

// 设置角色
export function setRoles(roles: string[]): void {
  localStorage.setItem(ROLES_KEY, JSON.stringify(roles))
}

// 检查是否已登录
export function isLoggedIn(): boolean {
  return !!getToken()
}

// 检查是否是管理员
export function isAdmin(): boolean {
  const roles = getRoles()
  return roles.includes('admin')
}

// 检查是否是普通用户
export function isUser(): boolean {
  const roles = getRoles()
  return roles.includes('user')
}

// 检查权限
export function hasPermission(permission: string): boolean {
  const permissions = getPermissions()
  const roles = getRoles()
  
  // 管理员拥有所有权限
  if (roles.includes('admin')) {
    return true
  }
  
  // 检查具体权限
  return permissions.includes(permission) || permissions.includes('*')
}

// 检查角色
export function hasRole(role: string): boolean {
  const roles = getRoles()
  return roles.includes(role)
}

// 清除所有认证信息
export function clearAuth(): void {
  removeToken()
  removeUser()
  localStorage.removeItem(PERMISSIONS_KEY)
  localStorage.removeItem(ROLES_KEY)
}

// 保存认证信息
export function saveAuth(data: {
  token: string
  user: any
  permissions?: string[]
  roles?: string[]
  remember?: boolean
}): void {
  const { token, user, permissions = [], roles = [], remember = false } = data
  
  setToken(token, remember)
  setUser(user)
  setPermissions(permissions)
  setRoles(roles)
}

// 从本地存储恢复认证信息
export function restoreAuth(): {
  token: string
  user: any
  permissions: string[]
  roles: string[]
} | null {
  const token = getToken()
  
  if (!token) {
    return null
  }
  
  return {
    token,
    user: getUser(),
    permissions: getPermissions(),
    roles: getRoles()
  }
}