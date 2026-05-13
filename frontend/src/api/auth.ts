import { request } from './index'
import service from './index'
import type { LoginForm, RegisterForm, User, PasswordChange, ApiResponse } from '@/types'

// 认证相关API
export const authApi = {
  // 用户登录
  login(data: LoginForm): Promise<ApiResponse<{ access_token: string; user: User }>> {
    // 使用 URLSearchParams 发送 application/x-www-form-urlencoded 格式
    // 后端使用 OAuth2PasswordRequestForm，需要这种格式
    const params = new URLSearchParams()
    params.append('username', data.username)
    params.append('password', data.password)
    return service.post('/v1/auth/login', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
  },
  
  // 用户注册（仅管理员）
  register(data: RegisterForm): Promise<ApiResponse<User>> {
    return request.post('/v1/auth/register', data)
  },
  
  // 获取当前用户信息
  getCurrentUser(): Promise<ApiResponse<User>> {
    return request.get('/v1/auth/me')
  },
  
  // 更新用户信息
  updateUser(userId: number, data: Partial<User>): Promise<ApiResponse<User>> {
    return request.put(`/v1/auth/me`, data)
  },
  
  // 修改密码
  changePassword(data: PasswordChange): Promise<ApiResponse<void>> {
    return request.post('/v1/auth/change-password', data)
  },
  
  // 刷新令牌
  refreshToken(): Promise<ApiResponse<{ access_token: string }>> {
    return request.post('/v1/auth/refresh-token')
  },
  
  // 获取用户统计
  getUserStats(): Promise<ApiResponse<any>> {
    return request.get('/v1/auth/users/stats')
  },
  
  // 初始化管理员（仅第一次部署）
  initAdmin(): Promise<ApiResponse<any>> {
    return request.post('/v1/auth/init-admin')
  }
}