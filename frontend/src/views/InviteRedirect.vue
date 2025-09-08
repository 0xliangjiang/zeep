<template>
  <div class="invite-redirect">
    <div class="loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">正在处理邀请链接...</p>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'

export default {
  name: 'InviteRedirect',
  setup() {
    const route = useRoute()
    
    onMounted(() => {
      const inviteCode = route.params.code
      console.log('邀请码:', inviteCode)
      
      // 直接跳转到微信授权，带上邀请码
      window.location.href = `/auth/wechat?invite=${inviteCode}`
    })
    
    return {}
  }
}
</script>

<style lang="scss" scoped>
.invite-redirect {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  
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
</style>
