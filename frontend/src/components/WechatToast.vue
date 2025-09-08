<template>
  <transition name="toast-fade">
    <div v-if="visible" :class="toastClass">
      <div class="toast-icon" v-if="showIcon">
        <span v-if="type === 'success'">✓</span>
        <span v-else-if="type === 'error'">✕</span>
        <span v-else-if="type === 'warning'">⚠</span>
        <span v-else-if="type === 'info'">ⓘ</span>
      </div>
      <div class="toast-message">{{ message }}</div>
    </div>
  </transition>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'

export default {
  name: 'WechatToast',
  props: {
    message: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: 'info',
      validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
    },
    duration: {
      type: Number,
      default: 3000
    },
    showIcon: {
      type: Boolean,
      default: true
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const visible = ref(false)
    let timer = null

    const toastClass = computed(() => {
      return [
        'wechat-toast',
        `wechat-toast--${props.type}`
      ]
    })

    const show = () => {
      visible.value = true
      if (props.duration > 0) {
        timer = setTimeout(() => {
          hide()
        }, props.duration)
      }
    }

    const hide = () => {
      visible.value = false
      if (timer) {
        clearTimeout(timer)
        timer = null
      }
      emit('close')
    }

    onMounted(() => {
      show()
    })

    watch(() => props.message, () => {
      if (props.message) {
        show()
      }
    })

    return {
      visible,
      toastClass,
      hide
    }
  }
}
</script>

<style lang="scss" scoped>
.wechat-toast {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: $z-index-toast;

  display: flex;
  align-items: center;
  justify-content: center;

  min-width: 120px;
  max-width: 300px;
  padding: $spacing-md $spacing-lg;

  background-color: rgba(0, 0, 0, 0.8);
  color: $text-color-white;
  border-radius: $border-radius-md;

  font-size: $font-size-md;
  text-align: center;
  word-break: break-word;

  .toast-icon {
    margin-right: $spacing-sm;
    font-size: $font-size-lg;
    font-weight: $font-weight-bold;
  }

  .toast-message {
    flex: 1;
  }

  // 类型样式
  &--success {
    .toast-icon {
      color: $success-color;
    }
  }

  &--error {
    .toast-icon {
      color: $danger-color;
    }
  }

  &--warning {
    .toast-icon {
      color: $warning-color;
    }
  }

  &--info {
    .toast-icon {
      color: $info-color;
    }
  }
}

// 动画
.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: all $transition-normal;
}

.toast-fade-enter-from {
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.8);
}

.toast-fade-leave-to {
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.8);
}
</style>