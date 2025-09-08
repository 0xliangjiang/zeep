<template>
  <div class="page">
    <div class="page-content">
      <!-- 页面标题 -->
      <div class="page-header">
        <h1 class="page-title">步数记录</h1>
        <p class="page-subtitle">查看您的步数修改历史</p>
      </div>

      <!-- 记录列表 -->
      <div class="records-container">
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
          <p class="loading-text">加载中...</p>
        </div>
        
        <div v-else-if="records.length === 0" class="empty-container">
          <div class="empty-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z" stroke="#999" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <polyline points="14,2 14,8 20,8" stroke="#999" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <line x1="16" y1="13" x2="8" y2="13" stroke="#999" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <line x1="16" y1="17" x2="8" y2="17" stroke="#999" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <polyline points="10,9 9,9 8,9" stroke="#999" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <p class="empty-text">暂无步数记录</p>
          <p class="empty-hint">修改步数后记录会显示在这里</p>
        </div>
        
        <div v-else class="records-list">
          <div 
            v-for="record in records" 
            :key="record.id"
            class="record-card"
          >
            <div class="record-header">
              <div class="record-steps">
                <span class="steps-number">{{ record.steps.toLocaleString() }}</span>
                <span class="steps-unit">步</span>
              </div>
              <div class="record-status" :class="record.status">
                <span class="status-text">{{ getStatusText(record.status) }}</span>
              </div>
            </div>
            
            <div class="record-details">
              <div class="detail-item">
                <span class="detail-label">修改时间</span>
                <span class="detail-value">{{ formatTime(record.created_at) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部导航 -->
    <WechatNavBar />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import WechatNavBar from '../components/WechatNavBar.vue'

export default {
  name: 'StepRecords',
  components: {
    WechatNavBar
  },
  setup() {
    const records = ref([])
    const loading = ref(false)
    
    // 获取步数记录
    const fetchRecords = async () => {
      loading.value = true
      
      try {
        const response = await fetch('/api/steps/records', {
          credentials: 'include'
        })
        
        if (response.ok) {
          const data = await response.json()
          records.value = data.records || []
        } else {
          window.$toast('获取记录失败', 'error')
        }
      } catch (error) {
        console.error('获取步数记录失败:', error)
        window.$toast('网络错误，请稍后重试', 'error')
      } finally {
        loading.value = false
      }
    }
    
    // 格式化时间
    const formatTime = (timestamp) => {
      const date = new Date(timestamp)
      const now = new Date()
      const diff = now - date
      
      // 小于1分钟
      if (diff < 60000) {
        return '刚刚'
      }
      
      // 小于1小时
      if (diff < 3600000) {
        return `${Math.floor(diff / 60000)}分钟前`
      }
      
      // 小于24小时
      if (diff < 86400000) {
        return `${Math.floor(diff / 3600000)}小时前`
      }
      
      // 超过24小时显示具体时间
      return date.toLocaleString('zh-CN', {
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    // 获取状态文本
    const getStatusText = (status) => {
      const statusMap = {
        'success': '成功',
        'failed': '失败',
        'pending': '处理中'
      }
      return statusMap[status] || status
    }
    
    onMounted(() => {
      fetchRecords()
    })
    
    return {
      records,
      loading,
      fetchRecords,
      formatTime,
      getStatusText
    }
  }
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background: #f5f5f5;

  .page-content {
    padding: 16px;
    padding-bottom: 80px; // 为底部导航栏留出空间
  }
}

.page-header {
  text-align: center;
  margin-bottom: 24px;
  
  .page-title {
    font-size: 24px;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 8px;
  }
  
  .page-subtitle {
    font-size: 14px;
    color: #666;
    margin: 0;
  }
}

.records-container {
  .loading-container {
    text-align: center;
    padding: 40px 20px;
    
    .loading-spinner {
      width: 32px;
      height: 32px;
      border: 3px solid #e1e8ed;
      border-top: 3px solid #007AFF;
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
  
  .empty-container {
    text-align: center;
    padding: 60px 20px;
    
    .empty-icon {
      display: flex;
      justify-content: center;
      margin-bottom: 16px;
    }
    
    .empty-text {
      font-size: 16px;
      color: #333;
      margin-bottom: 8px;
    }
    
    .empty-hint {
      font-size: 14px;
      color: #999;
      margin: 0;
    }
  }
}

.records-list {
  .record-card {
    background: #ffffff;
    border: 1px solid #e1e8ed;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
    transition: all 0.2s ease;
    
    &:hover {
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .record-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      
      .record-steps {
        .steps-number {
          font-size: 20px;
          font-weight: 600;
          color: #007AFF;
        }
        
        .steps-unit {
          font-size: 14px;
          color: #666;
          margin-left: 4px;
        }
      }
      
      .record-status {
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 500;
        
        &.success {
          background: #f0f9ff;
          color: #1e40af;
        }
        
        &.failed {
          background: #fef2f2;
          color: #dc2626;
        }
        
        &.pending {
          background: #fffbeb;
          color: #d97706;
        }
      }
    }
    
    .record-details {
      .detail-item {
        display: flex;
        justify-content: space-between;
        margin-bottom: 4px;
        
        &:last-child {
          margin-bottom: 0;
        }
        
        .detail-label {
          font-size: 13px;
          color: #666;
        }
        
        .detail-value {
          font-size: 13px;
          color: #333;
        }
      }
    }
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
