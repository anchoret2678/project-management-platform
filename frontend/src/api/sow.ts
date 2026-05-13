import { request } from './index'
import type { SOW, SOWCreateRequest, SOWUpdateRequest, PaginationResponse, ApiResponse } from '@/types'

// SOW相关API
export const sowApi = {
  // 获取SOW列表
  getSOWs(params?: {
    page?: number
    size?: number
    project_id?: number
    status?: string
    keyword?: string
  }): Promise<ApiResponse<PaginationResponse<SOW>>> {
    return request.get('/v1/sows', params)
  },
  
  // 获取SOW详情
  getSOW(id: number): Promise<ApiResponse<SOW>> {
    return request.get(`/v1/sows/${id}`)
  },
  
  // 创建SOW
  createSOW(data: SOWCreateRequest): Promise<ApiResponse<SOW>> {
    return request.post('/v1/sows', data)
  },
  
  // 更新SOW
  updateSOW(id: number, data: SOWUpdateRequest): Promise<ApiResponse<SOW>> {
    return request.put(`/v1/sows/${id}`, data)
  },
  
  // 删除SOW
  deleteSOW(id: number): Promise<ApiResponse<void>> {
    return request.delete(`/v1/sows/${id}`)
  },
  
  // 上传SOW文件
  uploadSOWFile(project_id: number, formData: FormData): Promise<ApiResponse<SOW>> {
    return request.upload(`/v1/sows/upload`, formData)
  },
  
  // 下载SOW文件
  downloadSOWFile(sow_id: number): Promise<Blob> {
    return request.download(`/v1/sows/${sow_id}/download`)
  },
  
  // 获取SOW统计
  getSOWStats(): Promise<ApiResponse<any>> {
    return request.get('/v1/sows/stats')
  }
}