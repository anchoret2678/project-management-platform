<template>
  <div class="knowledge-list-container">
    <!-- 页面标题和操作 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">知识库</h1>
        <p class="page-subtitle">项目知识文档管理</p>
      </div>
      <div class="header-right">
        <el-button type="primary" :icon="Plus" @click="handleCreate" v-if="isAdmin">
          添加文档
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
          
          <el-form-item label="文档标题">
            <el-input
              v-model="filterForm.document_title"
              placeholder="请输入文档标题"
              clearable
              @clear="handleFilter"
              @keyup.enter="handleFilter"
            />
          </el-form-item>
          
          <el-form-item label="分类">
            <el-select
              v-model="filterForm.category"
              placeholder="请选择分类"
              clearable
              @change="handleFilter"
            >
              <el-option
                v-for="category in categoryOptions"
                :key="category.value"
                :label="category.label"
                :value="category.value"
              />
            </el-select>
          </el-form-item>
          
          <el-form-item label="标签">
            <el-input
              v-model="filterForm.tags"
              placeholder="请输入标签，多个用逗号分隔"
              clearable
              @clear="handleFilter"
              @keyup.enter="handleFilter"
            />
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
    
    <!-- 知识库列表 -->
    <el-card class="list-card" shadow="never">
      <template #header>
        <div class="list-header">
          <div class="list-title">
            <span>知识文档列表</span>
            <el-tag type="info" size="small">
              共 {{ pagination.total }} 个文档
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
          :data="knowledgeList"
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
          
          <el-table-column prop="document_title" label="文档标题" width="200">
            <template #default="{ row }">
              <div class="document-cell">
                <el-icon class="document-icon"><Notebook /></el-icon>
                <span class="document-title">{{ row.document_title }}</span>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="category" label="分类" width="120">
            <template #default="{ row }">
              <el-tag :type="getCategoryType(row.category)" size="small">
                {{ getCategoryLabel(row.category) }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="tags" label="标签" width="180">
            <template #default="{ row }">
              <div class="tags-cell">
                <el-tag
                  v-for="tag in getTagArray(row.tags)"
                  :key="tag"
                  type="info"
                  size="small"
                  class="tag-item"
                >
                  {{ tag }}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column prop="file_size" label="文件大小" width="100">
            <template #default="{ row }">
              <span v-if="row.file_size">{{ formatFileSize(row.file_size) }}</span>
              <span v-else class="text-muted">-</span>
            </template>
          </el-table-column>
          
          <el-table-column prop="created_by_name" label="创建人" width="120">
            <template #default="{ row }">
              {{ row.created_by_name }}
            </template>
          </el-table-column>
          
          <el-table-column prop="created_at" label="创建时间" width="160">
            <template #default="{ row }">
              {{ formatDateTime(row.created_at) }}
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
                  v-if="row.file_path"
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
      </div>
      
      <!-- 卡片视图 -->
      <div v-else class="card-view">
        <div v-if="loading" class="loading-container">
          <el-icon class="loading-icon"><Loading /></el-icon>
          <span>加载中...</span>
        </div>
        
        <div v-else-if="knowledgeList.length === 0" class="empty-container">
          <el-icon class="empty-icon"><Notebook /></el-icon>
          <p class="empty-text">暂无知识文档</p>
          <el-button type="primary" :icon="Plus" @click="handleCreate" v-if="isAdmin">
            添加第一个文档
          </el-button>
        </div>
        
        <div v-else class="knowledge-cards">
          <el-row :gutter="20">
            <el-col
              v-for="doc in knowledgeList"
              :key="doc.id"
              :xs="24"
              :sm="12"
              :md="8"
              :lg="6"
              :xl="6"
            >
              <el-card class="knowledge-card" shadow="hover" @click="handleView(doc)">
                <template #header>
                  <div class="card-header">
                    <div class="doc-category">
                      <el-tag :type="getCategoryType(doc.category)" size="small">
                        {{ getCategoryLabel(doc.category) }}
                      </el-tag>
                    </div>
                    <div class="doc-actions">
                      <el-dropdown trigger="click" @command="handleCardCommand">
                        <el-icon class="more-icon"><More /></el-icon>
                        <template #dropdown>
                          <el-dropdown-menu>
                            <el-dropdown-item :command="{ action: 'view', doc }">
                              <el-icon><View /></el-icon>
                              查看
                            </el-dropdown-item>
                            <el-dropdown-item 
                              v-if="doc.file_path" 
                              :command="{ action: 'download', doc }"
                            >
                              <el-icon><Download /></el-icon>
                              下载
                            </el-dropdown-item>
                            <el-dropdown-item 
                              v-if="isAdmin" 
                              :command="{ action: 'edit', doc }"
                            >
                              <el-icon><Edit /></el-icon>
                              编辑
                            </el-dropdown-item>
                            <el-dropdown-item 
                              v-if="isAdmin" 
                              :command="{ action: 'delete', doc }"
                              divided
                            >
                              <el-icon><Delete /></el-icon>
                              删除
                            </el-dropdown-item>
                          </el-dropdown-menu>
                        </template>
                      </el-dropdown>
                    </div>
                  </div>
                </template>
                
                <div class="card-content">
                  <h3 class="doc-title">{{ doc.document_title }}</h3>
                  <p class="doc-description" v-if="doc.description">
                    {{ truncateText(doc.description, 100) }}
                  </p>
                  
                  <div class="doc-info">
                    <div class="info-item">
                      <el-icon><OfficeBuilding /></el-icon>
                      <span>{{ doc.project_name }}</span>
                    </div>
                    <div class="info-item" v-if="doc.file_size">
                      <el-icon><Document /></el-icon>
                      <span>{{ formatFileSize(doc.file_size) }}</span>
                    </div>
                    <div class="info-item">
                      <el-icon><User /></el-icon>
                      <span>{{ doc.created_by_name }}</span>
                    </div>
                  </div>
                  
                  <div class="doc-tags" v-if="doc.tags">
                    <el-tag
                      v-for="tag in getTagArray(doc.tags).slice(0, 3)"
                      :key="tag"
                      type="info"
                      size="small"
                      class="tag-item"
                    >
                      {{ tag }}
                    </el-tag>
                    <span v-if="getTagArray(doc.tags).length > 3" class="more-tags">
                      +{{ getTagArray(doc.tags).length - 3 }}
                    </span>
                  </div>
                </div>
                
                <template #footer>
                  <div class="card-footer">
                    <span class="create-time">{{ formatDateTime(doc.created_at) }}</span>
                  </div>
                </template>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </div>
      
      <!-- 分页 -->
      <div class="pagination-container" v-if="knowledgeList.length > 0">
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
  Notebook,
  OfficeBuilding,
  Document,
  User,
  More
} from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { useAppStore } from '@/store/app'
import dayjs from 'dayjs'
import type { Knowledge } from '@/types'

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
  document_title: '',
  category: '',
  tags: ''
})

// 项目列表
const projects = ref([
  { id: 1, project_code: 'P2024001', project_name: 'OA系统升级' },
  { id: 2, project_code: 'P2024002', project_name: '客户关系管理系统' },
  { id: 3, project_code: 'P2024003', project_name: '数据中台建设' },
  { id: 4, project_code: 'P2024004', project_name: '移动办公平台' },
  { id: 5, project_code: 'P2024005', project_name: '智能客服系统' }
])

// 分类选项
const categoryOptions = ref([
  { value: 'technical', label: '技术文档' },
  { value: 'operation', label: '运维手册' },
  { value: 'architecture', label: '架构文档' },
  { value: 'requirement', label: '需求文档' },
  { value: 'meeting', label: '会议纪要' },
  { value: 'other', label: '其他' }
])

// 知识库列表数据
const knowledgeList = ref<Knowledge[]>([
  {
    id: 1,
    project_id: 1,
    project_name: 'OA系统升级',
    project_code: 'P2024001',
    document_title: 'OA系统架构设计文档',
    description: 'OA系统升级项目的架构设计文档，包含系统架构、技术选型、部署方案等',
    category: 'architecture',
    tags: '架构,设计,OA系统',
    file_path: '/uploads/knowledge/oa-architecture-v1.0.pdf',
    file_name: 'oa-architecture-v1.0.pdf',
    file_size: 3145728,
    file_type: 'pdf',
    created_by: 1,
    created_by_name: '张三',
    created_at: '2024-01-05T14:30:00',
    updated_at: '2024-01-05T14:30:00'
  },
  {
    id: 2,
    project_id: 1,
    project_name: 'OA系统升级',
    project_code: 'P2024001',
    document_title: 'OA系统API接口规范',
    description: 'OA系统升级项目的API接口规范文档，包含接口定义、参数说明、错误码等',
    category: 'technical',
    tags: 'API,接口,规范',
    file_path: '/uploads/knowledge/oa-api-spec-v1.0.docx',
    file_name: 'oa-api-spec-v1.0.docx',
    file_size: 1048576,
    file_type: 'docx',
    created_by: 1,
    created_by_name: '张三',
    created_at: '2024-01-10T10:20:00',
    updated_at: '2024-01-10T10:20:00'
  },
  {
    id: 3,
    project_id: 2,
    project_name: '客户关系管理系统',
    project_code: 'P2024002',
    document_title: 'CRM系统需求文档',
    description: '客户关系管理系统的需求文档，包含功能需求、非功能需求、用户故事等',
    category: 'requirement',
    tags: '需求,CRM,用户故事',
    file_path: '/uploads/knowledge/crm-requirements-v1.0.pdf',
    file_name: 'crm-requirements-v1.0.pdf',
    file_size: 2097152,
    file_type: 'pdf',
    created_by: 1,
    created_by_name: '张三',
    created_at: '2024-01-15T16:45:00',
    updated_at: '2024-01-15T16:45:00'
  },
  {
    id: 4,
    project_id: 3,
    project_name: '数据中台建设',
    project_code: 'P2024003',
    document_title: '数据中台技术方案',
    description: '数据中台建设项目的技术方案文档，包含技术架构、数据流程、实施计划等',
    category: 'technical',
    tags: '数据中台,技术方案,大数据',
    file_path: '/uploads/knowledge/data-platform-tech-v1.0.pdf',
    file_name: 'data-platform-tech-v1.0.pdf',
    file_size: 4194304,
    file_type: 'pdf',
    created_by: 1,
    created_by_name: '张三',
    created_at: '2024-02-01T11:30:00',
    updated_at: '2024-02-01T11:30:00'
  },
  {
    id: 5,
    project_id: 4,
    project_name: '移动办公平台',
    project_code: 'P2024004',
    document_title: '移动办公平台项目启动会纪要',
    description: '移动办公平台项目启动会议纪要，包含会议内容、决策事项、行动计划等',
    category: 'meeting',
    tags: '会议纪要,项目启动,移动办公',
    file_path: '/uploads/knowledge/mobile-office-kickoff.docx',
    file_name: 'mobile-office-kickoff.docx',
    file_size: 524288,
    file_type: 'docx',
    created_by: 1,
    created_by_name: '张三',
    created_at: '2024-02-10T09:15:00',
    updated_at: '2024-02-10T09:15:00'
  },
  {
    id: 6,
    project_id: 1,
    project_name: 'OA系统升级',
    project_code: 'P2024001',
    document_title: 'OA系统运维手册',
    description: 'OA系统升级项目的运维手册，包含系统部署、监控、故障处理等',
    category: 'operation',
    tags: '运维,手册,监控',
    file_path: null,
    file_name: null,
    file_size: null,
    file_type: null,
    created_by: 1,
    created_by_name: '张三',
    created_at: '2024-02-15T14:00:00',
    updated_at: '2024-02-15T14:00:00'
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

// 获取分类标签
const getCategoryLabel = (category: string) => {
  const option = categoryOptions.value.find(opt => opt.value === category)
  return option ? option.label : category
}

// 获取分类类型
const getCategoryType = (category: string) => {
  const typeMap: Record<string, string> = {
    technical: 'primary',
    operation: 'success',
    architecture: 'warning',
    requirement: 'danger',
    meeting: 'info',
    other: 'info'
  }
  return typeMap[category] || 'info'
}

// 获取标签数组
const getTagArray = (tags: string) => {
  if (!tags) return []
  return tags.split(',').map(tag => tag.trim()).filter(tag => tag)
}

// 格式化文件大小
const formatFileSize = (bytes: number) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 格式化日期时间
const formatDateTime = (datetime: string) => {
  return dayjs(datetime).format('YYYY-MM-DD HH:mm')
}

// 截断文本
const truncateText = (text: string, maxLength: number) => {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

// 处理创建文档
const handleCreate = () => {
  router.push('/knowledge/create')
}

// 处理查看文档
const handleView = (doc: Knowledge) => {
  // 可以跳转到详情页，这里暂时用编辑页代替
  router.push(`/knowledge/${doc.id}/edit`)
}

// 处理下载文档
const handleDownload = (doc: Knowledge) => {
  if (doc.file_path) {
    ElMessage.info(`开始下载: ${doc.document_title}`)
    // 实际项目中这里会调用下载API
  }
}

// 处理编辑文档
const handleEdit = (doc: Knowledge) => {
  router.push(`/knowledge/${doc.id}/edit`)
}

// 处理删除文档
const handleDelete = async (doc: Knowledge) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除知识文档 "${doc.document_title}" 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 模拟删除操作
    const index = knowledgeList.value.findIndex(d => d.id === doc.id)
    if (index !== -1) {
      knowledgeList.value.splice(index, 1)
      ElMessage.success('知识文档删除成功')
    }
  } catch (error) {
    // 用户取消删除
  }
}

// 处理卡片命令
const handleCardCommand = (command: any) => {
  const { action, doc } = command
  switch (action) {
    case 'view':
      handleView(doc)
      break
    case 'download':
      handleDownload(doc)
      break
    case 'edit':
      handleEdit(doc)
      break
    case 'delete':
      handleDelete(doc)
      break
  }
}

// 处理行点击
const handleRowClick = (row: Knowledge) => {
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
    document_title: '',
    category: '',
    tags: ''
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
    let filteredData = [...knowledgeList.value]
    
    if (filterForm.project_id) {
      filteredData = filteredData.filter(d => d.project_id === Number(filterForm.project_id))
    }
    
    if (filterForm.document_title) {
      filteredData = filteredData.filter(d => 
        d.document_title.toLowerCase().includes(filterForm.document_title.toLowerCase())
      )
    }
    
    if (filterForm.category) {
      filteredData = filteredData.filter(d => d.category === filterForm.category)
    }
    
    if (filterForm.tags) {
      const searchTags = filterForm.tags.split(',').map(tag => tag.trim().toLowerCase())
      filteredData = filteredData.filter(d => {
        if (!d.tags) return false
        const docTags = d.tags.toLowerCase()
        return searchTags.some(tag => docTags.includes(tag))
      })
    }
    
    // 模拟分页
    const start = (pagination.current - 1) * pagination.size
    const end = start + pagination.size
    const paginatedData = filteredData.slice(start, end)
    
    // 更新数据
    knowledgeList.value = paginatedData
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
  appStore.setPageTitle('知识库')
})
</script>

<style lang="scss" scoped>
.knowledge-list-container {
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
    
    .document-title {
      font-weight: 500;
    }
  }
  
  .tags-cell {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    
    .tag-item {
      margin: 2px;
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
  
  .knowledge-cards {
    .knowledge-card {
      margin-bottom: 20px;
      cursor: pointer;
      transition: all 0.3s ease;
      border: 1px solid var(--border-color);
      height: 100%;
      
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
          
          .more-icon {
            cursor: pointer;
            color: var(--text-tertiary);
            font-size: 18px;
            
            &:hover {
              color: var(--text-primary);
            }
          }
        }
      }
      
      .card-content {
        padding: 16px;
        
        .doc-title {
          font-size: 16px;
          font-weight: 600;
          color: var(--text-primary);
          margin: 0 0 12px 0;
          line-height: 1.4;
        }
        
        .doc-description {
          font-size: 14px;
          color: var(--text-secondary);
          margin: 0 0 16px 0;
          line-height: 1.5;
        }
        
        .doc-info {
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
        
        .doc-tags {
          display: flex;
          flex-wrap: wrap;
          gap: 4px;
          
          .tag-item {
            margin: 2px;
          }
          
          .more-tags {
            font-size: 12px;
            color: var(--text-tertiary);
            align-self: center;
            margin-left: 4px;
          }
        }
      }
      
      :deep(.el-card__footer) {
        padding: 12px 16px;
        border-top: 1px solid var(--border-color);
        
        .card-footer {
          .create-time {
            font-size: 12px;
            color: var(--text-tertiary);
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
  
  .knowledge-cards {
    .el-col {
      width: 100%;
    }
  }
}
</style>