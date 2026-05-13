import { request } from './index'
import type { CloudAsset, CloudAssetCreateRequest, CloudAssetUpdateRequest, PaginationResponse, ApiResponse } from '@/types'

// 云资产相关API
export const cloudAssetApi = {
  // 获取云资产列表
  getCloudAssets(params?: {
    page?: number
    size?: number
    project_id?: number
    cloud_provider?: string
    resource_type?: string
    region?: string
    lifecycle?: string
    keyword?: string
  }): Promise<ApiResponse<PaginationResponse<CloudAsset>>> {
    return request.get('/v1/cloud-assets', params)
  },
  
  // 获取云资产详情
  getCloudAsset(id: number): Promise<ApiResponse<CloudAsset>> {
    return request.get(`/v1/cloud-assets/${id}`)
  },
  
  // 创建云资产
  createCloudAsset(data: CloudAssetCreateRequest): Promise<ApiResponse<CloudAsset>> {
    return request.post('/v1/cloud-assets', data)
  },
  
  // 更新云资产
  updateCloudAsset(id: number, data: CloudAssetUpdateRequest): Promise<ApiResponse<CloudAsset>> {
    return request.put(`/v1/cloud-assets/${id}`, data)
  },
  
  // 删除云资产
  deleteCloudAsset(id: number): Promise<ApiResponse<void>> {
    return request.delete(`/v1/cloud-assets/${id}`)
  },
  
  // 获取项目的所有云资产
  getAssetsByProject(project_id: number): Promise<ApiResponse<{ project_id: number; total: number; items: CloudAsset[] }>> {
    return request.get(`/v1/cloud-assets/project/${project_id}`)
  },
  
  // 获取云资产统计
  getCloudAssetStats(): Promise<ApiResponse<any>> {
    return request.get('/v1/cloud-assets/stats/summary')
  },
  
  // 导出云资产数据
  exportCloudAssets(): Promise<Blob> {
    return request.download('/v1/cloud-assets/export/excel')
  },
  
  // 更新云资产生命周期
  updateLifecycle(id: number, lifecycle: string): Promise<ApiResponse<CloudAsset>> {
    return request.put(`/v1/cloud-assets/${id}/lifecycle`, { lifecycle })
  },
  
  // 搜索云资产
  searchCloudAssets(keyword: string, limit?: number): Promise<ApiResponse<{ suggestions: any[] }>> {
    return request.get('/v1/cloud-assets/search/suggestions', { keyword, limit })
  }
}