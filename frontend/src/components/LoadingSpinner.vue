<template>
  <div class="loading-spinner" :class="[`size-${size}`, `type-${type}`]">
    <!-- 默认加载动画 -->
    <div v-if="type === 'default'" class="spinner-default">
      <div class="spinner-ring"></div>
      <div class="spinner-ring"></div>
      <div class="spinner-ring"></div>
    </div>
    
    <!-- 脉冲动画 -->
    <div v-else-if="type === 'pulse'" class="spinner-pulse">
      <div class="pulse-dot"></div>
      <div class="pulse-dot"></div>
      <div class="pulse-dot"></div>
    </div>
    
    <!-- 波浪动画 -->
    <div v-else-if="type === 'wave'" class="spinner-wave">
      <div class="wave-bar"></div>
      <div class="wave-bar"></div>
      <div class="wave-bar"></div>
      <div class="wave-bar"></div>
      <div class="wave-bar"></div>
    </div>
    
    <!-- 步数主题动画 -->
    <div v-else-if="type === 'steps'" class="spinner-steps">
      <div class="step-icon">👟</div>
      <div class="step-path">
        <div class="step-dot"></div>
        <div class="step-dot"></div>
        <div class="step-dot"></div>
      </div>
    </div>
    
    <!-- 心跳动画 -->
    <div v-else-if="type === 'heartbeat'" class="spinner-heartbeat">
      <div class="heart">💚</div>
    </div>
    
    <div v-if="text" class="loading-text">{{ text }}</div>
  </div>
</template>

<script>
export default {
  name: 'LoadingSpinner',
  props: {
    size: {
      type: String,
      default: 'medium', // small, medium, large
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    },
    type: {
      type: String,
      default: 'default', // default, pulse, wave, steps, heartbeat
      validator: (value) => ['default', 'pulse', 'wave', 'steps', 'heartbeat'].includes(value)
    },
    text: {
      type: String,
      default: ''
    }
  }
}
</script>

<style lang="scss" scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  
  &.size-small {
    .spinner-default .spinner-ring { width: 20px; height: 20px; }
    .spinner-pulse .pulse-dot { width: 6px; height: 6px; }
    .spinner-wave .wave-bar { width: 3px; height: 20px; }
    .spinner-steps .step-icon { font-size: 20px; }
    .spinner-heartbeat .heart { font-size: 20px; }
  }
  
  &.size-medium {
    .spinner-default .spinner-ring { width: 30px; height: 30px; }
    .spinner-pulse .pulse-dot { width: 8px; height: 8px; }
    .spinner-wave .wave-bar { width: 4px; height: 30px; }
    .spinner-steps .step-icon { font-size: 30px; }
    .spinner-heartbeat .heart { font-size: 30px; }
  }
  
  &.size-large {
    .spinner-default .spinner-ring { width: 40px; height: 40px; }
    .spinner-pulse .pulse-dot { width: 10px; height: 10px; }
    .spinner-wave .wave-bar { width: 5px; height: 40px; }
    .spinner-steps .step-icon { font-size: 40px; }
    .spinner-heartbeat .heart { font-size: 40px; }
  }
  
  .loading-text {
    margin-top: 12px;
    font-size: 14px;
    color: $text-color-secondary;
    text-align: center;
  }
}

// 默认环形加载动画
.spinner-default {
  position: relative;
  
  .spinner-ring {
    border: 3px solid transparent;
    border-top: 3px solid $primary-color;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    position: absolute;
    
    &:nth-child(1) {
      animation-delay: 0s;
      opacity: 1;
    }
    
    &:nth-child(2) {
      animation-delay: 0.3s;
      opacity: 0.7;
      transform: scale(0.8);
    }
    
    &:nth-child(3) {
      animation-delay: 0.6s;
      opacity: 0.4;
      transform: scale(0.6);
    }
  }
}

// 脉冲动画
.spinner-pulse {
  display: flex;
  gap: 4px;
  
  .pulse-dot {
    background: $primary-color;
    border-radius: 50%;
    animation: pulse 1.4s ease-in-out infinite both;
    
    &:nth-child(1) { animation-delay: -0.32s; }
    &:nth-child(2) { animation-delay: -0.16s; }
    &:nth-child(3) { animation-delay: 0s; }
  }
}

// 波浪动画
.spinner-wave {
  display: flex;
  gap: 2px;
  align-items: flex-end;
  
  .wave-bar {
    background: $primary-color;
    border-radius: 2px;
    animation: wave 1.2s ease-in-out infinite;
    
    &:nth-child(1) { animation-delay: 0s; }
    &:nth-child(2) { animation-delay: 0.1s; }
    &:nth-child(3) { animation-delay: 0.2s; }
    &:nth-child(4) { animation-delay: 0.3s; }
    &:nth-child(5) { animation-delay: 0.4s; }
  }
}

// 步数主题动画
.spinner-steps {
  display: flex;
  flex-direction: column;
  align-items: center;
  
  .step-icon {
    animation: stepBounce 1s ease-in-out infinite;
    margin-bottom: 8px;
  }
  
  .step-path {
    display: flex;
    gap: 8px;
    
    .step-dot {
      width: 6px;
      height: 6px;
      background: $primary-color;
      border-radius: 50%;
      animation: stepPath 1.5s ease-in-out infinite;
      
      &:nth-child(1) { animation-delay: 0s; }
      &:nth-child(2) { animation-delay: 0.2s; }
      &:nth-child(3) { animation-delay: 0.4s; }
    }
  }
}

// 心跳动画
.spinner-heartbeat {
  .heart {
    animation: heartbeat 1.5s ease-in-out infinite;
  }
}

// 动画定义
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 80%, 100% {
    transform: scale(0);
    opacity: 1;
  }
  40% {
    transform: scale(1);
    opacity: 0.5;
  }
}

@keyframes wave {
  0%, 40%, 100% {
    transform: scaleY(0.4);
  }
  20% {
    transform: scaleY(1);
  }
}

@keyframes stepBounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes stepPath {
  0%, 100% {
    opacity: 0.3;
    transform: scale(0.8);
  }
  50% {
    opacity: 1;
    transform: scale(1.2);
  }
}

@keyframes heartbeat {
  0%, 100% {
    transform: scale(1);
  }
  25% {
    transform: scale(1.1);
  }
  50% {
    transform: scale(1.3);
  }
  75% {
    transform: scale(1.1);
  }
}
</style>
