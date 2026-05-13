import { request } from './index'
import type { Project, ProjectCreateRequest, ProjectUpdateRequest, PaginationResponse, ApiResponse } from '@/types'

// 项目相关API
export const projectApi = {
  // 获取项目列表
  getProjects(params?: {
    page?: number
    size?: number
    keyword?: string
    status?: string
    department?: string
  }): Promise<ApiResponse<PaginationResponse<Project>>> {
    return request.get('/v1/projects', params)
  },
  
  // 获取项目详情
  getProject(id: number): Promise<ApiResponse<Project>> {
    return request.get(`/v1/projects/${id}`)
  },
  
  // 创建项目
  createProject(data: ProjectCreateRequest): Promise<ApiResponse<Project>> {
    return request.post('/v1/projects', data)
  },
  
  // 更新项目
  updateProject(id: number, data: ProjectUpdateRequest): Promise<ApiResponse<Project>> {
    return request.put(`/v1/projects/${id}`, data)
  },
  
  // 删除项目
  deleteProject(id: number): Promise<ApiResponse<void>> {
    return request.delete(`/v1/projects/${id}`)
  },
  
  // 导出项目数据
  exportProjects(format: 'excel' | 'csv' = 'excel'): Promise<Blob> {
    return request.download(`/v1/projects/export/${format}`)
  },
  
  // 获取项目统计
  getProjectStats(): Promise<ApiResponse<any>> {
    return request.get('/v1/projects/stats')
  }
}