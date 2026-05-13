<template>
  <div class="sla-form-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">{{ isEditMode ? '编辑SLA' : '创建SLA' }}</h1>
        <p class="page-subtitle">{{ isEditMode ? '修改服务等级协议信息' : '创建新的服务等级协议' }}</p>
      </div>
      <div class="header-right">
        <el-button :icon="ArrowLeft" @click="handleBack">
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
          <div class="section-title">
            <el-icon><InfoFilled /></el-icon>
            <span>基础信息</span>
          </div>
          
          <el-row :gutter="24">
            <el-col :xs="24" :sm="12" :md="12" :lg="8">
              <el-form-item label="关联项目" prop="project_id">
                <el-select
                  v-model="formData.project_id"
                  placeholder="请选择项目"
                  filterable
                  clearable
                  style="width: 100%"
                >
                  <el-option
                    v-for="project in projects"
                    :key="project.id"
                    :label="`${project.project_code} - ${project.project_name}`"
                    :value="project.id"
                  />
                </el-select>
              </el-form-item>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="12" :lg="8">
              <el-form-item label="协议名称" prop="agreement_name">
                <el-input
                  v-model="formData.agreement_name"
                  placeholder="请输入协议名称"
                  clearable
                />
              </el-form-item>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="12" :lg="8">
              <el-form-item label="状态" prop="status">
                <el-select
                  v-model="formData.status"
                  placeholder="请选择状态"
                  style="width: 100%"
                >
                  <el-option
                    v-for="status in statusOptions"
                    :key="status.value"
                    :label="status.label"
                    :value="status.value"
                  />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="24">
            <el-col :xs="24" :sm="12" :md="12" :lg="8">
              <el-form-item label="生效日期" prop="effective_date">
                <el-date-picker
                  v-model="formData.effective_date"
                  type="date"
                  placeholder="请选择生效日期"
                  style="width: 100%"
                  value-format="YYYY-MM-DD"
                />
              </el-form-item>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="12" :lg="8">
              <el-form-item label="到期日期" prop="expiry_date">
                <el-date-picker
                  v-model="formData.expiry_date"
                  type="date"
                  placeholder="请选择到期日期"
                  style="width: 100%"
                  value-format="YYYY-MM-DD"
                />
              </el-form-item>
            </el-col>
          </el-row>
        </div>
        
        <!-- 服务指标 -->
        <div class="form-section">
          <div class="section-title">
            <el-icon><Setting /></el-icon>
            <span>服务指标</span>
          </div>
          
          <el-row :gutter="24">
            <el-col :xs="24" :sm="12" :md="12" :lg="8">
              <el-form-item label="服务可用率" prop="availability">
                <el-input
                  v-model="formData.availability"
                  placeholder="请输入可用率"
                  clearable
                >
                  <template #append>%</template>
                </el-input>
                <div class="form-tip">
                  <el-icon><InfoFilled /></el-icon>
                  <span>例如：99.9 表示 99.9% 的可用率</span>
                </div>
              </el-form-item>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="12" :lg="8">
              <el-form-item label="响应时效" prop="response_time">
                <el-input
                  v-model="formData.response_time"
                  placeholder="请输入响应时效"
                  clearable
                >
                  <template #append>小时</template>
                </el-input>
                <div class="form-tip">
                  <el-icon><InfoFilled /></el-icon>
                  <span>从收到请求到开始处理的时间</span>
                </div>
              </el-form-item>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="12" :lg="8">
              <el-form-item label="故障处理时限" prop="fault_resolution_time">
                <el-input
                  v-model="formData.fault_resolution_time"
                  placeholder="请输入故障处理时限"
                  clearable
                >
                  <template #append>小时</template>
                </el-input>
                <div class="form-tip">
                  <el-icon><InfoFilled /></el-icon>
                  <span>从故障发生到解决的时间</span>
                </div>
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="24">
            <el-col :span="24">
              <el-form-item label="维护窗口" prop="maintenance_window">
                <el-input
                  v-model="formData.maintenance_window"
                  type="textarea"
                  :rows="2"
                  placeholder="请输入维护窗口时间，例如：每周日 02:00-04:00"
                  maxlength="200"
                  show-word-limit
                />
              </el-form-item>
            </el-col>
          </el-row>
        </div>
        
        <!-- 违约条款 -->
        <div class="form-section">
          <div class="section-title">
            <el-icon><Warning /></el-icon>
            <span>违约条款</span>
          </div>
          
          <el-row :gutter="24">
            <el-col :span="24">
              <el-form-item label="违约条款" prop="penalty_terms">
                <el-input
                  v-model="formData.penalty_terms"
                  type="textarea"
                  :rows="4"
                  placeholder="请输入违约条款内容"
                  maxlength="1000"
                  show-word-limit
                />
              </el-form-item>
            </el-col>
          </el-row>
        </div>
        
        <!-- 备注信息 -->
        <div class="form-section">
          <div class="section-title">
            <el-icon><Comment /></el-icon>
            <span>备注信息</span>
          </div>
          
          <el-row :gutter="24">
            <el-col :span="24">
              <el-form-item label="备注" prop="remarks">
                <el-input
                  v-model="formData.remarks"
                  type="textarea"
                  :rows="3"
                  placeholder="请输入备注信息"
                  maxlength="500"
                  show-word-limit
                />
              </el-form-item>
            </el-col>
          </el-row>
        </div>
        
        <!-- 表单操作 -->
        <div class="form-actions">
          <el-button :icon="ArrowLeft" @click="handleBack">
            取消
          </el-button>
          <el-button
            type="primary"
            :icon="isEditMode ? Check : Plus"
            :loading="submitting"
            @click="handleSubmit"
          >
            {{ isEditMode ? '保存修改' : '创建SLA' }}
          </el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import {
  ArrowLeft,
  InfoFilled,
  Setting,
  Warning,
  Comment,
  Check,
  Plus
} from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { useAppStore } from '@/store/app'
import dayjs from 'dayjs'
import type { SLA } from '@/types'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const appStore = useAppStore()

// 表单引用
const formRef = ref<FormInstance>()

// 状态
const loading = ref(false)
const submitting = ref(false)
const isEditMode = computed(() => !!route.params.id)

// 表单数据
const formData = reactive({
  project_id: '',
  agreement_name: '',
  availability: '',
  response_time: '',
  fault_resolution_time: '',
  maintenance_window: '',
  penalty_terms: '',
  status: 'draft',
  effective_date: '',
  expiry_date: '',
  remarks: ''
})

// 表单验证规则
const formRules: FormRules = {
  project_id: [
    { required: true, message: '请选择关联项目', trigger: 'change' }
  ],
  agreement_name: [
    { required: true, message: '请输入协议名称', trigger: 'blur' }
  ],
  availability: [
    { required: true, message: '请输入服务可用率', trigger: 'blur' },
    { 
      pattern: /^(100|[1-9]?\d(\.\d{1,2})?)$/,
      message: '请输入0-100之间的数字，最多两位小数',
      trigger: 'blur'
    }
  ],
  response_time: [
    { 
      pattern: /^\d+(\.\d{1,2})?$/,
      message: '请输入有效的数字，最多两位小数',
      trigger: 'blur'
    }
  ],
  fault_resolution_time: [
    { 
      pattern: /^\d+(\.\d{1,2})?$/,
      message: '请输入有效的数字，最多两位小数',
      trigger: 'blur'
    }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ],
  effective_date: [
    { required: true, message: '请选择生效日期', trigger: 'change' }
  ],
  expiry_date: [
    { required: true, message: '请选择到期日期', trigger: 'change' }
  ]
}

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

// 处理返回
const handleBack = () => {
  router.push('/slas')
}

// 处理提交
const handleSubmit = async () => {
  try {
    // 验证表单
    const valid = await formRef.value?.validate()
    if (!valid) return
    
    // 验证日期
    if (formData.effective_date && formData.expiry_date) {
      const effectiveDate = dayjs(formData.effective_date)
      const expiryDate = dayjs(formData.expiry_date)
      
      if (expiryDate.isBefore(effectiveDate)) {
        ElMessage.error('到期日期不能早于生效日期')
        return
      }
    }
    
    // 验证可用率
    const availability = parseFloat(formData.availability)
    if (availability < 0 || availability > 100) {
      ElMessage.error('可用率必须在0-100之间')
      return
    }
    
    submitting.value = true
    
    // 准备提交数据
    const submitData = {
      ...formData,
      availability: availability,
      response_time: formData.response_time ? parseFloat(formData.response_time) : null,
      fault_resolution_time: formData.fault_resolution_time ? parseFloat(formData.fault_resolution_time) : null,
      created_by: userStore.userInfo?.id
    }
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    if (isEditMode.value) {
      // 编辑模式
      ElMessage.success('SLA更新成功')
    } else {
      // 创建模式
      ElMessage.success('SLA创建成功')
    }
    
    // 返回列表页
    router.push('/slas')
    
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('提交失败，请重试')
  } finally {
    submitting.value = false
  }
}

// 加载数据（编辑模式）
const loadData = async () => {
  if (!isEditMode.value) return
  
  try {
    loading.value = true
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 800))
    
    // 模拟数据
    const mockData = {
      id: 1,
      project_id: 1,
      agreement_name: 'OA系统SLA',
      availability: 99.9,
      response_time: 4,
      fault_resolution_time: 8,
      maintenance_window: '每周日 02:00-04:00',
      penalty_terms: '服务不达标按合同约定赔偿',
      status: 'active',
      effective_date: '2024-01-01',
      expiry_date: '2024-12-31',
      remarks: 'OA系统服务等级协议'
    }
    
    // 填充表单数据
    Object.assign(formData, {
      project_id: mockData.project_id,
      agreement_name: mockData.agreement_name,
      availability: mockData.availability.toString(),
      response_time: mockData.response_time?.toString() || '',
      fault_resolution_time: mockData.fault_resolution_time?.toString() || '',
      maintenance_window: mockData.maintenance_window,
      penalty_terms: mockData.penalty_terms,
      status: mockData.status,
      effective_date: mockData.effective_date,
      expiry_date: mockData.expiry_date,
      remarks: mockData.remarks
    })
    
  } catch (error) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// 生命周期钩子
onMounted(() => {
  // 设置页面标题
  appStore.setPageTitle(isEditMode.value ? '编辑SLA' : '创建SLA')
  
  // 加载数据
  loadData()
})
</script>

<style lang="scss" scoped>
.sla-form-container {
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
    padding: 24px;
  }
}

// 表单区块
.form-section {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--border-color);
  
  &:last-child {
    margin-bottom: 0;
    padding-bottom: 0;
    border-bottom: none;
  }
  
  .section-title {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 20px;
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    
    .el-icon {
      color: var(--primary-color);
    }
  }
}

// 表单提示
.form-tip {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 8px;
  font-size: 12px;
  color: var(--text-tertiary);
  
  .el-icon {
    font-size: 12px;
  }
}

// 表单操作
.form-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  padding-top: 24px;
  border-top: 1px solid var(--border-color);
  
  .el-button {
    min-width: 120px;
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
  
  .form-actions {
    flex-direction: column;
    
    .el-button {
      width: 100%;
    }
  }
}
</style>