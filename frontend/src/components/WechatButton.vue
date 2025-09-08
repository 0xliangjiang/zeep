<template>
  <button
    :class="buttonClass"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <span v-if="loading" class="loading-icon">⟳</span>
    <slot v-else></slot>
  </button>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'WechatButton',
  props: {
    type: {
      type: String,
      default: 'primary',
      validator: (value) => ['primary', 'secondary', 'danger', 'plain', 'text'].includes(value)
    },
    size: {
      type: String,
      default: 'medium',
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    },
    disabled: {
      type: Boolean,
      default: false
    },
    loading: {
      type: Boolean,
      default: false
    },
    block: {
      type: Boolean,
      default: false
    },
    round: {
      type: Boolean,
      default: false
    }
  },
  emits: ['click'],
  setup(props, { emit }) {
    const buttonClass = computed(() => {
      return [
        'wechat-button',
        `wechat-button--${props.type}`,
        `wechat-button--${props.size}`,
        {
          'wechat-button--disabled': props.disabled,
          'wechat-button--loading': props.loading,
          'wechat-button--block': props.block,
          'wechat-button--round': props.round
        }
      ]
    })

    const handleClick = (event) => {
      if (!props.disabled && !props.loading) {
        emit('click', event)
      }
    }

    return {
      buttonClass,
      handleClick
    }
  }
}
</script>

<style lang="scss" scoped>
.wechat-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid transparent;
  border-radius: $border-radius-sm;
  font-weight: 500;
  text-align: center;
  cursor: pointer;
  user-select: none;
  transition: all 0.2s ease;

  &:active {
    transform: scale(0.98);
  }

  // 类型样式
  &--primary {
    background: #007AFF;
    color: #FFFFFF;
    border: 1px solid #0056CC;
    font-weight: 600;

    &:hover {
      background: #0056CC;
      border-color: #004499;
    }

    &:active {
      background: #004499;
      transform: scale(0.98);
    }
  }

  &--secondary {
    background: #5856D6;
    color: #FFFFFF;
    border: 1px solid #4B4ACF;
    font-weight: 600;

    &:hover {
      background: #4B4ACF;
      border-color: #3F3FB8;
    }
  }

  &--danger {
    background: linear-gradient(135deg, $danger-color 0%, darken($danger-color, 8%) 100%);
    border: none;
    color: $text-color-white;
    box-shadow: 0 2px 8px rgba($danger-color, 0.3);

    &:hover {
      background: linear-gradient(135deg, darken($danger-color, 5%) 0%, darken($danger-color, 13%) 100%);
      box-shadow: 0 4px 12px rgba($danger-color, 0.4);
      transform: translateY(-1px);
    }
  }

  &--plain {
    background-color: $bg-color-white;
    border: 1px solid $border-color-light;
    color: $text-color;

    &:hover {
      background-color: $bg-color-secondary;
      border-color: $border-color;
    }
  }

  &--text {
    background-color: transparent;
    border: none;
    color: $primary-color;

    &:hover {
      background-color: rgba($primary-color, 0.08);
    }
  }

  // 尺寸样式
  &--small {
    padding: 6px 12px;
    font-size: $font-size-sm;
    min-height: 32px;
  }

  &--medium {
    padding: 8px 16px;
    font-size: $font-size-md;
    min-height: 40px;
  }

  &--large {
    padding: 12px 24px;
    font-size: $font-size-lg;
    min-height: 48px;
  }

  // 状态样式
  &--disabled {
    opacity: 0.6;
    cursor: not-allowed;

    &:hover,
    &:active {
      transform: none;
    }
  }

  &--loading {
    cursor: not-allowed;

    .loading-icon {
      animation: spin 1s linear infinite;
      margin-right: 4px;
    }
  }

  &--block {
    width: 100%;
    display: flex;
  }

  &--round {
    border-radius: 20px;
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>