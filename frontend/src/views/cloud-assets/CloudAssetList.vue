<template>
  <div class="cloud-asset-list-container">
    <!-- 页面标题和操作 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">云资产管理</h1>
        <p class="page-subtitle">统一管理云平台资源资产</p>
      </div>
      <div class="header-right">
        <el-button type="primary" :icon="Plus" @click="handleCreate" v-if="isAdmin">
          添加资产
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
          
          <el-form-item label="云厂商">
            <el-select
              v-model="filterForm.cloud_provider"
              placeholder="请选择云厂商"
              clearable
              @change="handleFilter"
            >
              <el-option
                v-for="provider in cloudProviderOptions"
                :key="provider.value"
                :label="provider.label"
                :value="provider.value"
              />
            </el-select>
          </el-form-item>
          
          <el-form-item label="资源类型">
            <el-input
              v-model="filterForm.resource_type"
              placeholder="请输入资源类型"
              clearable
              @clear="handleFilter"
              @keyup.enter="handleFilter"
            />
          </el-form-item>
          
          <el-form-item label="地域">
            <el-input
              v-model="filterForm.region"
              placeholder="请输入地域"
              clearable
              @clear="handleFilter"
              @keyup.enter="handleFilter"
            />
          </el-form-item>
          
          <el-form-item label="生命周期">
            <el-select
              v-model="filterForm.lifecycle"
              placeholder="请选择生命周期"
              clearable
              @change="handleFilter"
            >
              <el-option
                v-for="lifecycle in lifecycleOptions"
                :key="lifecycle.value"
                :label="lifecycle.label"
                :value="lifecycle.value"
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
    
    <!-- 云资产列表 -->
    <el-card class="list-card" shadow="never">
      <template #header>
        <div class="list-header">
          <div class="list-title">
            <span>云资产列表</span>
            <el-tag type="info" size="small">
              共 {{ pagination.total }} 个资产
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
          :data="assetList"
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
          
          <el-table-column prop="cloud_provider" label="云厂商" width="120">
            <template #default="{ row }">
              <el-tag :type="getProviderType(row.cloud_provider)" size="small">
                {{ getProviderLabel(row.cloud_provider) }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="resource_type" label="资源类型" width="120">
            <template #default="{ row }">
              <el-tag type="info" size="small">{{ row.resource_type }}</el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="instance_spec" label="实例规格" width="150">
            <template #default="{ row }">
              <span v-if="row.instance_spec">{{ row.instance_spec }}</span>
              <span v-else class="text-muted">未设置</span>
            </template>
          </el-table-column>
          
          <el-table-column prop="region" label="地域" width="120">
            <template #default="{ row }">
              {{ row.region }}
            </template>
          </el-table-column>
          
          <el-table-column prop="zone" label="可用区" width="100">
            <template #default="{ row }">
              <span v-if="row.zone">{{ row.zone }}</span>
              <span v-else class="text-muted">-</span>
            </template>
          </el-table-column>
          
          <el-table-column prop="ip_address" label="IP地址" width="140">
            <template #default="{ row }">
              <span v-if="row.ip_address">{{ row.ip_address }}</span>
              <span v-else class="text-muted">未分配</span>
            </template>
          </el-table-column>
          
          <el-table-column prop="lifecycle" label="生命周期" width="100">
            <template #default="{ row }">
              <el-tag :type="getLifecycleType(row.lifecycle)" size="small">
                {{ getLifecycleLabel(row.lifecycle) }}
              </el-tag>
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
        
        <div v-else-if="assetList.length === 0" class="empty-container">
          <el-icon class="empty-icon"><Cloudy /></el-icon>
          <p class="empty-text">暂无云资产数据</p>
          <el-button type="primary" :icon="Plus" @click="handleCreate" v-if="isAdmin">
            添加第一个资产
          </el-button>
        </div>
        
        <div v-else class="asset-cards">
          <el-row :gutter="20">
            <el-col
              v-for="asset in assetList"
              :key="asset.id"
              :xs="24"
              :sm="12"
              :md="8"
              :lg="6"
              :xl="6"
            >
              <el-card class="asset-card" shadow="hover" @click="handleView(asset)">
                <template #header>
                  <div class="card-header">
                    <div class="asset-provider">
                      <el-tag :type="getProviderType(asset.cloud_provider)" size="small">
                        {{ getProviderLabel(asset.cloud_provider) }}
                      </el-tag>
                    </div>
                    <div class="asset-lifecycle">
                      <el-tag :type="getLifecycleType(asset.lifecycle)" size="small">
                        {{ getLifecycleLabel(asset.lifecycle) }}
                      </el-tag>
                    </div>
                  </div>
                </template>
                
                <div class="card-content">
                  <h3 class="asset-name">{{ asset.resource_type }}</h3>
                  <p class="asset-spec">{{ asset.instance_spec || '未设置规格' }}</p>
                  
                  <div class="asset-info">
                    <div class="info-item">
                      <el-icon><OfficeBuilding /></el-icon>
                      <span>{{ asset.project_name }}</span>
                    </div>
                    <div class="info-item">
                      <el-icon><Location /></el-icon>
                      <span>{{ asset.region }}{{ asset.zone ? `-${asset.zone}` : '' }}</span>
                    </div>
                    <div class="info-item" v-if="asset.ip_address">
                      <el-icon><Connection /></el-icon>
                      <span>{{ asset.ip_address }}</span>
                    </div>
                    <div class="info-item" v-if="asset.account_info">
                      <el-icon><User /></el-icon>
                      <span>{{ asset.account_info }}</span>
                    </div>
                  </div>
                </div>
                
                <template #footer>
                  <div class="card-footer">
                    <span class="create-time">{{ formatDateTime(asset.created_at) }}</span>
                    <div class="card-actions">
                      <el-button
                        v-if="isAdmin"
                        type="primary"
                        link
                        :icon="Edit"
                        @click.stop="handleEdit(asset)"
                      >
                        编辑
                      </el-button>
                      <el-button
                        v-if="isAdmin"
                        type="danger"
                        link
                        :icon="Delete"
                        @click.stop="handleDelete(asset)"
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
      <div class="pagination-container" v-if="assetList.length > 0">
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
  Grid,
  Menu,
  View,
  Edit,
  Delete,
  Loading,
  Cloudy,
  OfficeBuilding,
  Location,
  Connection,
  User
} from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { useAppStore } from '@/store/app'
import dayjs from 'dayjs'
import type { CloudAsset } from '@/types'

const router = useRouter()
const userStore = useUserStore()
const appStore = useAppStore()

// 视图模式
const viewMode = ref<'table' | 'card'>('table')

// 加载状态
const loading = ref(false)

// 筛选表单
const filterForm = reactive({
  project_id: '',
  cloud_provider: '',
  resource_type: '',
  region: '',
  lifecycle: ''
})

// 项目列表
const projects = ref([
  { id: 1, project_code: 'P2024001', project_name: 'OA系统升级' },
  { id: 2, project_code: 'P2024002', project_name: '客户关系管理系统' },
  { id: 3, project_code: 'P2024003', project_name: '数据中台建设' },
  { id: 4, project_code: 'P2024004', project_name: '移动办公平台' },
  { id: 5, project_code: 'P2024005', project_name: '智能客服系统' }
])

// 云厂商选项
const cloudProviderOptions = ref([
  { value: 'aliyun', label: '阿里云' },
  { value: 'huawei', label: '华为云' },
  { value: 'tencent', label: '腾讯云' },
  { value: 'self_built', label: '自建机房' }
])

// 生命周期选项
const lifecycleOptions = ref([
  { value: 'creating', label: '创建中' },
  { value: 'running', label: '运行中' },
  { value: 'stopped', label: '已停止' },
  { value: 'deleting', label: '删除中' },
  { value: 'deleted', label: '已删除' }
])

// 资产列表数据
const assetList = ref<CloudAsset[]>([
  {
    id: 1,
    project_id: 1,
    project_name: 'OA系统升级',
    project_code: 'P2024001',
    cloud_provider: 'aliyun',
    resource_type: 'ECS',
    instance_spec: 'ecs.g6.large',
    region: 'cn-hangzhou',
    zone: 'cn-hangzhou-h',
    account_info: 'test-account',
    ip_address: '192.168.1.100',
    config_json: {},
    lifecycle: 'running',
    created_by: 1,
    creator_name: '张三',
    created_at: '2024-01-15T10:30:00',
    updated_at: '2024-01-15T10:30:00'
  },
  {
    id: 2,
    project_id: 1,
    project_name: 'OA系统升级',
    project_code: 'P2024001',
    cloud_provider: 'aliyun',
    resource_type: 'RDS',
    instance_spec: 'rds.mysql.s3.large',
    region: 'cn-hangzhou',
    zone: 'cn-hangzhou-h',
    account_info: 'test-account',
    ip_address: '192.168.1.101',
    config_json: {},
    lifecycle: 'running',
    created_by: 1,
    creator_name: '张三',
    created_at: '2024-01-20T14:20:00',
    updated_at: '2024-01-20T14:20:00'
  },
  {
    id: 3,
    project_id: 2,
    project_name: '客户关系管理系统',
    project_code: 'P2024002',
    cloud_provider: 'huawei',
    resource_type: 'ECS',
    instance_spec: 's6.large.2',
    region: 'cn-north-4',
    zone: 'cn-north-4a',
    account_info: 'crm-account',
    ip_address: '10.0.1.100',
    config_json: {},
    lifecycle: 'running',
    created_by: 1,
    creator_name: '张三',
    created_at: '2024-02-10T09:15:00',
    updated_at: '2024-02-10T09:15:00'
  },
  {
    id: 4,
    project_id: 3,
    project_name: '数据中台建设',
    project_code: 'P2024003',
    cloud_provider: 'tencent',
    resource_type: 'CVM',
    instance_spec: 'S5.MEDIUM4',
    region: 'ap-guangzhou',
    zone: 'ap-guangzhou-3',
    account_info: 'data-account',
    ip_address: '172.16.1.100',
    config_json: {},
    lifecycle: 'creating',
    created_by: 1,
    creator_name: '张三',
    created_at: '2024-02-28T16:45:00',
    updated_at: '2024-02-28T16:45:00'
  },
  {
    id: 5,
    project_id: 4,
    project_name: '移动办公平台',
    project_code: 'P2024004',
    cloud_provider: 'self_built',
    resource_type: '物理服务器',
    instance_spec: 'Dell R740',
    region: '本地机房',
    zone: 'A区',
    account_info: 'local-admin',
    ip_address: '192.168.10.100',
    config_json: {},
    lifecycle: 'stopped',
    created_by: 1,
    creator_name: '张三',
    created_at: '2024-03-05T11:30:00',
    updated_at: '2024-03-05T11:30:00'
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

// 获取云厂商标签
const getProviderLabel = (provider: string) => {
  const option = cloudProviderOptions.value.find(opt => opt.value === provider)
  return option ? option.label : provider
}

// 获取云厂商类型
const getProviderType = (provider: string) => {
  const typeMap: Record<string, string> = {
    aliyun: 'primary',
    huawei: 'danger',
    tencent: 'info',
    self_built: 'warning'
  }
  return typeMap[provider] || 'info'
}

// 获取生命周期标签
const getLifecycleLabel = (lifecycle: string) => {
  const option = lifecycleOptions.value.find(opt => opt.value === lifecycle)
  return option ? option.label : lifecycle
}

// 获取生命周期类型
const getLifecycleType = (lifecycle: string) => {
  const typeMap: Record<string, string> = {
    creating: 'info',
    running: 'success',
    stopped: 'warning',
    deleting: 'danger',
    deleted: 'info'
  }
  return typeMap[lifecycle] || 'info'
}

// 格式化日期时间
const formatDateTime = (datetime: string) => {
  return dayjs(datetime).format('YYYY-MM-DD HH:mm')
}

// 处理创建资产
const handleCreate = () => {
  router.push('/cloud-assets/create')
}

// 处理查看资产
const handleView = (asset: CloudAsset) => {
  // 可以跳转到详情页，这里暂时用编辑页代替
  router.push(`/cloud-assets/${asset.id}/edit`)
}

// 处理编辑资产
const handleEdit = (asset: CloudAsset) => {
  router.push(`/cloud-assets/${asset.id}/edit`)
}

// 处理删除资产
const handleDelete = async (asset: CloudAsset) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除云资产 "${asset.resource_type}" 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 模拟删除操作
    const index = assetList.value.findIndex(a => a.id === asset.id)
    if (index !== -1) {
      assetList.value.splice(index, 1)
      ElMessage.success('云资产删除成功')
    }
  } catch (error) {
    // 用户取消删除
  }
}

// 处理行点击
const handleRowClick = (row: CloudAsset) => {
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
    cloud_provider: '',
    resource_type: '',
    region: '',
    lifecycle: ''
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
    let filteredData = [...assetList.value]
    
    if (filterForm.project_id) {
      filteredData = filteredData.filter(a => a.project_id === Number(filterForm.project_id))
    }
    
    if (filterForm.cloud_provider) {
      filteredData = filteredData.filter(a => a.cloud_provider === filterForm.cloud_provider)
    }
    
    if (filterForm.resource_type) {
      filteredData = filteredData.filter(a => 
        a.resource_type.toLowerCase().includes(filterForm.resource_type.toLowerCase())
      )
    }
    
    if (filterForm.region) {
      filteredData = filteredData.filter(a => 
        a.region.toLowerCase().includes(filterForm.region.toLowerCase())
      )
    }
    
    if (filterForm.lifecycle) {
      filteredData = filteredData.filter(a => a.lifecycle === filterForm.lifecycle)
    }
    
    // 模拟分页
    const start = (pagination.current - 1) * pagination.size
    const end = start + pagination.size
    const paginatedData = filteredData.slice(start, end)
    
    // 更新数据
    assetList.value = paginatedData
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
  appStore.setPageTitle('云资产管理')
})
</script>

<style lang="scss" scoped>
.cloud-asset-list-container {
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
  
  .asset-cards {
    .asset-card {
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
        
        .asset-name {
          font-size: 16px;
          font-weight: 600;
          color: var(--text-primary);
          margin: 0 0 8px 0;
          line-height: 1.4;
        }
        
        .asset-spec {
          font-size: 14px;
          color: var(--text-secondary);
          margin: 0 0 16px 0;
          line-height: 1.4;
        }
        
        .asset-info {
          display: flex;
          flex-direction: column;
          gap: 8px;
          
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
  
  .asset-cards {
    .el-col {
      width: 100%;
    }
  }
}
</style>