<template>
  <div class="progress-bar-container">
    <div class="progress-info" v-if="showInfo">
      <span class="progress-label">{{ label }}</span>
      <span class="progress-value">{{ current }}/{{ total }}</span>
    </div>
    
    <div class="progress-bar" :class="{ 'with-glow': glowEffect }">
      <div 
        class="progress-fill" 
        :style="{ 
          width: percentage + '%',
          background: gradientBackground 
        }"
      >
        <div v-if="showPercentage" class="progress-percentage">
          {{ Math.round(percentage) }}%
        </div>
      </div>
    </div>
    
    <div v-if="showDays" class="days-info">
      <span class="days-remaining">剩余 {{ remainingDays }} 天</span>
      <span class="days-total">共 {{ totalDays }} 天</span>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'ProgressBar',
  props: {
    current: {
      type: Number,
      default: 0
    },
    total: {
      type: Number,
      default: 100
    },
    label: {
      type: String,
      default: ''
    },
    showInfo: {
      type: Boolean,
      default: true
    },
    showPercentage: {
      type: Boolean,
      default: false
    },
    showDays: {
      type: Boolean,
      default: false
    },
    totalDays: {
      type: Number,
      default: 0
    },
    glowEffect: {
      type: Boolean,
      default: false
    },
    color: {
      type: String,
      default: 'primary' // primary, success, warning, danger
    }
  },
  setup(props) {
    const percentage = computed(() => {
      if (props.total === 0) return 0
      return Math.min((props.current / props.total) * 100, 100)
    })

    const remainingDays = computed(() => {
      return Math.max(props.totalDays - props.current, 0)
    })

    const gradientBackground = computed(() => {
      const colors = {
        primary: 'linear-gradient(90deg, #07c160, #00d084)',
        success: 'linear-gradient(90deg, #52c41a, #73d13d)',
        warning: 'linear-gradient(90deg, #faad14, #ffc53d)',
        danger: 'linear-gradient(90deg, #ff4d4f, #ff7875)'
      }
      return colors[props.color] || colors.primary
    })

    return {
      percentage,
      remainingDays,
      gradientBackground
    }
  }
}
</script>

<style lang="scss" scoped>
.progress-bar-container {
  .progress-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
    
    .progress-label {
      font-size: 14px;
      font-weight: 500;
      color: $text-color;
    }
    
    .progress-value {
      font-size: 14px;
      font-weight: 600;
      color: $primary-color;
    }
  }
  
  .progress-bar {
    height: 8px;
    background: #f0f0f0;
    border-radius: 4px;
    overflow: hidden;
    position: relative;
    
    &.with-glow {
      box-shadow: 0 0 10px rgba(7, 193, 96, 0.3);
    }
    
    .progress-fill {
      height: 100%;
      border-radius: 4px;
      transition: width 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
      position: relative;
      
      &::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: shimmer 2s infinite;
      }
      
      .progress-percentage {
        position: absolute;
        right: 8px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 10px;
        font-weight: 600;
        color: white;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
      }
    }
  }
  
  .days-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
    
    .days-remaining {
      font-size: 12px;
      color: $primary-color;
      font-weight: 600;
    }
    
    .days-total {
      font-size: 12px;
      color: $text-color-secondary;
    }
  }
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}
</style>
