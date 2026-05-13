<template>
  <div class="profile-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">个人中心</h1>
        <p class="page-subtitle">管理您的个人信息和账户设置</p>
      </div>
    </div>
    
    <!-- 主要内容 -->
    <div class="profile-content">
      <!-- 左侧：个人信息 -->
      <div class="left-column">
        <el-card class="profile-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="card-title">个人信息</span>
            </div>
          </template>
          
          <div class="profile-info">
            <!-- 头像区域 -->
            <div class="avatar-section">
              <div class="avatar-container">
                <el-avatar :size="120" :src="userInfo.avatar" class="user-avatar">
                  {{ getAvatarText(userInfo.full_name) }}
                </el-avatar>
                <div class="avatar-actions">
                  <el-button type="primary" link :icon="Edit" @click="handleAvatarEdit">
                    更换头像
                  </el-button>
                </div>
              </div>
            </div>
            
            <!-- 基本信息 -->
            <div class="info-section">
              <div class="info-item">
                <span class="info-label">用户名</span>
                <span class="info-value">{{ userInfo.username }}</span>
              </div>
              
              <div class="info-item">
                <span class="info-label">姓名</span>
                <span class="info-value">{{ userInfo.full_name }}</span>
              </div>
              
              <div class="info-item">
                <span class="info-label">邮箱</span>
                <span class="info-value">{{ userInfo.email }}</span>
              </div>
              
              <div class="info-item">
                <span class="info-label">角色</span>
                <el-tag :type="getRoleType(userInfo.role)" size="small">
                  {{ getRoleLabel(userInfo.role) }}
                </el-tag>
              </div>
              
              <div class="info-item">
                <span class="info-label">部门</span>
                <span class="info-value">{{ userInfo.department || '未设置' }}</span>
              </div>
              
              <div class="info-item">
                <span class="info-label">电话</span>
                <span class="info-value">{{ userInfo.phone || '未设置' }}</span>
              </div>
              
              <div class="info-item">
                <span class="info-label">账户状态</span>
                <el-tag :type="userInfo.is_active ? 'success' : 'danger'" size="small">
                  {{ userInfo.is_active ? '启用' : '禁用' }}
                </el-tag>
              </div>
              
              <div class="info-item">
                <span class="info-label">最后登录</span>
                <span class="info-value">{{ formatDateTime(userInfo.last_login) }}</span>
              </div>
              
              <div class="info-item">
                <span class="info-label">注册时间</span>
                <span class="info-value">{{ formatDateTime(userInfo.created_at) }}</span>
              </div>
            </div>
            
            <!-- 操作按钮 -->
            <div class="action-section">
              <el-button type="primary" :icon="Edit" @click="handleEditProfile">
                编辑个人信息
              </el-button>
            </div>
          </div>
        </el-card>
      </div>
      
      <!-- 右侧：账户设置 -->
      <div class="right-column">
        <!-- 修改密码 -->
        <el-card class="settings-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="card-title">修改密码</span>
            </div>
          </template>
          
          <el-form
            ref="passwordFormRef"
            :model="passwordForm"
            :rules="passwordRules"
            label-width="100px"
            label-position="left"
            :disabled="passwordLoading"
          >
            <el-form-item label="当前密码" prop="current_password">
              <el-input
                v-model="passwordForm.current_password"
                type="password"
                placeholder="请输入当前密码"
                show-password
              />
            </el-form-item>
            
            <el-form-item label="新密码" prop="new_password">
              <el-input
                v-model="passwordForm.new_password"
                type="password"
                placeholder="请输入新密码"
                show-password
              />
            </el-form-item>
            
            <el-form-item label="确认密码" prop="confirm_password">
              <el-input
                v-model="passwordForm.confirm_password"
                type="password"
                placeholder="请再次输入新密码"
                show-password
              />
            </el-form-item>
            
            <el-form-item>
              <el-button
                type="primary"
                :icon="Key"
                :loading="passwordLoading"
                @click="handleChangePassword"
              >
                修改密码
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
        
        <!-- 账户安全 -->
        <el-card class="settings-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="card-title">账户安全</span>
            </div>
          </template>
          
          <div class="security-settings">
            <div class="security-item">
              <div class="security-info">
                <el-icon class="security-icon"><Lock /></el-icon>
                <div class="security-details">
                  <div class="security-title">登录密码</div>
                  <div class="security-description">定期修改密码以保证账户安全</div>
                </div>
              </div>
              <div class="security-status">
                <el-tag type="success" size="small">已设置</el-tag>
              </div>
            </div>
            
            <div class="security-item">
              <div class="security-info">
                <el-icon class="security-icon"><Bell /></el-icon>
                <div class="security-details">
                  <div class="security-title">登录通知</div>
                  <div class="security-description">开启后，新设备登录时会发送通知</div>
                </div>
              </div>
              <div class="security-status">
                <el-switch v-model="securitySettings.login_notification" />
              </div>
            </div>
            
            <div class="security-item">
              <div class="security-info">
                <el-icon class="security-icon"><Clock /></el-icon>
                <div class="security-details">
                  <div class="security-title">会话管理</div>
                  <div class="security-description">管理您的登录会话</div>
                </div>
              </div>
              <div class="security-status">
                <el-button type="primary" link @click="handleSessionManage">
                  查看
                </el-button>
              </div>
            </div>
          </div>
        </el-card>
        
        <!-- 系统偏好 -->
        <el-card class="settings-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="card-title">系统偏好</span>
            </div>
          </template>
          
          <div class="preference-settings">
            <div class="preference-item">
              <div class="preference-info">
                <div class="preference-title">界面主题</div>
                <div class="preference-description">选择您喜欢的界面主题</div>
              </div>
              <div class="preference-control">
                <el-select v-model="preferenceSettings.theme" size="small">
                  <el-option label="深色主题" value="dark" />
                  <el-option label="浅色主题" value="light" />
                  <el-option label="自动" value="auto" />
                </el-select>
              </div>
            </div>
            
            <div class="preference-item">
              <div class="preference-info">
                <div class="preference-title">语言</div>
                <div class="preference-description">选择界面显示语言</div>
              </div>
              <div class="preference-control">
                <el-select v-model="preferenceSettings.language" size="small">
                  <el-option label="中文" value="zh-CN" />
                  <el-option label="English" value="en-US" />
                </el-select>
              </div>
            </div>
            
            <div class="preference-item">
              <div class="preference-info">
                <div class="preference-title">时区</div>
                <div class="preference-description">设置您的时区</div>
              </div>
              <div class="preference-control">
                <el-select v-model="preferenceSettings.timezone" size="small">
                  <el-option label="Asia/Shanghai (UTC+8)" value="Asia/Shanghai" />
                  <el-option label="UTC" value="UTC" />
                  <el-option label="America/New_York (UTC-5)" value="America/New_York" />
                </el-select>
              </div>
            </div>
            
            <div class="preference-item">
              <div class="preference-info">
                <div class="preference-title">页面大小</div>
                <div class="preference-description">设置表格每页显示条数</div>
              </div>
              <div class="preference-control">
                <el-select v-model="preferenceSettings.page_size" size="small">
                  <el-option label="10条/页" :value="10" />
                  <el-option label="20条/页" :value="20" />
                  <el-option label="50条/页" :value="50" />
                  <el-option label="100条/页" :value="100" />
                </el-select>
              </div>
            </div>
          </div>
          
          <div class="preference-actions">
            <el-button type="primary" :icon="Check" @click="handleSavePreferences">
              保存偏好设置
            </el-button>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import {
  Edit,
  Key,
  Lock,
  Bell,
  Clock,
  Check
} from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { useAppStore } from '@/store/app'
import dayjs from 'dayjs'
import type { User } from '@/types'

const userStore = useUserStore()
const appStore = useAppStore()

// 表单引用
const passwordFormRef = ref<FormInstance>()

// 加载状态
const passwordLoading = ref(false)

// 用户信息
const userInfo = ref<User>({
  id: 1,
  username: 'admin',
  email: 'admin@example.com',
  full_name: '系统管理员',
  role: 'admin',
  department: '技术部',
  phone: '13800138000',
  avatar: '',
  is_active: true,
  last_login: '2024-03-10T14:30:00',
  created_at: '2024-01-01T00:00:00',
  updated_at: '2024-03-10T14:30:00'
})

// 密码表单
const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

// 密码验证规则
const passwordRules: FormRules = {
  current_password: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule: any, value: any, callback: any) => {
        if (value !== passwordForm.new_password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 安全设置
const securitySettings = reactive({
  login_notification: true
})

// 偏好设置
const preferenceSettings = reactive({
  theme: 'dark',
  language: 'zh-CN',
  timezone: 'Asia/Shanghai',
  page_size: 20
})

// 获取角色标签
const getRoleLabel = (role: string) => {
  const roleMap: Record<string, string> = {
    admin: '管理员',
    user: '普通用户'
  }
  return roleMap[role] || role
}

// 获取角色类型
const getRoleType = (role: string) => {
  return role === 'admin' ? 'danger' : 'primary'
}

// 获取头像文本
const getAvatarText = (fullName: string) => {
  if (!fullName) return 'U'
  const names = fullName.split(' ')
  if (names.length > 1) {
    return names[0].charAt(0) + names[1].charAt(0)
  }
  return fullName.charAt(0)
}

// 格式化日期时间
const formatDateTime = (datetime: string) => {
  if (!datetime) return '从未登录'
  return dayjs(datetime).format('YYYY-MM-DD HH:mm:ss')
}

// 处理头像编辑
const handleAvatarEdit = () => {
  ElMessage.info('头像编辑功能开发中...')
}

// 处理编辑个人信息
const handleEditProfile = () => {
  ElMessage.info('个人信息编辑功能开发中...')
}

// 处理修改密码
const handleChangePassword = async () => {
  try {
    // 验证表单
    const valid = await passwordFormRef.value?.validate()
    if (!valid) return
    
    passwordLoading.value = true
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 清空表单
    passwordForm.current_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
    
    ElMessage.success('密码修改成功')
    
  } catch (error) {
    console.error('修改密码失败:', error)
    ElMessage.error('修改密码失败，请重试')
  } finally {
    passwordLoading.value = false
  }
}

// 处理会话管理
const handleSessionManage = () => {
  ElMessage.info('会话管理功能开发中...')
}

// 处理保存偏好设置
const handleSavePreferences = () => {
  // 保存到本地存储
  localStorage.setItem('user_preferences', JSON.stringify(preferenceSettings))
  ElMessage.success('偏好设置已保存')
}

// 加载用户数据
const loadUserData = async () => {
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // 从store获取用户信息
    if (userStore.userInfo) {
      userInfo.value = userStore.userInfo
    }
    
    // 加载偏好设置
    const savedPreferences = localStorage.getItem('user_preferences')
    if (savedPreferences) {
      Object.assign(preferenceSettings, JSON.parse(savedPreferences))
    }
    
  } catch (error) {
    console.error('加载用户数据失败:', error)
  }
}

// 生命周期钩子
onMounted(() => {
  // 设置页面标题
  appStore.setPageTitle('个人中心')
  
  // 加载用户数据
  loadUserData()
})
</script>

<style lang="scss" scoped>
.profile-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

// 页面标题
.page-header {
  margin-bottom: 8px;
  
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

// 主要内容
.profile-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  
  @media (max-width: 1200px) {
    grid-template-columns: 1fr;
  }
}

// 个人信息卡片
.profile-card {
  .profile-info {
    .avatar-section {
      display: flex;
      justify-content: center;
      margin-bottom: 24px;
      
      .avatar-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 12px;
        
        .user-avatar {
          background: var(--primary-color);
          color: white;
          font-weight: 600;
          font-size: 36px;
        }
      }
    }
    
    .info-section {
      display: flex;
      flex-direction: column;
      gap: 16px;
      margin-bottom: 24px;
      
      .info-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid var(--border-color);
        
        &:last-child {
          border-bottom: none;
        }
        
        .info-label {
          font-weight: 500;
          color: var(--text-secondary);
          font-size: 14px;
        }
        
        .info-value {
          color: var(--text-primary);
          font-size: 14px;
        }
      }
    }
    
    .action-section {
      display: flex;
      justify-content: center;
    }
  }
}

// 设置卡片
.settings-card {
  margin-bottom: 20px;
  
  &:last-child {
    margin-bottom: 0;
  }
  
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
  
  :deep(.el-card__body) {
    padding: 20px;
  }
}

// 安全设置
.security-settings {
  .security-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid var(--border-color);
    
    &:last-child {
      border-bottom: none;
    }
    
    .security-info {
      display: flex;
      align-items: center;
      gap: 12px;
      
      .security-icon {
        font-size: 20px;
        color: var(--text-tertiary);
      }
      
      .security-details {
        .security-title {
          font-weight: 500;
          color: var(--text-primary);
          margin-bottom: 4px;
          font-size: 14px;
        }
        
        .security-description {
          font-size: 12px;
          color: var(--text-tertiary);
        }
      }
    }
  }
}

// 偏好设置
.preference-settings {
  .preference-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid var(--border-color);
    
    &:last-child {
      border-bottom: none;
    }
    
    .preference-info {
      .preference-title {
        font-weight: 500;
        color: var(--text-primary);
        margin-bottom: 4px;
        font-size: 14px;
      }
      
      .preference-description {
        font-size: 12px;
        color: var(--text-tertiary);
      }
    }
    
    .preference-control {
      min-width: 150px;
    }
  }
  
  .preference-actions {
    display: flex;
    justify-content: center;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid var(--border-color);
  }
}

// 响应式调整
@media (max-width: 768px) {
  .profile-content {
    gap: 16px;
  }
  
  .info-item {
    flex-direction: column;
    align-items: flex-start !important;
    gap: 8px;
  }
  
  .security-item,
  .preference-item {
    flex-direction: column;
    align-items: flex-start !important;
    gap: 12px;
    
    .security-status,
    .preference-control {
      align-self: flex-end;
    }
  }
}
</style>