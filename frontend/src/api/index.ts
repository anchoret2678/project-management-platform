import axios from 'axios'
import { ElMessage } from 'element-plus'
import { getToken, removeToken } from '@/utils/auth'
import type { ApiResponse } from '@/types/api'

// 创建axios实例
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    // 添加token到请求头
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // 添加请求时间戳（防止缓存）
    if (config.method?.toLowerCase() === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now()
      }
    }
    
    return config
  },
  (error) => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response) => {
    const res = response.data
    
    // 如果返回的是文件流，直接返回
    if (response.config.responseType === 'blob') {
      return response
    }
    
    // 检查响应状态码
    if (res.code === 200) {
      return res
    } else {
      // 处理业务错误
      handleBusinessError(res)
      return Promise.reject(res)
    }
  },
  (error) => {
    // 处理HTTP错误
    handleHttpError(error)
    return Promise.reject(error)
  }
)

// 处理业务错误
function handleBusinessError(res: ApiResponse<any>) {
  const { code, message } = res
  
  switch (code) {
    case 401:
      // 未授权，清除token并跳转到登录页
      removeToken()
      window.location.href = '/login'
      ElMessage.error('登录已过期，请重新登录')
      break
      
    case 403:
      ElMessage.error('权限不足，无法访问')
      break
      
    case 404:
      ElMessage.error('请求的资源不存在')
      break
      
    case 500:
      ElMessage.error('服务器内部错误')
      break
      
    default:
      ElMessage.error(message || '请求失败')
  }
}

// 处理HTTP错误
function handleHttpError(error: any) {
  if (error.response) {
    // 服务器返回了错误状态码
    const { status, data } = error.response
    
    switch (status) {
      case 400:
        ElMessage.error(data?.message || '请求参数错误')
        break
        
      case 401:
        removeToken()
        window.location.href = '/login'
        ElMessage.error('登录已过期，请重新登录')
        break
        
      case 403:
        ElMessage.error('权限不足，无法访问')
        break
        
      case 404:
        ElMessage.error('请求的资源不存在')
        break
        
      case 413:
        ElMessage.error('文件大小超过限制')
        break
        
      case 415:
        ElMessage.error('不支持的文件类型')
        break
        
      case 422:
        ElMessage.error(data?.detail?.[0]?.msg || data?.message || '请求参数验证失败')
        break
        
      case 500:
        ElMessage.error('服务器内部错误')
        break
        
      case 502:
        ElMessage.error('网关错误')
        break
        
      case 503:
        ElMessage.error('服务不可用')
        break
        
      case 504:
        ElMessage.error('网关超时')
        break
        
      default:
        ElMessage.error(`请求失败: ${status}`)
    }
  } else if (error.request) {
    // 请求已发出但没有收到响应
    ElMessage.error('网络错误，请检查网络连接')
  } else {
    // 请求配置错误
    ElMessage.error('请求配置错误')
  }
  
  console.error('请求错误详情:', error)
}

// 通用请求方法
export const request = {
  get<T = any>(url: string, params?: any): Promise<ApiResponse<T>> {
    return service.get(url, { params })
  },
  
  post<T = any>(url: string, data?: any): Promise<ApiResponse<T>> {
    return service.post(url, data)
  },
  
  put<T = any>(url: string, data?: any): Promise<ApiResponse<T>> {
    return service.put(url, data)
  },
  
  delete<T = any>(url: string, params?: any): Promise<ApiResponse<T>> {
    return service.delete(url, { params })
  },
  
  patch<T = any>(url: string, data?: any): Promise<ApiResponse<T>> {
    return service.patch(url, data)
  },
  
  // 文件上传
  upload<T = any>(url: string, formData: FormData, onProgress?: (progress: number) => void): Promise<ApiResponse<T>> {
    return service.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          onProgress(progress)
        }
      }
    })
  },
  
  // 文件下载
  download(url: string, params?: any): Promise<Blob> {
    return service.get(url, {
      params,
      responseType: 'blob'
    }).then(response => response.data)
  }
}

export default service

// 导出所有API模块
export * from './auth'
export * from './project'
export * from './cloud-asset'
export * from './sow'
export * from './sla'
export * from './knowledge'
export * from './user'