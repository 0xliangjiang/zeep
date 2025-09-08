<template>
  <div class="error-state" :class="`error-${type}`">
    <div class="error-illustration">
      <div class="error-icon">{{ errorConfig.icon }}</div>
      <div class="error-animation">
        <div v-for="n in 3" :key="n" class="floating-element" :style="getFloatingStyle(n)">
          {{ errorConfig.floatingElements[n-1] }}
        </div>
      </div>
    </div>
    
    <div class="error-content">
      <h3 class="error-title">{{ title || errorConfig.title }}</h3>
      <p class="error-description">{{ description || errorConfig.description }}</p>
      
      <div v-if="showActions" class="error-actions">
        <WechatButton 
          v-if="showRetry"
          type="primary" 
          @click="handleRetry"
          :loading="retrying"
        >
          {{ retryText }}
        </WechatButton>
        
        <WechatButton 
          v-if="showHome"
          type="secondary" 
          @click="handleGoHome"
        >
          返回首页
        </WechatButton>
        
        <WechatButton 
          v-if="showContact"
          type="plain" 
          @click="handleContact"
        >
          联系客服
        </WechatButton>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import WechatButton from './WechatButton.vue'

export default {
  name: 'ErrorState',
  components: {
    WechatButton
  },
  props: {
    type: {
      type: String,
      default: 'network', // network, 404, 500, permission, empty
      validator: (value) => ['network', '404', '500', 'permission', 'empty', 'maintenance'].includes(value)
    },
    title: {
      type: String,
      default: ''
    },
    description: {
      type: String,
      default: ''
    },
    showActions: {
      type: Boolean,
      default: true
    },
    showRetry: {
      type: Boolean,
      default: true
    },
    showHome: {
      type: Boolean,
      default: true
    },
    showContact: {
      type: Boolean,
      default: false
    },
    retryText: {
      type: String,
      default: '重试'
    }
  },
  emits: ['retry', 'contact'],
  setup(props, { emit }) {
    const router = useRouter()
    const retrying = ref(false)

    const errorConfigs = {
      network: {
        icon: '📡',
        title: '网络连接异常',
        description: '请检查网络连接后重试',
        floatingElements: ['📶', '🌐', '📡']
      },
      404: {
        icon: '🔍',
        title: '页面不存在',
        description: '抱歉，您访问的页面不存在或已被删除',
        floatingElements: ['❓', '🔍', '📄']
      },
      500: {
        icon: '⚠️',
        title: '服务器错误',
        description: '服务器开小差了，请稍后重试',
        floatingElements: ['⚙️', '🔧', '⚠️']
      },
      permission: {
        icon: '🔒',
        title: '权限不足',
        description: '您没有访问此页面的权限',
        floatingElements: ['🔐', '🔑', '🚫']
      },
      empty: {
        icon: '📭',
        title: '暂无数据',
        description: '这里还没有任何内容',
        floatingElements: ['📄', '📋', '📊']
      },
      maintenance: {
        icon: '🔧',
        title: '系统维护中',
        description: '系统正在升级维护，请稍后访问',
        floatingElements: ['⚙️', '🔨', '🛠️']
      }
    }

    const errorConfig = computed(() => {
      return errorConfigs[props.type] || errorConfigs.network
    })

    const getFloatingStyle = (index) => {
      const positions = [
        { top: '10%', left: '20%', animationDelay: '0s' },
        { top: '30%', right: '15%', animationDelay: '1s' },
        { bottom: '20%', left: '15%', animationDelay: '2s' }
      ]
      
      return {
        ...positions[index - 1],
        fontSize: `${16 + Math.random() * 8}px`
      }
    }

    const handleRetry = async () => {
      retrying.value = true
      
      try {
        await new Promise(resolve => setTimeout(resolve, 1000))
        emit('retry')
      } finally {
        retrying.value = false
      }
    }

    const handleGoHome = () => {
      router.push('/')
    }

    const handleContact = () => {
      emit('contact')
    }

    return {
      retrying,
      errorConfig,
      getFloatingStyle,
      handleRetry,
      handleGoHome,
      handleContact
    }
  }
}
</script>

<style lang="scss" scoped>
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  padding: 40px 20px;
  text-align: center;
  
  .error-illustration {
    position: relative;
    margin-bottom: 30px;
    
    .error-icon {
      font-size: 80px;
      margin-bottom: 20px;
      animation: bounce 2s ease-in-out infinite;
    }
    
    .error-animation {
      position: relative;
      width: 200px;
      height: 100px;
      
      .floating-element {
        position: absolute;
        font-size: 20px;
        opacity: 0.6;
        animation: float 3s ease-in-out infinite;
        pointer-events: none;
      }
    }
  }
  
  .error-content {
    max-width: 300px;
    
    .error-title {
      font-size: 20px;
      font-weight: 600;
      color: $text-color;
      margin: 0 0 12px 0;
    }
    
    .error-description {
      font-size: 14px;
      color: $text-color-secondary;
      line-height: 1.5;
      margin: 0 0 30px 0;
    }
    
    .error-actions {
      display: flex;
      flex-direction: column;
      gap: 12px;
      
      .wechat-button {
        width: 100%;
      }
    }
  }
  
  // 不同类型的主题色
  &.error-network {
    .error-icon { color: #74b9ff; }
  }
  
  &.error-404 {
    .error-icon { color: #fdcb6e; }
  }
  
  &.error-500 {
    .error-icon { color: #e17055; }
  }
  
  &.error-permission {
    .error-icon { color: #fd79a8; }
  }
  
  &.error-empty {
    .error-icon { color: #a29bfe; }
  }
  
  &.error-maintenance {
    .error-icon { color: #00b894; }
  }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
    opacity: 0.6;
  }
  25% {
    transform: translateY(-10px) rotate(90deg);
    opacity: 0.8;
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
    opacity: 1;
  }
  75% {
    transform: translateY(-10px) rotate(270deg);
    opacity: 0.8;
  }
}
</style>
