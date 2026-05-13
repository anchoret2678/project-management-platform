<template>
  <div class="user-list-container">
    <!-- 页面标题和操作 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">用户管理</h1>
        <p class="page-subtitle">系统用户账号管理</p>
      </div>
      <div class="header-right">
        <el-button type="primary" :icon="Plus" @click="handleCreate">
          添加用户
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
          <el-form-item label="用户名">
            <el-input
              v-model="filterForm.username"
              placeholder="请输入用户名"
              clearable
              @clear="handleFilter"
              @keyup.enter="handleFilter"
            />
          </el-form-item>
          
          <el-form-item label="姓名">
            <el-input
              v-model="filterForm.full_name"
              placeholder="请输入姓名"
              clearable
              @clear="handleFilter"
              @keyup.enter="handleFilter"
            />
          </el-form-item>
          
          <el-form-item label="角色">
            <el-select
              v-model="filterForm.role"
              placeholder="请选择角色"
              clearable
              @change="handleFilter"
            >
              <el-option
                v-for="role in roleOptions"
                :key="role.value"
                :label="role.label"
                :value="role.value"
              />
            </el-select>
          </el-form-item>
          
          <el-form-item label="状态">
            <el-select
              v-model="filterForm.is_active"
              placeholder="请选择状态"
              clearable
              @change="handleFilter"
            >
              <el-option
                v-for="status in statusOptions"
                :key="status.value"
                :label="status.label"
                :value="status.value"
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
    
    <!-- 用户列表 -->
    <el-card class="list-card" shadow="never">
      <template #header>
        <div class="list-header">
          <div class="list-title">
            <span>用户列表</span>
            <el-tag type="info" size="small">
              共 {{ pagination.total }} 个用户
            </el-tag>
          </div>
        </div>
      </template>
      
      <!-- 表格 -->
      <el-table
        v-loading="loading"
        :data="userList"
        style="width: 100%"
      >
        <el-table-column prop="username" label="用户名" width="120">
          <template #default="{ row }">
            <div class="user-cell">
              <el-avatar :size="32" :src="row.avatar" class="user-avatar">
                {{ getAvatarText(row.full_name) }}
              </el-avatar>
              <span class="username">{{ row.username }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="full_name" label="姓名" width="120">
          <template #default="{ row }">
            {{ row.full_name }}
          </template>
        </el-table-column>
        
        <el-table-column prop="email" label="邮箱" width="180">
          <template #default="{ row }">
            <span class="email">{{ row.email }}</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="role" label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="getRoleType(row.role)" size="small">
              {{ getRoleLabel(row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="department" label="部门" width="120">
          <template #default="{ row }">
            <span v-if="row.department">{{ row.department }}</span>
            <span v-else class="text-muted">未设置</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="phone" label="电话" width="140">
          <template #default="{ row }">
            <span v-if="row.phone">{{ row.phone }}</span>
            <span v-else class="text-muted">未设置</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="last_login" label="最后登录" width="160">
          <template #default="{ row }">
            <span v-if="row.last_login">{{ formatDateTime(row.last_login) }}</span>
            <span v-else class="text-muted">从未登录</span>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button
                type="primary"
                link
                :icon="Edit"
                @click="handleEdit(row)"
              >
                编辑
              </el-button>
              <el-button
                v-if="row.id !== currentUserId"
                type="danger"
                link
                :icon="Delete"
                @click="handleDelete(row)"
              >
                删除
              </el-button>
              <el-button
                type="primary"
                link
                :icon="Key"
                @click="handleResetPassword(row)"
              >
                重置密码
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container" v-if="userList.length > 0">
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
  Edit,
  Delete,
  Key
} from '@element-plus/icons-vue'
import { useUserStore } from '@/store/user'
import { useAppStore } from '@/store/app'
import dayjs from 'dayjs'
import type { User } from '@/types'

const router = useRouter()
const userStore = useUserStore()
const appStore = useAppStore()

// 加载状态
const loading = ref(false)

// 筛选表单
const filterForm = reactive({
  username: '',
  full_name: '',
  role: '',
  is_active: ''
})

// 角色选项
const roleOptions = ref([
  { value: 'admin', label: '管理员' },
  { value: 'user', label: '普通用户' }
])

// 状态选项
const statusOptions = ref([
  { value: 'true', label: '启用' },
  { value: 'false', label: '禁用' }
])

// 用户列表数据
const userList = ref<User[]>([
  {
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
  },
  {
    id: 2,
    username: 'zhangsan',
    email: 'zhangsan@example.com',
    full_name: '张三',
    role: 'user',
    department: '项目部',
    phone: '13800138001',
    avatar: '',
    is_active: true,
    last_login: '2024-03-09T10:20:00',
    created_at: '2024-01-05T09:00:00',
    updated_at: '2024-03-09T10:20:00'
  },
  {
    id: 3,
    username: 'lisi',
    email: 'lisi@example.com',
    full_name: '李四',
    role: 'user',
    department: '运维部',
    phone: '13800138002',
    avatar: '',
    is_active: true,
    last_login: '2024-03-08T16:45:00',
    created_at: '2024-01-10T14:00:00',
    updated_at: '2024-03-08T16:45:00'
  },
  {
    id: 4,
    username: 'wangwu',
    email: 'wangwu@example.com',
    full_name: '王五',
    role: 'user',
    department: '技术部',
    phone: '13800138003',
    avatar: '',
    is_active: false,
    last_login: '2024-02-28T11:30:00',
    created_at: '2024-01-15T11:00:00',
    updated_at: '2024-02-28T11:30:00'
  },
  {
    id: 5,
    username: 'zhaoliu',
    email: 'zhaoliu@example.com',
    full_name: '赵六',
    role: 'user',
    department: '项目部',
    phone: '13800138004',
    avatar: '',
    is_active: true,
    last_login: '2024-03-07T09:15:00',
    created_at: '2024-01-20T16:00:00',
    updated_at: '2024-03-07T09:15:00'
  }
])

// 分页配置
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
})

// 计算属性
const currentUserId = computed(() => userStore.userInfo?.id)

// 获取角色标签
const getRoleLabel = (role: string) => {
  const option = roleOptions.value.find(opt => opt.value === role)
  return option ? option.label : role
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
  return dayjs(datetime).format('YYYY-MM-DD HH:mm')
}

// 处理创建用户
const handleCreate = () => {
  ElMessage.info('用户创建功能开发中...')
}

// 处理编辑用户
const handleEdit = (user: User) => {
  ElMessage.info(`编辑用户: ${user.username}`)
}

// 处理删除用户
const handleDelete = async (user: User) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户 "${user.username}" 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 模拟删除操作
    const index = userList.value.findIndex(u => u.id === user.id)
    if (index !== -1) {
      userList.value.splice(index, 1)
      ElMessage.success('用户删除成功')
    }
  } catch (error) {
    // 用户取消删除
  }
}

// 处理重置密码
const handleResetPassword = (user: User) => {
  ElMessageBox.prompt('请输入新密码', '重置密码', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    inputType: 'password',
    inputPlaceholder: '请输入新密码',
    inputValidator: (value) => {
      if (!value) {
        return '密码不能为空'
      }
      if (value.length < 6) {
        return '密码长度不能少于6位'
      }
      return true
    }
  }).then(({ value }) => {
    ElMessage.success(`用户 ${user.username} 密码重置成功`)
  }).catch(() => {
    // 用户取消
  })
}

// 处理筛选
const handleFilter = () => {
  pagination.current = 1
  loadData()
}

// 重置筛选
const resetFilter = () => {
  Object.assign(filterForm, {
    username: '',
    full_name: '',
    role: '',
    is_active: ''
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
    let filteredData = [...userList.value]
    
    if (filterForm.username) {
      filteredData = filteredData.filter(u => 
        u.username.toLowerCase().includes(filterForm.username.toLowerCase())
      )
    }
    
    if (filterForm.full_name) {
      filteredData = filteredData.filter(u => 
        u.full_name.toLowerCase().includes(filterForm.full_name.toLowerCase())
      )
    }
    
    if (filterForm.role) {
      filteredData = filteredData.filter(u => u.role === filterForm.role)
    }
    
    if (filterForm.is_active) {
      const isActive = filterForm.is_active === 'true'
      filteredData = filteredData.filter(u => u.is_active === isActive)
    }
    
    // 模拟分页
    const start = (pagination.current - 1) * pagination.size
    const end = start + pagination.size
    const paginatedData = filteredData.slice(start, end)
    
    // 更新数据
    userList.value = paginatedData
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
  appStore.setPageTitle('用户管理')
})
</script>

<style lang="scss" scoped>
.user-list-container {
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
  .user-cell {
    display: flex;
    align-items: center;
    gap: 12px;
    
    .user-avatar {
      background: var(--primary-color);
      color: white;
      font-weight: 600;
    }
    
    .username {
      font-weight: 500;
    }
  }
  
  .email {
    color: var(--text-secondary);
    font-size: 13px;
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

// 分页容器
.pagination-container {
  display: flex;
  justify-content: center;
  padding: 20px 0 0 0;
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
}
</style>