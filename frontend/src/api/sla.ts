import { request } from './index'
import type { SLA, SLACreateRequest, SLAUpdateRequest, PaginationResponse, ApiResponse } from '@/types'

// SLA相关API
export const slaApi = {
  // 获取SLA列表
  getSLAs(params?: {
    page?: number
    size?: number
    project_id?: number
    status?: string
    keyword?: string
  }): Promise<ApiResponse<PaginationResponse<SLA>>> {
    return request.get('/v1/slas', params)
  },
  
  // 获取SLA详情
  getSLA(id: number): Promise<ApiResponse<SLA>> {
    return request.get(`/v1/slas/${id}`)
  },
  
  // 创建SLA
  createSLA(data: SLACreateRequest): Promise<ApiResponse<SLA>> {
    return request.post('/v1/slas', data)
  },
  
  // 更新SLA
  updateSLA(id: number, data: SLAUpdateRequest): Promise<ApiResponse<SLA>> {
    return request.put(`/v1/slas/${id}`, data)
  },
  
  // 删除SLA
  deleteSLA(id: number): Promise<ApiResponse<void>> {
    return request.delete(`/v1/slas/${id}`)
  },
  
  // 获取SLA统计
  getSLAStats(): Promise<ApiResponse<any>> {
    return request.get('/v1/slas/stats')
  }
}