<template>
  <div class="weather-info" :class="weatherClass">
    <div v-if="loading" class="weather-loading">
      <SkeletonLoader :rows="2" type="card" />
    </div>
    
    <div v-else-if="weather" class="weather-content">
      <div class="weather-main">
        <div class="weather-icon">{{ weatherIcon }}</div>
        <div class="weather-details">
          <div class="temperature">{{ weather.temperature }}°C</div>
          <div class="description">{{ weather.description }}</div>
          <div class="location">📍 {{ weather.location }}</div>
        </div>
      </div>
      
      <div class="weather-suggestion">
        <div class="suggestion-icon">💡</div>
        <div class="suggestion-text">{{ weatherSuggestion }}</div>
      </div>
    </div>
    
    <div v-else class="weather-error">
      <div class="error-icon">🌤️</div>
      <div class="error-text">暂时无法获取天气信息</div>
      <button class="retry-btn" @click="fetchWeather">重试</button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import SkeletonLoader from './SkeletonLoader.vue'

export default {
  name: 'WeatherInfo',
  components: {
    SkeletonLoader
  },
  setup() {
    const loading = ref(true)
    const weather = ref(null)
    const error = ref(null)

    // 模拟天气数据（实际项目中应该调用真实的天气API）
    const mockWeatherData = [
      {
        temperature: 22,
        description: '晴朗',
        condition: 'sunny',
        location: '北京市',
        humidity: 45,
        windSpeed: 12
      },
      {
        temperature: 18,
        description: '多云',
        condition: 'cloudy',
        location: '上海市',
        humidity: 60,
        windSpeed: 8
      },
      {
        temperature: 15,
        description: '小雨',
        condition: 'rainy',
        location: '广州市',
        humidity: 80,
        windSpeed: 15
      }
    ]

    const weatherIcon = computed(() => {
      if (!weather.value) return '🌤️'
      
      const icons = {
        sunny: '☀️',
        cloudy: '☁️',
        rainy: '🌧️',
        snowy: '❄️',
        foggy: '🌫️'
      }
      
      return icons[weather.value.condition] || '🌤️'
    })

    const weatherClass = computed(() => {
      if (!weather.value) return ''
      
      return `weather-${weather.value.condition}`
    })

    const weatherSuggestion = computed(() => {
      if (!weather.value) return ''
      
      const suggestions = {
        sunny: '天气晴朗，适合户外运动！快去走走吧 🚶‍♂️',
        cloudy: '多云天气，温度适宜，是散步的好时机 🌤️',
        rainy: '下雨天，室内运动也很棒！做做拉伸吧 🏠',
        snowy: '雪天路滑，注意安全，室内活动更安全 ❄️',
        foggy: '雾天能见度低，建议室内运动 🌫️'
      }
      
      return suggestions[weather.value.condition] || '保持运动，保持健康！'
    })

    const fetchWeather = async () => {
      loading.value = true
      error.value = null
      
      try {
        // 模拟API调用延迟
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // 随机选择一个天气数据
        const randomWeather = mockWeatherData[Math.floor(Math.random() * mockWeatherData.length)]
        weather.value = randomWeather
        
        // 模拟偶尔的错误
        if (Math.random() < 0.1) {
          throw new Error('网络错误')
        }
        
      } catch (err) {
        error.value = err.message
        weather.value = null
      } finally {
        loading.value = false
      }
    }

    onMounted(() => {
      fetchWeather()
    })

    return {
      loading,
      weather,
      error,
      weatherIcon,
      weatherClass,
      weatherSuggestion,
      fetchWeather
    }
  }
}
</script>

<style lang="scss" scoped>
.weather-info {
  border-radius: $border-radius-lg;
  padding: 16px;
  background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
  color: white;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
    animation: float 6s ease-in-out infinite;
  }
  
  &.weather-sunny {
    background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%);
  }
  
  &.weather-cloudy {
    background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
  }
  
  &.weather-rainy {
    background: linear-gradient(135deg, #636e72 0%, #2d3436 100%);
  }
  
  &.weather-snowy {
    background: linear-gradient(135deg, #ddd6fe 0%, #8b5cf6 100%);
  }
  
  .weather-loading,
  .weather-content,
  .weather-error {
    position: relative;
    z-index: 1;
  }
  
  .weather-main {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
    
    .weather-icon {
      font-size: 40px;
      margin-right: 16px;
    }
    
    .weather-details {
      flex: 1;
      
      .temperature {
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 4px;
      }
      
      .description {
        font-size: 14px;
        opacity: 0.9;
        margin-bottom: 4px;
      }
      
      .location {
        font-size: 12px;
        opacity: 0.8;
      }
    }
  }
  
  .weather-suggestion {
    display: flex;
    align-items: flex-start;
    background: rgba(255, 255, 255, 0.2);
    border-radius: $border-radius-sm;
    padding: 12px;
    
    .suggestion-icon {
      font-size: 16px;
      margin-right: 8px;
      margin-top: 2px;
    }
    
    .suggestion-text {
      font-size: 13px;
      line-height: 1.4;
      opacity: 0.95;
    }
  }
  
  .weather-error {
    text-align: center;
    
    .error-icon {
      font-size: 32px;
      margin-bottom: 8px;
    }
    
    .error-text {
      font-size: 14px;
      margin-bottom: 12px;
      opacity: 0.9;
    }
    
    .retry-btn {
      background: rgba(255, 255, 255, 0.2);
      border: 1px solid rgba(255, 255, 255, 0.3);
      color: white;
      padding: 6px 12px;
      border-radius: 16px;
      font-size: 12px;
      cursor: pointer;
      transition: all 0.2s ease;
      
      &:hover {
        background: rgba(255, 255, 255, 0.3);
      }
    }
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}
</style>
