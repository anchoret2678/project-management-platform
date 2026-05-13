<template>
  <div class="sow-form-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">{{ isEditMode ? '编辑SOW' : '创建SOW' }}</h1>
        <p class="page-subtitle">{{ isEditMode ? '修改SOW文档信息' : '上传新的工作说明书文档' }}</p>
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
              <el-form-item label="文档名称" prop="document_name">
                <el-input
                  v-model="formData.document_name"
                  placeholder="请输入文档名称"
                  clearable
                />
              </el-form-item>
            </el-col>
            
            <el-col :xs="24" :sm="12" :md="12" :lg="8">
              <el-form-item label="版本号" prop="version">
                <el-input
                  v-model="formData.version"
                  placeholder="请输入版本号，如：1.0"
                  clearable
                />
              </el-form-item>
            </el-col>
          </el-row>
          
          <el-row :gutter="24">
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
        </div>
        
        <!-- 文件上传 -->
        <div class="form-section">
          <div class="section-title">
            <el-icon><UploadFilled /></el-icon>
            <span>文件上传</span>
          </div>
          
          <el-row :gutter="24">
            <el-col :span="24">
              <el-form-item label="SOW文档" prop="file">
                <el-upload
                  ref="uploadRef"
                  class="upload-demo"
                  drag
                  :action="uploadUrl"
                  :headers="uploadHeaders"
                  :data="uploadData"
                  :multiple="false"
                  :limit="1"
                  :on-success="handleUploadSuccess"
                  :on-error="handleUploadError"
                  :on-exceed="handleUploadExceed"
                  :on-remove="handleUploadRemove"
                  :before-upload="beforeUpload"
                  :file-list="fileList"
                  :disabled="isEditMode && formData.file_path"
                >
                  <el-icon class="el-icon--upload"><upload-filled /></el-icon>
                  <div class="el-upload__text">
                    拖拽文件到此处或 <em>点击上传</em>
                  </div>
                  <template #tip>
                    <div class="el-upload__tip">
                      支持 PDF、Word、Excel 格式，文件大小不超过 50MB
                    </div>
                  </template>
                </el-upload>
                
                <!-- 已上传文件信息 -->
                <div v-if="formData.file_path" class="uploaded-file-info">
                  <div class="file-info">
                    <el-icon class="file-icon"><Document /></el-icon>
                    <div class="file-details">
                      <div class="file-name">{{ formData.file_name }}</div>
                      <div class="file-meta">
                        <span class="file-size">{{ formatFileSize(formData.file_size || 0) }}</span>
                        <span class="file-type">{{ getFileTypeLabel(formData.file_type || '') }}</span>
                      </div>
                    </div>
                  </div>
                  <div class="file-actions" v-if="!isEditMode">
                    <el-button
                      type="danger"
                      link
                      :icon="Delete"
                      @click="handleRemoveFile"
                    >
                      移除
                    </el-button>
                  </div>
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
                  :rows="4"
                  placeholder="请输入备注信息"
                  maxlength="1000"
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
            {{ isEditMode ? '保存修改' : '创建SOW' }}
          </el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules, type UploadInstance, type UploadRawFile } from 'element-plus'
import {
  ArrowLeft,
  InfoFilled,
  UploadFilled,
  Comment,
  Check,
  Plus,
  Document,
  Delete
} from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { useAppStore } from '@/store/app'
import type { SOW } from '@/types'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const appStore = useAppStore()

// 表单引用
const formRef = ref<FormInstance>()
const uploadRef = ref<UploadInstance>()

// 状态
const loading = ref(false)
const submitting = ref(false)
const isEditMode = computed(() => !!route.params.id)

// 表单数据
const formData = reactive({
  project_id: '',
  document_name: '',
  version: '',
  file_path: '',
  file_name: '',
  file_size: 0,
  file_type: '',
  status: 'draft',
  remarks: ''
})

// 文件列表
const fileList = ref<any[]>([])

// 上传配置
const uploadUrl = ref('/api/sows/upload') // 实际项目中替换为真实API地址
const uploadHeaders = ref({
  Authorization: `Bearer ${userStore.token}`
})
const uploadData = ref({
  project_id: '',
  document_name: '',
  version: ''
})

// 表单验证规则
const formRules: FormRules = {
  project_id: [
    { required: true, message: '请选择关联项目', trigger: 'change' }
  ],
  document_name: [
    { required: true, message: '请输入文档名称', trigger: 'blur' }
  ],
  version: [
    { required: true, message: '请输入版本号', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ],
  file: [
    { 
      required: true, 
      validator: (rule: any, value: any, callback: any) => {
        if (!isEditMode.value && !formData.file_path) {
          callback(new Error('请上传SOW文档'))
        } else {
          callback()
        }
      },
      trigger: 'change'
    }
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
  { value: 'reviewing', label: '审核中' },
  { value: 'approved', label: '已批准' },
  { value: 'rejected', label: '已拒绝' },
  { value: 'archived', label: '已归档' }
])

// 获取文件类型标签
const getFileTypeLabel = (fileType: string) => {
  const typeMap: Record<string, string> = {
    pdf: 'PDF',
    docx: 'Word',
    doc: 'Word',
    xlsx: 'Excel',
    xls: 'Excel',
    pptx: 'PPT',
    ppt: 'PPT',
    txt: '文本'
  }
  return typeMap[fileType] || fileType.toUpperCase()
}

// 格式化文件大小
const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 上传前验证
const beforeUpload = (file: UploadRawFile) => {
  // 检查文件类型
  const allowedTypes = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  ]
  
  const isAllowedType = allowedTypes.includes(file.type)
  const isLt50M = file.size / 1024 / 1024 < 50
  
  if (!isAllowedType) {
    ElMessage.error('只支持 PDF、Word、Excel 格式的文件')
    return false
  }
  
  if (!isLt50M) {
    ElMessage.error('文件大小不能超过 50MB')
    return false
  }
  
  // 更新上传数据
  uploadData.value.project_id = formData.project_id
  uploadData.value.document_name = formData.document_name
  uploadData.value.version = formData.version
  
  return true
}

// 上传成功处理
const handleUploadSuccess = (response: any, file: any) => {
  if (response.code === 200) {
    const fileData = response.data
    formData.file_path = fileData.file_path
    formData.file_name = fileData.file_name
    formData.file_size = fileData.file_size
    formData.file_type = fileData.file_type
    
    ElMessage.success('文件上传成功')
  } else {
    ElMessage.error(response.message || '文件上传失败')
  }
}

// 上传失败处理
const handleUploadError = (error: Error) => {
  console.error('上传失败:', error)
  ElMessage.error('文件上传失败，请重试')
}

// 文件超出限制
const handleUploadExceed = () => {
  ElMessage.warning('只能上传一个文件，请先移除已上传的文件')
}

// 文件移除处理
const handleUploadRemove = () => {
  formData.file_path = ''
  formData.file_name = ''
  formData.file_size = 0
  formData.file_type = ''
}

// 手动移除文件
const handleRemoveFile = () => {
  handleUploadRemove()
  if (uploadRef.value) {
    uploadRef.value.clearFiles()
  }
}

// 处理返回
const handleBack = () => {
  router.push('/sows')
}

// 处理提交
const handleSubmit = async () => {
  try {
    // 验证表单
    const valid = await formRef.value?.validate()
    if (!valid) return
    
    // 检查文件（创建模式下）
    if (!isEditMode.value && !formData.file_path) {
      ElMessage.error('请上传SOW文档')
      return
    }
    
    submitting.value = true
    
    // 准备提交数据
    const submitData = {
      ...formData,
      uploaded_by: userStore.userInfo?.id
    }
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    if (isEditMode.value) {
      // 编辑模式
      ElMessage.success('SOW更新成功')
    } else {
      // 创建模式
      ElMessage.success('SOW创建成功')
    }
    
    // 返回列表页
    router.push('/sows')
    
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
      document_name: 'OA系统升级SOW',
      version: '1.0',
      file_path: '/uploads/sows/oa-upgrade-sow-v1.0.pdf',
      file_name: 'oa-upgrade-sow-v1.0.pdf',
      file_size: 2048576,
      file_type: 'pdf',
      status: 'approved',
      remarks: 'OA系统升级工作说明书'
    }
    
    // 填充表单数据
    Object.assign(formData, {
      project_id: mockData.project_id,
      document_name: mockData.document_name,
      version: mockData.version,
      file_path: mockData.file_path,
      file_name: mockData.file_name,
      file_size: mockData.file_size,
      file_type: mockData.file_type,
      status: mockData.status,
      remarks: mockData.remarks
    })
    
    // 设置文件列表
    if (mockData.file_path) {
      fileList.value = [{
        name: mockData.file_name,
        url: mockData.file_path
      }]
    }
    
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
  appStore.setPageTitle(isEditMode.value ? '编辑SOW' : '创建SOW')
  
  // 加载数据
  loadData()
})
</script>

<style lang="scss" scoped>
.sow-form-container {
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

// 上传组件
:deep(.upload-demo) {
  .el-upload {
    width: 100%;
    
    .el-upload-dragger {
      width: 100%;
      padding: 40px 20px;
      background: var(--bg-secondary);
      border: 2px dashed var(--border-color);
      border-radius: var(--radius-lg);
      
      &:hover {
        border-color: var(--primary-color);
      }
      
      .el-icon--upload {
        font-size: 48px;
        color: var(--text-tertiary);
        margin-bottom: 16px;
      }
      
      .el-upload__text {
        color: var(--text-secondary);
        font-size: 14px;
        
        em {
          color: var(--primary-color);
          font-style: normal;
        }
      }
    }
  }
  
  .el-upload__tip {
    margin-top: 12px;
    font-size: 12px;
    color: var(--text-tertiary);
  }
}

// 已上传文件信息
.uploaded-file-info {
  margin-top: 16px;
  padding: 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  .file-info {
    display: flex;
    align-items: center;
    gap: 12px;
    
    .file-icon {
      font-size: 24px;
      color: var(--primary-color);
    }
    
    .file-details {
      .file-name {
        font-weight: 500;
        color: var(--text-primary);
        margin-bottom: 4px;
        font-size: 14px;
      }
      
      .file-meta {
        display: flex;
        gap: 12px;
        font-size: 12px;
        color: var(--text-tertiary);
      }
    }
  }
  
  .file-actions {
    .el-button {
      padding: 2px 0;
    }
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
  
  .uploaded-file-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    
    .file-actions {
      align-self: flex-end;
    }
  }
}
</style>