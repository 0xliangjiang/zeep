<template>
  <div class="donation-manage">
    <!-- 权限验证中 -->
    <div v-if="!isAdmin" class="permission-check">
      <div class="loading-container">
        <div class="loading-spinner"></div>
        <p class="loading-text">验证管理员权限中...</p>
      </div>
    </div>

    <!-- 管理员界面 -->
    <template v-else>
      <!-- 顶部标题 -->
      <div class="page-header">
        <h1 class="page-title">捐赠管理</h1>
        <p class="page-subtitle">设置捐赠价格和对应天数</p>
      </div>

      <!-- 配置表单 -->
      <div class="config-form">
        <h2 class="form-title">捐赠方案配置</h2>
        
        <div v-for="(config, index) in configs" :key="index" class="config-item">
          <h3 class="config-title">方案{{ index + 1 }}</h3>
          
          <div class="form-row">
            <div class="form-group">
              <label>捐赠价格（元）</label>
              <input 
                v-model.number="config.price" 
                type="number" 
                step="0.01"
                min="0.01"
                class="form-input"
                placeholder="请输入价格"
              />
            </div>
            
            <div class="form-group">
              <label>获得天数</label>
              <input 
                v-model.number="config.days" 
                type="number" 
                min="1"
                class="form-input"
                placeholder="请输入天数"
              />
            </div>
          </div>
        </div>

        <div class="form-actions">
          <WechatButton 
            type="primary" 
            @click="saveConfigs"
            :loading="saving"
          >
            保存配置
          </WechatButton>
        </div>
      </div>

      <!-- 当前配置预览 -->
      <div v-if="currentConfigs.length > 0" class="current-configs">
        <h3>当前生效配置</h3>
        <div class="config-list">
          <div v-for="config in currentConfigs" :key="config.id" class="config-preview">
            <div class="config-info">
              <span class="price">￥{{ config.price }}</span>
              <span class="days">{{ config.days }}天</span>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import WechatButton from '../components/WechatButton.vue'

export default {
  name: 'DonationManage',
  components: {
    WechatButton
  },
  setup() {
    const router = useRouter()
    const isAdmin = ref(false)
    const saving = ref(false)
    const currentConfigs = ref([])
    
    // 默认配置
    const configs = ref([
      { price: 9.9, days: 30 },
      { price: 19.9, days: 90 },
      { price: 39.9, days: 365 }
    ])

    // 检查管理员权限
    const checkAdminPermission = async () => {
      try {
        const response = await fetch('/api/donation/check-admin', {
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

    // 获取当前配置
    const loadCurrentConfigs = async () => {
      try {
        const response = await fetch('/api/donation/configs', {
          credentials: 'include'
        })

        if (response.ok) {
          const data = await response.json()
          if (data.success && data.configs.length > 0) {
            currentConfigs.value = data.configs
            // 更新表单数据
            data.configs.forEach((config, index) => {
              if (index < configs.value.length) {
                configs.value[index] = {
                  price: config.price,
                  days: config.days
                }
              }
            })
          }
        }
      } catch (error) {
        console.error('获取当前配置失败:', error)
      }
    }

    // 保存配置
    const saveConfigs = async () => {
      // 验证配置
      for (let i = 0; i < configs.value.length; i++) {
        const config = configs.value[i]
        if (!config.price || config.price <= 0) {
          window.$toast(`方案${i + 1}的价格无效`, 'warning')
          return
        }
        if (!config.days || config.days <= 0) {
          window.$toast(`方案${i + 1}的天数无效`, 'warning')
          return
        }
      }

      saving.value = true

      try {
        const response = await fetch('/api/donation/configs', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include',
          body: JSON.stringify({
            configs: configs.value
          })
        })

        const data = await response.json()

        if (response.ok && data.success) {
          window.$toast('配置保存成功', 'success')
          await loadCurrentConfigs()
        } else {
          // 处理权限错误
          if (handleApiError(data)) {
            return
          }
          window.$toast(data.error || '保存失败', 'error')
        }
      } catch (error) {
        console.error('保存配置失败:', error)
        window.$toast('保存失败，请稍后重试', 'error')
      } finally {
        saving.value = false
      }
    }

    // 页面加载时检查权限和加载配置
    onMounted(async () => {
      await checkAdminPermission()
      if (isAdmin.value) {
        await loadCurrentConfigs()
      }
    })

    return {
      isAdmin,
      configs,
      currentConfigs,
      saving,
      saveConfigs
    }
  }
}
</script>

<style lang="scss" scoped>
.donation-manage {
  min-height: 100vh;
  background: $bg-color;
  padding: 20px;
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

.page-header {
  text-align: center;
  margin-bottom: 30px;
  
  .page-title {
    font-size: 24px;
    font-weight: 600;
    color: $text-color;
    margin: 0 0 8px 0;
  }
  
  .page-subtitle {
    font-size: 14px;
    color: $text-color-secondary;
    margin: 0;
  }
}

.config-form {
  background: white;
  border-radius: $border-radius-lg;
  padding: 20px;
  margin-bottom: 20px;
  
  .form-title {
    font-size: 18px;
    font-weight: 600;
    color: $text-color;
    margin: 0 0 20px 0;
  }
  
  .config-item {
    margin-bottom: 24px;
    padding: 16px;
    border: 1px solid $border-color-light;
    border-radius: $border-radius-sm;
    
    .config-title {
      font-size: 16px;
      font-weight: 600;
      color: $text-color;
      margin: 0 0 16px 0;
    }
    
    .form-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }
    
    .form-group {
      label {
        display: block;
        font-size: 14px;
        font-weight: 500;
        color: $text-color;
        margin-bottom: 8px;
      }
      
      .form-input {
        width: 100%;
        padding: 12px;
        border: 1px solid $border-color;
        border-radius: $border-radius-sm;
        font-size: 16px;
        
        &:focus {
          outline: none;
          border-color: $primary-color;
          box-shadow: 0 0 0 2px rgba($primary-color, 0.1);
        }
      }
    }
  }
  
  .form-actions {
    text-align: center;
    margin-top: 30px;
  }
}

.current-configs {
  background: white;
  border-radius: $border-radius-lg;
  padding: 20px;
  
  h3 {
    font-size: 16px;
    font-weight: 600;
    color: $text-color;
    margin: 0 0 16px 0;
  }
  
  .config-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 12px;
    
    .config-preview {
      padding: 12px;
      border: 1px solid $border-color-light;
      border-radius: $border-radius-sm;
      text-align: center;
      
      .config-info {
        display: flex;
        flex-direction: column;
        gap: 4px;
        
        .price {
          font-size: 16px;
          font-weight: 600;
          color: $primary-color;
        }
        
        .days {
          font-size: 14px;
          color: $text-color-secondary;
        }
      }
    }
  }
}
</style>
