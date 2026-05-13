<template>
  <div class="settings-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">系统设置</h1>
      <div class="page-actions">
        <el-button type="primary" :icon="Save" @click="handleSave" :loading="saving">保存设置</el-button>
        <el-button :icon="Refresh" @click="handleReset">重置</el-button>
      </div>
    </div>
    
    <!-- 设置内容 -->
    <div class="settings-content">
      <!-- 基础参数配置 -->
      <el-card class="settings-section" shadow="hover">
        <template #header>
          <div class="section-header">
            <el-icon class="section-icon"><Setting /></el-icon>
            <span class="section-title">基础参数配置</span>
          </div>
        </template>
        
        <el-form ref="settingsFormRef" :model="settingsForm" :rules="settingsRules" label-width="120px">
          <!-- 系统名称 -->
          <el-form-item label="系统名称" prop="systemName">
            <el-input
              v-model="settingsForm.systemName"
              placeholder="请输入系统名称"
              clearable
              style="width: 300px;"
            />
            <div class="form-tip">显示在浏览器标签页和登录页面的系统名称</div>
          </el-form-item>
          
          <!-- 系统版本 -->
          <el-form-item label="系统版本" prop="systemVersion">
            <el-input
              v-model="settingsForm.systemVersion"
              placeholder="请输入系统版本"
              clearable
              style="width: 200px;"
            />
          </el-form-item>
          
          <!-- 每页显示数量 -->
          <el-form-item label="每页显示数量" prop="pageSize">
            <el-input-number
              v-model="settingsForm.pageSize"
              :min="10"
              :max="100"
              :step="10"
              controls-position="right"
            />
            <div class="form-tip">列表页面默认每页显示的数据条数</div>
          </el-form-item>
          
          <!-- 文件上传限制 -->
          <el-form-item label="文件上传限制" prop="uploadLimit">
            <el-input-number
              v-model="settingsForm.uploadLimit"
              :min="1"
              :max="100"
              :step="1"
              controls-position="right"
            />
            <span class="unit">MB</span>
            <div class="form-tip">单个文件最大上传大小限制</div>
          </el-form-item>
          
          <!-- 数据保留天数 -->
          <el-form-item label="数据保留天数" prop="dataRetentionDays">
            <el-input-number
              v-model="settingsForm.dataRetentionDays"
              :min="30"
              :max="3650"
              :step="30"
              controls-position="right"
            />
            <div class="form-tip">日志和操作记录保留的天数</div>
          </el-form-item>
          
          <!-- 系统描述 -->
          <el-form-item label="系统描述" prop="systemDescription">
            <el-input
              v-model="settingsForm.systemDescription"
              type="textarea"
              :rows="3"
              placeholder="请输入系统描述"
              maxlength="200"
              show-word-limit
              style="width: 400px;"
            />
          </el-form-item>
        </el-form>
      </el-card>
      
      <!-- 开关选项 -->
      <el-card class="settings-section" shadow="hover">
        <template #header>
          <div class="section-header">
            <el-icon class="section-icon"><Switch /></el-icon>
            <span class="section-title">开关选项</span>
          </div>
        </template>
        
        <div class="switch-grid">
          <!-- 系统维护模式 -->
          <div class="switch-item">
            <div class="switch-label">
              <span class="label-text">系统维护模式</span>
              <span class="label-desc">开启后普通用户无法访问系统</span>
            </div>
            <el-switch
              v-model="settingsForm.maintenanceMode"
              active-text="开启"
              inactive-text="关闭"
              inline-prompt
            />
          </div>
          
          <!-- 用户注册 -->
          <div class="switch-item">
            <div class="switch-label">
              <span class="label-text">允许用户注册</span>
              <span class="label-desc">是否允许新用户自行注册账号</span>
            </div>
            <el-switch
              v-model="settingsForm.allowRegistration"
              active-text="允许"
              inactive-text="禁止"
              inline-prompt
            />
          </div>
          
          <!-- 邮件通知 -->
          <div class="switch-item">
            <div class="switch-label">
              <span class="label-text">邮件通知</span>
              <span class="label-desc">是否发送系统通知邮件</span>
            </div>
            <el-switch
              v-model="settingsForm.emailNotification"
              active-text="开启"
              inactive-text="关闭"
              inline-prompt
            />
          </div>
          
          <!-- 操作日志 -->
          <div class="switch-item">
            <div class="switch-label">
              <span class="label-text">记录操作日志</span>
              <span class="label-desc">是否记录用户操作日志</span>
            </div>
            <el-switch
              v-model="settingsForm.operationLog"
              active-text="开启"
              inactive-text="关闭"
              inline-prompt
            />
          </div>
          
          <!-- 自动备份 -->
          <div class="switch-item">
            <div class="switch-label">
              <span class="label-text">自动备份</span>
              <span class="label-desc">是否自动备份系统数据</span>
            </div>
            <el-switch
              v-model="settingsForm.autoBackup"
              active-text="开启"
              inactive-text="关闭"
              inline-prompt
            />
          </div>
          
          <!-- 数据导出 -->
          <div class="switch-item">
            <div class="switch-label">
              <span class="label-text">允许数据导出</span>
              <span class="label-desc">是否允许用户导出数据</span>
            </div>
            <el-switch
              v-model="settingsForm.allowExport"
              active-text="允许"
              inactive-text="禁止"
              inline-prompt
            />
          </div>
        </div>
      </el-card>
      
      <!-- 高级设置 -->
      <el-card class="settings-section" shadow="hover">
        <template #header>
          <div class="section-header">
            <el-icon class="section-icon"><Tools /></el-icon>
            <span class="section-title">高级设置</span>
          </div>
        </template>
        
        <el-form :model="settingsForm" label-width="120px">
          <!-- API接口地址 -->
          <el-form-item label="API接口地址">
            <el-input
              v-model="settingsForm.apiBaseUrl"
              placeholder="请输入API接口地址"
              clearable
              style="width: 400px;"
            />
            <div class="form-tip">后端API服务的基础地址</div>
          </el-form-item>
          
          <!-- 数据库连接 -->
          <el-form-item label="数据库连接">
            <el-input
              v-model="settingsForm.databaseUrl"
              type="textarea"
              :rows="2"
              placeholder="请输入数据库连接字符串"
              style="width: 400px;"
            />
            <div class="form-tip">MySQL数据库连接配置</div>
          </el-form-item>
          
          <!-- 缓存配置 -->
          <el-form-item label="缓存配置">
            <el-select v-model="settingsForm.cacheType" placeholder="请选择缓存类型" style="width: 200px;">
              <el-option label="内存缓存" value="memory" />
              <el-option label="Redis缓存" value="redis" />
              <el-option label="文件缓存" value="file" />
            </el-select>
          </el-form-item>
          
          <!-- 缓存过期时间 -->
          <el-form-item label="缓存过期时间" v-if="settingsForm.cacheType !== 'memory'">
            <el-input-number
              v-model="settingsForm.cacheExpire"
              :min="1"
              :max="1440"
              :step="10"
              controls-position="right"
            />
            <span class="unit">分钟</span>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { Save, Refresh, Setting, Switch, Tools } from '@element-plus/icons-vue'
import { useAppStore } from '@/store/app'

const appStore = useAppStore()

// 表单引用
const settingsFormRef = ref<FormInstance>()

// 保存状态
const saving = ref(false)

// 表单数据
const settingsForm = reactive({
  // 基础参数
  systemName: '企业项目管理平台',
  systemVersion: '1.0.0',
  pageSize: 20,
  uploadLimit: 10,
  dataRetentionDays: 365,
  systemDescription: '统一管理项目全生命周期信息，包含知识库、SOW、SLA、云平台资产等核心资产',
  
  // 开关选项
  maintenanceMode: false,
  allowRegistration: false,
  emailNotification: true,
  operationLog: true,
  autoBackup: true,
  allowExport: true,
  
  // 高级设置
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || '/api',
  databaseUrl: '',
  cacheType: 'memory',
  cacheExpire: 30
})

// 表单验证规则
const settingsRules: FormRules = {
  systemName: [
    { required: true, message: '请输入系统名称', trigger: 'blur' },
    { min: 2, max: 50, message: '系统名称长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  systemVersion: [
    { required: true, message: '请输入系统版本', trigger: 'blur' },
    { pattern: /^\d+\.\d+\.\d+$/, message: '版本号格式为 x.x.x', trigger: 'blur' }
  ],
  pageSize: [
    { required: true, message: '请输入每页显示数量', trigger: 'blur' }
  ],
  uploadLimit: [
    { required: true, message: '请输入文件上传限制', trigger: 'blur' }
  ],
  dataRetentionDays: [
    { required: true, message: '请输入数据保留天数', trigger: 'blur' }
  ]
}

// 加载设置
const loadSettings = () => {
  // 这里应该调用API加载设置
  // 暂时使用模拟数据
  console.log('加载系统设置')
}

// 保存设置
const handleSave = async () => {
  if (!settingsFormRef.value) return
  
  try {
    // 验证表单
    await settingsFormRef.value.validate()
    
    saving.value = true
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 这里应该调用API保存设置
    console.log('保存设置:', settingsForm)
    
    ElMessage.success('设置保存成功')
    
  } catch (error) {
    console.error('保存设置失败:', error)
    ElMessage.error('保存设置失败')
  } finally {
    saving.value = false
  }
}

// 重置设置
const handleReset = () => {
  if (settingsFormRef.value) {
    settingsFormRef.value.resetFields()
    ElMessage.info('设置已重置')
  }
}

// 生命周期钩子
onMounted(() => {
  // 加载设置
  loadSettings()
  
  // 设置页面标题
  appStore.setPageTitle('系统设置')
})
</script>

<style lang="scss" scoped>
.settings-container {
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

// 设置内容
.settings-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

// 设置区块
.settings-section {
  border: 1px solid var(--border-color);
  
  :deep(.el-card__header) {
    padding: 16px 20px;
    border-bottom: 1px solid var(--border-color);
    background: var(--bg-secondary);
  }
  
  .section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    
    .section-icon {
      font-size: 18px;
      color: var(--primary-color);
    }
    
    .section-title {
      font-weight: 600;
      color: var(--text-primary);
      font-size: 16px;
    }
  }
  
  :deep(.el-card__body) {
    padding: 24px;
  }
}

// 表单样式
:deep(.el-form-item) {
  margin-bottom: 20px;
  
  &:last-child {
    margin-bottom: 0;
  }
  
  .el-form-item__label {
    font-weight: 500;
    color: var(--text-primary);
  }
  
  .form-tip {
    font-size: 12px;
    color: var(--text-tertiary);
    margin-top: 4px;
    line-height: 1.4;
  }
  
  .unit {
    margin-left: 8px;
    color: var(--text-secondary);
    font-size: 14px;
  }
}

// 开关网格
.switch-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.switch-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  transition: all 0.3s ease;
  
  &:hover {
    background: var(--bg-hover);
    border-color: var(--primary-color);
  }
  
  .switch-label {
    display: flex;
    flex-direction: column;
    gap: 4px;
    
    .label-text {
      font-weight: 500;
      color: var(--text-primary);
      font-size: 14px;
    }
    
    .label-desc {
      font-size: 12px;
      color: var(--text-tertiary);
      line-height: 1.4;
    }
  }
  
  :deep(.el-switch) {
    .el-switch__core {
      border-color: var(--border-color);
      background-color: var(--bg-tertiary);
    }
    
    &.is-checked {
      .el-switch__core {
        border-color: var(--primary-color);
        background-color: var(--primary-color);
      }
    }
  }
}
</style>