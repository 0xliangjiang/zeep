<template>
  <div v-if="show" class="donation-modal-overlay" @click="handleOverlayClick">
    <div class="donation-modal" @click.stop>
      <!-- VIP动图 -->
      <div class="vip-animation">
        <img src="/static/images/vip.gif" alt="VIP" class="vip-gif" />
      </div>
      
      <!-- 标题 -->
      <div class="modal-header">
        <h2 class="modal-title">服务器炸了</h2>
        <p class="modal-subtitle">捐赠者可挽救服务器继续使用</p>
        <p class="modal-description">只需要捐赠￥{{ minPrice }}，即可获得永久娱乐权</p>
      </div>
      
      <!-- 捐赠选项 -->
      <div class="donation-options">
        <WechatButton 
          type="plain" 
          class="cancel-btn"
          @click="handleCancel"
        >
          不想捐赠
        </WechatButton>
        
        <WechatButton 
          v-for="config in configs" 
          :key="config.id"
          type="primary" 
          class="donation-btn"
          :loading="processingConfigId === config.id"
          @click="handleDonation(config)"
        >
          捐赠￥{{ config.price }} ({{ config.days }}天)
        </WechatButton>
      </div>
      
      <!-- 关闭按钮 -->
      <button class="close-btn" @click="handleClose">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import WechatButton from './WechatButton.vue'

export default {
  name: 'DonationModal',
  components: {
    WechatButton
  },
  props: {
    show: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close', 'success', 'failed'],
  setup(props, { emit }) {
    const configs = ref([])
    const processingConfigId = ref(null)

    // 第三个按钮价格（用于永久权限显示）
    const minPrice = computed(() => {
      if (configs.value.length < 3) return '9.9'
      // 按价格排序后取第三个
      const sortedConfigs = [...configs.value].sort((a, b) => a.price - b.price)
      return sortedConfigs[2].price.toFixed(1)
    })

    // 获取捐赠配置
    const loadConfigs = async () => {
      try {
        const response = await fetch('/api/donation/configs', {
          credentials: 'include'
        })

        if (response.ok) {
          const data = await response.json()
          if (data.success) {
            configs.value = data.configs
          }
        }
      } catch (error) {
        console.error('获取捐赠配置失败:', error)
      }
    }

    // 处理捐赠
    const handleDonation = async (config) => {
      processingConfigId.value = config.id

      try {
        // 创建订单
        const response = await fetch('/api/donation/create-order', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include',
          body: JSON.stringify({
            config_id: config.id
          })
        })

        const data = await response.json()

        if (response.ok && data.success) {
          // 调用微信支付
          await callWechatPay(data.payment_params, config.days)
        } else {
          // 处理错误信息，确保显示可读的中文
          let errorMsg = '创建订单失败'
          if (data.error) {
            // 如果错误信息包含乱码，尝试解码
            try {
              errorMsg = data.error
              // 如果错误信息太长或包含特殊字符，截取前100个字符
              if (errorMsg.length > 100) {
                errorMsg = errorMsg.substring(0, 100) + '...'
              }
            } catch (e) {
              errorMsg = '创建订单失败，请稍后重试'
            }
          }
          console.error('创建订单失败:', data)
          window.$toast(errorMsg, 'error')
          emit('failed')
        }
      } catch (error) {
        console.error('处理捐赠失败:', error)
        window.$toast('捐赠失败，请重试', 'error')
        emit('failed')
      } finally {
        processingConfigId.value = null
      }
    }

    // 调用微信支付
    const callWechatPay = (paymentParams, days) => {
      return new Promise((resolve, reject) => {
        // 检查是否在微信环境中
        if (typeof WeixinJSBridge === 'undefined') {
          window.$toast('请在微信中打开', 'error')
          emit('failed')
          reject(new Error('不在微信环境中'))
          return
        }

        // 调用微信支付
        WeixinJSBridge.invoke('getBrandWCPayRequest', {
          appId: paymentParams.appId,
          timeStamp: paymentParams.timeStamp,
          nonceStr: paymentParams.nonceStr,
          package: paymentParams.package,
          signType: paymentParams.signType,
          paySign: paymentParams.paySign
        }, (res) => {
          if (res.err_msg === 'get_brand_wcpay_request:ok') {
            // 支付成功
            window.$toast(`捐赠成功，已获得${days}天体验时间`, 'success')
            emit('success', days)
            handleClose()
            resolve()
          } else if (res.err_msg === 'get_brand_wcpay_request:cancel') {
            // 用户取消支付
            window.$toast('支付已取消', 'warning')
            emit('failed')
            reject(new Error('用户取消支付'))
          } else {
            // 支付失败
            window.$toast('支付失败，请重试', 'error')
            emit('failed')
            reject(new Error('支付失败'))
          }
        })
      })
    }



    // 处理取消
    const handleCancel = () => {
      handleClose()
    }

    // 处理关闭
    const handleClose = () => {
      emit('close')
    }

    // 处理遮罩点击
    const handleOverlayClick = () => {
      handleClose()
    }

    // 监听显示状态，加载配置
    watch(() => props.show, (newShow) => {
      if (newShow) {
        loadConfigs()
      }
    })

    // 页面加载时获取配置
    onMounted(() => {
      if (props.show) {
        loadConfigs()
      }
    })

    return {
      configs,
      processingConfigId,
      minPrice,
      handleDonation,
      handleCancel,
      handleClose,
      handleOverlayClick,
      callWechatPay
    }
  }
}
</script>

<style lang="scss" scoped>
.donation-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.donation-modal {
  background: white;
  border-radius: $border-radius-lg;
  padding: 30px 20px;
  max-width: 400px;
  width: 100%;
  position: relative;
  max-height: 80vh;
  overflow-y: auto;
  
  .close-btn {
    position: absolute;
    top: 16px;
    right: 16px;
    width: 32px;
    height: 32px;
    border: none;
    background: none;
    color: #999;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all 0.2s ease;
    
    &:hover {
      background: #f5f5f5;
      color: #666;
    }
  }
}

.vip-animation {
  text-align: center;
  margin-bottom: 20px;

  .vip-placeholder {
    display: inline-block;
    border-radius: $border-radius-sm;
    background: linear-gradient(45deg, #FFD700, #FFA500);
    padding: 10px;
    box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
  }

  .vip-gif {
    width: 120px;
    height: auto;
    border-radius: $border-radius-sm;
  }
}

.modal-header {
  text-align: center;
  margin-bottom: 30px;
  
  .modal-title {
    font-size: 24px;
    font-weight: 600;
    color: $text-color;
    margin: 0 0 12px 0;
  }
  
  .modal-subtitle {
    font-size: 16px;
    color: $text-color-secondary;
    margin: 0 0 8px 0;
  }
  
  .modal-description {
    font-size: 14px;
    color: $primary-color;
    margin: 0;
    font-weight: 500;
  }
}

.donation-options {
  display: flex;
  flex-direction: column;
  gap: 12px;
  
  .cancel-btn {
    order: -1;
    margin-bottom: 8px;
  }
  
  .donation-btn {
    font-weight: 600;
  }
}

// 动画效果
.donation-modal-overlay {
  animation: fadeIn 0.3s ease;
}

.donation-modal {
  animation: slideUp 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
</style>
