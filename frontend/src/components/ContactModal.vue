<template>
  <WechatModal
    v-if="show"
    title="联系客服"
    :show-cancel="true"
    confirm-text="我知道了"
    @confirm="handleClose"
    @cancel="handleClose"
    @close="handleClose"
  >
    <div class="contact-content">
      <div class="contact-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M8 9h8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M8 13h6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      
      <div class="contact-text" v-if="!loading">
        <div v-if="contactContent" class="custom-content">
          {{ contactContent }}
        </div>
        <div v-else class="default-content">
          <p>如需帮助，请通过以下方式联系我们：</p>
          <p>📧 邮箱：support@example.com</p>
          <p>💬 微信：zepp_support</p>
          <p>⏰ 服务时间：9:00-18:00</p>
        </div>

        <!-- 微信标识符 -->
        <div class="openid-section">
          <div class="openid-label">当前微信标识符：</div>
          <div class="openid-value">{{ userOpenid || '获取中...' }}</div>
        </div>
      </div>
      
      <div v-else class="loading-content">
        <div class="loading-spinner"></div>
        <p>正在加载客服信息...</p>
      </div>
    </div>
  </WechatModal>
</template>

<script>
import { ref, watch } from 'vue'
import WechatModal from './WechatModal.vue'

export default {
  name: 'ContactModal',
  components: {
    WechatModal
  },
  props: {
    show: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const loading = ref(false)
    const contactContent = ref('')
    const userOpenid = ref('')

    // 获取客服联系方式内容
    const fetchContactContent = async () => {
      loading.value = true

      try {
        const response = await fetch('/api/admin/system-settings/contact-content', {
          method: 'GET',
          credentials: 'include'
        })

        if (response.ok) {
          const data = await response.json()
          if (data.success && data.content) {
            contactContent.value = data.content
          }
        }
      } catch (error) {
        console.error('获取客服内容失败:', error)
      } finally {
        loading.value = false
      }
    }

    // 获取用户openid
    const fetchUserOpenid = async () => {
      try {
        const response = await fetch('/auth/user', {
          method: 'GET',
          credentials: 'include'
        })

        if (response.ok) {
          const data = await response.json()
          if (data.openid) {
            userOpenid.value = data.openid
          }
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
      }
    }

    // 关闭弹窗
    const handleClose = () => {
      emit('close')
    }

    // 监听弹窗显示状态
    watch(() => props.show, (newShow) => {
      if (newShow) {
        fetchContactContent()
        fetchUserOpenid()
      }
    })

    return {
      loading,
      contactContent,
      userOpenid,
      handleClose
    }
  }
}
</script>

<style lang="scss" scoped>
.contact-content {
  text-align: center;
  padding: 20px 0;
  
  .contact-icon {
    margin-bottom: 20px;
    
    svg {
      color: #4682B4;
    }
  }
  
  .contact-text {
    .custom-content {
      font-size: 14px;
      line-height: 1.6;
      color: #2c3e50;
      white-space: pre-wrap;
      text-align: left;
      background: #f8f9fa;
      padding: 16px;
      border-radius: 8px;
      border-left: 4px solid #4682B4;
    }
    
    .default-content {
      text-align: left;
      
      p {
        margin: 8px 0;
        font-size: 14px;
        line-height: 1.5;
        color: #2c3e50;
        
        &:first-child {
          font-weight: 500;
          margin-bottom: 16px;
        }
      }
    }
  }
  
  .loading-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;

    .loading-spinner {
      width: 24px;
      height: 24px;
      border: 2px solid #e1e8ed;
      border-top: 2px solid #4682B4;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }

    p {
      font-size: 14px;
      color: #7f8c8d;
      margin: 0;
    }
  }

  .openid-section {
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px solid #e1e8ed;

    .openid-label {
      font-size: 12px;
      color: #7f8c8d;
      margin-bottom: 4px;
    }

    .openid-value {
      font-size: 11px;
      color: #2c3e50;
      font-family: 'Courier New', monospace;
      background: #f8f9fa;
      padding: 6px 8px;
      border-radius: 4px;
      word-break: break-all;
      border: 1px solid #e1e8ed;
    }
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
