<template>
  <WechatModal
    v-if="show"
    title="意见反馈"
    :show-cancel="true"
    :confirm-text="submitting ? '提交中...' : '提交反馈'"
    :confirm-loading="submitting"
    @confirm="submitFeedback"
    @cancel="handleClose"
    @close="handleClose"
  >
    <div class="feedback-form">
      <!-- 反馈类型 -->
      <div class="form-group">
        <label>反馈类型</label>
        <div class="feedback-types">
          <div 
            v-for="type in feedbackTypes" 
            :key="type.value"
            class="type-item"
            :class="{ active: feedbackData.type === type.value }"
            @click="feedbackData.type = type.value"
          >
            <span class="type-emoji">{{ type.emoji }}</span>
            <span class="type-label">{{ type.label }}</span>
          </div>
        </div>
      </div>

      <!-- 反馈内容 -->
      <div class="form-group">
        <label>反馈内容</label>
        <textarea
          v-model="feedbackData.content"
          placeholder="请详细描述您遇到的问题或建议..."
          class="feedback-textarea"
          rows="4"
          maxlength="500"
        ></textarea>
        <div class="char-count">{{ feedbackData.content.length }}/500</div>
      </div>

      <!-- 联系方式（可选） -->
      <div class="form-group">
        <label>联系方式（可选）</label>
        <input
          v-model="feedbackData.contact"
          type="text"
          placeholder="微信号、QQ号或邮箱（方便我们回复您）"
          class="feedback-input"
        />
      </div>

      <!-- 历史反馈 -->
      <div v-if="historyFeedbacks.length > 0" class="history-section">
        <div class="history-header" @click="showHistory = !showHistory">
          <span>历史反馈</span>
          <span class="toggle-icon" :class="{ expanded: showHistory }">▼</span>
        </div>
        
        <div v-if="showHistory" class="history-list">
          <div 
            v-for="feedback in historyFeedbacks" 
            :key="feedback.id"
            class="history-item"
          >
            <div class="history-content">
              <div class="history-type">
                {{ feedbackTypes.find(t => t.value === feedback.type)?.emoji }}
                {{ feedbackTypes.find(t => t.value === feedback.type)?.label }}
              </div>
              <div class="history-text">{{ feedback.content }}</div>
              <div class="history-time">{{ formatTime(feedback.created_at) }}</div>
            </div>
            
            <div v-if="feedback.reply" class="history-reply">
              <div class="reply-label">开发者回复：</div>
              <div class="reply-content">{{ feedback.reply }}</div>
              <div class="reply-time">{{ formatTime(feedback.reply_time) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </WechatModal>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import WechatModal from './WechatModal.vue'

export default {
  name: 'FeedbackModal',
  components: {
    WechatModal
  },
  props: {
    show: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close', 'success'],
  setup(props, { emit }) {
    const submitting = ref(false)
    const showHistory = ref(false)
    const historyFeedbacks = ref([])

    const feedbackTypes = [
      { value: 'bug', label: '问题反馈', emoji: '🐛' },
      { value: 'feature', label: '功能建议', emoji: '💡' },
      { value: 'ui', label: '界面优化', emoji: '🎨' },
      { value: 'other', label: '其他', emoji: '💬' }
    ]

    const feedbackData = reactive({
      type: 'bug',
      content: '',
      contact: ''
    })

    // 提交反馈
    const submitFeedback = async () => {
      if (!feedbackData.content.trim()) {
        window.$toast('请输入反馈内容', 'warning')
        return
      }

      submitting.value = true

      try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 1500))
        
        // 模拟成功
        if (Math.random() > 0.1) {
          window.$toast('反馈提交成功，感谢您的建议！', 'success')
          emit('success')
          handleClose()
          
          // 重置表单
          feedbackData.content = ''
          feedbackData.contact = ''
          feedbackData.type = 'bug'
          
          // 刷新历史记录
          loadHistoryFeedbacks()
        } else {
          throw new Error('提交失败')
        }
      } catch (error) {
        window.$toast('提交失败，请稍后重试', 'error')
      } finally {
        submitting.value = false
      }
    }

    // 加载历史反馈
    const loadHistoryFeedbacks = async () => {
      try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 500))
        
        // 模拟数据
        historyFeedbacks.value = [
          {
            id: 1,
            type: 'bug',
            content: '步数修改后没有立即生效',
            created_at: '2025-01-07T10:30:00Z',
            reply: '感谢反馈！这个问题已经修复，步数修改现在会立即生效。',
            reply_time: '2025-01-07T14:20:00Z'
          },
          {
            id: 2,
            type: 'feature',
            content: '希望能添加步数历史记录功能',
            created_at: '2025-01-06T16:45:00Z',
            reply: '好建议！我们正在开发这个功能，预计下个版本上线。',
            reply_time: '2025-01-06T18:30:00Z'
          },
          {
            id: 3,
            type: 'ui',
            content: '界面可以更美观一些',
            created_at: '2025-01-05T09:15:00Z',
            reply: null,
            reply_time: null
          }
        ]
      } catch (error) {
        console.error('加载历史反馈失败:', error)
      }
    }

    // 格式化时间
    const formatTime = (timeStr) => {
      if (!timeStr) return ''
      const date = new Date(timeStr)
      return date.toLocaleString('zh-CN', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    // 关闭弹窗
    const handleClose = () => {
      emit('close')
    }

    onMounted(() => {
      if (props.show) {
        loadHistoryFeedbacks()
      }
    })

    return {
      submitting,
      showHistory,
      historyFeedbacks,
      feedbackTypes,
      feedbackData,
      submitFeedback,
      formatTime,
      handleClose
    }
  }
}
</script>

<style lang="scss" scoped>
.feedback-form {
  .form-group {
    margin-bottom: 20px;
    
    label {
      display: block;
      font-size: 14px;
      font-weight: 500;
      color: $text-color;
      margin-bottom: 8px;
    }
    
    .feedback-types {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      
      .type-item {
        display: flex;
        align-items: center;
        padding: 12px;
        border: 1px solid $border-color;
        border-radius: $border-radius-sm;
        cursor: pointer;
        transition: all 0.2s ease;
        
        &:hover {
          border-color: $primary-color;
        }
        
        &.active {
          border-color: $primary-color;
          background: rgba($primary-color, 0.1);
        }
        
        .type-emoji {
          font-size: 16px;
          margin-right: 8px;
        }
        
        .type-label {
          font-size: 14px;
          color: $text-color;
        }
      }
    }
    
    .feedback-textarea {
      width: 100%;
      padding: 12px;
      border: 1px solid $border-color;
      border-radius: $border-radius-sm;
      font-size: 14px;
      resize: vertical;
      font-family: inherit;
      
      &:focus {
        outline: none;
        border-color: $primary-color;
        box-shadow: 0 0 0 2px rgba($primary-color, 0.1);
      }
    }
    
    .feedback-input {
      width: 100%;
      padding: 12px;
      border: 1px solid $border-color;
      border-radius: $border-radius-sm;
      font-size: 14px;
      
      &:focus {
        outline: none;
        border-color: $primary-color;
        box-shadow: 0 0 0 2px rgba($primary-color, 0.1);
      }
    }
    
    .char-count {
      text-align: right;
      font-size: 12px;
      color: $text-color-secondary;
      margin-top: 4px;
    }
  }
  
  .history-section {
    border-top: 1px solid $border-color-light;
    padding-top: 16px;
    
    .history-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      padding: 8px 0;
      font-size: 14px;
      font-weight: 500;
      color: $text-color;
      
      .toggle-icon {
        transition: transform 0.2s ease;
        
        &.expanded {
          transform: rotate(180deg);
        }
      }
    }
    
    .history-list {
      .history-item {
        border: 1px solid $border-color-light;
        border-radius: $border-radius-sm;
        padding: 12px;
        margin-bottom: 8px;
        
        .history-content {
          .history-type {
            font-size: 12px;
            color: $primary-color;
            margin-bottom: 4px;
          }
          
          .history-text {
            font-size: 14px;
            color: $text-color;
            margin-bottom: 4px;
          }
          
          .history-time {
            font-size: 12px;
            color: $text-color-secondary;
          }
        }
        
        .history-reply {
          margin-top: 8px;
          padding-top: 8px;
          border-top: 1px solid $border-color-light;
          background: rgba($primary-color, 0.05);
          border-radius: $border-radius-sm;
          padding: 8px;
          
          .reply-label {
            font-size: 12px;
            color: $primary-color;
            font-weight: 500;
            margin-bottom: 4px;
          }
          
          .reply-content {
            font-size: 13px;
            color: $text-color;
            margin-bottom: 4px;
          }
          
          .reply-time {
            font-size: 11px;
            color: $text-color-secondary;
          }
        }
      }
    }
  }
}
</style>
