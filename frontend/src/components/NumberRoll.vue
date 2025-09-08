<template>
  <span class="number-roll">
    <span 
      v-for="(digit, index) in displayDigits" 
      :key="index" 
      class="digit-container"
    >
      <span 
        class="digit" 
        :style="{ transform: `translateY(-${digit * 10}%)` }"
      >
        <span v-for="n in 10" :key="n-1" class="digit-item">{{ n-1 }}</span>
      </span>
    </span>
  </span>
</template>

<script>
import { ref, watch, computed } from 'vue'

export default {
  name: 'NumberRoll',
  props: {
    value: {
      type: [Number, String],
      default: 0
    },
    duration: {
      type: Number,
      default: 1000
    }
  },
  setup(props) {
    const currentValue = ref(0)
    const isAnimating = ref(false)

    const displayDigits = computed(() => {
      const str = currentValue.value.toString().padStart(5, '0')
      return str.split('').map(Number)
    })

    const animateToValue = (targetValue) => {
      if (isAnimating.value) return
      
      isAnimating.value = true
      const startValue = currentValue.value
      const difference = targetValue - startValue
      const startTime = Date.now()

      const animate = () => {
        const elapsed = Date.now() - startTime
        const progress = Math.min(elapsed / props.duration, 1)
        
        // 使用缓动函数
        const easeOutCubic = 1 - Math.pow(1 - progress, 3)
        
        currentValue.value = Math.round(startValue + difference * easeOutCubic)
        
        if (progress < 1) {
          requestAnimationFrame(animate)
        } else {
          isAnimating.value = false
        }
      }
      
      requestAnimationFrame(animate)
    }

    watch(() => props.value, (newValue) => {
      const numValue = typeof newValue === 'string' ? parseInt(newValue) : newValue
      if (!isNaN(numValue) && numValue !== currentValue.value) {
        animateToValue(numValue)
      }
    }, { immediate: true })

    return {
      displayDigits
    }
  }
}
</script>

<style lang="scss" scoped>
.number-roll {
  display: inline-flex;
  font-variant-numeric: tabular-nums;
  
  .digit-container {
    display: inline-block;
    height: 1.2em;
    overflow: hidden;
    position: relative;
    
    .digit {
      display: flex;
      flex-direction: column;
      transition: transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
      
      .digit-item {
        height: 1.2em;
        display: flex;
        align-items: center;
        justify-content: center;
        line-height: 1;
      }
    }
  }
}
</style>
