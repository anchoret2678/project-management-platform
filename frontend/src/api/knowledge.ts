import { request } from './index'
import type { Knowledge, KnowledgeCreateRequest, KnowledgeUpdateRequest, PaginationResponse, ApiResponse } from '@/types'

// 知识库相关API
export const knowledgeApi = {
  // 获取知识库列表
  getKnowledge(params?: {
    page?: number
    size?: number
    project_id?: number
    category?: string
    keyword?: string
  }): Promise<ApiResponse<PaginationResponse<Knowledge>>> {
    return request.get('/v1/knowledge', params)
  },
  
  // 获取知识库详情
  getKnowledgeItem(id: number): Promise<ApiResponse<Knowledge>> {
    return request.get(`/v1/knowledge/${id}`)
  },
  
  // 创建知识库文档
  createKnowledge(data: KnowledgeCreateRequest): Promise<ApiResponse<Knowledge>> {
    return request.post('/v1/knowledge', data)
  },
  
  // 更新知识库文档
  updateKnowledge(id: number, data: KnowledgeUpdateRequest): Promise<ApiResponse<Knowledge>> {
    return request.put(`/v1/knowledge/${id}`, data)
  },
  
  // 删除知识库文档
  deleteKnowledge(id: number): Promise<ApiResponse<void>> {
    return request.delete(`/v1/knowledge/${id}`)
  },
  
  // 上传知识库文件
  uploadKnowledgeFile(formData: FormData): Promise<ApiResponse<Knowledge>> {
    return request.upload(`/v1/knowledge/upload`, formData)
  },
  
  // 下载知识库文件
  downloadKnowledgeFile(knowledge_id: number): Promise<Blob> {
    return request.download(`/v1/knowledge/${knowledge_id}/download`)
  },
  
  // 获取知识库统计
  getKnowledgeStats(): Promise<ApiResponse<any>> {
    return request.get('/v1/knowledge/stats')
  },
  
  // 获取知识库分类统计
  getCategoryStats(): Promise<ApiResponse<any>> {
    return request.get('/v1/knowledge/category-stats')
  }
}