<template>
  <div class="project-form-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">{{ isEditMode ? '编辑项目' : '创建项目' }}</h1>
        <p class="page-subtitle">{{ isEditMode ? '修改项目信息' : '创建新的项目' }}</p>
      </div>
      <div class="header-right">
        <el-button @click="router.push('/projects')">
          返回列表
        </el-button>
      </div>
    </div>
    
    <!-- 表单内容 -->
    <el-card class="form-card" shadow="never">
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="120px"
        label-position="left"
        :disabled="loading"
      >
        <!-- 基础信息 -->
        <div class="form-section">
          <div class="section-header">
            <el-icon><Document /></el-icon>
            <span class="section-title">基础信息</span>
          </div>
          
          <el-row :gutter="24">
            <el-col :xs="24" :sm="12" :md="8">
              <el-form-item label="项目编号" prop="project_code">
                <el-input
                  v-model="formData.project_code"
                  placeholder="请输入项目编号"
                  :disabled="isEditMode"
                />
                <div class="form-hint">项目唯一标识，创建后不可修改</div>
              </el-form-item>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="8">
              <el-form-item label="项目名称" prop="project_name">
                <el-input
                  v-model="formData.project_name"
                  placeholder="请输入项目名称"
                />
              </el-form-item>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="8">
              <el-form-item label="应用名称" prop="application_name">
                <el-input
                  v-model="formData.application_name"
                  placeholder="请输入应用名称"
                />
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="24">
            <el-col :xs="24" :sm="12" :md="8">
              <el-form-item label="所属部门" prop="department">
                <el-select
                  v-model="formData.department"
                  placeholder="请选择部门"
                  filterable
                  allow-create
                >
                  <el-option
                    v-for="dept in departments"
                    :key="dept"
                    :label="dept"
                    :value="dept"
                  />
                </el-select>
              </el-form-item>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="8">
              <el-form-item label="负责人" prop="manager_id">
                <el-select
                  v-model="formData.manager_id"
                  placeholder="请选择负责人"
                  filterable
                >
                  <el-option
                    v-for="user in users"
                    :key="user.id"
                    :label="user.full_name"
                    :value="user.id"
                  >
                    <div class="user-option">
                      <el-avatar :size="24" :src="user.avatar">
                        {{ user.full_name?.charAt(0) || 'U' }}
                      </el-avatar>
                      <div class="user-info">
                        <div class="user-name">{{ user.full_name }}</div>
                        <div class="user-department">{{ user.department }}</div>
                      </div>
                    </div>
                  </el-option>
                </el-select>
              </el-form-item>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="8">
              <el-form-item label="项目状态" prop="status">
                <el-select
                  v-model="formData.status"
                  placeholder="请选择项目状态"
                >
                  <el-option
                    v-for="status in projectStatusOptions"
                    :key="status.value"
                    :label="status.label"
                    :value="status.value"
                  />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="24">
            <el-col :xs="24" :sm="12" :md="8">
              <el-form-item label="上线时间" prop="launch_date">
                <el-date-picker
                  v-model="formData.launch_date"
                  type="date"
                  placeholder="选择上线日期"
                  value-format="YYYY-MM-DD"
                  style="width: 100%"
                />
              </el-form-item>
            </el-col>
          </el-row>
        </div>
        
        <!-- 项目描述 -->
        <div class="form-section">
          <div class="section-header">
            <el-icon><Edit /></el-icon>
            <span class="section-title">项目描述</span>
          </div>
          
          <el-form-item label="项目描述" prop="description">
            <el-input
              v-model="formData.description"
              type="textarea"
              :rows="4"
              placeholder="请输入项目描述"
              maxlength="500"
              show-word-limit
            />
          </el-form-item>
          
          <el-form-item label="备注" prop="remark">
            <el-input
              v-model="formData.remark"
              type="textarea"
              :rows="2"
              placeholder="请输入备注信息"
              maxlength="200"
              show-word-limit
            />
          </el-form-item>
        </div>
        
        <!-- 表单操作 -->
        <div class="form-actions">
          <el-button @click="handleCancel">
            取消
          </el-button>
          <el-button type="primary" :loading="loading" @click="handleSubmit">
            {{ isEditMode ? '更新项目' : '创建项目' }}
          </el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { Document, Edit } from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { useAppStore } from '@/store/app'
import type { Project, ProjectCreate, ProjectUpdate } from '@/types'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const appStore = useAppStore()

// 表单引用
const formRef = ref<FormInstance>()

// 加载状态
const loading = ref(false)

// 是否为编辑模式
const isEditMode = computed(() => route.name === 'ProjectEdit')

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
  { id: 1, full_name: '张三', department: '研发部', avatar: '' },
  { id: 2, full_name: '李四', department: '产品部', avatar: '' },
  { id: 3, full_name: '王五', department: '设计部', avatar: '' },
  { id: 4, full_name: '赵六', department: '测试部', avatar: '' },
  { id: 5, full_name: '钱七', department: '运维部', avatar: '' }
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

// 表单数据
const formData = reactive<ProjectCreate & { id?: number }>({
  project_code: '',
  project_name: '',
  application_name: '',
  department: '',
  manager_id: 0,
  status: 'planning',
  launch_date: '',
  description: '',
  remark: ''
})

// 表单验证规则
const formRules: FormRules = {
  project_code: [
    { required: true, message: '请输入项目编号', trigger: 'blur' },
    { min: 3, max: 50, message: '项目编号长度在 3 到 50 个字符', trigger: 'blur' },
    { pattern: /^[A-Za-z0-9_-]+$/, message: '项目编号只能包含字母、数字、下划线和横线', trigger: 'blur' }
  ],
  project_name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' },
    { min: 2, max: 200, message: '项目名称长度在 2 到 200 个字符', trigger: 'blur' }
  ],
  application_name: [
    { required: true, message: '请输入应用名称', trigger: 'blur' },
    { min: 2, max: 200, message: '应用名称长度在 2 到 200 个字符', trigger: 'blur' }
  ],
  department: [
    { required: true, message: '请选择所属部门', trigger: 'change' }
  ],
  manager_id: [
    { required: true, message: '请选择负责人', trigger: 'change' },
    { type: 'number', min: 1, message: '请选择有效的负责人', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择项目状态', trigger: 'change' }
  ],
  launch_date: [
    { pattern: /^\d{4}-\d{2}-\d{2}$/, message: '日期格式为 YYYY-MM-DD', trigger: 'blur' }
  ],
  description: [
    { max: 500, message: '项目描述不能超过 500 个字符', trigger: 'blur' }
  ],
  remark: [
    { max: 200, message: '备注不能超过 200 个字符', trigger: 'blur' }
  ]
}

// 生成项目编号
const generateProjectCode = () => {
  const date = new Date()
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const random = Math.floor(Math.random() * 1000).toString().padStart(3, '0')
  return `P${year}${month}${day}${random}`
}

// 加载项目数据（编辑模式）
const loadProjectData = async () => {
  if (!isEditMode.value) return
  
  try {
    loading.value = true
    const projectId = Number(route.params.id)
    
    if (!projectId) {
      ElMessage.error('项目ID无效')
      router.push('/projects')
      return
    }
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 800))
    
    // 模拟数据
    const mockProject: Project = {
      id: projectId,
      project_code: 'P2024001',
      project_name: 'OA系统升级',
      application_name: 'OA系统',
      department: '研发部',
      manager_id: 1,
      status: 'in_progress',
      launch_date: '2024-06-01',
      description: '办公自动化系统升级项目',
      remark: '重要项目，需按时完成',
      created_by: 1,
      created_at: '2024-01-15T10:30:00',
      updated_at: '2024-01-15T10:30:00'
    }
    
    // 填充表单数据
    Object.assign(formData, {
      id: mockProject.id,
      project_code: mockProject.project_code,
      project_name: mockProject.project_name,
      application_name: mockProject.application_name,
      department: mockProject.department,
      manager_id: mockProject.manager_id,
      status: mockProject.status,
      launch_date: mockProject.launch_date || '',
      description: mockProject.description || '',
      remark: mockProject.remark || ''
    })
    
  } catch (error) {
    console.error('加载项目数据失败:', error)
    ElMessage.error('加载项目数据失败')
    router.push('/projects')
  } finally {
    loading.value = false
  }
}

// 处理提交
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    // 验证表单
    await formRef.value.validate()
    
    loading.value = true
    
    if (isEditMode.value) {
      // 更新项目
      await updateProject()
    } else {
      // 创建项目
      await createProject()
    }
    
  } catch (error) {
    console.error('表单验证失败:', error)
  } finally {
    loading.value = false
  }
}

// 创建项目
const createProject = async () => {
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 构建请求数据
    const requestData: ProjectCreate = {
      project_code: formData.project_code,
      project_name: formData.project_name,
      application_name: formData.application_name,
      department: formData.department,
      manager_id: formData.manager_id,
      status: formData.status,
      launch_date: formData.launch_date || undefined,
      description: formData.description || undefined,
      remark: formData.remark || undefined
    }
    
    console.log('创建项目数据:', requestData)
    
    ElMessage.success('项目创建成功')
    router.push('/projects')
    
  } catch (error) {
    console.error('创建项目失败:', error)
    ElMessage.error('创建项目失败')
  }
}

// 更新项目
const updateProject = async () => {
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 构建请求数据
    const requestData: ProjectUpdate = {
      project_name: formData.project_name,
      application_name: formData.application_name,
      department: formData.department,
      manager_id: formData.manager_id,
      status: formData.status,
      launch_date: formData.launch_date || undefined,
      description: formData.description || undefined,
      remark: formData.remark || undefined
    }
    
    console.log('更新项目数据:', requestData)
    
    ElMessage.success('项目更新成功')
    router.push('/projects')
    
  } catch (error) {
    console.error('更新项目失败:', error)
    ElMessage.error('更新项目失败')
  }
}

// 处理取消
const handleCancel = () => {
  router.push('/projects')
}

// 生命周期钩子
onMounted(() => {
  // 设置页面标题
  appStore.setPageTitle(isEditMode.value ? '编辑项目' : '创建项目')
  
  // 如果是创建模式，生成项目编号
  if (!isEditMode.value) {
    formData.project_code = generateProjectCode()
  }
  
  // 加载项目数据（编辑模式）
  loadProjectData()
})
</script>

<style lang="scss" scoped>
.project-form-container {
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
}

// 表单卡片
.form-card {
  :deep(.el-card__body) {
    padding: 30px;
  }
}

// 表单区域
.form-section {
  margin-bottom: 30px;
  padding-bottom: 30px;
  border-bottom: 1px solid var(--border-color);
  
  &:last-child {
    margin-bottom: 0;
    padding-bottom: 0;
    border-bottom: none;
  }
  
  .section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
    
    .el-icon {
      font-size: 18px;
      color: var(--primary-color);
    }
    
    .section-title {
      font-size: 18px;
      font-weight: 600;
      color: var(--text-primary);
    }
  }
}

// 表单提示
.form-hint {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-top: 4px;
  line-height: 1.4;
}

// 用户选项
.user-option {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 4px 0;
  
  .user-info {
    display: flex;
    flex-direction: column;
    
    .user-name {
      font-weight: 500;
      color: var(--text-primary);
      font-size: 14px;
    }
    
    .user-department {
      font-size: 12px;
      color: var(--text-tertiary);
    }
  }
}

// 表单操作
.form-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
  
  .el-button {
    min-width: 120px;
    height: 40px;
  }
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
  
  .form-card {
    :deep(.el-card__body) {
      padding: 20px;
    }
  }
  
  .form-actions {
    flex-direction: column;
    gap: 12px;
    
    .el-button {
      width: 100%;
    }
  }
}

@media (max-width: 480px) {
  :deep(.el-form) {
    .el-form-item {
      :deep(.el-form-item__label) {
        text-align: left;
        padding-right: 0;
        margin-bottom: 8px;
        display: block;
        width: 100% !important;
        float: none;
      }
      
      :deep(.el-form-item__content) {
        margin-left: 0 !important;
      }
    }
  }
}
</style>