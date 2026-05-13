<template>
  <div class="project-list-container">
    <!-- 页面标题和操作 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">项目管理</h1>
        <p class="page-subtitle">统一管理项目全生命周期信息</p>
      </div>
      <div class="header-right">
        <el-button type="primary" :icon="Plus" @click="handleCreate" v-if="isAdmin">
          创建项目
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
          <el-form-item label="项目编号">
            <el-input
              v-model="filterForm.project_code"
              placeholder="请输入项目编号"
              clearable
              @clear="handleFilter"
              @keyup.enter="handleFilter"
            />
          </el-form-item>
          
          <el-form-item label="项目名称">
            <el-input
              v-model="filterForm.project_name"
              placeholder="请输入项目名称"
              clearable
              @clear="handleFilter"
              @keyup.enter="handleFilter"
            />
          </el-form-item>
          
          <el-form-item label="所属部门">
            <el-select
              v-model="filterForm.department"
              placeholder="请选择部门"
              clearable
              filterable
              @change="handleFilter"
            >
              <el-option
                v-for="dept in departments"
                :key="dept"
                :label="dept"
                :value="dept"
              />
            </el-select>
          </el-form-item>
          
          <el-form-item label="项目状态">
            <el-select
              v-model="filterForm.status"
              placeholder="请选择状态"
              clearable
              @change="handleFilter"
            >
              <el-option
                v-for="status in projectStatusOptions"
                :key="status.value"
                :label="status.label"
                :value="status.value"
              />
            </el-select>
          </el-form-item>
          
          <el-form-item label="负责人">
            <el-select
              v-model="filterForm.manager_id"
              placeholder="请选择负责人"
              clearable
              filterable
              @change="handleFilter"
            >
              <el-option
                v-for="user in users"
                :key="user.id"
                :label="user.full_name"
                :value="user.id"
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
    
    <!-- 项目列表 -->
    <el-card class="list-card" shadow="never">
      <template #header>
        <div class="list-header">
          <div class="list-title">
            <span>项目列表</span>
            <el-tag type="info" size="small">
              共 {{ pagination.total }} 个项目
            </el-tag>
          </div>
          <div class="list-actions">
            <el-button-group>
              <el-button :type="viewMode === 'table' ? 'primary' : 'default'" @click="viewMode = 'table'">
                <el-icon><Grid /></el-icon>
              </el-button>
              <el-button :type="viewMode === 'card' ? 'primary' : 'default'" @click="viewMode = 'card'">
                <el-icon><Menu /></el-icon>
              </el-button>
            </el-button-group>
          </div>
        </div>
      </template>
      
      <!-- 表格视图 -->
      <div v-if="viewMode === 'table'">
        <el-table
          v-loading="loading"
          :data="projectList"
          :row-class-name="tableRowClassName"
          @row-click="handleRowClick"
          style="width: 100%"
        >
          <el-table-column prop="project_code" label="项目编号" width="120" fixed>
            <template #default="{ row }">
              <el-tag type="info" size="small">{{ row.project_code }}</el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="project_name" label="项目名称" min-width="180">
            <template #default="{ row }">
              <div class="project-name-cell">
                <span class="project-name">{{ row.project_name }}</span>
                <span class="application-name">{{ row.application_name }}</span>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="department" label="所属部门" width="120">
            <template #default="{ row }">
              <el-tag size="small">{{ row.department }}</el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="manager_name" label="负责人" width="120">
            <template #default="{ row }">
              <div class="manager-cell">
                <el-avatar :size="24" :src="row.manager_avatar">
                  {{ row.manager_name?.charAt(0) || 'U' }}
                </el-avatar>
                <span class="manager-name">{{ row.manager_name }}</span>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)" size="small">
                {{ getStatusLabel(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="launch_date" label="上线时间" width="120">
            <template #default="{ row }">
              <span v-if="row.launch_date">{{ formatDate(row.launch_date) }}</span>
              <span v-else class="text-muted">未设置</span>
            </template>
          </el-table-column>
          
          <el-table-column prop="created_at" label="创建时间" width="160">
            <template #default="{ row }">
              {{ formatDateTime(row.created_at) }}
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="180" fixed="right">
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
      </div>
      
      <!-- 卡片视图 -->
      <div v-else class="card-view">
        <div v-if="loading" class="loading-container">
          <el-icon class="loading-icon"><Loading /></el-icon>
          <span>加载中...</span>
        </div>
        
        <div v-else-if="projectList.length === 0" class="empty-container">
          <el-icon class="empty-icon"><Document /></el-icon>
          <p class="empty-text">暂无项目数据</p>
          <el-button type="primary" :icon="Plus" @click="handleCreate" v-if="isAdmin">
            创建第一个项目
          </el-button>
        </div>
        
        <div v-else class="project-cards">
          <el-row :gutter="20">
            <el-col
              v-for="project in projectList"
              :key="project.id"
              :xs="24"
              :sm="12"
              :md="8"
              :lg="6"
              :xl="6"
            >
              <el-card class="project-card" shadow="hover" @click="handleView(project)">
                <template #header>
                  <div class="card-header">
                    <div class="project-code">
                      <el-tag type="info" size="small">{{ project.project_code }}</el-tag>
                    </div>
                    <div class="project-status">
                      <el-tag :type="getStatusType(project.status)" size="small">
                        {{ getStatusLabel(project.status) }}
                      </el-tag>
                    </div>
                  </div>
                </template>
                
                <div class="card-content">
                  <h3 class="project-name">{{ project.project_name }}</h3>
                  <p class="application-name">{{ project.application_name }}</p>
                  
                  <div class="project-info">
                    <div class="info-item">
                      <el-icon><OfficeBuilding /></el-icon>
                      <span>{{ project.department }}</span>
                    </div>
                    <div class="info-item">
                      <el-icon><User /></el-icon>
                      <span>{{ project.manager_name }}</span>
                    </div>
                    <div class="info-item" v-if="project.launch_date">
                      <el-icon><Calendar /></el-icon>
                      <span>{{ formatDate(project.launch_date) }}</span>
                    </div>
                  </div>
                  
                  <div class="project-stats">
                    <div class="stat-item">
                      <div class="stat-label">云资产</div>
                      <div class="stat-value">{{ project.cloud_assets_count || 0 }}</div>
                    </div>
                    <div class="stat-item">
                      <div class="stat-label">SOW</div>
                      <div class="stat-value">{{ project.sows_count || 0 }}</div>
                    </div>
                    <div class="stat-item">
                      <div class="stat-label">SLA</div>
                      <div class="stat-value">{{ project.slas_count || 0 }}</div>
                    </div>
                    <div class="stat-item">
                      <div class="stat-label">文档</div>
                      <div class="stat-value">{{ project.knowledge_documents_count || 0 }}</div>
                    </div>
                  </div>
                </div>
                
                <template #footer>
                  <div class="card-footer">
                    <span class="create-time">{{ formatDateTime(project.created_at) }}</span>
                    <div class="card-actions">
                      <el-button
                        v-if="isAdmin"
                        type="primary"
                        link
                        :icon="Edit"
                        @click.stop="handleEdit(project)"
                      >
                        编辑
                      </el-button>
                      <el-button
                        v-if="isAdmin"
                        type="danger"
                        link
                        :icon="Delete"
                        @click.stop="handleDelete(project)"
                      >
                        删除
                      </el-button>
                    </div>
                  </div>
                </template>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </div>
      
      <!-- 分页 -->
      <div class="pagination-container" v-if="projectList.length > 0">
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
import { ElMessage, ElMessageBox, type TableColumnCtx } from 'element-plus'
import {
  Plus,
  Download,
  Refresh,
  Search,
  Grid,
  Menu,
  View,
  Edit,
  Delete,
  Loading,
  Document,
  OfficeBuilding,
  User,
  Calendar
} from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { useAppStore } from '@/store/app'
import dayjs from 'dayjs'
import type { Project } from '@/types'

const router = useRouter()
const userStore = useUserStore()
const appStore = useAppStore()

// 视图模式
const viewMode = ref<'table' | 'card'>('table')

// 加载状态
const loading = ref(false)

// 筛选表单
const filterForm = reactive({
  project_code: '',
  project_name: '',
  department: '',
  status: '',
  manager_id: ''
})

// 部门列表
const departments = ref([
  '研发部',
  '产品部',
  '设计部',
  '测试部',
  '运维部',
  '市场部',
  '销售部',
  '客服部',
  '财务部',
  '人事部'
])

// 用户列表
const users = ref([
  { id: 1, full_name: '张三' },
  { id: 2, full_name: '李四' },
  { id: 3, full_name: '王五' },
  { id: 4, full_name: '赵六' }
])

// 项目状态选项
const projectStatusOptions = ref([
  { value: 'planning', label: '规划中' },
  { value: 'in_progress', label: '进行中' },
  { value: 'testing', label: '测试中' },
  { value: 'online', label: '已上线' },
  { value: 'maintenance', label: '维护中' },
  { value: 'archived', label: '已归档' }
])

// 项目列表数据
const projectList = ref<Project[]>([
  {
    id: 1,
    project_code: 'P2024001',
    project_name: 'OA系统升级',
    application_name: 'OA系统',
    department: '研发部',
    manager_id: 1,
    manager_name: '张三',
    status: 'in_progress',
    launch_date: '2024-06-01',
    description: '办公自动化系统升级项目',
    remark: '重要项目，需按时完成',
    created_by: 1,
    created_at: '2024-01-15T10:30:00',
    updated_at: '2024-01-15T10:30:00',
    cloud_assets_count: 5,
    sows_count: 2,
    slas_count: 1,
    knowledge_documents_count: 8
  },
  {
    id: 2,
    project_code: 'P2024002',
    project_name: '客户关系管理系统',
    application_name: 'CRM系统',
    department: '产品部',
    manager_id: 2,
    manager_name: '李四',
    status: 'online',
    launch_date: '2024-03-15',
    description: '客户关系管理平台',
    remark: '已稳定运行',
    created_by: 1,
    created_at: '2024-01-20T14:20:00',
    updated_at: '2024-01-20T14:20:00',
    cloud_assets_count: 8,
    sows_count: 3,
    slas_count: 2,
    knowledge_documents_count: 12
  },
  {
    id: 3,
    project_code: 'P2024003',
    project_name: '数据中台建设',
    application_name: '数据中台',
    department: '研发部',
    manager_id: 3,
    manager_name: '王五',
    status: 'planning',
    launch_date: '',
    description: '企业级数据中台建设项目',
    remark: '技术预研阶段',
    created_by: 1,
    created_at: '2024-02-10T09:15:00',
    updated_at: '2024-02-10T09:15:00',
    cloud_assets_count: 0,
    sows_count: 1,
    slas_count: 0,
    knowledge_documents_count: 3
  },
  {
    id: 4,
    project_code: 'P2024004',
    project_name: '移动办公平台',
    application_name: '移动办公',
    department: '设计部',
    manager_id: 4,
    manager_name: '赵六',
    status: 'testing',
    launch_date: '2024-05-20',
    description: '移动端办公平台开发',
    remark: '测试阶段，bug修复中',
    created_by: 1,
    created_at: '2024-02-28T16:45:00',
    updated_at: '2024-02-28T16:45:00',
    cloud_assets_count: 3,
    sows_count: 2,
    slas_count: 1,
    knowledge_documents_count: 6
  },
  {
    id: 5,
    project_code: 'P2024005',
    project_name: '智能客服系统',
    application_name: '智能客服',
    department: '客服部',
    manager_id: 1,
    manager_name: '张三',
    status: 'maintenance',
    launch_date: '2023-11-10',
    description: 'AI智能客服系统',
    remark: '日常维护和优化',
    created_by: 1,
    created_at: '2023-10-05T11:30:00',
    updated_at: '2023-10-05T11:30:00',
    cloud_assets_count: 6,
    sows_count: 2,
    slas_count: 1,
    knowledge_documents_count: 10
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

// 获取状态标签
const getStatusLabel = (status: string) => {
  const option = projectStatusOptions.value.find(opt => opt.value === status)
  return option ? option.label : status
}

// 获取状态类型
const getStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    planning: 'info',
    in_progress: 'primary',
    testing: 'warning',
    online: 'success',
    maintenance: 'danger',
    archived: 'info'
  }
  return typeMap[status] || 'info'
}

// 格式化日期
const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD')
}

// 格式化日期时间
const formatDateTime = (datetime: string) => {
  return dayjs(datetime).format('YYYY-MM-DD HH:mm')
}

// 表格行样式
const tableRowClassName = ({ row }: { row: Project }) => {
  if (row.status === 'online') {
    return 'success-row'
  } else if (row.status === 'maintenance') {
    return 'warning-row'
  }
  return ''
}

// 处理创建项目
const handleCreate = () => {
  router.push('/projects/create')
}

// 处理查看项目
const handleView = (project: Project) => {
  router.push(`/projects/${project.id}`)
}

// 处理编辑项目
const handleEdit = (project: Project) => {
  router.push(`/projects/${project.id}/edit`)
}

// 处理删除项目
const handleDelete = async (project: Project) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除项目 "${project.project_name}" 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 模拟删除操作
    const index = projectList.value.findIndex(p => p.id === project.id)
    if (index !== -1) {
      projectList.value.splice(index, 1)
      ElMessage.success('项目删除成功')
    }
  } catch (error) {
    // 用户取消删除
  }
}

// 处理行点击
const handleRowClick = (row: Project) => {
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
    project_code: '',
    project_name: '',
    department: '',
    status: '',
    manager_id: ''
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
    let filteredData = [...projectList.value]
    
    if (filterForm.project_code) {
      filteredData = filteredData.filter(p => 
        p.project_code.toLowerCase().includes(filterForm.project_code.toLowerCase())
      )
    }
    
    if (filterForm.project_name) {
      filteredData = filteredData.filter(p => 
        p.project_name.toLowerCase().includes(filterForm.project_name.toLowerCase())
      )
    }
    
    if (filterForm.department) {
      filteredData = filteredData.filter(p => p.department === filterForm.department)
    }
    
    if (filterForm.status) {
      filteredData = filteredData.filter(p => p.status === filterForm.status)
    }
    
    if (filterForm.manager_id) {
      filteredData = filteredData.filter(p => p.manager_id === Number(filterForm.manager_id))
    }
    
    // 模拟分页
    const start = (pagination.current - 1) * pagination.size
    const end = start + pagination.size
    const paginatedData = filteredData.slice(start, end)
    
    // 更新数据
    projectList.value = paginatedData
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
  appStore.setPageTitle('项目管理')
})
</script>

<style lang="scss" scoped>
.project-list-container {
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
  .success-row {
    --el-table-tr-bg-color: rgba(16, 185, 129, 0.05);
  }
  
  .warning-row {
    --el-table-tr-bg-color: rgba(245, 158, 11, 0.05);
  }
  
  .project-name-cell {
    display: flex;
    flex-direction: column;
    
    .project-name {
      font-weight: 500;
      color: var(--text-primary);
      margin-bottom: 4px;
    }
    
    .application-name {
      font-size: 12px;
      color: var(--text-tertiary);
    }
  }
  
  .manager-cell {
    display: flex;
    align-items: center;
    gap: 8px;
    
    .manager-name {
      color: var(--text-primary);
    }
  }
  
  .action-buttons {
    display: flex;
    gap: 8px;
    
    .el-button {
      padding: 4px 0;
    }
  }
  
  .text-muted {
    color: var(--text-tertiary);
    font-style: italic;
  }
}

// 卡片视图
.card-view {
  .loading-container,
  .empty-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 20px;
    color: var(--text-tertiary);
    
    .loading-icon {
      font-size: 32px;
      margin-bottom: 12px;
      animation: spin 1s linear infinite;
    }
    
    .empty-icon {
      font-size: 48px;
      margin-bottom: 16px;
      opacity: 0.5;
    }
    
    .empty-text {
      margin-bottom: 20px;
      font-size: 14px;
    }
  }
  
  .project-cards {
    .project-card {
      margin-bottom: 20px;
      cursor: pointer;
      transition: all 0.3s ease;
      border: 1px solid var(--border-color);
      
      &:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg) !important;
        border-color: var(--primary-color);
      }
      
      :deep(.el-card__header) {
        padding: 12px 16px;
        border-bottom: 1px solid var(--border-color);
        
        .card-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
      }
      
      .card-content {
        padding: 16px;
        
        .project-name {
          font-size: 16px;
          font-weight: 600;
          color: var(--text-primary);
          margin: 0 0 8px 0;
          line-height: 1.4;
        }
        
        .application-name {
          font-size: 14px;
          color: var(--text-secondary);
          margin: 0 0 16px 0;
          line-height: 1.4;
        }
        
        .project-info {
          display: flex;
          flex-direction: column;
          gap: 8px;
          margin-bottom: 16px;
          
          .info-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            color: var(--text-secondary);
            
            .el-icon {
              font-size: 14px;
              color: var(--text-tertiary);
            }
          }
        }
        
        .project-stats {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 8px;
          padding: 12px;
          background: var(--bg-secondary);
          border-radius: var(--radius-md);
          
          .stat-item {
            display: flex;
            flex-direction: column;
            align-items: center;
            
            .stat-label {
              font-size: 11px;
              color: var(--text-tertiary);
              margin-bottom: 4px;
              text-transform: uppercase;
              letter-spacing: 0.5px;
            }
            
            .stat-value {
              font-size: 16px;
              font-weight: 600;
              color: var(--text-primary);
            }
          }
        }
      }
      
      :deep(.el-card__footer) {
        padding: 12px 16px;
        border-top: 1px solid var(--border-color);
        
        .card-footer {
          display: flex;
          justify-content: space-between;
          align-items: center;
          
          .create-time {
            font-size: 12px;
            color: var(--text-tertiary);
          }
          
          .card-actions {
            display: flex;
            gap: 8px;
            
            .el-button {
              padding: 2px 0;
              font-size: 12px;
            }
          }
        }
      }
    }
  }
}

// 分页容器
.pagination-container {
  display: flex;
  justify-content: center;
  padding: 20px 0 0 0;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
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
  
  .list-header {
    flex-direction: column;
    align-items: flex-start !important;
    gap: 12px;
    
    .list-actions {
      align-self: flex-end;
    }
  }
  
  .project-cards {
    .el-col {
      width: 100%;
    }
  }
}
</style>