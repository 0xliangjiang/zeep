<template>
  <transition name="modal-fade">
    <div v-if="visible" class="wechat-modal-overlay" @click="handleOverlayClick">
      <div class="wechat-modal" @click.stop>
        <div class="modal-header" v-if="title">
          <h3 class="modal-title">{{ title }}</h3>
        </div>

        <div class="modal-body">
          <div v-if="content" class="modal-content">{{ content }}</div>
          <slot v-else></slot>
        </div>

        <div class="modal-footer" v-if="showCancel || showConfirm">
          <WechatButton
            v-if="showCancel"
            type="plain"
            @click="handleCancel"
            class="modal-button"
          >
            {{ cancelText }}
          </WechatButton>
          <WechatButton
            v-if="showConfirm"
            type="primary"
            @click="handleConfirm"
            class="modal-button"
          >
            {{ confirmText }}
          </WechatButton>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { ref, onMounted } from 'vue'
import WechatButton from './WechatButton.vue'

export default {
  name: 'WechatModal',
  components: {
    WechatButton
  },
  props: {
    title: {
      type: String,
      default: ''
    },
    content: {
      type: String,
      default: ''
    },
    showCancel: {
      type: Boolean,
      default: true
    },
    showConfirm: {
      type: Boolean,
      default: true
    },
    confirmText: {
      type: String,
      default: '确定'
    },
    cancelText: {
      type: String,
      default: '取消'
    },
    closeOnOverlay: {
      type: Boolean,
      default: true
    }
  },
  emits: ['confirm', 'cancel', 'close'],
  setup(props, { emit }) {
    const visible = ref(false)

    const handleConfirm = () => {
      emit('confirm')
      close()
    }

    const handleCancel = () => {
      emit('cancel')
      close()
    }

    const handleOverlayClick = () => {
      if (props.closeOnOverlay) {
        handleCancel()
      }
    }

    const close = () => {
      visible.value = false
      emit('close')
    }

    onMounted(() => {
      visible.value = true
    })

    return {
      visible,
      handleConfirm,
      handleCancel,
      handleOverlayClick,
      close
    }
  }
}
</script>

<style lang="scss" scoped>
.wechat-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: $z-index-modal;

  display: flex;
  align-items: center;
  justify-content: center;

  background: rgba(0, 0, 0, 0.5);
  padding: 20px;
}

.wechat-modal {
  background: #ffffff;
  border-radius: $border-radius-lg;
  border: 1px solid #e1e8ed;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);

  min-width: 300px;
  max-width: 380px;
  width: 90%;

  overflow: hidden;

  .modal-header {
    padding: $spacing-xl $spacing-lg $spacing-md;
    text-align: center;
    border-bottom: 1px solid rgba(0, 0, 0, 0.08);

    .modal-title {
      font-size: $font-size-xl;
      font-weight: $font-weight-bold;
      color: $text-color;
      margin: 0;
    }
  }

  .modal-body {
    padding: $spacing-lg $spacing-xl;
    text-align: center;

    .modal-content {
      font-size: $font-size-md;
      color: $text-color-secondary;
      line-height: $line-height-loose;
    }
  }

  .modal-footer {
    display: flex;
    border-top: 1px solid $border-color-light;

    .modal-button {
      flex: 1;
      border-radius: 0;
      border: none;
      height: 48px;

      &:not(:last-child) {
        border-right: 1px solid $border-color-light;
      }

      &.wechat-button--plain {
        background-color: transparent;
        color: $text-color-secondary;

        &:hover {
          background-color: $bg-color-secondary;
        }
      }

      &.wechat-button--primary {
        background-color: transparent;
        color: $primary-color;

        &:hover {
          background-color: rgba($primary-color, 0.1);
        }
      }
    }
  }
}

// 动画
.modal-fade-enter-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.modal-fade-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 1, 1);
}

.modal-fade-enter-from {
  opacity: 0;

  .wechat-modal {
    transform: scale(0.9) translateY(-20px);
  }
}

.modal-fade-leave-to {
  opacity: 0;

  .wechat-modal {
    transform: scale(0.95) translateY(10px);
  }
}
</style>