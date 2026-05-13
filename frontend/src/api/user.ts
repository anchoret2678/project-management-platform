import { request } from './index'
import type { User, PaginationResponse, ApiResponse } from '@/types'

// 用户相关API
export const userApi = {
  // 获取用户列表
  getUsers(params?: {
    page?: number
    size?: number
    keyword?: string
    role?: string
    is_active?: boolean
  }): Promise<ApiResponse<PaginationResponse<User>>> {
    return request.get('/v1/users', params)
  },
  
  // 获取用户详情
  getUser(id: number): Promise<ApiResponse<User>> {
    return request.get(`/v1/users/${id}`)
  },
  
  // 更新用户信息
  updateUser(id: number, data: Partial<User>): Promise<ApiResponse<User>> {
    return request.put(`/v1/users/${id}`, data)
  },
  
  // 删除用户
  deleteUser(id: number): Promise<ApiResponse<void>> {
    return request.delete(`/v1/users/${id}`)
  },
  
  // 更新用户状态
  updateUserStatus(id: number, is_active: boolean): Promise<ApiResponse<User>> {
    return request.put(`/v1/users/${id}/status`, { is_active })
  },
  
  // 获取用户统计
  getUserStats(): Promise<ApiResponse<any>> {
    return request.get('/v1/users/stats')
  }
}