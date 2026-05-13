<template>
  <div class="sla-list-container">
    <!-- 页面标题和操作 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">SLA管理</h1>
        <p class="page-subtitle">服务等级协议管理</p>
      </div>
      <div class="header-right">
        <el-button type="primary" :icon="Plus" @click="handleCreate" v-if="isAdmin">
          创建SLA
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
          
          <el-form-item label="协议名称">
            <el-input
              v-model="filterForm.agreement_name"
              placeholder="请输入协议名称"
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
          
          <el-form-item label="可用率">
            <el-input
              v-model="filterForm.availability"
              placeholder="请输入可用率"
              clearable
              @clear="handleFilter"
              @keyup.enter="handleFilter"
            >
              <template #append>%</template>
            </el-input>
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
    
    <!-- SLA列表 -->
    <el-card class="list-card" shadow="never">
      <template #header>
        <div class="list-header">
          <div class="list-title">
            <span>SLA协议列表</span>
            <el-tag type="info" size="small">
              共 {{ pagination.total }} 个协议
            </el-tag>
          </div>
        </div>
      </template>
      
      <!-- 表格 -->
      <el-table
        v-loading="loading"
        :data="slaList"
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
        
        <el-table-column prop="agreement_name" label="协议名称" width="200">
          <template #default="{ row }">
            <div class="agreement-cell">
              <el-icon class="agreement-icon"><Document /></el-icon>
              <span class="agreement-name">{{ row.agreement_name }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="availability" label="可用率" width="120">
          <template #default="{ row }">
            <div class="availability-cell">
              <el-progress
                :percentage="row.availability"
                :color="getAvailabilityColor(row.availability)"
                :show-text="false"
                :stroke-width="8"
              />
              <span class="availability-value">{{ row.availability }}%</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="response_time" label="响应时效" width="120">
          <template #default="{ row }">
            <span v-if="row.response_time">{{ row.response_time }}小时</span>
            <span v-else class="text-muted">未设置</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="fault_resolution_time" label="故障处理" width="120">
          <template #default="{ row }">
            <span v-if="row.fault_resolution_time">{{ row.fault_resolution_time }}小时</span>
            <span v-else class="text-muted">未设置</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="effective_date" label="生效日期" width="120">
          <template #default="{ row }">
            {{ formatDate(row.effective_date) }}
          </template>
        </el-table-column>
        
        <el-table-column prop="expiry_date" label="到期日期" width="120">
          <template #default="{ row }">
            {{ formatDate(row.expiry_date) }}
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
      
      <!-- 分页 -->
      <div class="pagination-container" v-if="slaList.length > 0">
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
import type { SLA } from '@/types'

const router = useRouter()
const userStore = useUserStore()
const appStore = useAppStore()

// 加载状态
const loading = ref(false)

// 筛选表单
const filterForm = reactive({
  project_id: '',
  agreement_name: '',
  status: '',
  availability: ''
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
  { value: 'active', label: '生效中' },
  { value: 'expired', label: '已过期' },
  { value: 'terminated', label: '已终止' }
])

// SLA列表数据
const slaList = ref<SLA[]>([
  {
    id: 1,
    project_id: 1,
    project_name: 'OA系统升级',
    project_code: 'P2024001',
    agreement_name: 'OA系统SLA',
    availability: 99.9,
    response_time: 4,
    fault_resolution_time: 8,
    maintenance_window: '每周日 02:00-04:00',
    penalty_terms: '服务不达标按合同约定赔偿',
    status: 'active',
    effective_date: '2024-01-01',
    expiry_date: '2024-12-31',
    created_by: 1,
    creator_name: '张三',
    created_at: '2024-01-01T10:00:00',
    updated_at: '2024-01-01T10:00:00'
  },
  {
    id: 2,
    project_id: 1,
    project_name: 'OA系统升级',
    project_code: 'P2024001',
    agreement_name: 'OA系统SLA (高级)',
    availability: 99.99,
    response_time: 2,
    fault_resolution_time: 4,
    maintenance_window: '每月第一个周日 01:00-03:00',
    penalty_terms: '服务不达标按合同约定赔偿',
    status: 'active',
    effective_date: '2024-02-01',
    expiry_date: '2024-12-31',
    created_by: 1,
    creator_name: '张三',
    created_at: '2024-02-01T14:30:00',
    updated_at: '2024-02-01T14:30:00'
  },
  {
    id: 3,
    project_id: 2,
    project_name: '客户关系管理系统',
    project_code: 'P2024002',
    agreement_name: 'CRM系统SLA',
    availability: 99.5,
    response_time: 8,
    fault_resolution_time: 24,
    maintenance_window: '每周六 00:00-06:00',
    penalty_terms: '服务不达标按合同约定赔偿',
    status: 'active',
    effective_date: '2024-01-15',
    expiry_date: '2024-12-31',
    created_by: 1,
    creator_name: '张三',
    created_at: '2024-01-15T09:00:00',
    updated_at: '2024-01-15T09:00:00'
  },
  {
    id: 4,
    project_id: 3,
    project_name: '数据中台建设',
    project_code: 'P2024003',
    agreement_name: '数据中台SLA',
    availability: 99.95,
    response_time: 6,
    fault_resolution_time: 12,
    maintenance_window: '每周日 01:00-03:00',
    penalty_terms: '服务不达标按合同约定赔偿',
    status: 'draft',
    effective_date: '2024-03-01',
    expiry_date: '2024-12-31',
    created_by: 1,
    creator_name: '张三',
    created_at: '2024-02-28T16:00:00',
    updated_at: '2024-02-28T16:00:00'
  },
  {
    id: 5,
    project_id: 4,
    project_name: '移动办公平台',
    project_code: 'P2024004',
    agreement_name: '移动办公平台SLA',
    availability: 99.0,
    response_time: 12,
    fault_resolution_time: 48,
    maintenance_window: '每月最后一个周日 00:00-06:00',
    penalty_terms: '服务不达标按合同约定赔偿',
    status: 'expired',
    effective_date: '2023-01-01',
    expiry_date: '2023-12-31',
    created_by: 1,
    creator_name: '张三',
    created_at: '2023-01-01T10:00:00',
    updated_at: '2023-12-31T23:59:59'
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

// 获取可用率颜色
const getAvailabilityColor = (availability: number) => {
  if (availability >= 99.9) return '#10b981' // 绿色
  if (availability >= 99.5) return '#3b82f6' // 蓝色
  if (availability >= 99.0) return '#f59e0b' // 橙色
  return '#ef4444' // 红色
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
    active: 'success',
    expired: 'warning',
    terminated: 'danger'
  }
  return typeMap[status] || 'info'
}

// 格式化日期
const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD')
}

// 处理创建SLA
const handleCreate = () => {
  router.push('/slas/create')
}

// 处理查看SLA
const handleView = (sla: SLA) => {
  // 可以跳转到详情页，这里暂时用编辑页代替
  router.push(`/slas/${sla.id}/edit`)
}

// 处理编辑SLA
const handleEdit = (sla: SLA) => {
  router.push(`/slas/${sla.id}/edit`)
}

// 处理删除SLA
const handleDelete = async (sla: SLA) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除SLA协议 "${sla.agreement_name}" 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 模拟删除操作
    const index = slaList.value.findIndex(s => s.id === sla.id)
    if (index !== -1) {
      slaList.value.splice(index, 1)
      ElMessage.success('SLA协议删除成功')
    }
  } catch (error) {
    // 用户取消删除
  }
}

// 处理行点击
const handleRowClick = (row: SLA) => {
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
    agreement_name: '',
    status: '',
    availability: ''
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
    let filteredData = [...slaList.value]
    
    if (filterForm.project_id) {
      filteredData = filteredData.filter(s => s.project_id === Number(filterForm.project_id))
    }
    
    if (filterForm.agreement_name) {
      filteredData = filteredData.filter(s => 
        s.agreement_name.toLowerCase().includes(filterForm.agreement_name.toLowerCase())
      )
    }
    
    if (filterForm.status) {
      filteredData = filteredData.filter(s => s.status === filterForm.status)
    }
    
    if (filterForm.availability) {
      const availability = parseFloat(filterForm.availability)
      if (!isNaN(availability)) {
        filteredData = filteredData.filter(s => s.availability >= availability)
      }
    }
    
    // 模拟分页
    const start = (pagination.current - 1) * pagination.size
    const end = start + pagination.size
    const paginatedData = filteredData.slice(start, end)
    
    // 更新数据
    slaList.value = paginatedData
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
  appStore.setPageTitle('SLA管理')
})
</script>

<style lang="scss" scoped>
.sla-list-container {
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
  
  .agreement-cell {
    display: flex;
    align-items: center;
    gap: 8px;
    
    .agreement-icon {
      color: var(--primary-color);
    }
    
    .agreement-name {
      font-weight: 500;
    }
  }
  
  .availability-cell {
    display: flex;
    align-items: center;
    gap: 12px;
    
    .el-progress {
      flex: 1;
    }
    
    .availability-value {
      font-weight: 600;
      color: var(--text-primary);
      min-width: 40px;
      text-align: right;
    }
  }
  
  .text-muted {
    color: var(--text-tertiary);
    font-style: italic;
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
  
  .availability-cell {
    flex-direction: column;
    align-items: flex-start !important;
    gap: 4px !important;
    
    .availability-value {
      text-align: left !important;
    }
  }
}
</style>