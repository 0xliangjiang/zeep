<template>
  <div class="page" :class="{ 'festival-theme': hasFestivalTheme }">
    <!-- 节日装饰 -->
    <div v-if="hasFestivalTheme" class="festival-decorations">
      <div
        v-for="(decoration, index) in getFestivalDecorations"
        :key="index"
        class="decoration-item"
        :style="getDecorationStyle(index)"
      >
        {{ decoration }}
      </div>
    </div>

    <!-- 下拉刷新区域 -->
    <div
      class="pull-refresh"
      :class="{ 'pulling': isPulling, 'refreshing': isRefreshing }"
      @touchstart="handleTouchStart"
      @touchmove="handleTouchMove"
      @touchend="handleTouchEnd"
    >
      <div class="refresh-indicator">
        <LoadingSpinner v-if="isRefreshing" type="steps" size="small" />
        <div v-else class="pull-text">{{ pullText }}</div>
      </div>
    </div>

    <div class="page-content">
      <!-- 主要内容 -->
      <div>
        <!-- 节日问候 -->
        <div v-if="getFestivalGreeting" class="festival-greeting">
          <div class="greeting-icon">🎉</div>
          <div class="greeting-text">{{ getFestivalGreeting }}</div>
        </div>

        <!-- 用户状态卡片已移除 -->

        <!-- 防失联提示 -->
        <div class="backup-notice">
          <div class="notice-content">
            <div class="notice-icon">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M10 13C10.4295 13.5741 10.9774 14.0491 11.6066 14.3929C12.2357 14.7367 12.9315 14.9411 13.6467 14.9923C14.3618 15.0435 15.0796 14.9403 15.7513 14.6897C16.4231 14.4392 17.0331 14.047 17.54 13.54L20.54 10.54C21.4508 9.59695 21.9548 8.33394 21.9434 7.02296C21.932 5.71198 21.4061 4.45791 20.4791 3.53087C19.5521 2.60383 18.298 2.07799 16.987 2.0666C15.676 2.0552 14.413 2.55918 13.47 3.47L11.75 5.18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M14 11C13.5705 10.4259 13.0226 9.95086 12.3934 9.60712C11.7643 9.26339 11.0685 9.05895 10.3533 9.00775C9.63819 8.95655 8.92037 9.05972 8.24864 9.31026C7.5769 9.5608 6.96687 9.95303 6.46 10.46L3.46 13.46C2.54918 14.403 2.04520 15.6661 2.05660 16.977C2.06799 18.288 2.59383 19.5421 3.52087 20.4691C4.44791 21.3962 5.70198 21.922 7.01296 21.9334C8.32394 21.9448 9.58695 21.4408 10.53 20.53L12.24 18.82" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <span class="notice-text">防失联请复制：</span>
            <span class="notice-url" @click="copyUrl">bs.444k.cn</span>
          </div>
        </div>

      <!-- 滚动公告 -->
      <div class="announcement-card">
        <div class="announcement-header">
          <div class="announcement-icon">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 11L22 2L13 21L11 13L3 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <span class="announcement-label">公告</span>
        </div>
        <div class="announcement-content">
          <div class="announcement-text">
            {{ announcementText || '加载中...' }}
          </div>
        </div>
      </div>

        <!-- 快捷步数设置 - 暂时简化 -->
        <div class="quick-actions-card">
          <div class="card-header">
            <h3 class="card-title">⚡ 快捷设置</h3>
            <div class="card-subtitle">一键设置常用步数</div>
          </div>

          <div class="quick-buttons">
            <button
              class="quick-btn"
              @click="handleStepClick(8000)"
              :disabled="loading"
            >
              8000
            </button>
            <button
              class="quick-btn"
              @click="handleStepClick(10000)"
              :disabled="loading"
            >
              10000
            </button>
            <button
              class="quick-btn"
              @click="handleStepClick(15000)"
              :disabled="loading"
            >
              15000
            </button>
          </div>
        </div>

        <!-- 预设步数网格 -->
        <div class="steps-section">
          <div class="section-header">
            <h3 class="section-title">🎯 精选步数</h3>
            <div class="section-subtitle">选择适合的步数目标</div>
          </div>

          <div class="steps-grid">
            <!-- 自定义步数按钮 - 放在第一个位置 -->
            <div
              class="step-card custom-card"
              @click="showCustomModal"
              :class="{ 'disabled': loading }"
            >
              <div class="step-content">
                <div class="step-icon">✏️</div>
                <div class="step-number">自定义</div>
                <div class="step-label">步数</div>
              </div>
            </div>

            <!-- 预设步数按钮 -->
            <div
              v-for="(steps, index) in presetSteps"
              :key="steps"
              class="step-card"
              @click="handleStepClick(steps)"
              :class="{
                'loading': loading && selectedSteps === steps,
                'disabled': loading
              }"
            >
              <div class="step-content">
                <div class="step-number">{{ steps.toLocaleString() }}</div>
                <div class="step-label">步数</div>
              </div>
              <div class="step-overlay" v-if="loading && selectedSteps === steps">
                <div class="loading-spinner"></div>
                <div class="loading-text">处理中...</div>
              </div>
            </div>
          </div>
        </div>

        <!-- VIP功能预览已移除 -->
      </div>
    </div>

    <!-- 底部导航 -->
    <WechatNavBar />

    <!-- 浮动联系客服按钮 -->
    <FloatingContactButton @click="showContactModal = true" />

    <!-- 联系客服弹窗 -->
    <ContactModal
      :show="showContactModal"
      @close="showContactModal = false"
    />

    <!-- 粒子效果和反馈弹窗暂时移除 -->

    <!-- 自定义步数弹窗 -->
    <WechatModal
      v-if="showCustomStepsModal"
      title="自定义步数"
      :show-cancel="true"
      confirm-text="确定"
      @confirm="confirmCustomSteps"
      @cancel="hideCustomModal"
      @close="hideCustomModal"
    >
      <div class="custom-steps-form">
        <div class="input-group">
          <input
            v-model="customStepsInput"
            type="number"
            :min="minSteps"
            :max="maxSteps"
            placeholder="请输入步数"
            class="custom-input"
          />
          <button
            type="button"
            class="random-btn"
            @click="generateRandomSteps"
            title="随机生成"
          >
            随机
          </button>
        </div>
        <p class="input-hint">
          步数范围：{{ minSteps.toLocaleString() }} - {{ maxSteps.toLocaleString() }}
        </p>
      </div>
    </WechatModal>

    <!-- VIP功能预览弹窗已移除 -->

    <!-- 步数处理统一模态框 -->
    <WechatModal
      v-if="showProcessModal"
      :title="processModalTitle"
      :show-cancel="processModalState !== 'loading' && processModalState !== 'success' && processModalState !== 'bind'"
      :show-confirm="processModalState !== 'bind'"
      :confirm-text="processModalConfirmText"
      @confirm="handleProcessConfirm"
      @cancel="handleProcessCancel"
      @close="handleProcessCancel"
    >
      <!-- 加载状态 -->
      <div v-if="processModalState === 'loading'" class="process-loading">
        <div class="loading-spinner-large"></div>
        <p class="loading-text">{{ processModalMessage }}</p>
      </div>

      <!-- 绑定二维码状态 -->
      <div v-else-if="processModalState === 'bind'" class="bind-form">
        <div class="qr-code-container">
          <img :src="bindQrCodeUrl" alt="绑定二维码" class="qr-code" />
        </div>
        <div class="bind-steps">
          <p class="bind-step">1. 长按二维码后点击"识别图中二维码"</p>
          <p class="bind-step">2. 点击 [ 绑定设备 ] 后返回到当前页</p>
          <p class="bind-step bind-tip">3. 绑定设备成功后请耐心等待系统绑定完成</p>
        </div>
        <div class="bind-timeout" v-if="remainingTime > 0">
          <div class="timeout-icon">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
              <polyline points="12,6 12,12 16,14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <p class="timeout-text">二维码有效期：{{ remainingTime }}秒</p>
        </div>
        <div class="bind-timeout expired" v-else>
          <div class="timeout-icon">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
              <path d="M8 8L16 16M16 8L8 16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <p class="timeout-text">二维码已过期，请重新获取</p>
        </div>
      </div>

      <!-- 成功状态 -->
      <div v-else-if="processModalState === 'success'" class="success-form">
        <div class="success-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" fill="#34C759"/>
            <path d="M8.5 12.5L10.5 14.5L15.5 9.5" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <p class="success-message">{{ processModalMessage }}</p>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="processModalState === 'error'" class="error-form">
        <div class="error-icon">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="10" fill="#FF3B30"/>
            <path d="M8 8L16 16M16 8L8 16" stroke="white" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </div>
        <p class="error-message">{{ processModalMessage }}</p>
      </div>
    </WechatModal>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import WechatButton from '../components/WechatButton.vue'
import WechatNavBar from '../components/WechatNavBar.vue'
import WechatModal from '../components/WechatModal.vue'
import FloatingContactButton from '../components/FloatingContactButton.vue'
import ContactModal from '../components/ContactModal.vue'
// import SkeletonLoader from '../components/SkeletonLoader.vue'
// import NumberRoll from '../components/NumberRoll.vue'
// import ParticleEffect from '../components/ParticleEffect.vue'
// import ProgressBar from '../components/ProgressBar.vue'
// import HealthTips from '../components/HealthTips.vue'
// import WeatherInfo from '../components/WeatherInfo.vue'
// import FeedbackModal from '../components/FeedbackModal.vue'
// import LoadingSpinner from '../components/LoadingSpinner.vue'
// import { useTheme } from '../composables/useTheme.js'

export default {
  name: 'Home',
  components: {
    WechatButton,
    WechatNavBar,
    WechatModal,
    FloatingContactButton,
    ContactModal
    // SkeletonLoader,
    // NumberRoll,
    // ParticleEffect,
    // ProgressBar,
    // HealthTips,
    // WeatherInfo,
    // FeedbackModal,
    // LoadingSpinner
  },
  setup() {
    // 主题相关 - 暂时注释
    // const {
    //   initTheme,
    //   hasFestivalTheme,
    //   getFestivalDecorations,
    //   getFestivalGreeting
    // } = useTheme()

    // 临时变量
    const hasFestivalTheme = ref(false)
    const getFestivalDecorations = ref([])
    const getFestivalGreeting = ref('')

    // 基础数据
    const userInfo = ref(null)
    const presetSteps = ref([])
    const customSteps = ref('')
    const customStepsInput = ref('')
    const minSteps = ref(1)
    const maxSteps = ref(98800)
    const loading = ref(false)

    // 加载状态
    const initialLoading = ref(true)

    // 下拉刷新
    const isPulling = ref(false)
    const isRefreshing = ref(false)
    const pullDistance = ref(0)
    const touchStartY = ref(0)

    // 弹窗状态
    const showCustomStepsModal = ref(false)
    const showProcessModal = ref(false)
    const showContactModal = ref(false)

    // 公告内容
    const announcementText = ref('')
    const showVipModal = ref(false)
    const showFeedbackModal = ref(false)

    // 粒子效果
    const showParticles = ref(false)
    const particleMessage = ref('')
    const particleType = ref('success')

    // 处理模态框
    const processModalState = ref('loading') // loading, bind, success, error
    const processModalTitle = ref('处理中')
    const processModalMessage = ref('正在处理，请稍候...')
    const processModalConfirmText = ref('确定')
    const bindQrCodeUrl = ref('')
    const bindCheckTimer = ref(null)
    const currentSteps = ref(null)
    const remainingTime = ref(120)
    const countdownTimer = ref(null)

    // 快捷步数
    const quickSteps = ref([8000, 10000, 15000])

    // 用户体验数据
    const usedDays = computed(() => {
      if (!userInfo.value) return 0
      const totalDays = userInfo.value.total_days || 7
      const remainingDays = userInfo.value.remaining_days || 7
      return totalDays - remainingDays
    })

    const totalDays = computed(() => {
      return userInfo.value?.total_days || 7
    })

    const selectedSteps = computed(() => {
      return customSteps.value ? parseInt(customSteps.value) : null
    })

    // 获取用户信息
    const fetchUserInfo = async () => {
      try {
        const response = await fetch('/auth/user', {
          credentials: 'include'
        })
        if (response.ok) {
          userInfo.value = await response.json()
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
      }
    }

    // 获取预设步数
    const fetchPresetSteps = async () => {
      try {
        const response = await fetch('/api/steps/presets')
        if (response.ok) {
          const data = await response.json()
          presetSteps.value = data.presets
          minSteps.value = data.min_steps
          maxSteps.value = data.max_steps
        }
      } catch (error) {
        console.error('获取预设步数失败:', error)
      }
    }

    // 简化的方法，移除可能有问题的部分

    // 选择预设步数
    const selectSteps = (steps) => {
      customSteps.value = steps.toString()
    }

    // 处理步数卡片点击
    const handleStepClick = async (steps) => {
      if (loading.value) return

      // 检查用户授权
      if (userInfo.value?.is_expired) {
        window.$toast('授权已过期，请续费或邀请好友获取体验时间', 'error')
        return
      }

      // 保存当前选择的步数
      currentSteps.value = steps
      customSteps.value = steps.toString()

      // 显示处理模态框并开始处理流程
      showProcessModalWithState('loading', '步数修改', '正在检查账号状态...', '取消')

      // 开始处理流程
      await processStepsModification(steps)
    }

    // 显示自定义弹窗
    const showCustomModal = () => {
      if (loading.value) return
      customStepsInput.value = ''
      showCustomStepsModal.value = true
    }

    // 显示处理模态框
    const showProcessModalWithState = (state, title, message, confirmText) => {
      processModalState.value = state
      processModalTitle.value = title
      processModalMessage.value = message
      processModalConfirmText.value = confirmText
      showProcessModal.value = true
    }

    // 隐藏处理模态框
    const hideProcessModal = () => {
      showProcessModal.value = false
      processModalState.value = 'loading'
      bindQrCodeUrl.value = ''
      currentSteps.value = null
      remainingTime.value = 120

      // 清理定时器
      if (bindCheckTimer.value) {
        clearInterval(bindCheckTimer.value)
        bindCheckTimer.value = null
      }
      if (countdownTimer.value) {
        clearInterval(countdownTimer.value)
        countdownTimer.value = null
      }

      // 取消绑定会话
      cancelBindSession()
    }

    // 开始倒计时
    const startCountdown = () => {
      countdownTimer.value = setInterval(() => {
        remainingTime.value--
        if (remainingTime.value <= 0) {
          clearInterval(countdownTimer.value)
          countdownTimer.value = null
          // 倒计时结束，显示过期提示
          showProcessModalWithState('error', '绑定超时', '二维码已过期，请重新尝试', '确定')
        }
      }, 1000)
    }

    // 取消绑定会话
    const cancelBindSession = async () => {
      try {
        await fetch('/api/steps/cancel-bind', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include'
        })
      } catch (error) {
        console.error('取消绑定会话失败:', error)
      }
    }

    // 处理步数修改的完整流程
    const processStepsModification = async (steps) => {
      try {
        const response = await fetch('/api/steps/modify', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            steps: parseInt(steps)
          })
        })

        const data = await response.json()

        if (response.ok) {
          if (data.success) {
            // 修改成功
            showProcessModalWithState('success', '修改成功', `步数已成功修改为 ${steps.toLocaleString()}`, '确定')

            // 延迟关闭弹窗
            setTimeout(() => {
              hideProcessModal()
            }, 1500)
          } else if (data.need_bind) {
            // 需要绑定
            bindQrCodeUrl.value = data.qr_code_url
            remainingTime.value = data.timeout || 120
            showProcessModalWithState('bind', '绑定Zepp账号', '请扫描二维码完成绑定', '已完成绑定')
            startBindCheck()
            startCountdown()
          } else {
            // 其他错误
            showProcessModalWithState('error', '修改失败', data.message || data.error || '修改失败', '确定')
          }
        } else {
          showProcessModalWithState('error', '修改失败', data.message || data.error || '修改失败', '确定')
        }
      } catch (error) {
        console.error('修改步数失败:', error)
        showProcessModalWithState('error', '修改失败', '网络错误，请稍后重试', '确定')
      }
    }

    // 复制网址
    const copyUrl = async () => {
      try {
        await navigator.clipboard.writeText('bs.444k.cn')
        window.$toast('网址已复制到剪贴板', 'success')
      } catch (error) {
        // 降级方案
        const textArea = document.createElement('textarea')
        textArea.value = 'https://bs.444k.cn'
        document.body.appendChild(textArea)
        textArea.select()
        document.execCommand('copy')
        document.body.removeChild(textArea)
        window.$toast('网址已复制到剪贴板', 'success')
      }
    }



    // 隐藏自定义步数弹窗
    const hideCustomModal = () => {
      showCustomStepsModal.value = false
      customStepsInput.value = ''
    }

    // 确认自定义步数
    const confirmCustomSteps = async () => {
      if (!customStepsInput.value) {
        window.$toast('请输入步数', 'warning')
        return
      }

      const steps = parseInt(customStepsInput.value)
      if (steps < minSteps.value || steps > maxSteps.value) {
        window.$toast(`步数必须在${minSteps.value.toLocaleString()}-${maxSteps.value.toLocaleString()}之间`, 'warning')
        return
      }

      // 关闭自定义弹窗
      hideCustomModal()

      // 开始修改步数流程
      await handleStepClick(steps)
    }

    // 生成随机步数
    const generateRandomSteps = async () => {
      try {
        const response = await fetch('/api/steps/random')
        if (response.ok) {
          const data = await response.json()
          customStepsInput.value = data.steps.toString()
        }
      } catch (error) {
        console.error('生成随机步数失败:', error)
      }
    }

    // 修改步数方法已移除

    // 格式化步数显示
    const formatSteps = (steps) => {
      return steps.toLocaleString() + ' 步'
    }

    // 格式化时间显示
    const formatTime = (timeStr) => {
      const date = new Date(timeStr)
      const now = new Date()
      const diff = now - date

      if (diff < 60000) { // 1分钟内
        return '刚刚'
      } else if (diff < 3600000) { // 1小时内
        return Math.floor(diff / 60000) + '分钟前'
      } else if (diff < 86400000) { // 1天内
        return Math.floor(diff / 3600000) + '小时前'
      } else {
        return date.toLocaleDateString()
      }
    }

    // 处理模态框确认按钮
    const handleProcessConfirm = async () => {
      if (processModalState.value === 'bind') {
        // 绑定状态下，检查绑定状态
        await checkBindStatus()
      } else {
        // 其他状态直接关闭
        hideProcessModal()
      }
    }

    // 处理模态框取消/关闭按钮
    const handleProcessCancel = () => {
      if (processModalState.value === 'bind') {
        // 绑定状态下取消，需要清理绑定会话
        hideProcessModal()
      } else {
        // 其他状态直接关闭
        hideProcessModal()
      }
    }

    // 开始检查绑定状态
    const startBindCheck = () => {
      // 立即检查一次，然后每3秒检查一次绑定状态
      checkBindStatus()
      bindCheckTimer.value = setInterval(async () => {
        await checkBindStatus()
      }, 3000)
    }

    // 检查绑定状态
    const checkBindStatus = async () => {
      try {
        const response = await fetch('/api/steps/check-bind-status', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include',
          body: JSON.stringify({})
        })

        const data = await response.json()

        if (response.ok && data.bind_status) {
          // 绑定成功，停止检查
          if (bindCheckTimer.value) {
            clearInterval(bindCheckTimer.value)
            bindCheckTimer.value = null
          }

          // 停止倒计时
          if (countdownTimer.value) {
            clearInterval(countdownTimer.value)
            countdownTimer.value = null
          }

          // 显示加载状态
          showProcessModalWithState('loading', '步数修改', '绑定成功，正在修改步数...', '取消')

          // 重新尝试修改步数
          if (currentSteps.value) {
            await processStepsModification(currentSteps.value)
          }
        }
      } catch (error) {
        console.error('检查绑定状态失败:', error)
      }
    }

    // 简化的反馈处理
    const handleFeedbackSuccess = () => {
      console.log('反馈成功')
    }

    // 获取首页公告内容
    const fetchAnnouncement = async () => {
      try {
        const response = await fetch('/api/admin/system-settings/home-announcement', {
          method: 'GET',
          credentials: 'include'
        })

        if (response.ok) {
          const data = await response.json()
          if (data.success && data.content) {
            announcementText.value = data.content
          } else {
            announcementText.value = '欢迎使用Zepp步数修改工具！'
          }
        } else {
          announcementText.value = '欢迎使用Zepp步数修改工具！'
        }
      } catch (error) {
        console.error('获取公告内容失败:', error)
        announcementText.value = '欢迎使用Zepp步数修改工具！'
      }
    }

    onMounted(() => {
      fetchUserInfo()
      fetchPresetSteps()
      fetchAnnouncement()
    })

    return {
      // 基础数据
      userInfo,
      presetSteps,
      customSteps,
      customStepsInput,
      minSteps,
      maxSteps,
      selectedSteps,
      loading,

      // 主题相关
      hasFestivalTheme,
      getFestivalDecorations,
      getFestivalGreeting,

      // 弹窗状态
      showCustomStepsModal,
      showProcessModal,
      showContactModal,

      // 公告内容
      announcementText,

      // 处理模态框
      processModalState,
      processModalTitle,
      processModalMessage,
      processModalConfirmText,
      bindQrCodeUrl,
      currentSteps,
      remainingTime,

      // 基础方法
      selectSteps,
      handleStepClick,
      copyUrl,
      showCustomModal,
      hideCustomModal,
      confirmCustomSteps,
      generateRandomSteps,
      hideProcessModal,
      handleProcessConfirm,
      handleProcessCancel,
      checkBindStatus
    }
  }
}
</script>

<style lang="scss" scoped>
// 页面基础样式
.page {
  position: relative;
  min-height: 100vh;

  &.festival-theme {
    background: var(--festival-background, $bg-color);
  }
}

// 节日装饰
.festival-decorations {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 1;

  .decoration-item {
    position: absolute;
    animation: festivalFloat 6s ease-in-out infinite;
    user-select: none;
  }
}

@keyframes festivalFloat {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
    opacity: 0.7;
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
    opacity: 1;
  }
}

// 下拉刷新
.pull-refresh {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.95);
  transform: translateY(-60px);
  transition: transform 0.3s ease;
  z-index: 10;

  &.pulling {
    transform: translateY(-30px);
  }

  &.refreshing {
    transform: translateY(0);
  }

  .refresh-indicator {
    display: flex;
    align-items: center;
    gap: 8px;

    .pull-text {
      font-size: 14px;
      color: $text-color-secondary;
    }
  }
}

// 骨架屏容器
.skeleton-container {
  padding: 20px;

  > * {
    margin-bottom: 20px;
  }
}

// 节日问候
.festival-greeting {
  background: var(--festival-background, linear-gradient(135deg, #667eea 0%, #764ba2 100%));
  color: white;
  border-radius: $border-radius-lg;
  padding: 16px;
  margin-bottom: 16px;
  text-align: center;

  .greeting-icon {
    font-size: 24px;
    margin-bottom: 8px;
  }

  .greeting-text {
    font-size: 14px;
    line-height: 1.4;
  }
}

// 用户状态卡片
.user-status-card {
  background: white;
  border-radius: $border-radius-lg;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);

  .status-header {
    display: flex;
    align-items: center;
    margin-bottom: 16px;

    .user-avatar {
      width: 50px;
      height: 50px;
      background: $primary-color;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      color: white;
      margin-right: 12px;
    }

    .user-info {
      flex: 1;

      .user-name {
        font-size: 16px;
        font-weight: 600;
        color: $text-color;
        margin-bottom: 4px;
      }

      .user-status {
        font-size: 12px;
        color: $text-color-secondary;
        background: rgba($primary-color, 0.1);
        padding: 2px 8px;
        border-radius: 10px;
        display: inline-block;
      }
    }

    .status-actions {
      .feedback-btn {
        width: 36px;
        height: 36px;
        border: none;
        background: rgba($primary-color, 0.1);
        border-radius: 50%;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.2s ease;

        &:hover {
          background: rgba($primary-color, 0.2);
          transform: scale(1.1);
        }
      }
    }
  }

  .experience-progress {
    margin-top: 16px;
  }
}

// 快捷操作卡片
.quick-actions-card {
  background: white;
  border-radius: $border-radius-lg;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);

  .card-header {
    margin-bottom: 16px;

    .card-title {
      font-size: 16px;
      font-weight: 600;
      color: $text-color;
      margin: 0 0 4px 0;
    }

    .card-subtitle {
      font-size: 12px;
      color: $text-color-secondary;
      margin: 0;
    }
  }

  .quick-buttons {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;

    .quick-btn {
      background: linear-gradient(135deg, $primary-color, #00d084);
      color: white;
      border: none;
      border-radius: $border-radius-sm;
      padding: 12px;
      font-size: 16px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;

      &:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba($primary-color, 0.3);
      }

      &:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        transform: none;
      }
    }
  }
}

// 步数选择区域
.steps-section {
  background: white;
  border-radius: $border-radius-lg;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);

  .section-header {
    margin-bottom: 16px;

    .section-title {
      font-size: 16px;
      font-weight: 600;
      color: $text-color;
      margin: 0 0 4px 0;
    }

    .section-subtitle {
      font-size: 12px;
      color: $text-color-secondary;
      margin: 0;
    }
  }
}

// 防失联提示
.backup-notice {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: $border-radius-sm;
  padding: 8px 12px;
  margin-bottom: 16px;

  .notice-content {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    font-size: 13px;

    .notice-text {
      color: #856404;
    }

    .notice-url {
      color: #e17055;
      font-weight: 600;
      cursor: pointer;
      padding: 2px 4px;
      border-radius: 2px;

      &:hover {
        background: #ffeaa7;
      }
    }
  }
}</style>

<style lang="scss" scoped>

// 步数网格
.steps-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;

  .step-card {
    background: #ffffff;
    border: 1px solid #e1e8ed;
    border-radius: $border-radius-lg;
    padding: 16px 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    min-height: 80px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;

    &:hover {
      border-color: $primary-color;
      box-shadow: 0 4px 16px rgba($primary-color, 0.2);
      transform: translateY(-2px);
    }

    &:active {
      transform: translateY(-1px) scale(0.98);
    }

    &.loading {
      pointer-events: none;
      opacity: 0.7;
    }

    &.disabled {
      opacity: 0.5;
      cursor: not-allowed;

      &:hover {
        transform: none;
        box-shadow: none;
        border-color: #e1e8ed;
      }
    }

    &.recommended {
      border-color: $primary-color;
      background: linear-gradient(135deg, rgba($primary-color, 0.05), rgba($primary-color, 0.1));

      &::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, $primary-color, #00d084);
      }
    }

    &.custom-card {
      background: white;
      border: 2px dashed $primary-color;
      color: $primary-color;

      .step-icon {
        font-size: 20px;
        margin-bottom: 4px;
      }

      &:hover {
        background: rgba($primary-color, 0.05);
        border-color: $primary-color;
      }
    }
  }

  .step-card {
    .recommended-badge {
      position: absolute;
      top: 4px;
      right: 4px;
      background: $primary-color;
      color: white;
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 8px;
      font-weight: 500;
    }

    .step-content {
      text-align: center;
      width: 100%;

      .step-number {
        font-size: 16px;
        font-weight: 600;
        color: $text-color;
        line-height: 1.2;
        margin-bottom: 4px;
      }

      .step-label {
        font-size: 10px;
        color: $text-color-secondary;
        line-height: 1;
      }

      .step-icon {
        font-size: 16px;
        margin-bottom: 4px;
      }
    }

    .step-overlay {
      position: absolute;
      inset: 0;
      background: rgba(255, 255, 255, 0.95);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      border-radius: $border-radius-sm;
      gap: 4px;

      .loading-spinner {
        width: 14px;
        height: 14px;
        border: 2px solid #e1e8ed;
        border-top: 2px solid #007AFF;
        border-radius: 50%;
        animation: spin 1s linear infinite;
      }

      .loading-text {
        font-size: 10px;
        color: #007AFF;
        font-weight: 500;
      }
    }

    &.custom-card {
      .step-content .step-number {
        color: #5856D6;
      }
    }

    &.disabled {
      pointer-events: none;
      opacity: 0.6;
    }
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

// 自定义步数弹窗
.custom-steps-form {
  .input-group {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
  }

  .custom-input {
    flex: 1;
    max-width: 200px; // 限制输入框最大宽度
    padding: 12px;
    border: 1px solid #e1e8ed;
    border-radius: $border-radius-sm;
    font-size: 16px;
    text-align: center;

    &:focus {
      outline: none;
      border-color: #007AFF;
      box-shadow: 0 0 0 2px rgba(0, 122, 255, 0.1);
    }
  }

  .random-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 60px; // 确保按钮宽度足够
    height: 40px;
    padding: 0 12px;
    border: 1px solid $primary-color;
    border-radius: $border-radius-sm;
    background: white;
    color: $primary-color;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 14px;
    font-weight: 500;
    white-space: nowrap; // 强制文字横向显示

    &:hover {
      background: $primary-color;
      color: white;
    }
  }

  .input-hint {
    font-size: 12px;
    color: #666;
    text-align: center;
    margin: 0;
    padding: 8px;
    background: #f8f9fa;
    border-radius: $border-radius-xs;
    border: 1px solid #e9ecef;
  }
}

// 处理模态框样式
.process-loading {
  text-align: center;
  padding: 20px;

  .loading-spinner-large {
    width: 40px;
    height: 40px;
    border: 3px solid #e1e8ed;
    border-top: 3px solid #007AFF;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 16px;
  }

  .loading-text {
    font-size: 14px;
    color: #666;
    margin: 0;
  }
}

.bind-form {
  text-align: center;

  .qr-code-container {
    margin-bottom: 20px;

    .qr-code {
      width: 200px;
      height: 200px;
      border: 1px solid #e1e8ed;
      border-radius: $border-radius-sm;
    }
  }

  .bind-steps {
    text-align: left;
    margin-bottom: 16px;

    .bind-step {
      font-size: 14px;
      color: #333;
      margin-bottom: 8px;
      line-height: 1.5;

      &:last-child {
        margin-bottom: 0;
      }

      &.bind-tip {
        color: #007AFF;
        font-weight: 500;
        background: #f0f9ff;
        padding: 8px 12px;
        border-radius: 4px;
        border-left: 3px solid #007AFF;
        margin-top: 12px;
      }
    }
  }

  .bind-timeout {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    padding: 8px 12px;
    border-radius: $border-radius-sm;
    background: #f0f9ff;
    border: 1px solid #bfdbfe;

    .timeout-icon {
      display: flex;
      align-items: center;

      svg {
        color: #1e40af;
      }
    }

    .timeout-text {
      font-size: 13px;
      color: #1e40af;
      margin: 0;
      font-weight: 500;
    }

    &.expired {
      background: #fef2f2;
      border-color: #fecaca;

      .timeout-icon svg {
        color: #dc2626;
      }

      .timeout-text {
        color: #dc2626;
      }
    }
  }
}

.success-form {
  text-align: center;
  padding: 20px;

  .success-icon {
    display: flex;
    justify-content: center;
    margin-bottom: 16px;
  }

  .success-message {
    font-size: 16px;
    color: #333;
    margin-bottom: 20px;
    line-height: 1.5;
  }

  .success-actions {
    display: flex;
    justify-content: center;
  }
}

.error-form {
  text-align: center;
  padding: 20px;

  .error-icon {
    display: flex;
    justify-content: center;
    margin-bottom: 16px;
  }

  .error-message {
    font-size: 14px;
    color: #ff3b30;
    margin: 0;
    line-height: 1.5;
  }
}

.action-buttons {
  margin: $spacing-lg 0;
}

.record-list {
  .record-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: $spacing-sm 0;
    border-bottom: 1px solid $border-color-light;

    &:last-child {
      border-bottom: none;
    }

    .record-steps {
      font-weight: $font-weight-medium;
      color: $text-color;
    }

    .record-status {
      padding: 2px 8px;
      border-radius: $border-radius-sm;
      font-size: $font-size-xs;
      font-weight: $font-weight-medium;

      &.success {
        background-color: rgba($success-color, 0.1);
        color: $success-color;
      }

      &.failure,
      &.network_error {
        background-color: rgba($danger-color, 0.1);
        color: $danger-color;
      }
    }

    .record-time {
      font-size: $font-size-xs;
      color: $text-color-secondary;
    }
  }
}

// 滚动公告
.announcement-card {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: $border-radius-sm;
  margin-bottom: 16px;
  overflow: hidden;

  .announcement-header {
    background: #007AFF;
    color: white;
    padding: 6px 12px;
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    font-weight: 500;

    .announcement-icon {
      font-size: 14px;
    }
  }

  .announcement-content {
    padding: 8px 12px;
    overflow: hidden;

    .announcement-text {
      font-size: 13px;
      color: #333;
      line-height: 1.4;
      white-space: nowrap;
      animation: scroll-text 20s linear infinite;
    }
  }
}

@keyframes scroll-text {
  0% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(-100%);
  }
}

// VIP预览卡片
.vip-preview-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: $border-radius-lg;
  padding: 20px;
  margin-bottom: 16px;
  color: white;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
    animation: vipShine 4s ease-in-out infinite;
  }

  .vip-header {
    text-align: center;
    margin-bottom: 16px;
    position: relative;
    z-index: 1;

    .vip-badge {
      background: rgba(255, 255, 255, 0.2);
      padding: 4px 12px;
      border-radius: 16px;
      font-size: 12px;
      font-weight: 600;
      display: inline-block;
      margin-bottom: 8px;
    }

    .vip-title {
      font-size: 16px;
      font-weight: 600;
      margin: 0;
    }
  }

  .vip-features {
    position: relative;
    z-index: 1;

    .feature-item {
      display: flex;
      align-items: center;
      padding: 8px 0;

      .feature-icon {
        font-size: 16px;
        margin-right: 12px;
        width: 20px;
        text-align: center;
      }

      .feature-text {
        flex: 1;
        font-size: 14px;
      }

      .feature-status {
        font-size: 12px;
        background: rgba(255, 255, 255, 0.2);
        padding: 2px 8px;
        border-radius: 10px;
        opacity: 0.8;
      }
    }
  }

  .vip-action {
    text-align: center;
    margin-top: 16px;
    position: relative;
    z-index: 1;

    .vip-btn {
      background: rgba(255, 255, 255, 0.2);
      border: 1px solid rgba(255, 255, 255, 0.3);
      color: white;
      padding: 8px 20px;
      border-radius: 20px;
      font-size: 14px;
      cursor: pointer;
      transition: all 0.2s ease;

      &:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-1px);
      }
    }
  }
}

@keyframes vipShine {
  0%, 100% {
    transform: rotate(0deg);
    opacity: 0.3;
  }
  50% {
    transform: rotate(180deg);
    opacity: 0.6;
  }
}

// VIP弹窗内容
.vip-modal-content {
  .vip-intro {
    text-align: center;
    margin-bottom: 20px;

    .vip-icon {
      font-size: 48px;
      margin-bottom: 12px;
    }

    .vip-text {
      font-size: 16px;
      color: $text-color;
      font-weight: 500;
    }
  }

  .vip-feature-list {
    .vip-feature-item {
      display: flex;
      align-items: center;
      padding: 12px 0;
      border-bottom: 1px solid $border-color-light;

      &:last-child {
        border-bottom: none;
      }

      .feature-icon {
        font-size: 20px;
        margin-right: 16px;
        width: 24px;
        text-align: center;
      }

      .feature-info {
        flex: 1;

        .feature-name {
          font-size: 14px;
          font-weight: 500;
          color: $text-color;
          margin-bottom: 4px;
        }

        .feature-desc {
          font-size: 12px;
          color: $text-color-secondary;
          line-height: 1.3;
        }
      }

      .feature-badge {
        background: rgba($primary-color, 0.1);
        color: $primary-color;
        font-size: 10px;
        padding: 4px 8px;
        border-radius: 8px;
        font-weight: 500;
      }
    }
  }

  .vip-footer {
    text-align: center;
    margin-top: 20px;

    .vip-note {
      font-size: 12px;
      color: $text-color-secondary;
      line-height: 1.4;
    }
  }
}
</style>