<template>
  <div v-if="show" class="particle-effect" @click="hide">
    <div 
      v-for="particle in particles" 
      :key="particle.id"
      class="particle"
      :style="particle.style"
    >
      {{ particle.emoji }}
    </div>
    <div class="success-message">
      <div class="success-icon">🎉</div>
      <div class="success-text">{{ message }}</div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'

export default {
  name: 'ParticleEffect',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    message: {
      type: String,
      default: '操作成功！'
    },
    type: {
      type: String,
      default: 'success' // success, celebration
    }
  },
  emits: ['hide'],
  setup(props, { emit }) {
    const particles = ref([])

    const createParticles = () => {
      const particleCount = 20
      const emojis = props.type === 'celebration' 
        ? ['🎉', '🎊', '✨', '🌟', '💫', '🎈'] 
        : ['✨', '⭐', '💫', '🌟', '✅', '👍']
      
      particles.value = []
      
      for (let i = 0; i < particleCount; i++) {
        const particle = {
          id: i,
          emoji: emojis[Math.floor(Math.random() * emojis.length)],
          style: {
            left: Math.random() * 100 + '%',
            animationDelay: Math.random() * 2 + 's',
            animationDuration: (2 + Math.random() * 2) + 's',
            fontSize: (16 + Math.random() * 8) + 'px'
          }
        }
        particles.value.push(particle)
      }
    }

    const hide = () => {
      emit('hide')
    }

    watch(() => props.show, (newShow) => {
      if (newShow) {
        createParticles()
        // 3秒后自动隐藏
        setTimeout(() => {
          hide()
        }, 3000)
      }
    })

    return {
      particles,
      hide
    }
  }
}
</script>

<style lang="scss" scoped>
.particle-effect {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: auto;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.1);
  
  .particle {
    position: absolute;
    pointer-events: none;
    animation: particleFloat 3s ease-out forwards;
    user-select: none;
  }
  
  .success-message {
    background: white;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    text-align: center;
    animation: messageAppear 0.5s ease-out;
    
    .success-icon {
      font-size: 48px;
      margin-bottom: 16px;
      animation: iconBounce 0.6s ease-out 0.2s both;
    }
    
    .success-text {
      font-size: 18px;
      font-weight: 600;
      color: $text-color;
      animation: textSlideUp 0.5s ease-out 0.4s both;
    }
  }
}

@keyframes particleFloat {
  0% {
    transform: translateY(100vh) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100px) rotate(360deg);
    opacity: 0;
  }
}

@keyframes messageAppear {
  0% {
    transform: scale(0.5);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes iconBounce {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes textSlideUp {
  0% {
    transform: translateY(20px);
    opacity: 0;
  }
  100% {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
