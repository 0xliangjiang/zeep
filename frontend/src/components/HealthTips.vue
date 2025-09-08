<template>
  <div class="health-tips">
    <div class="tips-header">
      <div class="tips-icon">💡</div>
      <div class="tips-title">健康小贴士</div>
      <div class="tips-indicator">
        <span 
          v-for="(tip, index) in tips" 
          :key="index"
          class="indicator-dot"
          :class="{ active: index === currentIndex }"
        ></span>
      </div>
    </div>
    
    <div class="tips-content" @touchstart="handleTouchStart" @touchend="handleTouchEnd">
      <transition :name="slideDirection" mode="out-in">
        <div :key="currentIndex" class="tip-item">
          <div class="tip-emoji">{{ currentTip.emoji }}</div>
          <div class="tip-text">{{ currentTip.text }}</div>
          <div class="tip-category">{{ currentTip.category }}</div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'

export default {
  name: 'HealthTips',
  setup() {
    const currentIndex = ref(0)
    const slideDirection = ref('slide-left')
    const autoPlayTimer = ref(null)
    const touchStartX = ref(0)
    const touchEndX = ref(0)

    const tips = ref([
      {
        emoji: '🚶‍♂️',
        text: '每天走路30分钟，可以有效降低心血管疾病风险',
        category: '运动健康'
      },
      {
        emoji: '💧',
        text: '每天至少喝8杯水，保持身体水分平衡',
        category: '饮食健康'
      },
      {
        emoji: '😴',
        text: '充足的睡眠有助于身体恢复和免疫力提升',
        category: '睡眠健康'
      },
      {
        emoji: '🥗',
        text: '多吃蔬菜水果，补充维生素和纤维素',
        category: '营养均衡'
      },
      {
        emoji: '🧘‍♀️',
        text: '适当的冥想和放松可以减轻压力',
        category: '心理健康'
      },
      {
        emoji: '🏃‍♂️',
        text: '规律运动能提高新陈代谢，保持健康体重',
        category: '运动健康'
      },
      {
        emoji: '🌞',
        text: '适量晒太阳有助于维生素D的合成',
        category: '生活习惯'
      },
      {
        emoji: '🚭',
        text: '戒烟限酒，远离有害物质对身体的伤害',
        category: '健康生活'
      }
    ])

    const currentTip = computed(() => tips.value[currentIndex.value])

    const nextTip = () => {
      slideDirection.value = 'slide-left'
      currentIndex.value = (currentIndex.value + 1) % tips.value.length
    }

    const prevTip = () => {
      slideDirection.value = 'slide-right'
      currentIndex.value = currentIndex.value === 0 ? tips.value.length - 1 : currentIndex.value - 1
    }

    const startAutoPlay = () => {
      autoPlayTimer.value = setInterval(() => {
        nextTip()
      }, 5000) // 每5秒切换
    }

    const stopAutoPlay = () => {
      if (autoPlayTimer.value) {
        clearInterval(autoPlayTimer.value)
        autoPlayTimer.value = null
      }
    }

    const handleTouchStart = (e) => {
      touchStartX.value = e.touches[0].clientX
      stopAutoPlay()
    }

    const handleTouchEnd = (e) => {
      touchEndX.value = e.changedTouches[0].clientX
      const diff = touchStartX.value - touchEndX.value
      
      if (Math.abs(diff) > 50) { // 滑动距离大于50px
        if (diff > 0) {
          nextTip() // 向左滑动，下一个
        } else {
          prevTip() // 向右滑动，上一个
        }
      }
      
      startAutoPlay()
    }

    onMounted(() => {
      startAutoPlay()
    })

    onUnmounted(() => {
      stopAutoPlay()
    })

    return {
      tips,
      currentIndex,
      currentTip,
      slideDirection,
      handleTouchStart,
      handleTouchEnd
    }
  }
}
</script>

<style lang="scss" scoped>
.health-tips {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: $border-radius-lg;
  padding: 20px;
  color: white;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
    pointer-events: none;
  }
  
  .tips-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
    position: relative;
    z-index: 1;
    
    .tips-icon {
      font-size: 20px;
    }
    
    .tips-title {
      font-size: 16px;
      font-weight: 600;
    }
    
    .tips-indicator {
      display: flex;
      gap: 4px;
      
      .indicator-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.4);
        transition: all 0.3s ease;
        
        &.active {
          background: white;
          transform: scale(1.2);
        }
      }
    }
  }
  
  .tips-content {
    position: relative;
    z-index: 1;
    min-height: 80px;
    
    .tip-item {
      text-align: center;
      
      .tip-emoji {
        font-size: 32px;
        margin-bottom: 12px;
      }
      
      .tip-text {
        font-size: 14px;
        line-height: 1.5;
        margin-bottom: 8px;
        opacity: 0.95;
      }
      
      .tip-category {
        font-size: 12px;
        opacity: 0.7;
        background: rgba(255, 255, 255, 0.2);
        padding: 4px 8px;
        border-radius: 12px;
        display: inline-block;
      }
    }
  }
}

// 滑动动画
.slide-left-enter-active,
.slide-left-leave-active,
.slide-right-enter-active,
.slide-right-leave-active {
  transition: all 0.3s ease;
}

.slide-left-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.slide-left-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

.slide-right-enter-from {
  transform: translateX(-100%);
  opacity: 0;
}

.slide-right-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>
