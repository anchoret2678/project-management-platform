// 用户相关类型
export interface User {
  id: number
  username: string
  email: string
  full_name: string
  role: 'admin' | 'user'
  department?: string
  phone?: string
  avatar?: string
  is_active: boolean
  last_login?: string
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  expires_in: number
  user: User
}

// 项目相关类型
export interface Project {
  id: number
  project_code: string
  project_name: string
  application_name: string
  department: string
  manager: string
  status: 'planning' | 'in_progress' | 'testing' | 'online' | 'maintenance' | 'archived'
  launch_date?: string
  remarks?: string
  created_by: number
  creator_name: string
  created_at: string
  updated_at: string
}

export interface ProjectCreateRequest {
  project_code: string
  project_name: string
  application_name: string
  department: string
  manager: string
  status: string
  launch_date?: string
  remarks?: string
}

export interface ProjectUpdateRequest extends Partial<ProjectCreateRequest> {}

// 云资产相关类型
export interface CloudAsset {
  id: number
  project_id: number
  project_name: string
  project_code: string
  cloud_provider: 'aliyun' | 'huawei' | 'tencent' | 'self_built'
  resource_type: string
  instance_spec?: string
  region: string
  zone?: string
  account_info?: string
  ip_address?: string
  config_json: Record<string, any>
  lifecycle: 'creating' | 'running' | 'stopped' | 'deleting' | 'deleted'
  created_by: number
  creator_name: string
  created_at: string
  updated_at: string
}

export interface CloudAssetCreateRequest {
  project_id: number
  cloud_provider: string
  resource_type: string
  instance_spec?: string
  region: string
  zone?: string
  account_info?: string
  ip_address?: string
  config_json?: Record<string, any>
  lifecycle: string
  remarks?: string
}

export interface CloudAssetUpdateRequest extends Partial<CloudAssetCreateRequest> {}

// SOW相关类型
export interface SOW {
  id: number
  project_id: number
  project_name: string
  project_code: string
  document_name: string
  version: string
  file_path: string
  file_name: string
  file_size: number
  file_type: string
  status: 'draft' | 'reviewing' | 'approved' | 'rejected' | 'archived'
  uploaded_by: number
  uploaded_by_name: string
  uploaded_at: string
  remarks?: string
  created_at: string
  updated_at: string
}

export interface SOWCreateRequest {
  project_id: number
  document_name: string
  version: string
  file_path: string
  file_name: string
  file_size: number
  file_type: string
  status: string
  remarks?: string
}

export interface SOWUpdateRequest extends Partial<SOWCreateRequest> {}

// SLA相关类型
export interface SLA {
  id: number
  project_id: number
  project_name: string
  project_code: string
  agreement_name: string
  availability: number
  response_time?: number
  fault_resolution_time?: number
  maintenance_window?: string
  penalty_terms?: string
  status: 'draft' | 'active' | 'expired' | 'terminated'
  effective_date: string
  expiry_date: string
  created_by: number
  creator_name: string
  created_at: string
  updated_at: string
}

export interface SLACreateRequest {
  project_id: number
  agreement_name: string
  availability: number
  response_time?: number
  fault_resolution_time?: number
  maintenance_window?: string
  penalty_terms?: string
  status: string
  effective_date: string
  expiry_date: string
  remarks?: string
}

export interface SLAUpdateRequest extends Partial<SLACreateRequest> {}

// 知识库相关类型
export interface Knowledge {
  id: number
  project_id: number
  project_name: string
  project_code: string
  document_title: string
  description?: string
  category: 'technical' | 'operation' | 'architecture' | 'requirement' | 'meeting' | 'other'
  tags?: string
  file_path?: string
  file_name?: string
  file_size?: number
  file_type?: string
  created_by: number
  created_by_name: string
  created_at: string
  updated_at: string
}

export interface KnowledgeCreateRequest {
  project_id: number
  document_title: string
  description?: string
  category: string
  tags?: string
  file_path?: string
  file_name?: string
  file_size?: number
  file_type?: string
  remarks?: string
}

export interface KnowledgeUpdateRequest extends Partial<KnowledgeCreateRequest> {}

// 通用类型
export interface PaginationParams {
  page?: number
  size?: number
  sort_by?: string
  sort_order?: 'asc' | 'desc'
}

export interface PaginationResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
  total_pages: number
}

export interface FilterParams {
  project_id?: number
  keyword?: string
  status?: string
  start_date?: string
  end_date?: string
}

export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
  timestamp: string
}

export interface ErrorResponse {
  code: number
  message: string
  details?: Record<string, any>
  timestamp: string
}

// 仪表盘统计类型
export interface DashboardStats {
  projects: {
    total: number
    active: number
    online: number
  }
  cloudAssets: {
    total: number
    running: number
    aliyun: number
  }
  sows: {
    total: number
    approved: number
    reviewing: number
  }
  slas: {
    total: number
    active: number
    avgAvailability: number
  }
}

// 活动记录类型
export interface Activity {
  id: string
  type: 'project' | 'sow' | 'cloud' | 'sla' | 'knowledge'
  title: string
  description: string
  time: Date
}

// 文件上传类型
export interface FileUploadResponse {
  file_path: string
  file_name: string
  file_size: number
  file_type: string
  original_name: string
}

// 导出类型
export interface ExportRequest {
  format: 'excel' | 'csv' | 'pdf'
  filters?: FilterParams
  columns?: string[]
}