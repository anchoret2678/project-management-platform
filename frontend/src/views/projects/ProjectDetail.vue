<template>
  <div class="project-detail-container">
    <!-- 页面标题和操作 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">项目详情</h1>
        <div class="project-basic">
          <el-tag type="info" size="large">{{ projectData.project_code }}</el-tag>
          <h2 class="project-name">{{ projectData.project_name }}</h2>
          <p class="project-application">{{ projectData.application_name }}</p>
        </div>
      </div>
      <div class="header-right">
        <el-button-group>
          <el-button @click="router.push('/projects')">
            返回列表
          </el-button>
          <el-button type="primary" :icon="Edit" @click="handleEdit" v-if="isAdmin">
            编辑项目
          </el-button>
          <el-button type="danger" :icon="Delete" @click="handleDelete" v-if="isAdmin">
            删除项目
          </el-button>
        </el-button-group>
      </div>
    </div>
    
    <!-- 项目状态和基本信息 -->
    <el-row :gutter="20" class="project-overview">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="overview-card" shadow="hover">
          <div class="overview-item">
            <div class="overview-label">项目状态</div>
            <div class="overview-value">
              <el-tag :type="getStatusType(projectData.status)" size="large">
                {{ getStatusLabel(projectData.status) }}
              </el-tag>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="overview-card" shadow="hover">
          <div class="overview-item">
            <div class="overview-label">所属部门</div>
            <div class="overview-value">{{ projectData.department }}</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="overview-card" shadow="hover">
          <div class="overview-item">
            <div class="overview-label">负责人</div>
            <div class="overview-value">
              <div class="manager-info">
                <el-avatar :size="32" :src="projectData.manager_avatar">
                  {{ projectData.manager_name?.charAt(0) || 'U' }}
                </el-avatar>
                <span class="manager-name">{{ projectData.manager_name }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="overview-card" shadow="hover">
          <div class="overview-item">
            <div class="overview-label">上线时间</div>
            <div class="overview-value">
              <span v-if="projectData.launch_date">{{ formatDate(projectData.launch_date) }}</span>
              <span v-else class="text-muted">未设置</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 项目详情标签页 -->
    <el-tabs v-model="activeTab" class="project-tabs">
      <!-- 基本信息 -->
      <el-tab-pane label="基本信息" name="basic">
        <el-card shadow="never">
          <div class="info-section">
            <h3 class="section-title">项目描述</h3>
            <div class="section-content">
              <p v-if="projectData.description" class="description-text">
                {{ projectData.description }}
              </p>
              <p v-else class="text-muted">暂无项目描述</p>
            </div>
          </div>
          
          <div class="info-section">
            <h3 class="section-title">备注信息</h3>
            <div class="section-content">
              <p v-if="projectData.remark" class="remark-text">
                {{ projectData.remark }}
              </p>
              <p v-else class="text-muted">暂无备注信息</p>
            </div>
          </div>
          
          <div class="info-section">
            <h3 class="section-title">项目信息</h3>
            <div class="info-grid">
              <div class="info-item">
                <div class="info-label">创建人</div>
                <div class="info-value">{{ projectData.creator_name || '系统' }}</div>
              </div>
              <div class="info-item">
                <div class="info-label">创建时间</div>
                <div class="info-value">{{ formatDateTime(projectData.created_at) }}</div>
              </div>
              <div class="info-item">
                <div class="info-label">更新时间</div>
                <div class="info-value">{{ formatDateTime(projectData.updated_at) }}</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-tab-pane>
      
      <!-- 关联资产 -->
      <el-tab-pane label="关联资产" name="assets">
        <el-row :gutter="20">
          <!-- 云资产统计 -->
          <el-col :xs="24" :sm="12" :md="6">
            <el-card class="asset-card" shadow="hover" @click="router.push('/cloud-assets')">
              <div class="asset-content">
                <div class="asset-icon">
                  <el-icon color="#3b82f6" size="32"><Cloudy /></el-icon>
                </div>
                <div class="asset-info">
                  <div class="asset-count">{{ projectData.cloud_assets_count || 0 }}</div>
                  <div class="asset-label">云资产</div>
                </div>
              </div>
            </el-card>
          </el-col>
          
          <!-- SOW统计 -->
          <el-col :xs="24" :sm="12" :md="6">
            <el-card class="asset-card" shadow="hover" @click="router.push('/sows')">
              <div class="asset-content">
                <div class="asset-icon">
                  <el-icon color="#f59e0b" size="32"><DocumentCopy /></el-icon>
                </div>
                <div class="asset-info">
                  <div class="asset-count">{{ projectData.sows_count || 0 }}</div>
                  <div class="asset-label">SOW文档</div>
                </div>
              </div>
            </el-card>
          </el-col>
          
          <!-- SLA统计 -->
          <el-col :xs="24" :sm="12" :md="6">
            <el-card class="asset-card" shadow="hover" @click="router.push('/slas')">
              <div class="asset-content">
                <div class="asset-icon">
                  <el-icon color="#8b5cf6" size="32"><Setting /></el-icon>
                </div>
                <div class="asset-info">
                  <div class="asset-count">{{ projectData.slas_count || 0 }}</div>
                  <div class="asset-label">SLA协议</div>
                </div>
              </div>
            </el-card>
          </el-col>
          
          <!-- 知识库统计 -->
          <el-col :xs="24" :sm="12" :md="6">
            <el-card class="asset-card" shadow="hover" @click="router.push('/knowledge')">
              <div class="asset-content">
                <div class="asset-icon">
                  <el-icon color="#10b981" size="32"><Notebook /></el-icon>
                </div>
                <div class="asset-info">
                  <div class="asset-count">{{ projectData.knowledge_documents_count || 0 }}</div>
                  <div class="asset-label">知识库文档</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        
        <!-- 快速操作 -->
        <el-card class="quick-actions-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span class="card-title">快速操作</span>
            </div>
          </template>
          <div class="actions-grid">
            <div class="action-item" @click="router.push('/cloud-assets/create')" v-if="isAdmin">
              <el-icon class="action-icon"><Plus /></el-icon>
              <span class="action-label">添加云资产</span>
            </div>
            <div class="action-item" @click="router.push('/sows/create')" v-if="isAdmin">
              <el-icon class="action-icon"><DocumentAdd /></el-icon>
              <span class="action-label">上传SOW</span>
            </div>
            <div class="action-item" @click="router.push('/slas/create')" v-if="isAdmin">
              <el-icon class="action-icon"><Setting /></el-icon>
              <span class="action-label">创建SLA</span>
            </div>
            <div class="action-item" @click="router.push('/knowledge/create')" v-if="isAdmin">
              <el-icon class="action-icon"><Notebook /></el-icon>
              <span class="action-label">添加文档</span>
            </div>
          </div>
        </el-card>
      </el-tab-pane>
      
      <!-- 项目时间线 -->
      <el-tab-pane label="时间线" name="timeline">
        <el-card shadow="never">
          <div class="timeline-container">
            <div v-if="timelineEvents.length === 0" class="timeline-empty">
              <el-icon><Clock /></el-icon>
              <p>暂无时间线记录</p>
            </div>
            
            <el-timeline v-else>
              <el-timeline-item
                v-for="event in timelineEvents"
                :key="event.id"
                :timestamp="formatDateTime(event.time)"
                :type="event.type"
                :icon="getTimelineIcon(event.type)"
                :color="getTimelineColor(event.type)"
                placement="top"
              >
                <el-card shadow="hover">
                  <div class="timeline-event">
                    <div class="event-header">
                      <h4 class="event-title">{{ event.title }}</h4>
                      <el-tag :type="event.type" size="small">{{ getEventTypeLabel(event.type) }}</el-tag>
                    </div>
                    <div class="event-content">
                      <p>{{ event.description }}</p>
                    </div>
                    <div class="event-footer">
                      <span class="event-user">{{ event.user }}</span>
                    </div>
                  </div>
                </el-card>
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Edit,
  Delete,
  Cloudy,
  DocumentCopy,
  Setting,
  Notebook,
  Plus,
  DocumentAdd,
  Clock,
  Check,
  Warning,
  InfoFilled,
  User
} from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { useAppStore } from '@/store/app'
import dayjs from 'dayjs'
import type { Project } from '@/types'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const appStore = useAppStore()

// 活动标签页
const activeTab = ref('basic')

// 项目数据
const projectData = ref<Project & {
  cloud_assets_count?: number
  sows_count?: number
  slas_count?: number
  knowledge_documents_count?: number
  manager_avatar?: string
  creator_name?: string
}>({
  id: 0,
  project_code: '',
  project_name: '',
  application_name: '',
  department: '',
  manager_id: 0,
  manager_name: '',
  status: 'planning',
  launch_date: '',
  description: '',
  remark: '',
  created_by: 0,
  created_at: '',
  updated_at: '',
  cloud_assets_count: 0,
  sows_count: 0,
  slas_count: 0,
  knowledge_documents_count: 0
})

// 时间线事件
const timelineEvents = ref([
  {
    id: '1',
    type: 'primary',
    title: '项目创建',
    description: '项目正式创建并分配负责人',
    time: '2024-01-15T10:30:00',
    user: '系统管理员'
  },
  {
    id: '2',
    type: 'success',
    title: '需求评审通过',
    description: '项目需求文档通过评审，进入开发阶段',
    time: '2024-01-20T14:20:00',
    user: '产品经理'
  },
  {
    id: '3',
    type: 'warning',
    title: '技术方案调整',
    description: '根据技术评估调整了系统架构方案',
    time: '2024-01-25T09:15:00',
    user: '技术负责人'
  },
  {
    id: '4',
    type: 'info',
    title: 'SOW文档上传',
    description: '项目工作说明书已上传并审核通过',
    time: '2024-02-01T11:30:00',
    user: '项目经理'
  },
  {
    id: '5',
    type: 'success',
    title: '开发完成',
    description: '主要功能开发完成，进入测试阶段',
    time: '2024-02-28T16:45:00',
    user: '开发团队'
  }
])

// 计算属性
const isAdmin = computed(() => userStore.isAdmin)

// 获取状态标签
const getStatusLabel = (status: string) => {
  const statusMap: Record<string, string> = {
    planning: '规划中',
    in_progress: '进行中',
    testing: '测试中',
    online: '已上线',
    maintenance: '维护中',
    archived: '已归档'
  }
  return statusMap[status] || status
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

// 获取时间线图标
const getTimelineIcon = (type: string) => {
  const iconMap: Record<string, any> = {
    primary: Check,
    success: Check,
    warning: Warning,
    danger: Warning,
    info: InfoFilled
  }
  return iconMap[type] || InfoFilled
}

// 获取时间线颜色
const getTimelineColor = (type: string) => {
  const colorMap: Record<string, string> = {
    primary: '#3b82f6',
    success: '#10b981',
    warning: '#f59e0b',
    danger: '#ef4444',
    info: '#6b7280'
  }
  return colorMap[type] || '#6b7280'
}

// 获取事件类型标签
const getEventTypeLabel = (type: string) => {
  const labelMap: Record<string, string> = {
    primary: '创建',
    success: '完成',
    warning: '调整',
    danger: '问题',
    info: '信息'
  }
  return labelMap[type] || '事件'
}

// 加载项目数据
const loadProjectData = async () => {
  try {
    const projectId = Number(route.params.id)
    
    if (!projectId) {
      ElMessage.error('项目ID无效')
      router.push('/projects')
      return
    }
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 800))
    
    // 模拟数据
    const mockProject = {
      id: projectId,
      project_code: 'P2024001',
      project_name: 'OA系统升级',
      application_name: 'OA系统',
      department: '研发部',
      manager_id: 1,
      manager_name: '张三',
      manager_avatar: '',
      status: 'in_progress',
      launch_date: '2024-06-01',
      description: '办公自动化系统升级项目，旨在提升办公效率，优化工作流程。项目包括前端界面重构、后端服务优化、数据库迁移等核心工作。',
      remark: '重要项目，需按时完成。需要重点关注系统性能和用户体验。',
      created_by: 1,
      creator_name: '系统管理员',
      created_at: '2024-01-15T10:30:00',
      updated_at: '2024-01-15T10:30:00',
      cloud_assets_count: 5,
      sows_count: 2,
      slas_count: 1,
      knowledge_documents_count: 8
    }
    
    projectData.value = mockProject
    
    // 设置页面标题
    appStore.setPageTitle(`${mockProject.project_name} - 项目详情`)
    
  } catch (error) {
    console.error('加载项目数据失败:', error)
    ElMessage.error('加载项目数据失败')
    router.push('/projects')
  }
}

// 处理编辑
const handleEdit = () => {
  router.push(`/projects/${projectData.value.id}/edit`)
}

// 处理删除
const handleDelete = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要删除项目 "${projectData.value.project_name}" 吗？此操作不可恢复，且会删除所有关联数据。`,
      '确认删除',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 模拟删除操作
    await new Promise(resolve => setTimeout(resolve, 800))
    
    ElMessage.success('项目删除成功')
    router.push('/projects')
    
  } catch (error) {
    // 用户取消删除
  }
}

// 生命周期钩子
onMounted(() => {
  loadProjectData()
})
</script>

<style lang="scss" scoped>
.project-detail-container {
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
      margin: 0 0 16px 0;
    }
    
    .project-basic {
      .project-name {
        font-size: 20px;
        font-weight: 600;
        color: var(--text-primary);
        margin: 12px 0 8px 0;
      }
      
      .project-application {
        font-size: 16px;
        color: var(--text-secondary);
        margin: 0;
      }
    }
  }
  
  .header-right {
    .el-button-group {
      display: flex;
      gap: 8px;
    }
  }
}

// 项目概览
.project-overview {
  margin-bottom: 20px;
  
  .overview-card {
    height: 100%;
    border: 1px solid var(--border-color);
    
    :deep(.el-card__body) {
      padding: 20px;
    }
    
    .overview-item {
      .overview-label {
        font-size: 14px;
        color: var(--text-tertiary);
        margin-bottom: 8px;
      }
      
      .overview-value {
        font-size: 16px;
        font-weight: 500;
        color: var(--text-primary);
        
        .manager-info {
          display: flex;
          align-items: center;
          gap: 10px;
          
          .manager-name {
            font-weight: 500;
          }
        }
        
        .text-muted {
          color: var(--text-tertiary);
          font-style: italic;
        }
      }
    }
  }
}

// 项目标签页
.project-tabs {
  :deep(.el-tabs__header) {
    margin-bottom: 20px;
  }
  
  :deep(.el-tabs__item) {
    font-weight: 500;
  }
}

// 基本信息
.info-section {
  margin-bottom: 30px;
  
  &:last-child {
    margin-bottom: 0;
  }
  
  .section-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border-color);
  }
  
  .section-content {
    .description-text,
    .remark-text {
      line-height: 1.6;
      color: var(--text-secondary);
      margin: 0;
    }
    
    .text-muted {
      color: var(--text-tertiary);
      font-style: italic;
    }
  }
  
  .info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    
    .info-item {
      .info-label {
        font-size: 14px;
        color: var(--text-tertiary);
        margin-bottom: 4px;
      }
      
      .info-value {
        font-size: 16px;
        font-weight: 500;
        color: var(--text-primary);
      }
    }
  }
}

// 关联资产卡片
.asset-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid var(--border-color);
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg) !important;
    border-color: var(--primary-color);
  }
  
  :deep(.el-card__body) {
    padding: 20px;
  }
  
  .asset-content {
    display: flex;
    align-items: center;
    gap: 16px;
    
    .asset-info {
      .asset-count {
        font-size: 28px;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
        margin-bottom: 4px;
      }
      
      .asset-label {
        font-size: 14px;
        color: var(--text-secondary);
      }
    }
  }
}

// 快速操作
.quick-actions-card {
  margin-top: 20px;
  
  :deep(.el-card__header) {
    padding: 16px 20px;
    border-bottom: 1px solid var(--border-color);
    background: var(--bg-secondary);
    
    .card-header {
      .card-title {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 16px;
      }
    }
  }
  
  .actions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    padding: 20px;
    
    @media (max-width: 768px) {
      grid-template-columns: repeat(2, 1fr);
    }
    
    @media (max-width: 480px) {
      grid-template-columns: 1fr;
    }
    
    .action-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 24px 16px;
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      cursor: pointer;
      transition: all 0.3s ease;
      
      &:hover {
        background: var(--bg-hover);
        border-color: var(--primary-color);
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
        
        .action-icon {
          color: var(--primary-color);
          transform: scale(1.1);
        }
        
        .action-label {
          color: var(--primary-color);
        }
      }
      
      .action-icon {
        font-size: 32px;
        color: var(--text-secondary);
        margin-bottom: 12px;
        transition: all 0.3s ease;
      }
      
      .action-label {
        font-weight: 500;
        color: var(--text-primary);
        text-align: center;
        transition: color 0.3s ease;
      }
    }
  }
}

// 时间线
.timeline-container {
  .timeline-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 20px;
    color: var(--text-tertiary);
    
    .el-icon {
      font-size: 48px;
      margin-bottom: 16px;
      opacity: 0.5;
    }
    
    p {
      margin: 0;
      font-size: 14px;
    }
  }
  
  :deep(.el-timeline) {
    padding-left: 20px;
    
    .el-timeline-item {
      padding-bottom: 20px;
      
      &:last-child {
        padding-bottom: 0;
      }
      
      .el-timeline-item__node {
        width: 12px;
        height: 12px;
      }
      
      .el-timeline-item__wrapper {
        .el-timeline-item__timestamp {
          color: var(--text-tertiary);
          font-size: 13px;
          margin-bottom: 8px;
        }
        
        .el-card {
          border: 1px solid var(--border-color);
          
          :deep(.el-card__body) {
            padding: 16px;
          }
          
          .timeline-event {
            .event-header {
              display: flex;
              justify-content: space-between;
              align-items: flex-start;
              margin-bottom: 12px;
              
              .event-title {
                font-size: 16px;
                font-weight: 600;
                color: var(--text-primary);
                margin: 0;
                flex: 1;
                margin-right: 12px;
              }
            }
            
            .event-content {
              p {
                margin: 0;
                color: var(--text-secondary);
                line-height: 1.6;
                font-size: 14px;
              }
            }
            
            .event-footer {
              margin-top: 12px;
              padding-top: 8px;
              border-top: 1px solid var(--border-color);
              
              .event-user {
                font-size: 12px;
                color: var(--text-tertiary);
              }
            }
          }
        }
      }
    }
  }
}

// 响应式调整
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
    
    .header-right {
      width: 100%;
      
      .el-button-group {
        width: 100%;
        flex-direction: column;
        
        .el-button {
          width: 100%;
        }
      }
    }
  }
  
  .project-overview {
    .el-col {
      margin-bottom: 16px;
      
      &:last-child {
        margin-bottom: 0;
      }
    }
  }
}
</style>