<template>
  <div class="dashboard-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">仪表盘</h1>
      <div class="page-actions">
        <el-button type="primary" :icon="Refresh" @click="refreshData">刷新数据</el-button>
        <el-button :icon="Download" @click="exportDashboard">导出报表</el-button>
      </div>
    </div>
    
    <!-- 统计卡片 -->
    <div class="stats-grid">
      <!-- 项目统计 -->
      <el-card class="stat-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon class="card-icon" color="#3b82f6"><DataBoard /></el-icon>
            <span class="card-title">项目统计</span>
          </div>
        </template>
        <div class="card-content">
          <div class="stat-number">{{ stats.projects?.total || 0 }}</div>
          <div class="stat-label">总项目数</div>
          <div class="stat-details">
            <div class="stat-item">
              <span class="stat-item-label">进行中</span>
              <span class="stat-item-value">{{ stats.projects?.active || 0 }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-item-label">已上线</span>
              <span class="stat-item-value">{{ stats.projects?.online || 0 }}</span>
            </div>
          </div>
        </div>
      </el-card>
      
      <!-- 云资产统计 -->
      <el-card class="stat-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon class="card-icon" color="#10b981"><Cloudy /></el-icon>
            <span class="card-title">云资产统计</span>
          </div>
        </template>
        <div class="card-content">
          <div class="stat-number">{{ stats.cloudAssets?.total || 0 }}</div>
          <div class="stat-label">总资产数</div>
          <div class="stat-details">
            <div class="stat-item">
              <span class="stat-item-label">运行中</span>
              <span class="stat-item-value">{{ stats.cloudAssets?.running || 0 }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-item-label">阿里云</span>
              <span class="stat-item-value">{{ stats.cloudAssets?.aliyun || 0 }}</span>
            </div>
          </div>
        </div>
      </el-card>
      
      <!-- SOW统计 -->
      <el-card class="stat-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon class="card-icon" color="#f59e0b"><DocumentCopy /></el-icon>
            <span class="card-title">SOW统计</span>
          </div>
        </template>
        <div class="card-content">
          <div class="stat-number">{{ stats.sows?.total || 0 }}</div>
          <div class="stat-label">总文档数</div>
          <div class="stat-details">
            <div class="stat-item">
              <span class="stat-item-label">已批准</span>
              <span class="stat-item-value">{{ stats.sows?.approved || 0 }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-item-label">审核中</span>
              <span class="stat-item-value">{{ stats.sows?.reviewing || 0 }}</span>
            </div>
          </div>
        </div>
      </el-card>
      
      <!-- SLA统计 -->
      <el-card class="stat-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon class="card-icon" color="#8b5cf6"><Setting /></el-icon>
            <span class="card-title">SLA统计</span>
          </div>
        </template>
        <div class="card-content">
          <div class="stat-number">{{ stats.slas?.total || 0 }}</div>
          <div class="stat-label">总协议数</div>
          <div class="stat-details">
            <div class="stat-item">
              <span class="stat-item-label">有效</span>
              <span class="stat-item-value">{{ stats.slas?.active || 0 }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-item-label">平均可用率</span>
              <span class="stat-item-value">{{ stats.slas?.avgAvailability || 0 }}%</span>
            </div>
          </div>
        </div>
      </el-card>
    </div>
    
    <!-- 图表区域 -->
    <div class="charts-grid">
      <!-- 项目状态分布 -->
      <el-card class="chart-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span class="card-title">项目状态分布</span>
          </div>
        </template>
        <div class="chart-container">
          <div v-if="loading" class="chart-loading">
            <el-icon class="loading-icon"><Loading /></el-icon>
            <span>加载中...</span>
          </div>
          <div v-else-if="projectStatusData.length === 0" class="chart-empty">
            <el-icon><PieChart /></el-icon>
            <span>暂无数据</span>
          </div>
          <div v-else ref="projectStatusChart" class="chart-content"></div>
        </div>
      </el-card>
      
      <!-- 云资产类型分布 -->
      <el-card class="chart-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span class="card-title">云资产类型分布</span>
          </div>
        </template>
        <div class="chart-container">
          <div v-if="loading" class="chart-loading">
            <el-icon class="loading-icon"><Loading /></el-icon>
            <span>加载中...</span>
          </div>
          <div v-else-if="cloudAssetTypeData.length === 0" class="chart-empty">
            <el-icon><PieChart /></el-icon>
            <span>暂无数据</span>
          </div>
          <div v-else ref="cloudAssetTypeChart" class="chart-content"></div>
        </div>
      </el-card>
    </div>
    
    <!-- 最近活动 -->
    <div class="recent-activities">
      <el-card shadow="hover">
        <template #header>
          <div class="card-header">
            <span class="card-title">最近活动</span>
          </div>
        </template>
        <div class="activities-list">
          <div v-if="loading" class="activities-loading">
            <el-icon class="loading-icon"><Loading /></el-icon>
            <span>加载中...</span>
          </div>
          <div v-else-if="activities.length === 0" class="activities-empty">
            <el-icon><List /></el-icon>
            <span>暂无活动记录</span>
          </div>
          <div v-else class="activities-items">
            <div 
              v-for="activity in activities" 
              :key="activity.id" 
              class="activity-item"
            >
              <div class="activity-icon">
                <el-icon :color="getActivityColor(activity.type)">
                  <component :is="getActivityIcon(activity.type)" />
                </el-icon>
              </div>
              <div class="activity-content">
                <div class="activity-title">{{ activity.title }}</div>
                <div class="activity-description">{{ activity.description }}</div>
                <div class="activity-time">{{ formatTime(activity.time) }}</div>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>
    
    <!-- 快速操作 -->
    <div class="quick-actions">
      <el-card shadow="hover">
        <template #header>
          <div class="card-header">
            <span class="card-title">快速操作</span>
          </div>
        </template>
        <div class="actions-grid">
          <div class="action-item" @click="router.push('/projects/create')">
            <el-icon class="action-icon"><Plus /></el-icon>
            <span class="action-label">创建项目</span>
          </div>
          <div class="action-item" @click="router.push('/cloud-assets/create')">
            <el-icon class="action-icon"><Cloudy /></el-icon>
            <span class="action-label">添加云资产</span>
          </div>
          <div class="action-item" @click="router.push('/sows/create')">
            <el-icon class="action-icon"><DocumentAdd /></el-icon>
            <span class="action-label">上传SOW</span>
          </div>
          <div class="action-item" @click="router.push('/knowledge/create')">
            <el-icon class="action-icon"><Notebook /></el-icon>
            <span class="action-label">添加文档</span>
          </div>
          <div class="action-item" @click="handleExportProjects">
            <el-icon class="action-icon"><Download /></el-icon>
            <span class="action-label">导出项目</span>
          </div>
          <div class="action-item" @click="handleViewReports">
            <el-icon class="action-icon"><DataAnalysis /></el-icon>
            <span class="action-label">查看报表</span>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import dayjs from 'dayjs'
import {
  Refresh,
  Download,
  DataBoard,
  Cloudy,
  DocumentCopy,
  Setting,
  Loading,
  PieChart,
  List,
  Plus,
  DocumentAdd,
  Notebook,
  DataAnalysis,
  Document,
  User,
  Check,
  Warning,
  InfoFilled
} from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { useAppStore } from '@/store/app'

const router = useRouter()
const userStore = useUserStore()
const appStore = useAppStore()

// 图表引用
const projectStatusChart = ref<HTMLElement>()
const cloudAssetTypeChart = ref<HTMLElement>()

// 图表实例
let projectStatusChartInstance: echarts.ECharts | null = null
let cloudAssetTypeChartInstance: echarts.ECharts | null = null

// 状态
const loading = ref(true)
const stats = ref({
  projects: {
    total: 0,
    active: 0,
    online: 0
  },
  cloudAssets: {
    total: 0,
    running: 0,
    aliyun: 0
  },
  sows: {
    total: 0,
    approved: 0,
    reviewing: 0
  },
  slas: {
    total: 0,
    active: 0,
    avgAvailability: 0
  }
})

// 图表数据
const projectStatusData = ref<Array<{ name: string; value: number }>>([])
const cloudAssetTypeData = ref<Array<{ name: string; value: number }>>([])

// 活动数据
const activities = ref([
  {
    id: '1',
    type: 'project',
    title: '新项目创建',
    description: '项目"OA系统升级"已创建',
    time: new Date(Date.now() - 3600000)
  },
  {
    id: '2',
    type: 'sow',
    title: 'SOW上传',
    description: 'SOW文档"客户服务协议"已上传',
    time: new Date(Date.now() - 7200000)
  },
  {
    id: '3',
    type: 'cloud',
    title: '云资产添加',
    description: '新增阿里云ECS实例',
    time: new Date(Date.now() - 10800000)
  },
  {
    id: '4',
    type: 'sla',
    title: 'SLA更新',
    description: 'SLA"服务等级协议"已更新',
    time: new Date(Date.now() - 14400000)
  },
  {
    id: '5',
    type: 'knowledge',
    title: '文档添加',
    description: '技术文档"API接口规范"已添加',
    time: new Date(Date.now() - 18000000)
  }
])

// 获取活动图标
const getActivityIcon = (type: string) => {
  switch (type) {
    case 'project': return Document
    case 'sow': return DocumentCopy
    case 'cloud': return Cloudy
    case 'sla': return Setting
    case 'knowledge': return Notebook
    default: return InfoFilled
  }
}

// 获取活动颜色
const getActivityColor = (type: string) => {
  switch (type) {
    case 'project': return '#3b82f6'
    case 'sow': return '#f59e0b'
    case 'cloud': return '#10b981'
    case 'sla': return '#8b5cf6'
    case 'knowledge': return '#ef4444'
    default: return '#6b7280'
  }
}

// 格式化时间
const formatTime = (time: Date) => {
  return dayjs(time).fromNow()
}

// 初始化图表
const initCharts = () => {
  // 销毁现有图表
  if (projectStatusChartInstance) {
    projectStatusChartInstance.dispose()
  }
  if (cloudAssetTypeChartInstance) {
    cloudAssetTypeChartInstance.dispose()
  }

  // 初始化项目状态图表
  if (projectStatusChart.value && projectStatusData.value.length > 0) {
    projectStatusChartInstance = echarts.init(projectStatusChart.value)
    
    const option = {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        right: 10,
        top: 'center',
        textStyle: {
          color: 'var(--text-secondary)'
        }
      },
      series: [
        {
          name: '项目状态',
          type: 'pie',
          radius: ['40%', '70%'],
          center: ['40%', '50%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: 'var(--bg-card)',
            borderWidth: 2
          },
          label: {
            show: false,
            position: 'center'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: '16',
              fontWeight: 'bold',
              color: 'var(--text-primary)'
            }
          },
          labelLine: {
            show: false
          },
          data: projectStatusData.value,
          color: [
            '#3b82f6', // planning
            '#10b981', // in_progress
            '#f59e0b', // testing
            '#8b5cf6', // online
            '#ef4444', // maintenance
            '#6b7280'  // archived
          ]
        }
      ]
    }
    
    projectStatusChartInstance.setOption(option)
  }

  // 初始化云资产类型图表
  if (cloudAssetTypeChart.value && cloudAssetTypeData.value.length > 0) {
    cloudAssetTypeChartInstance = echarts.init(cloudAssetTypeChart.value)
    
    const option = {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        right: 10,
        top: 'center',
        textStyle: {
          color: 'var(--text-secondary)'
        }
      },
      series: [
        {
          name: '云资产类型',
          type: 'pie',
          radius: ['40%', '70%'],
          center: ['40%', '50%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: 'var(--bg-card)',
            borderWidth: 2
          },
          label: {
            show: false,
            position: 'center'
          },
          emphasis: {
            label: {
              show: true,
              fontSize: '16',
              fontWeight: 'bold',
              color: 'var(--text-primary)'
            }
          },
          labelLine: {
            show: false
          },
          data: cloudAssetTypeData.value,
          color: [
            '#3b82f6', // ECS
            '#10b981', // RDS
            '#f59e0b', // OSS
            '#8b5cf6', // VPC
            '#ef4444', // SLB
            '#6b7280'  // Others
          ]
        }
      ]
    }
    
    cloudAssetTypeChartInstance.setOption(option)
  }
}

// 加载数据
const loadData = async () => {
  try {
    loading.value = true
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 模拟数据
    stats.value = {
      projects: {
        total: 24,
        active: 8,
        online: 12
      },
      cloudAssets: {
        total: 156,
        running: 142,
        aliyun: 89
      },
      sows: {
        total: 45,
        approved: 32,
        reviewing: 5
      },
      slas: {
        total: 18,
        active: 15,
        avgAvailability: 99.5
      }
    }
    
    // 模拟图表数据
    projectStatusData.value = [
      { name: '规划中', value: 4 },
      { name: '进行中', value: 8 },
      { name: '测试中', value: 3 },
      { name: '已上线', value: 12 },
      { name: '维护中', value: 2 },
      { name: '已归档', value: 1 }
    ]
    
    cloudAssetTypeData.value = [
      { name: 'ECS', value: 56 },
      { name: 'RDS', value: 32 },
      { name: 'OSS', value: 28 },
      { name: 'VPC', value: 18 },
      { name: 'SLB', value: 12 },
      { name: '其他', value: 10 }
    ]
    
    // 初始化图表
    await nextTick()
    initCharts()
    
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// 刷新数据
const refreshData = () => {
  loadData()
  ElMessage.success('数据已刷新')
}

// 导出仪表盘
const exportDashboard = () => {
  ElMessage.info('导出功能开发中...')
}

// 导出项目
const handleExportProjects = () => {
  ElMessage.info('项目导出功能开发中...')
}

// 查看报表
const handleViewReports = () => {
  ElMessage.info('报表查看功能开发中...')
}

// 窗口大小变化时重绘图表
const handleResize = () => {
  if (projectStatusChartInstance) {
    projectStatusChartInstance.resize()
  }
  if (cloudAssetTypeChartInstance) {
    cloudAssetTypeChartInstance.resize()
  }
}

// 生命周期钩子
onMounted(() => {
  // 加载数据
  loadData()
  
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
  
  // 设置页面标题
  appStore.setPageTitle('仪表盘')
})

onUnmounted(() => {
  // 销毁图表实例
  if (projectStatusChartInstance) {
    projectStatusChartInstance.dispose()
  }
  if (cloudAssetTypeChartInstance) {
    cloudAssetTypeChartInstance.dispose()
  }
  
  // 移除事件监听
  window.removeEventListener('resize', handleResize)
})
</script>

<style lang="scss" scoped>
.dashboard-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

// 页面标题
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  
  .page-title {
    font-size: 24px;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
  }
  
  .page-actions {
    display: flex;
    gap: 12px;
  }
}

// 统计卡片网格
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.stat-card {
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg) !important;
  }
  
  :deep(.el-card__header) {
    padding: 16px 20px;
    border-bottom: 1px solid var(--border-color);
    background: var(--bg-secondary);
  }
  
  .card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    
    .card-icon {
      font-size: 20px;
    }
    
    .card-title {
      font-weight: 600;
      color: var(--text-primary);
      font-size: 16px;
    }
  }
  
  .card-content {
    padding: 20px;
    
    .stat-number {
      font-size: 36px;
      font-weight: 700;
      color: var(--text-primary);
      line-height: 1;
      margin-bottom: 8px;
    }
    
    .stat-label {
      font-size: 14px;
      color: var(--text-secondary);
      margin-bottom: 16px;
    }
    
    .stat-details {
      display: flex;
      gap: 20px;
      
      .stat-item {
        display: flex;
        flex-direction: column;
        
        .stat-item-label {
          font-size: 12px;
          color: var(--text-tertiary);
          margin-bottom: 4px;
        }
        
        .stat-item-value {
          font-size: 16px;
          font-weight: 600;
          color: var(--text-primary);
        }
      }
    }
  }
}

// 图表网格
.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.chart-card {
  border: 1px solid var(--border-color);
  
  :deep(.el-card__header) {
    padding: 16px 20px;
    border-bottom: 1px solid var(--border-color);
    background: var(--bg-secondary);
  }
  
  .card-header {
    .card-title {
      font-weight: 600;
      color: var(--text-primary);
      font-size: 16px;
    }
  }
  
  .chart-container {
    height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
    
    .chart-loading,
    .chart-empty {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: var(--text-tertiary);
      
      .loading-icon {
        font-size: 32px;
        margin-bottom: 12px;
        animation: spin 1s linear infinite;
      }
      
      .el-icon {
        font-size: 48px;
        margin-bottom: 12px;
        opacity: 0.5;
      }
    }
    
    .chart-content {
      width: 100%;
      height: 100%;
    }
  }
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

// 最近活动
.recent-activities {
  .activities-list {
    min-height: 200px;
    
    .activities-loading,
    .activities-empty {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 200px;
      color: var(--text-tertiary);
      
      .loading-icon {
        font-size: 32px;
        margin-bottom: 12px;
        animation: spin 1s linear infinite;
      }
      
      .el-icon {
        font-size: 48px;
        margin-bottom: 12px;
        opacity: 0.5;
      }
    }
    
    .activities-items {
      .activity-item {
        display: flex;
        align-items: flex-start;
        padding: 16px;
        border-bottom: 1px solid var(--border-color);
        transition: background 0.2s ease;
        
        &:last-child {
          border-bottom: none;
        }
        
        &:hover {
          background: var(--bg-hover);
        }
        
        .activity-icon {
          margin-right: 16px;
          padding: 8px;
          background: var(--bg-secondary);
          border-radius: var(--radius-md);
          
          .el-icon {
            font-size: 20px;
          }
        }
        
        .activity-content {
          flex: 1;
          
          .activity-title {
            font-weight: 500;
            color: var(--text-primary);
            margin-bottom: 4px;
            font-size: 14px;
          }
          
          .activity-description {
            font-size: 13px;
            color: var(--text-secondary);
            margin-bottom: 4px;
            line-height: 1.4;
          }
          
          .activity-time {
            font-size: 12px;
            color: var(--text-tertiary);
          }
        }
      }
    }
  }
}

// 快速操作
.quick-actions {
  .actions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
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
</style>