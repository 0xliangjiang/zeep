<template>
  <div class="zepp-manage">
    <!-- 权限验证中 -->
    <div v-if="!isAdmin" class="permission-check">
      <div class="loading-container">
        <div class="loading-spinner"></div>
        <p class="loading-text">验证管理员权限中...</p>
      </div>
    </div>

    <!-- 管理员界面 -->
    <template v-else>
      <!-- 顶部导航 -->
      <WechatNavBar title="Zepp账号管理" :show-back="true" />

      <!-- 统计信息 -->
      <div class="stats-section">
        <div class="stat-card">
          <div class="stat-number">{{ accounts.length }}</div>
          <div class="stat-label">总账号数</div>
        </div>
        <div class="stat-card">
          <div class="stat-number">{{ activeAccountsCount }}</div>
          <div class="stat-label">活跃账号</div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <WechatButton 
          type="primary" 
          @click="showAddModal"
          :loading="loading"
        >
          添加账号
        </WechatButton>
        
        <WechatButton 
          type="secondary" 
          @click="refreshAccounts"
          :loading="loading"
        >
          刷新列表
        </WechatButton>
      </div>

      <!-- 搜索功能 -->
      <div class="search-section" v-if="accounts.length > 0">
        <div class="search-container">
          <div class="search-input-wrapper">
            <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="11" cy="11" r="8" stroke="currentColor" stroke-width="2"/>
              <path d="m21 21-4.35-4.35" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              class="search-input"
              placeholder="搜索用户名、ID或状态..."
              @input="handleSearch"
            />
            <button
              v-if="searchQuery"
              @click="clearSearch"
              class="clear-button"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>

          <!-- 搜索结果统计 -->
          <div v-if="searchQuery" class="search-stats">
            找到 {{ filteredAccounts.length }} 个账号
          </div>
        </div>
      </div>

      <!-- 账号列表 -->
      <div class="accounts-section">
        <div v-if="accounts.length === 0" class="empty-state">
          <p>暂无Zepp账号</p>
          <p class="empty-desc">点击"添加账号"开始添加</p>
        </div>

        <!-- 搜索无结果 -->
        <div v-else-if="searchQuery && filteredAccounts.length === 0" class="empty-state">
          <p>未找到匹配的账号</p>
          <p class="empty-desc">尝试修改搜索关键词</p>
        </div>

        <div v-else class="account-list">
          <div
            v-for="account in displayAccounts"
            :key="account.id"
            class="account-item"
          >
            <div class="account-info">
              <div class="account-username">{{ account.username }}</div>
              <div class="account-details">
                <span class="account-userid">ID: {{ account.userid }}</span>
                <span class="account-status" :class="{ active: account.is_active }">
                  {{ account.is_active ? '活跃' : '停用' }}
                </span>
                <span class="bind-status" :class="{ bound: account.bind_status }">
                  {{ account.bind_status ? '已绑定' : '未绑定' }}
                </span>
              </div>
              <div class="account-time">
                创建时间: {{ account.created_at }}
              </div>
            </div>
            <div class="account-actions">
              <WechatButton 
                type="danger" 
                size="small"
                @click="confirmDelete(account)"
                :loading="deletingId === account.id"
              >
                删除
              </WechatButton>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- 添加进度显示（在模态框上方） -->
    <div v-if="addingProgress.show" class="progress-overlay">
      <div class="progress-container">
        <div class="progress-header">
          <h3>正在添加Zepp账号</h3>
          <div class="progress-stats">
            {{ addingProgress.current }} / {{ addingProgress.total }}
          </div>
        </div>

        <div class="progress-bar-container">
          <div class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: (addingProgress.current / addingProgress.total * 100) + '%' }"
            ></div>
          </div>
          <div class="progress-percentage">
            {{ Math.round(addingProgress.current / addingProgress.total * 100) }}%
          </div>
        </div>

        <div class="current-account">
          <span class="current-label">当前处理:</span>
          <span class="current-username">{{ addingProgress.currentUsername }}</span>
        </div>
      </div>
    </div>

    <!-- 添加账号弹窗 -->
    <WechatModal
      v-if="showAddAccountModal && !addingProgress.show"
      title="添加Zepp账号"
      :show-cancel="true"
      confirm-text="开始添加"
      @confirm="addAccounts"
      @cancel="hideAddModal"
      @close="hideAddModal"
    >
      <div class="add-account-form">
        <div class="form-group">
          <label>账号信息</label>
          <textarea
            v-model="accountsText"
            placeholder="请输入账号信息，每行一个账号&#10;格式：用户名 密码&#10;例如：&#10;user1@example.com password1&#10;user2@example.com password2"
            class="accounts-textarea"
            rows="8"
          ></textarea>
          <p class="form-hint">支持批量添加，每行一个账号，格式：用户名 密码</p>
        </div>
        

      </div>
    </WechatModal>

    <!-- 删除确认弹窗 -->
    <WechatModal
      v-if="showDeleteModal"
      title="确认删除"
      :content="`确定要删除账号 ${accountToDelete?.username} 吗？删除后将无法恢复。`"
      :show-cancel="true"
      confirm-text="删除"
      cancel-text="取消"
      @confirm="deleteAccount"
      @cancel="hideDeleteModal"
      @close="hideDeleteModal"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import WechatNavBar from '../components/WechatNavBar.vue'
import WechatButton from '../components/WechatButton.vue'
import WechatModal from '../components/WechatModal.vue'

export default {
  name: 'ZeppManage',
  components: {
    WechatNavBar,
    WechatButton,
    WechatModal
  },
  setup() {
    const router = useRouter()
    const isAdmin = ref(false)
    const loading = ref(false)
    const accounts = ref([])
    const showAddAccountModal = ref(false)
    const accountsText = ref('')
    const deletingId = ref(null)
    const showDeleteModal = ref(false)
    const accountToDelete = ref(null)
    
    // 添加进度
    const addingProgress = ref({
      show: false,
      current: 0,
      total: 0,
      currentUsername: ''
    })

    // 搜索相关状态
    const searchQuery = ref('')

    // 活跃账号数量
    const activeAccountsCount = computed(() => {
      return accounts.value.filter(account => account.is_active).length
    })

    // 过滤后的账号列表
    const filteredAccounts = computed(() => {
      if (!searchQuery.value.trim()) {
        return accounts.value
      }

      const query = searchQuery.value.toLowerCase().trim()
      return accounts.value.filter(account => {
        // 搜索用户名
        if (account.username && account.username.toLowerCase().includes(query)) {
          return true
        }

        // 搜索用户ID
        if (account.userid && account.userid.toString().includes(query)) {
          return true
        }

        // 搜索状态
        const statusText = account.is_active ? '活跃' : '停用'
        if (statusText.includes(query)) {
          return true
        }

        // 搜索绑定状态
        const bindText = account.bind_status ? '已绑定' : '未绑定'
        if (bindText.includes(query)) {
          return true
        }

        return false
      })
    })

    // 显示的账号列表（用于模板）
    const displayAccounts = computed(() => {
      return filteredAccounts.value
    })

    // 检查管理员权限
    const checkAdminPermission = async () => {
      try {
        const response = await fetch('/api/zepp-manage/check-admin', {
          credentials: 'include'
        })

        if (response.ok) {
          const data = await response.json()
          isAdmin.value = data.is_admin
          
          if (!data.is_admin) {
            window.$toast('权限不足，即将返回首页', 'error')
            setTimeout(() => {
              router.push('/')
            }, 2000)
          }
        } else {
          window.$toast('权限验证失败，即将返回首页', 'error')
          setTimeout(() => {
            router.push('/')
          }, 2000)
        }
      } catch (error) {
        console.error('检查管理员权限失败:', error)
        window.$toast('权限验证失败，即将返回首页', 'error')
        setTimeout(() => {
          router.push('/')
        }, 2000)
      }
    }

    // 处理API错误响应
    const handleApiError = (data) => {
      if (data.need_logout) {
        window.$toast('权限已失效，即将返回首页', 'error')
        setTimeout(() => {
          router.push('/')
        }, 2000)
        return true
      }
      if (data.need_login) {
        window.$toast('登录已过期，请重新登录', 'error')
        window.location.href = '/auth/wechat'
        return true
      }
      return false
    }

    // 获取账号列表
    const fetchAccounts = async () => {
      try {
        loading.value = true
        const response = await fetch('/api/zepp-manage/accounts', {
          credentials: 'include'
        })

        const data = await response.json()

        if (response.ok && data.success) {
          accounts.value = data.accounts
        } else {
          if (handleApiError(data)) return
          window.$toast(data.error || '获取账号列表失败', 'error')
        }
      } catch (error) {
        console.error('获取账号列表失败:', error)
        window.$toast('获取账号列表失败', 'error')
      } finally {
        loading.value = false
      }
    }

    // 刷新账号列表
    const refreshAccounts = () => {
      fetchAccounts()
    }

    // 显示添加弹窗
    const showAddModal = () => {
      accountsText.value = ''
      addingProgress.value.show = false
      showAddAccountModal.value = true
    }

    // 隐藏添加弹窗
    const hideAddModal = () => {
      // 如果正在添加中，不允许关闭
      if (addingProgress.value.show) {
        return
      }

      showAddAccountModal.value = false
      accountsText.value = ''
      addingProgress.value = {
        show: false,
        current: 0,
        total: 0,
        currentUsername: ''
      }
    }

    // 添加账号
    const addAccounts = async () => {
      if (!accountsText.value.trim()) {
        window.$toast('请输入账号信息', 'warning')
        return
      }

      // 如果正在添加中，不允许重复点击
      if (addingProgress.value.show) {
        return
      }

      try {
        // 解析账号信息
        const lines = accountsText.value.trim().split('\n').filter(line => line.trim())
        const accounts = []

        for (const line of lines) {
          const parts = line.trim().split(/\s+/)
          if (parts.length >= 2) {
            accounts.push({
              username: parts[0],
              password: parts.slice(1).join(' ')
            })
          }
        }

        if (accounts.length === 0) {
          window.$toast('没有有效的账号信息', 'warning')
          return
        }

        // 显示进度
        addingProgress.value = {
          show: true,
          current: 0,
          total: accounts.length,
          currentUsername: '初始化中...'
        }

        // 启动模拟进度更新
        const progressInterval = startProgressSimulation(accounts)

        try {
          // 使用后端的批量添加API
          const response = await fetch('/api/zepp-manage/accounts', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({
              accounts: accountsText.value
            })
          })

          const data = await response.json()

          // 停止进度模拟
          clearInterval(progressInterval)

          // 设置完成状态
          addingProgress.value.current = addingProgress.value.total
          addingProgress.value.currentUsername = '处理完成'

          if (response.ok && data.success) {
            // 延迟显示最终结果，让用户看到完成状态
            setTimeout(() => {
              window.$toast(data.message, 'success')
              hideAddModal()
            }, 1500)
            await fetchAccounts()
          } else {
            if (handleApiError(data)) return
            window.$toast(data.error || '添加账号失败', 'error')
          }
        } catch (error) {
          // 停止进度模拟
          clearInterval(progressInterval)
          throw error
        }

      } catch (error) {
        console.error('添加账号失败:', error)
        window.$toast('添加账号失败', 'error')
      } finally {
        // 延迟隐藏进度，让用户看到最终状态
        setTimeout(() => {
          addingProgress.value.show = false
        }, 2000)
      }
    }

    // 启动进度模拟
    const startProgressSimulation = (accounts) => {
      let currentIndex = 0

      const interval = setInterval(() => {
        if (currentIndex < accounts.length) {
          addingProgress.value.current = currentIndex + 1
          addingProgress.value.currentUsername = accounts[currentIndex].username
          currentIndex++
        }
      }, 800) // 每0.8秒更新一次进度，更快的反馈

      return interval
    }

    // 确认删除
    const confirmDelete = (account) => {
      accountToDelete.value = account
      showDeleteModal.value = true
    }

    // 隐藏删除弹窗
    const hideDeleteModal = () => {
      showDeleteModal.value = false
      accountToDelete.value = null
    }

    // 删除账号
    const deleteAccount = async () => {
      if (!accountToDelete.value) return

      try {
        deletingId.value = accountToDelete.value.id
        
        const response = await fetch(`/api/zepp-manage/accounts/${accountToDelete.value.id}`, {
          method: 'DELETE',
          credentials: 'include'
        })

        const data = await response.json()

        if (response.ok && data.success) {
          window.$toast(data.message, 'success')
          hideDeleteModal()
          await fetchAccounts()
        } else {
          if (handleApiError(data)) return
          window.$toast(data.error || '删除账号失败', 'error')
        }
      } catch (error) {
        console.error('删除账号失败:', error)
        window.$toast('删除账号失败', 'error')
      } finally {
        deletingId.value = null
      }
    }

    // 搜索处理
    const handleSearch = () => {
      // 搜索是响应式的，不需要额外处理
      console.log('搜索关键词:', searchQuery.value)
    }

    // 清除搜索
    const clearSearch = () => {
      searchQuery.value = ''
    }

    // 页面加载时检查权限和获取数据
    onMounted(async () => {
      await checkAdminPermission()
      if (isAdmin.value) {
        await fetchAccounts()
      }
    })

    return {
      isAdmin,
      loading,
      accounts,
      activeAccountsCount,
      showAddAccountModal,
      accountsText,
      addingProgress,
      deletingId,
      showDeleteModal,
      accountToDelete,

      // 搜索相关
      searchQuery,
      filteredAccounts,
      displayAccounts,
      handleSearch,
      clearSearch,

      // 方法
      refreshAccounts,
      showAddModal,
      hideAddModal,
      addAccounts,
      confirmDelete,
      hideDeleteModal,
      deleteAccount
    }
  }
}
</script>

<style lang="scss" scoped>
.zepp-manage {
  min-height: 100vh;
  background: $bg-color;
  padding-bottom: 100px;
}

.permission-check {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  
  .loading-container {
    text-align: center;
    
    .loading-spinner {
      width: 40px;
      height: 40px;
      border: 3px solid #e1e8ed;
      border-top: 3px solid #07c160;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin: 0 auto 16px;
    }
    
    .loading-text {
      font-size: 14px;
      color: #666;
      margin: 0;
    }
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.progress-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;

  .progress-container {
    background: white;
    border-radius: $border-radius-lg;
    padding: 30px;
    max-width: 400px;
    width: 90%;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);

    .progress-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;

      h3 {
        font-size: 18px;
        font-weight: 600;
        color: $text-color;
        margin: 0;
      }

      .progress-stats {
        font-size: 16px;
        font-weight: 600;
        color: $primary-color;
        background: rgba($primary-color, 0.1);
        padding: 4px 12px;
        border-radius: 20px;
      }
    }

    .progress-bar-container {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 20px;

      .progress-bar {
        flex: 1;
        height: 8px;
        background: #e1e8ed;
        border-radius: 4px;
        overflow: hidden;

        .progress-fill {
          height: 100%;
          background: linear-gradient(90deg, $primary-color, #00d084);
          transition: width 0.3s ease;
          border-radius: 4px;
        }
      }

      .progress-percentage {
        font-size: 14px;
        font-weight: 600;
        color: $primary-color;
        min-width: 40px;
        text-align: right;
      }
    }

    .current-account {
      text-align: center;
      padding: 12px;
      background: #f8f9fa;
      border-radius: $border-radius-sm;

      .current-label {
        font-size: 14px;
        color: $text-color-secondary;
        margin-right: 8px;
      }

      .current-username {
        font-size: 14px;
        font-weight: 600;
        color: $text-color;
      }
    }
  }
}

.stats-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  padding: 20px;
  
  .stat-card {
    background: white;
    border-radius: $border-radius-lg;
    padding: 20px;
    text-align: center;
    
    .stat-number {
      font-size: 32px;
      font-weight: 600;
      color: $primary-color;
      margin-bottom: 8px;
    }
    
    .stat-label {
      font-size: 14px;
      color: $text-color-secondary;
    }
  }
}

.action-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  padding: 0 20px 20px;
}

// 搜索功能样式
.search-section {
  padding: 0 20px 16px;

  .search-container {
    .search-input-wrapper {
      position: relative;
      display: flex;
      align-items: center;
      background: white;
      border-radius: 12px;
      border: 1px solid #e1e8ed;
      padding: 12px 16px;
      transition: all 0.2s ease;

      &:focus-within {
        border-color: #4682B4;
        box-shadow: 0 0 0 3px rgba(70, 130, 180, 0.1);
      }

      .search-icon {
        color: #7f8c8d;
        margin-right: 12px;
        flex-shrink: 0;
      }

      .search-input {
        flex: 1;
        border: none;
        outline: none;
        font-size: 14px;
        color: #2c3e50;
        background: transparent;

        &::placeholder {
          color: #bdc3c7;
        }
      }

      .clear-button {
        background: none;
        border: none;
        padding: 4px;
        margin-left: 8px;
        border-radius: 50%;
        color: #7f8c8d;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;

        &:hover {
          background: #f8f9fa;
          color: #2c3e50;
        }
      }
    }

    .search-stats {
      margin-top: 8px;
      font-size: 12px;
      color: #7f8c8d;
      text-align: center;
    }
  }
}

.accounts-section {
  padding: 0 20px;
  
  .empty-state {
    background: white;
    border-radius: $border-radius-lg;
    padding: 40px 20px;
    text-align: center;
    
    p {
      margin: 0 0 8px 0;
      color: $text-color;
    }
    
    .empty-desc {
      color: $text-color-secondary;
      font-size: 14px;
    }
  }
  
  .account-list {
    .account-item {
      background: white;
      border-radius: $border-radius-lg;
      padding: 16px;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      
      .account-info {
        flex: 1;

        .account-username {
          font-size: 16px;
          font-weight: 600;
          color: $text-color;
          margin-bottom: 8px;
        }
        
        .account-details {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 4px;
          
          .account-userid {
            font-size: 12px;
            color: $text-color-secondary;
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 4px;
          }
          
          .account-status {
            font-size: 12px;
            padding: 2px 6px;
            border-radius: 4px;
            background: #ffeaa7;
            color: #d63031;

            &.active {
              background: #d1f2eb;
              color: #00b894;
            }
          }

          .bind-status {
            font-size: 12px;
            padding: 2px 6px;
            border-radius: 4px;
            background: #ddd6fe;
            color: #7c3aed;

            &.bound {
              background: #fef3c7;
              color: #d97706;
            }
          }
        }
        
        .account-time {
          font-size: 12px;
          color: $text-color-secondary;
        }
      }
      
      .account-actions {
        margin-left: 16px;
      }
    }
  }
}

.add-account-form {
  .form-group {
    margin-bottom: 20px;
    
    label {
      display: block;
      font-size: 14px;
      font-weight: 500;
      color: $text-color;
      margin-bottom: 8px;
    }
    
    .accounts-textarea {
      width: 100%;
      padding: 12px;
      border: 1px solid $border-color;
      border-radius: $border-radius-sm;
      font-size: 14px;
      font-family: monospace;
      resize: vertical;
      
      &:focus {
        outline: none;
        border-color: $primary-color;
        box-shadow: 0 0 0 2px rgba($primary-color, 0.1);
      }
    }
    
    .form-hint {
      font-size: 12px;
      color: $text-color-secondary;
      margin: 8px 0 0 0;
    }
  }
  

}
</style>
