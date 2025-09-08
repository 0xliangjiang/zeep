<template>
  <div class="page">
    <div class="page-content">
      <div class="card">
        <div class="card-header">
          <h3>绑定Zepp账号</h3>
        </div>
        <div class="card-body">
          <p class="bind-desc">
            请扫描下方二维码关注公众号，完成Zepp账号绑定后即可开始使用步数修改功能。
          </p>
          <div class="qr-code-container">
            <div v-if="qrCodeUrl" class="qr-code">
              <img :src="qrCodeUrl" alt="绑定二维码" />
            </div>
            <div v-else class="qr-loading">
              <div class="loading-spinner"></div>
              <p>正在生成绑定二维码...</p>
            </div>
          </div>
          <div class="bind-status">
            <p v-if="!bindStatus" class="status-waiting">
              等待绑定中...
            </p>
            <p v-else class="status-success">
              ✓ 绑定成功！
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'Bind',
  setup() {
    const router = useRouter()
    const qrCodeUrl = ref('')
    const bindStatus = ref(false)
    let checkInterval = null

    // 获取绑定二维码
    const fetchQRCode = async () => {
      try {
        const response = await fetch('/api/zepp/qrcode', {
          credentials: 'include'
        })
        if (response.ok) {
          const data = await response.json()
          qrCodeUrl.value = data.qr_code_url
          startCheckBinding()
        }
      } catch (error) {
        console.error('获取二维码失败:', error)
      }
    }

    // 检查绑定状态
    const checkBindStatus = async () => {
      try {
        const response = await fetch('/api/zepp/bind-status', {
          credentials: 'include'
        })
        if (response.ok) {
          const data = await response.json()
          if (data.bind_status) {
            bindStatus.value = true
            stopCheckBinding()
            setTimeout(() => {
              router.push('/')
            }, 2000)
          }
        }
      } catch (error) {
        console.error('检查绑定状态失败:', error)
      }
    }

    // 开始检查绑定状态
    const startCheckBinding = () => {
      checkInterval = setInterval(checkBindStatus, 3000)
    }

    // 停止检查绑定状态
    const stopCheckBinding = () => {
      if (checkInterval) {
        clearInterval(checkInterval)
        checkInterval = null
      }
    }

    onMounted(() => {
      fetchQRCode()
    })

    onUnmounted(() => {
      stopCheckBinding()
    })

    return {
      qrCodeUrl,
      bindStatus
    }
  }
}
</script>

<style lang="scss" scoped>
.bind-desc {
  text-align: center;
  margin-bottom: $spacing-lg;
  line-height: $line-height-loose;
}

.qr-code-container {
  display: flex;
  justify-content: center;
  margin-bottom: $spacing-lg;

  .qr-code {
    img {
      width: 200px;
      height: 200px;
      border: 1px solid $border-color;
      border-radius: $border-radius-md;
    }
  }

  .qr-loading {
    text-align: center;

    .loading-spinner {
      width: 40px;
      height: 40px;
      border: 3px solid $border-color-light;
      border-top: 3px solid $primary-color;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin: 0 auto $spacing-md;
    }
  }
}

.bind-status {
  text-align: center;

  .status-waiting {
    color: $text-color-secondary;
  }

  .status-success {
    color: $success-color;
    font-weight: $font-weight-bold;
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>