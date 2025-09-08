<template>
  <div class="floating-contact-button" @click="handleClick">
    <div class="contact-button">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M8 9h8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M8 13h6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </div>
    
    <!-- 提示文字 -->
    <div class="contact-tooltip" :class="{ 'show': showTooltip }">
      联系客服
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  name: 'FloatingContactButton',
  emits: ['click'],
  setup(props, { emit }) {
    const showTooltip = ref(false)
    let tooltipTimer = null

    const handleClick = () => {
      emit('click')
    }

    // 自动显示提示文字
    const showTooltipTemporarily = () => {
      showTooltip.value = true
      tooltipTimer = setTimeout(() => {
        showTooltip.value = false
      }, 3000)
    }

    onMounted(() => {
      // 页面加载后3秒显示提示
      setTimeout(() => {
        showTooltipTemporarily()
      }, 3000)
    })

    onUnmounted(() => {
      if (tooltipTimer) {
        clearTimeout(tooltipTimer)
      }
    })

    return {
      showTooltip,
      handleClick
    }
  }
}
</script>

<style lang="scss" scoped>
.floating-contact-button {
  position: fixed;
  bottom: 80px; // 避免与底部导航重叠
  right: 20px;
  z-index: 1000;
  
  .contact-button {
    width: 56px;
    height: 56px;
    background: linear-gradient(135deg, #4682B4 0%, #87CEEB 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 16px rgba(70, 130, 180, 0.3);
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(70, 130, 180, 0.4);
    }
    
    &:active {
      transform: translateY(0);
    }
    
    svg {
      color: white;
    }
  }
  
  .contact-tooltip {
    position: absolute;
    right: 70px;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 12px;
    white-space: nowrap;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    
    &::after {
      content: '';
      position: absolute;
      left: 100%;
      top: 50%;
      transform: translateY(-50%);
      border: 6px solid transparent;
      border-left-color: rgba(0, 0, 0, 0.8);
    }
    
    &.show {
      opacity: 1;
      visibility: visible;
    }
  }
  
  // 悬停时显示提示
  &:hover .contact-tooltip {
    opacity: 1;
    visibility: visible;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .floating-contact-button {
    bottom: 90px;
    right: 16px;
    
    .contact-button {
      width: 48px;
      height: 48px;
      
      svg {
        width: 20px;
        height: 20px;
      }
    }
  }
}
</style>
