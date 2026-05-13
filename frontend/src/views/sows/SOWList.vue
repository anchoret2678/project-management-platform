<template>
  <div class="sow-list-container">
    <!-- 页面标题和操作 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">SOW管理</h1>
        <p class="page-subtitle">工作说明书文档管理</p>
      </div>
      <div class="header-right">
        <el-button type="primary" :icon="Plus" @click="handleCreate" v-if="isAdmin">
          上传SOW
        </el-button>
        <el-button :icon="Download" @click="handleExport">
          导出Excel
        </el-button>
        <el-button :icon="Refresh" @click="refreshData">
          刷新
        </el-button>
      </div>
    </div>
    
    <!-- 筛选条件 -->
    <el-card class="filter-card" shadow="never">
      <div class="filter-form">
        <el-form :model="filterForm" inline>
          <el-form-item label="项目">
            <el-select
              v-model="filterForm.project_id"
              placeholder="请选择项目"
              clearable
              filterable
              @change="handleFilter"
            >
              <el-option
                v-for="project in projects"
                :key="project.id"
                :label="project.project_name"
                :value="project.id"
              />
            </el-select>
          </el-form-item>
          
          <el-form-item label="文档名称">
            <el-input
              v-model="filterForm.document_name"
              placeholder="请输入文档名称"
              clearable
              @clear="handleFilter"
              @keyup.enter="handleFilter"
            />
          </el-form-item>
          
          <el-form-item label="版本">
            <el-input
              v-model="filterForm.version"
              placeholder="请输入版本号"
              clearable
              @clear="handleFilter"
              @keyup.enter="handleFilter"
            />
          </el-form-item>
          
          <el-form-item label="状态">
            <el-select
              v-model="filterForm.status"
              placeholder="请选择状态"
              clearable
              @change="handleFilter"
            >
              <el-option
                v-for="status in statusOptions"
                :key="status.value"
                :label="status.label"
                :value="status.value"
              />
            </el-select>
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" :icon="Search" @click="handleFilter">
              搜索
            </el-button>
            <el-button :icon="Refresh" @click="resetFilter">
              重置
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
    
    <!-- SOW列表 -->
    <el-card class="list-card" shadow="never">
      <template #header>
        <div class="list-header">
          <div class="list-title">
            <span>SOW文档列表</span>
            <el-tag type="info" size="small">
              共 {{ pagination.total }} 个文档
            </el-tag>
          </div>
        </div>
      </template>
      
      <!-- 表格 -->
      <el-table
        v-loading="loading"
        :data="sowList"
        style="width: 100%"
        @row-click="handleRowClick"
      >
        <el-table-column prop="project_name" label="项目" width="150">
          <template #default="{ row }">
            <div class="project-cell">
              <el-tag type="info" size="small">{{ row.project_code }}</el-tag>
              <span class="project-name">{{ row.project_name }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="document_name" label="文档名称" width="200">
          <template #default="{ row }">
            <div class="document-cell">
              <el-icon class="document-icon"><Document /></el-icon>
              <span class="document-name">{{ row.document_name }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="version" label="版本" width="100">
          <template #default="{ row }">
            <el-tag type="info" size="small">v{{ row.version }}</el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="file_size" label="文件大小" width="100">
          <template #default="{ row }">
            {{ formatFileSize(row.file_size) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="file_type" label="文件类型" width="120">
          <template #default="{ row }">
            <el-tag :type="getFileTypeTag(row.file_type)" size="small">
              {{ getFileTypeLabel(row.file_type) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="uploaded_by_name" label="上传人" width="120">
          <template #default="{ row }">
            {{ row.uploaded_by_name }}
          </template>
        </el-table-column>
        
        <el-table-column prop="uploaded_at" label="上传时间" width="160">
          <template #default="{ row }">
            {{ formatDateTime(row.uploaded_at) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button
                type="primary"
                link
                :icon="View"
                @click.stop="handleView(row)"
              >
                查看
              </el-button>
              <el-button
                type="primary"
                link
                :icon="Download"
                @click.stop="handleDownload(row)"
              >
                下载
              </el-button>
              <el-button
                v-if="isAdmin"
                type="primary"
                link
                :icon="Edit"
                @click.stop="handleEdit(row)"
              >
                编辑
              </el-button>
              <el-button
                v-if="isAdmin"
                type="danger"
                link
                :icon="Delete"
                @click.stop="handleDelete(row)"
              >
                删除
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container" v-if="sowList.length > 0">
        <el-pagination
          v-model:current-page="pagination.current"
          v-model:page-size="pagination.size"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Download,
  Refresh,
  Search,
  View,
  Edit,
  Delete,
  Document
} from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { useAppStore } from '@/store/app'
import dayjs from 'dayjs'
import type { SOW } from '@/types'

const router = useRouter()
const userStore = useUserStore()
const appStore = useAppStore()

// 加载状态
const loading = ref(false)

// 筛选表单
const filterForm = reactive({
  project_id: '',
  document_name: '',
  version: '',
  status: ''
})

// 项目列表
const projects = ref([
  { id: 1, project_code: 'P2024001', project_name: 'OA系统升级' },
  { id: 2, project_code: 'P2024002', project_name: '客户关系管理系统' },
  { id: 3, project_code: 'P2024003', project_name: '数据中台建设' },
  { id: 4, project_code: 'P2024004', project_name: '移动办公平台' },
  { id: 5, project_code: 'P2024005', project_name: '智能客服系统' }
])

// 状态选项
const statusOptions = ref([
  { value: 'draft', label: '草稿' },
  { value: 'reviewing', label: '审核中' },
  { value: 'approved', label: '已批准' },
  { value: 'rejected', label: '已拒绝' },
  { value: 'archived', label: '已归档' }
])

// SOW列表数据
const sowList = ref<SOW[]>([
  {
    id: 1,
    project_id: 1,
    project_name: 'OA系统升级',
    project_code: 'P2024001',
    document_name: 'OA系统升级SOW',
    version: '1.0',
    file_path: '/uploads/sows/oa-upgrade-sow-v1.0.pdf',
    file_name: 'oa-upgrade-sow-v1.0.pdf',
    file_size: 2048576,
    file_type: 'pdf',
    status: 'approved',
    uploaded_by: 1,
    uploaded_by_name: '张三',
    uploaded_at: '2024-01-10T14:30:00',
    remarks: 'OA系统升级工作说明书',
    created_at: '2024-01-10T14:30:00',
    updated_at: '2024-01-10T14:30:00'
  },
  {
    id: 2,
    project_id: 1,
    project_name: 'OA系统升级',
    project_code: 'P2024001',
    document_name: 'OA系统升级SOW',
    version: '2.0',
    file_path: '/uploads/sows/oa-upgrade-sow-v2.0.pdf',
    file_name: 'oa-upgrade-sow-v2.0.pdf',
    file_size: 2568192,
    file_type: 'pdf',
    status: 'reviewing',
    uploaded_by: 1,
    uploaded_by_name: '张三',
    uploaded_at: '2024-02-15T10:20:00',
    remarks: 'OA系统升级工作说明书v2.0',
    created_at: '2024-02-15T10:20:00',
    updated_at: '2024-02-15T10:20:00'
  },
  {
    id: 3,
    project_id: 2,
    project_name: '客户关系管理系统',
    project_code: 'P2024002',
    document_name: 'CRM系统SOW',
    version: '1.0',
    file_path: '/uploads/sows/crm-sow-v1.0.docx',
    file_name: 'crm-sow-v1.0.docx',
    file_size: 1048576,
    file_type: 'docx',
    status: 'approved',
    uploaded_by: 1,
    uploaded_by_name: '张三',
    uploaded_at: '2024-01-20T16:45:00',
    remarks: '客户关系管理系统工作说明书',
    created_at: '2024-01-20T16:45:00',
    updated_at: '2024-01-20T16:45:00'
  },
  {
    id: 4,
    project_id: 3,
    project_name: '数据中台建设',
    project_code: 'P2024003',
    document_name: '数据中台SOW',
    version: '1.0',
    file_path: '/uploads/sows/data-platform-sow-v1.0.pdf',
    file_name: 'data-platform-sow-v1.0.pdf',
    file_size: 3145728,
    file_type: 'pdf',
    status: 'draft',
    uploaded_by: 1,
    uploaded_by_name: '张三',
    uploaded_at: '2024-02-28T11:30:00',
    remarks: '数据中台建设工作说明书',
    created_at: '2024-02-28T11:30:00',
    updated_at: '2024-02-28T11:30:00'
  },
  {
    id: 5,
    project_id: 4,
    project_name: '移动办公平台',
    project_code: 'P2024004',
    document_name: '移动办公平台SOW',
    version: '1.0',
    file_path: '/uploads/sows/mobile-office-sow-v1.0.pdf',
    file_name: 'mobile-office-sow-v1.0.pdf',
    file_size: 2097152,
    file_type: 'pdf',
    status: 'archived',
    uploaded_by: 1,
    uploaded_by_name: '张三',
    uploaded_at: '2024-03-05T09:15:00',
    remarks: '移动办公平台工作说明书',
    created_at: '2024-03-05T09:15:00',
    updated_at: '2024-03-05T09:15:00'
  }
])

// 分页配置
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
})

// 计算属性
const isAdmin = computed(() => userStore.isAdmin)

// 获取文件类型标签
const getFileTypeTag = (fileType: string) => {
  const typeMap: Record<string, string> = {
    pdf: 'danger',
    docx: 'primary',
    doc: 'primary',
    xlsx: 'success',
    xls: 'success',
    pptx: 'warning',
    ppt: 'warning',
    txt: 'info'
  }
  return typeMap[fileType] || 'info'
}

// 获取文件类型标签
const getFileTypeLabel = (fileType: string) => {
  const typeMap: Record<string, string> = {
    pdf: 'PDF',
    docx: 'Word',
    doc: 'Word',
    xlsx: 'Excel',
    xls: 'Excel',
    pptx: 'PPT',
    ppt: 'PPT',
    txt: '文本'
  }
  return typeMap[fileType] || fileType.toUpperCase()
}

// 获取状态标签
const getStatusLabel = (status: string) => {
  const option = statusOptions.value.find(opt => opt.value === status)
  return option ? option.label : status
}

// 获取状态类型
const getStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    draft: 'info',
    reviewing: 'warning',
    approved: 'success',
    rejected: 'danger',
    archived: 'info'
  }
  return typeMap[status] || 'info'
}

// 格式化文件大小
const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 格式化日期时间
const formatDateTime = (datetime: string) => {
  return dayjs(datetime).format('YYYY-MM-DD HH:mm')
}

// 处理创建SOW
const handleCreate = () => {
  router.push('/sows/create')
}

// 处理查看SOW
const handleView = (sow: SOW) => {
  // 可以跳转到预览页，这里暂时用编辑页代替
  router.push(`/sows/${sow.id}/edit`)
}

// 处理下载SOW
const handleDownload = (sow: SOW) => {
  ElMessage.info(`开始下载: ${sow.document_name}`)
  // 实际项目中这里会调用下载API
}

// 处理编辑SOW
const handleEdit = (sow: SOW) => {
  router.push(`/sows/${sow.id}/edit`)
}

// 处理删除SOW
const handleDelete = async (sow: SOW) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除SOW文档 "${sow.document_name}" 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 模拟删除操作
    const index = sowList.value.findIndex(s => s.id === sow.id)
    if (index !== -1) {
      sowList.value.splice(index, 1)
      ElMessage.success('SOW文档删除成功')
    }
  } catch (error) {
    // 用户取消删除
  }
}

// 处理行点击
const handleRowClick = (row: SOW) => {
  handleView(row)
}

// 处理筛选
const handleFilter = () => {
  pagination.current = 1
  loadData()
}

// 重置筛选
const resetFilter = () => {
  Object.assign(filterForm, {
    project_id: '',
    document_name: '',
    version: '',
    status: ''
  })
  handleFilter()
}

// 处理导出
const handleExport = () => {
  ElMessage.info('导出功能开发中...')
}

// 处理分页大小变化
const handleSizeChange = (size: number) => {
  pagination.size = size
  pagination.current = 1
  loadData()
}

// 处理当前页变化
const handleCurrentChange = (page: number) => {
  pagination.current = page
  loadData()
}

// 刷新数据
const refreshData = () => {
  loadData()
  ElMessage.success('数据已刷新')
}

// 加载数据
const loadData = async () => {
  try {
    loading.value = true
    
    // 模拟API调用延迟
    await new Promise(resolve => setTimeout(resolve, 800))
    
    // 模拟筛选逻辑
    let filteredData = [...sowList.value]
    
    if (filterForm.project_id) {
      filteredData = filteredData.filter(s => s.project_id === Number(filterForm.project_id))
    }
    
    if (filterForm.document_name) {
      filteredData = filteredData.filter(s => 
        s.document_name.toLowerCase().includes(filterForm.document_name.toLowerCase())
      )
    }
    
    if (filterForm.version) {
      filteredData = filteredData.filter(s => 
        s.version.toLowerCase().includes(filterForm.version.toLowerCase())
      )
    }
    
    if (filterForm.status) {
      filteredData = filteredData.filter(s => s.status === filterForm.status)
    }
    
    // 模拟分页
    const start = (pagination.current - 1) * pagination.size
    const end = start + pagination.size
    const paginatedData = filteredData.slice(start, end)
    
    // 更新数据
    sowList.value = paginatedData
    pagination.total = filteredData.length
    
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// 生命周期钩子
onMounted(() => {
  // 加载数据
  loadData()
  
  // 设置页面标题
  appStore.setPageTitle('SOW管理')
})
</script>

<style lang="scss" scoped>
.sow-list-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

// 页面标题
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
  
  .header-left {
    .page-title {
      font-size: 24px;
      font-weight: 600;
      color: var(--text-primary);
      margin: 0 0 8px 0;
    }
    
    .page-subtitle {
      font-size: 14px;
      color: var(--text-tertiary);
      margin: 0;
    }
  }
  
  .header-right {
    display: flex;
    gap: 12px;
  }
}

// 筛选卡片
.filter-card {
  :deep(.el-card__body) {
    padding: 20px;
  }
  
  .filter-form {
    :deep(.el-form-item) {
      margin-bottom: 0;
      margin-right: 16px;
      
      &:last-child {
        margin-right: 0;
      }
    }
    
    @media (max-width: 768px) {
      :deep(.el-form) {
        display: flex;
        flex-direction: column;
        gap: 12px;
        
        .el-form-item {
          margin-right: 0;
          width: 100%;
        }
      }
    }
  }
}

// 列表卡片
.list-card {
  :deep(.el-card__header) {
    padding: 16px 20px;
    border-bottom: 1px solid var(--border-color);
    background: var(--bg-secondary);
  }
  
  .list-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .list-title {
      display: flex;
      align-items: center;
      gap: 12px;
      
      span {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 16px;
      }
    }
  }
}

// 表格样式
:deep(.el-table) {
  .project-cell {
    display: flex;
    flex-direction: column;
    gap: 4px;
    
    .project-name {
      font-size: 12px;
      color: var(--text-secondary);
    }
  }
  
  .document-cell {
    display: flex;
    align-items: center;
    gap: 8px;
    
    .document-icon {
      color: var(--primary-color);
    }
    
    .document-name {
      font-weight: 500;
    }
  }
  
  .action-buttons {
    display: flex;
    gap: 8px;
    
    .el-button {
      padding: 4px 0;
    }
  }
}

// 分页容器
.pagination-container {
  display: flex;
  justify-content: center;
  padding: 20px 0 0 0;
}

// 响应式调整
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    
    .header-right {
      width: 100%;
      justify-content: flex-start;
    }
  }
}
</style>