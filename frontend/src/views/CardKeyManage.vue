<template>
  <div class="card-key-manage">
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
        <h1 class="page-title">卡密管理</h1>
        <p class="page-subtitle">生成和管理卡密</p>
      </div>

      <!-- 生成卡密表单 -->
      <div class="generate-form">
      <h2 class="form-title">生成卡密</h2>
      
      <div class="form-group">
        <label>卡密长度</label>
        <input 
          v-model.number="form.length" 
          type="number" 
          min="6" 
          max="32" 
          class="form-input"
          placeholder="6-32位"
        />
      </div>

      <div class="form-group">
        <label>包含字符类型</label>
        <div class="checkbox-group">
          <label class="checkbox-item">
            <input v-model="form.include_numbers" type="checkbox" />
            <span>数字</span>
          </label>
          <label class="checkbox-item">
            <input v-model="form.include_lowercase" type="checkbox" />
            <span>小写英文</span>
          </label>
          <label class="checkbox-item">
            <input v-model="form.include_uppercase" type="checkbox" />
            <span>大写英文</span>
          </label>
          <label class="checkbox-item">
            <input v-model="form.include_symbols" type="checkbox" />
            <span>特殊符号</span>
          </label>
        </div>
      </div>

      <div class="form-group">
        <label>生成个数</label>
        <input 
          v-model.number="form.count" 
          type="number" 
          min="1" 
          max="1000" 
          class="form-input"
          placeholder="1-1000个"
        />
      </div>

      <div class="form-group">
        <label>增加天数</label>
        <input 
          v-model.number="form.days" 
          type="number" 
          min="1" 
          max="3650" 
          class="form-input"
          placeholder="1-3650天"
        />
      </div>

      <div class="form-group">
        <label>卡密有效期</label>
        <div class="expire-group">
          <select v-model="form.expire_type" class="form-select">
            <option value="permanent">永久有效</option>
            <option value="minutes">分钟</option>
            <option value="hours">小时</option>
            <option value="days">天</option>
            <option value="weeks">周</option>
            <option value="months">月</option>
            <option value="years">年</option>
          </select>
          <input 
            v-if="form.expire_type !== 'permanent'"
            v-model.number="form.expire_value" 
            type="number" 
            min="1" 
            class="form-input expire-value"
            placeholder="数量"
          />
        </div>
      </div>

      <div class="form-actions">
        <WechatButton 
          type="primary" 
          @click="showConfirmDialog"
          :loading="generating"
        >
          生成卡密
        </WechatButton>
      </div>
    </div>

    <!-- 生成结果 -->
    <div v-if="generatedKeys.length > 0" class="generated-result">
      <h3>生成成功</h3>
      <div class="keys-container">
        <div class="keys-list">
          <div v-for="key in generatedKeys" :key="key" class="key-item">
            {{ key }}
          </div>
        </div>
        <WechatButton type="plain" @click="copyAllKeys">
          复制全部
        </WechatButton>
      </div>
    </div>

    <!-- 确认对话框 -->
    <WechatModal
      v-if="showConfirm"
      title="确认生成卡密"
      :content="confirmMessage"
      :show-cancel="true"
      confirm-text="确定生成"
      @confirm="generateKeys"
      @cancel="hideConfirmDialog"
      @close="hideConfirmDialog"
    />
    </template>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import WechatButton from '../components/WechatButton.vue'
import WechatModal from '../components/WechatModal.vue'

export default {
  name: 'CardKeyManage',
  components: {
    WechatButton,
    WechatModal
  },
  setup() {
    const router = useRouter()
    const form = ref({
      length: 12,
      include_numbers: true,
      include_lowercase: true,
      include_uppercase: false,
      include_symbols: false,
      count: 10,
      days: 7,
      expire_type: 'permanent',
      expire_value: 1
    })

    const generating = ref(false)
    const generatedKeys = ref([])
    const showConfirm = ref(false)
    const isAdmin = ref(false)

    // 检查管理员权限
    const checkAdminPermission = async () => {
      try {
        const response = await fetch('/api/card/check-admin', {
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

    const confirmMessage = computed(() => {
      const expireText = form.value.expire_type === 'permanent' 
        ? '永久有效' 
        : `${form.value.expire_value}${getExpireTypeText(form.value.expire_type)}后过期`
      
      return `确定生成 ${form.value.count} 个卡密吗？\n` +
             `卡密长度：${form.value.length} 位\n` +
             `增加天数：${form.value.days} 天\n` +
             `有效期：${expireText}`
    })

    const getExpireTypeText = (type) => {
      const typeMap = {
        minutes: '分钟',
        hours: '小时',
        days: '天',
        weeks: '周',
        months: '月',
        years: '年'
      }
      return typeMap[type] || ''
    }

    const showConfirmDialog = () => {
      // 验证表单
      if (!validateForm()) {
        return
      }
      showConfirm.value = true
    }

    const hideConfirmDialog = () => {
      showConfirm.value = false
    }

    const validateForm = () => {
      if (form.value.length < 6 || form.value.length > 32) {
        window.$toast('卡密长度必须在6-32位之间', 'warning')
        return false
      }

      if (!form.value.include_numbers && !form.value.include_lowercase && 
          !form.value.include_uppercase && !form.value.include_symbols) {
        window.$toast('至少选择一种字符类型', 'warning')
        return false
      }

      if (form.value.count < 1 || form.value.count > 1000) {
        window.$toast('生成个数必须在1-1000之间', 'warning')
        return false
      }

      if (form.value.days < 1 || form.value.days > 3650) {
        window.$toast('天数必须在1-3650之间', 'warning')
        return false
      }

      return true
    }

    const generateKeys = async () => {
      hideConfirmDialog()
      generating.value = true
      generatedKeys.value = []

      try {
        const response = await fetch('/api/card/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include',
          body: JSON.stringify(form.value)
        })

        const data = await response.json()

        if (response.ok && data.success) {
          generatedKeys.value = data.keys
          window.$toast(`成功生成${data.count}个卡密`, 'success')
        } else {
          // 处理权限错误
          if (handleApiError(data)) {
            return
          }
          window.$toast(data.error || '生成失败', 'error')
        }
      } catch (error) {
        console.error('生成卡密失败:', error)
        window.$toast('生成失败，请稍后重试', 'error')
      } finally {
        generating.value = false
      }
    }

    const copyAllKeys = async () => {
      try {
        const keysText = generatedKeys.value.join('\n')
        await navigator.clipboard.writeText(keysText)
        window.$toast('已复制到剪贴板', 'success')
      } catch (error) {
        console.error('复制失败:', error)
        window.$toast('复制失败', 'error')
      }
    }

    // 页面加载时检查权限
    onMounted(() => {
      checkAdminPermission()
    })

    return {
      form,
      generating,
      generatedKeys,
      showConfirm,
      confirmMessage,
      isAdmin,
      showConfirmDialog,
      hideConfirmDialog,
      generateKeys,
      copyAllKeys
    }
  }
}
</script>

<style lang="scss" scoped>
.card-key-manage {
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

.generate-form {
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
  
  .form-group {
    margin-bottom: 20px;
    
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
    
    .form-select {
      width: 100%;
      padding: 12px;
      border: 1px solid $border-color;
      border-radius: $border-radius-sm;
      font-size: 16px;
      background: white;
      
      &:focus {
        outline: none;
        border-color: $primary-color;
      }
    }
  }
  
  .checkbox-group {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    
    .checkbox-item {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 14px;
      cursor: pointer;
      
      input[type="checkbox"] {
        width: 16px;
        height: 16px;
      }
    }
  }
  
  .expire-group {
    display: flex;
    gap: 12px;
    
    .form-select {
      flex: 1;
    }
    
    .expire-value {
      flex: 1;
    }
  }
  
  .form-actions {
    text-align: center;
    margin-top: 30px;
  }
}

.generated-result {
  background: white;
  border-radius: $border-radius-lg;
  padding: 20px;
  
  h3 {
    font-size: 16px;
    font-weight: 600;
    color: $success-color;
    margin: 0 0 16px 0;
  }
  
  .keys-container {
    .keys-list {
      background: $bg-color-secondary;
      border-radius: $border-radius-sm;
      padding: 16px;
      margin-bottom: 16px;
      max-height: 200px;
      overflow-y: auto;
      
      .key-item {
        font-family: 'Courier New', monospace;
        font-size: 14px;
        color: $text-color;
        padding: 4px 0;
        border-bottom: 1px solid $border-color-light;

        &:last-child {
          border-bottom: none;
        }
      }
    }
  }
}
</style>
