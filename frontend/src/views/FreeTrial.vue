<template>
  <div class="page">
    <div class="page-content">
      <!-- 邀请好友卡片 -->
      <div class="invite-card">
        <div class="invite-header">
          <div class="invite-icon">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="9" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
              <path d="m19 8 2 2-2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="m15 10 4 0" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div class="invite-title">
            <h3>邀请好友</h3>
            <p class="invite-subtitle">分享获得更多体验时间</p>
          </div>
        </div>

        <div class="invite-content">
          <div class="invite-reward">
            <div class="reward-item">
              <div class="reward-number">3</div>
              <div class="reward-label">天体验时间</div>
            </div>
            <div class="reward-desc">每邀请一位好友注册即可获得</div>
          </div>

          <div class="invite-link-section">
            <div class="link-container">
              <input
                ref="linkInput"
                :value="inviteLink"
                readonly
                class="link-input"
                placeholder="正在生成邀请链接..."
              />
              <button
                class="copy-button"
                @click="copyInviteLink"
                :disabled="!inviteLink"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <rect x="9" y="9" width="13" height="13" rx="2" ry="2" stroke="currentColor" stroke-width="2"/>
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" stroke="currentColor" stroke-width="2"/>
                </svg>
                复制链接
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 邀请规则 -->
      <div class="rules-card">
        <div class="rules-header">
          <h3>邀请规则</h3>
        </div>
        <div class="rules-content">
          <div class="rule-item">
            <div class="rule-number">1</div>
            <div class="rule-text">
              <div class="rule-title">分享链接</div>
              <div class="rule-desc">将专属邀请链接分享给好友</div>
            </div>
          </div>
          <div class="rule-item">
            <div class="rule-number">2</div>
            <div class="rule-text">
              <div class="rule-title">好友注册</div>
              <div class="rule-desc">好友通过链接完成注册</div>
            </div>
          </div>
          <div class="rule-item">
            <div class="rule-number">3</div>
            <div class="rule-text">
              <div class="rule-title">获得奖励</div>
              <div class="rule-desc">立即获得3天免费体验时间</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 邀请历史 -->
      <div class="card" v-if="inviteHistory.length > 0">
        <div class="card-header">
          <h3>邀请历史</h3>
        </div>
        <div class="card-body">
          <div class="history-list">
            <div
              v-for="record in inviteHistory"
              :key="record.id"
              class="history-item"
            >
              <div class="history-avatar">
                <span class="avatar-placeholder">{{ record.invitee_nickname?.charAt(0) || '?' }}</span>
              </div>
              <div class="history-details">
                <div class="history-name">{{ record.invitee_nickname || '匿名用户' }}</div>
                <div class="history-time">{{ formatTime(record.created_at) }}</div>
              </div>
              <div class="history-reward">
                +{{ record.reward_days }}天
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 统计信息 -->
      <div class="card">
        <div class="card-header">
          <h3>邀请统计</h3>
        </div>
        <div class="card-body">
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-number">{{ inviteCount }}</div>
              <div class="stat-label">邀请人数</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">{{ totalRewardDays }}</div>
              <div class="stat-label">获得天数</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 增加体验时长按钮 -->
      <div class="action-buttons">
        <WechatButton
          type="secondary"
          size="large"
          block
          @click="showUpgradeModal"
        >
          💎 增加体验时长
        </WechatButton>
      </div>
    </div>

    <!-- 底部导航 -->
    <WechatNavBar />

    <!-- 捐赠弹窗 -->
    <DonationModal
      :show="showDonationModal"
      @close="hideDonationModal"
      @success="handleDonationSuccess"
      @failed="handleDonationFailed"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import WechatButton from '../components/WechatButton.vue'
import WechatNavBar from '../components/WechatNavBar.vue'
import DonationModal from '../components/DonationModal.vue'

export default {
  name: 'FreeTrial',
  components: {
    WechatButton,
    WechatNavBar,
    DonationModal
  },
  setup() {
    const userInfo = ref(null)
    const inviteHistory = ref([])
    const inviteLink = ref('')
    const linkInput = ref(null)
    const showDonationModal = ref(false)

    const inviteCount = computed(() => inviteHistory.value.length)
    const totalRewardDays = computed(() => {
      return inviteHistory.value.reduce((total, record) => total + record.reward_days, 0)
    })

    // 获取用户信息
    const fetchUserInfo = async () => {
      try {
        const response = await fetch('/auth/user', {
          credentials: 'include'
        })
        if (response.ok) {
          userInfo.value = await response.json()
          generateInviteLink()
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
      }
    }

    // 生成邀请链接
    const generateInviteLink = () => {
      if (userInfo.value?.invite_code) {
        inviteLink.value = `https://3ff67dd78f5e.ngrok-free.app/invite/${userInfo.value.invite_code}`
      }
    }

    // 获取邀请历史
    const fetchInviteHistory = async () => {
      try {
        const response = await fetch('/api/invite/history', {
          credentials: 'include'
        })
        if (response.ok) {
          const data = await response.json()
          inviteHistory.value = data.records || []
        }
      } catch (error) {
        console.error('获取邀请历史失败:', error)
      }
    }

    // 复制邀请链接
    const copyInviteLink = async () => {
      if (!inviteLink.value) return

      try {
        await navigator.clipboard.writeText(inviteLink.value)
        window.$toast('邀请链接已复制', 'success')
      } catch (error) {
        // 降级方案：选中文本
        if (linkInput.value) {
          linkInput.value.select()
          linkInput.value.setSelectionRange(0, 99999)
          try {
            document.execCommand('copy')
            window.$toast('邀请链接已复制', 'success')
          } catch (e) {
            window.$toast('复制失败，请手动复制链接', 'error')
          }
        }
      }
    }

    // 显示升级弹窗（现在显示捐赠弹窗）
    const showUpgradeModal = () => {
      showDonationModal.value = true
    }

    // 隐藏捐赠弹窗
    const hideDonationModal = () => {
      showDonationModal.value = false
    }

    // 处理捐赠成功
    const handleDonationSuccess = async (days) => {
      // 刷新用户信息
      await fetchUserInfo()
    }

    // 处理捐赠失败
    const handleDonationFailed = () => {
      // 可以在这里添加失败处理逻辑
    }

    // 格式化时间显示
    const formatTime = (timeStr) => {
      const date = new Date(timeStr)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
    }

    onMounted(() => {
      fetchUserInfo()
      fetchInviteHistory()
    })

    return {
      userInfo,
      inviteHistory,
      inviteLink,
      linkInput,
      inviteCount,
      totalRewardDays,
      showDonationModal,
      copyInviteLink,
      showUpgradeModal,
      hideDonationModal,
      handleDonationSuccess,
      handleDonationFailed,
      formatTime
    }
  }
}
</script>

<style lang="scss" scoped>
// 邀请卡片
.invite-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(135, 206, 235, 0.1);

  .invite-header {
    display: flex;
    align-items: center;
    margin-bottom: 24px;

    .invite-icon {
      width: 48px;
      height: 48px;
      background: linear-gradient(135deg, #87CEEB 0%, #4682B4 100%);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 16px;

      svg {
        color: white;
      }
    }

    .invite-title {
      h3 {
        font-size: 20px;
        font-weight: 600;
        color: #2c3e50;
        margin: 0 0 4px 0;
      }

      .invite-subtitle {
        font-size: 14px;
        color: #7f8c8d;
        margin: 0;
      }
    }
  }

  .invite-content {
    .invite-reward {
      background: linear-gradient(135deg, rgba(135, 206, 235, 0.1) 0%, rgba(70, 130, 180, 0.05) 100%);
      border-radius: 12px;
      padding: 20px;
      text-align: center;
      margin-bottom: 24px;
      border: 1px solid rgba(135, 206, 235, 0.2);

      .reward-item {
        display: flex;
        align-items: baseline;
        justify-content: center;
        gap: 8px;
        margin-bottom: 8px;

        .reward-number {
          font-size: 32px;
          font-weight: 700;
          color: #4682B4;
          line-height: 1;
        }

        .reward-label {
          font-size: 16px;
          color: #4682B4;
          font-weight: 500;
        }
      }

      .reward-desc {
        font-size: 14px;
        color: #7f8c8d;
        margin: 0;
      }
    }

    .invite-link-section {
      .link-container {
        display: flex;
        gap: 12px;
        align-items: center;

        .link-input {
          flex: 1;
          padding: 12px 16px;
          border: 1px solid #e1e8ed;
          border-radius: 8px;
          font-size: 14px;
          background: #f8f9fa;
          color: #2c3e50;

          &:focus {
            outline: none;
            border-color: #87CEEB;
            box-shadow: 0 0 0 3px rgba(135, 206, 235, 0.1);
          }
        }

        .copy-button {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 12px 20px;
          background: #4682B4;
          color: white;
          border: none;
          border-radius: 8px;
          font-size: 14px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s ease;
          white-space: nowrap;

          &:hover:not(:disabled) {
            background: #5a9bd4;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(70, 130, 180, 0.3);
          }

          &:disabled {
            background: #bdc3c7;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
          }

          svg {
            width: 16px;
            height: 16px;
          }
        }
      }
    }
  }
}

.rules-list {
  .rule-item {
    display: flex;
    align-items: center;
    gap: $spacing-md;
    padding: $spacing-sm 0;

    .rule-icon {
      font-size: $font-size-lg;
      flex-shrink: 0;
    }

    .rule-text {
      flex: 1;
      font-size: $font-size-sm;
      line-height: $line-height-normal;
    }
  }
}

.history-list {
  .history-item {
    display: flex;
    align-items: center;
    gap: $spacing-md;
    padding: $spacing-sm 0;
    border-bottom: 1px solid $border-color-light;

    &:last-child {
      border-bottom: none;
    }

    .history-avatar {
      width: 40px;
      height: 40px;
      border-radius: $border-radius-round;
      background-color: $primary-color;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;

      .avatar-placeholder {
        color: $text-color-white;
        font-weight: $font-weight-bold;
        font-size: $font-size-md;
      }
    }

    .history-details {
      flex: 1;

      .history-name {
        font-weight: $font-weight-medium;
        margin-bottom: $spacing-xs;
      }

      .history-time {
        font-size: $font-size-xs;
        color: $text-color-secondary;
      }
    }

    .history-reward {
      color: $success-color;
      font-weight: $font-weight-bold;
      font-size: $font-size-sm;
    }
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $spacing-lg;

  .stat-item {
    text-align: center;

    .stat-number {
      font-size: $font-size-xxl;
      font-weight: $font-weight-bold;
      color: $primary-color;
      margin-bottom: $spacing-xs;
    }

    .stat-label {
      font-size: $font-size-sm;
      color: $text-color-secondary;
    }
  }
}

.action-buttons {
  margin: $spacing-lg 0;
}

// 规则卡片
.rules-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(135, 206, 235, 0.1);

  .rules-header {
    margin-bottom: 20px;

    h3 {
      font-size: 18px;
      font-weight: 600;
      color: #2c3e50;
      margin: 0;
    }
  }

  .rules-content {
    .rule-item {
      display: flex;
      align-items: flex-start;
      margin-bottom: 20px;

      &:last-child {
        margin-bottom: 0;
      }

      .rule-number {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #87CEEB 0%, #4682B4 100%);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: 600;
        margin-right: 16px;
        flex-shrink: 0;
      }

      .rule-text {
        flex: 1;
        padding-top: 2px;

        .rule-title {
          font-size: 16px;
          font-weight: 500;
          color: #2c3e50;
          margin-bottom: 4px;
        }

        .rule-desc {
          font-size: 14px;
          color: #7f8c8d;
          line-height: 1.4;
        }
      }
    }
  }
}
</style>