<template>
  <div class="cloud-asset-form-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">{{ isEditMode ? '编辑云资产' : '创建云资产' }}</h1>
        <p class="page-subtitle">{{ isEditMode ? '修改云资产信息' : '添加新的云平台资源资产' }}</p>
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
              <el-form-item label="云厂商" prop="cloud_provider">
                <el-select
                  v-model="formData.cloud_provider"
                  placeholder="请选择云厂商"
                  style="width: 100%"
                  @change="handleProviderChange"
                >
                  <el-option
                    v-for="provider in cloudProviderOptions"
                    :key="provider.value"
                    :label="provider.label"
                    :value="provider.value"
                  />
                </el-select>
              </el-form-item>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="12" :lg="8">
              <el-form-item label="资源类型" prop="resource_type">
                <el-select
                  v-model="formData.resource_type"
                  placeholder="请选择资源类型"
                  style="width: 100%"
                >
                  <el-option
                    v-for="type in resourceTypeOptions"
                    :key="type.value"
                    :label="type.label"
                    :value="type.value"
                  />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="24">
            <el-col :xs="24" :sm="12" :md="12" :lg="8">
              <el-form-item label="实例规格" prop="instance_spec">
                <el-input
                  v-model="formData.instance_spec"
                  placeholder="请输入实例规格"
                  clearable
                />
              </el-form-item>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="12" :lg="8">
              <el-form-item label="地域" prop="region">
                <el-input
                  v-model="formData.region"
                  placeholder="请输入地域"
                  clearable
                />
              </el-form-item>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="12" :lg="8">
              <el-form-item label="可用区" prop="zone">
                <el-input
                  v-model="formData.zone"
                  placeholder="请输入可用区"
                  clearable
                />
              </el-form-item>
            </el-col>
          </el-row>
        </div>
        
        <!-- 配置信息 -->
        <div class="form-section">
          <div class="section-title">
            <el-icon><Setting /></el-icon>
            <span>配置信息</span>
          </div>
          
          <el-row :gutter="24">
            <el-col :xs="24" :sm="12" :md="12" :lg="8">
              <el-form-item label="账号信息" prop="account_info">
                <el-input
                  v-model="formData.account_info"
                  placeholder="请输入账号信息"
                  clearable
                />
              </el-form-item>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="12" :lg="8">
              <el-form-item label="IP地址" prop="ip_address">
                <el-input
                  v-model="formData.ip_address"
                  placeholder="请输入IP地址"
                  clearable
                />
              </el-form-item>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="12" :lg="8">
              <el-form-item label="生命周期" prop="lifecycle">
                <el-select
                  v-model="formData.lifecycle"
                  placeholder="请选择生命周期"
                  style="width: 100%"
                >
                  <el-option
                    v-for="lifecycle in lifecycleOptions"
                    :key="lifecycle.value"
                    :label="lifecycle.label"
                    :value="lifecycle.value"
                  />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="24">
            <el-col :span="24">
              <el-form-item label="配置JSON" prop="config_json">
                <el-input
                  v-model="formData.config_json_str"
                  type="textarea"
                  :rows="6"
                  placeholder="请输入JSON配置信息"
                  @input="handleConfigJsonInput"
                />
                <div class="form-tip">
                  <el-icon><InfoFilled /></el-icon>
                  <span>请输入有效的JSON格式配置信息</span>
                </div>
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
            {{ isEditMode ? '保存修改' : '创建资产' }}
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
  Comment,
  Check,
  Plus
} from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { useAppStore } from '@/store/app'
import type { CloudAsset } from '@/types'

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
  cloud_provider: '',
  resource_type: '',
  instance_spec: '',
  region: '',
  zone: '',
  account_info: '',
  ip_address: '',
  lifecycle: 'running',
  config_json_str: '{}',
  remarks: ''
})

// 表单验证规则
const formRules: FormRules = {
  project_id: [
    { required: true, message: '请选择关联项目', trigger: 'change' }
  ],
  cloud_provider: [
    { required: true, message: '请选择云厂商', trigger: 'change' }
  ],
  resource_type: [
    { required: true, message: '请选择资源类型', trigger: 'change' }
  ],
  instance_spec: [
    { required: true, message: '请输入实例规格', trigger: 'blur' }
  ],
  region: [
    { required: true, message: '请输入地域', trigger: 'blur' }
  ],
  lifecycle: [
    { required: true, message: '请选择生命周期', trigger: 'change' }
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

// 云厂商选项
const cloudProviderOptions = ref([
  { value: 'aliyun', label: '阿里云' },
  { value: 'huawei', label: '华为云' },
  { value: 'tencent', label: '腾讯云' },
  { value: 'self_built', label: '自建机房' }
])

// 资源类型选项
const resourceTypeOptions = ref([
  { value: 'ECS', label: '云服务器 (ECS)' },
  { value: 'RDS', label: '关系型数据库 (RDS)' },
  { value: 'OSS', label: '对象存储 (OSS)' },
  { value: 'SLB', label: '负载均衡 (SLB)' },
  { value: 'VPC', label: '虚拟私有云 (VPC)' },
  { value: 'CDN', label: '内容分发网络 (CDN)' },
  { value: 'WAF', label: 'Web应用防火墙 (WAF)' },
  { value: 'DDoS', label: 'DDoS防护' },
  { value: '物理服务器', label: '物理服务器' },
  { value: '其他', label: '其他' }
])

// 生命周期选项
const lifecycleOptions = ref([
  { value: 'creating', label: '创建中' },
  { value: 'running', label: '运行中' },
  { value: 'stopped', label: '已停止' },
  { value: 'deleting', label: '删除中' },
  { value: 'deleted', label: '已删除' }
])

// 处理云厂商变更
const handleProviderChange = (value: string) => {
  // 根据云厂商设置默认地域
  if (value === 'aliyun') {
    formData.region = 'cn-hangzhou'
  } else if (value === 'huawei') {
    formData.region = 'cn-north-4'
  } else if (value === 'tencent') {
    formData.region = 'ap-guangzhou'
  } else if (value === 'self_built') {
    formData.region = '本地机房'
  }
}

// 处理JSON配置输入
const handleConfigJsonInput = (value: string) => {
  try {
    // 尝试解析JSON
    if (value.trim()) {
      JSON.parse(value)
    }
  } catch (error) {
    // JSON格式错误，不更新
  }
}

// 处理返回
const handleBack = () => {
  router.push('/cloud-assets')
}

// 处理提交
const handleSubmit = async () => {
  try {
    // 验证表单
    const valid = await formRef.value?.validate()
    if (!valid) return
    
    // 验证JSON配置
    let configJson = {}
    if (formData.config_json_str.trim()) {
      try {
        configJson = JSON.parse(formData.config_json_str)
      } catch (error) {
        ElMessage.error('JSON配置格式错误，请检查')
        return
      }
    }
    
    submitting.value = true
    
    // 准备提交数据
    const submitData = {
      ...formData,
      config_json: configJson,
      created_by: userStore.userInfo?.id
    }
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    if (isEditMode.value) {
      // 编辑模式
      ElMessage.success('云资产更新成功')
    } else {
      // 创建模式
      ElMessage.success('云资产创建成功')
    }
    
    // 返回列表页
    router.push('/cloud-assets')
    
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
      cloud_provider: 'aliyun',
      resource_type: 'ECS',
      instance_spec: 'ecs.g6.large',
      region: 'cn-hangzhou',
      zone: 'cn-hangzhou-h',
      account_info: 'test-account',
      ip_address: '192.168.1.100',
      config_json: { cpu: 2, memory: 4, disk: 50 },
      lifecycle: 'running',
      remarks: '测试云服务器'
    }
    
    // 填充表单数据
    Object.assign(formData, {
      project_id: mockData.project_id,
      cloud_provider: mockData.cloud_provider,
      resource_type: mockData.resource_type,
      instance_spec: mockData.instance_spec,
      region: mockData.region,
      zone: mockData.zone,
      account_info: mockData.account_info,
      ip_address: mockData.ip_address,
      lifecycle: mockData.lifecycle,
      config_json_str: JSON.stringify(mockData.config_json, null, 2),
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
  appStore.setPageTitle(isEditMode.value ? '编辑云资产' : '创建云资产')
  
  // 加载数据
  loadData()
})
</script>

<style lang="scss" scoped>
.cloud-asset-form-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

// 页���标题
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