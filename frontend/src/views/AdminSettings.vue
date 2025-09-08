<template>
  <div class="admin-settings">
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
      <WechatNavBar title="管理员设置" :show-back="true" />

      <!-- 功能列表 -->
      <div class="admin-menu">
        <div class="menu-item" @click="goToCardManage">
          <div class="menu-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
              <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
              <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="menu-content">
            <div class="menu-title">卡密管理</div>
            <div class="menu-desc">生成和管理卡密</div>
          </div>
          <div class="menu-arrow">›</div>
        </div>

        <div class="menu-item" @click="goToDonationManage">
          <div class="menu-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" stroke="currentColor" stroke-width="2"/>
            </svg>
          </div>
          <div class="menu-content">
            <div class="menu-title">捐赠管理</div>
            <div class="menu-desc">设置捐赠价格和天数</div>
          </div>
          <div class="menu-arrow">›</div>
        </div>

        <div class="menu-item" @click="goToZeppManage">
          <div class="menu-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="8.5" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
              <line x1="20" y1="8" x2="20" y2="14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <line x1="23" y1="11" x2="17" y2="11" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <div class="menu-content">
            <div class="menu-title">Zepp账号管理</div>
            <div class="menu-desc">管理Zepp账号池</div>
          </div>
          <div class="menu-arrow">›</div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import WechatNavBar from '../components/WechatNavBar.vue'

export default {
  name: 'AdminSettings',
  components: {
    WechatNavBar
  },
  setup() {
    const router = useRouter()
    const isAdmin = ref(false)

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

    // 跳转到卡密管理
    const goToCardManage = () => {
      router.push('/card-manage')
    }

    // 跳转到捐赠管理
    const goToDonationManage = () => {
      router.push('/donation-manage')
    }

    // 跳转到Zepp账号管理
    const goToZeppManage = () => {
      router.push('/zepp-manage')
    }

    // 页面加载时检查权限
    onMounted(() => {
      checkAdminPermission()
    })

    return {
      isAdmin,
      goToCardManage,
      goToDonationManage,
      goToZeppManage
    }
  }
}
</script>

<style lang="scss" scoped>
.admin-settings {
  min-height: 100vh;
  background: $bg-color;
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

.admin-menu {
  padding: 20px;
  
  .menu-item {
    display: flex;
    align-items: center;
    padding: 16px;
    background: white;
    border-radius: $border-radius-lg;
    margin-bottom: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
    
    &:hover {
      background: #f8f9fa;
    }
    
    &:active {
      transform: scale(0.98);
    }
    
    .menu-icon {
      width: 40px;
      height: 40px;
      background: $primary-color;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      margin-right: 16px;
    }
    
    .menu-content {
      flex: 1;
      
      .menu-title {
        font-size: 16px;
        font-weight: 600;
        color: $text-color;
        margin-bottom: 4px;
      }
      
      .menu-desc {
        font-size: 14px;
        color: $text-color-secondary;
      }
    }
    
    .menu-arrow {
      font-size: 20px;
      color: $text-color-secondary;
      font-weight: 300;
    }
  }
}
</style>
