<template>
  <div class="page">
    <div class="page-content">
      <!-- 用户信息卡片 -->
      <div class="profile-card" v-if="userInfo">
        <div class="profile-header">
          <div class="profile-avatar">
            <img :src="userInfo.headimgurl" :alt="userInfo.nickname" />
          </div>
          <div class="profile-info">
            <h2 class="profile-name">{{ userInfo.nickname }}</h2>
            <div class="profile-status" :class="{ 'expired': userInfo.is_expired }">
              <div class="status-indicator"></div>
              <span class="status-text">
                {{ userInfo.is_expired ? '授权已过期' : `剩余 ${userInfo.remaining_days} 天` }}
              </span>
            </div>
          </div>
        </div>

        <div class="profile-stats">
          <div class="stat-item">
            <div class="stat-value">{{ userInfo.total_days }}</div>
            <div class="stat-label">总授权天数</div>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <div class="stat-value">{{ inviteCount }}</div>
            <div class="stat-label">邀请好友</div>
          </div>
        </div>
      </div>

      <!-- 功能菜单 -->
      <div class="menu-card">
        <div class="menu-list">
          <div class="menu-item" @click="goToInvite">
            <div class="menu-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="9" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
                <path d="m19 8 2 2-2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="m15 10 4 0" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="menu-content">
              <div class="menu-title">邀请好友</div>
              <div class="menu-desc">分享获得更多体验时间</div>
            </div>
            <div class="menu-arrow">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="m9 18 6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>

          <div class="menu-item" @click="showCardModal">
            <div class="menu-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="2" y="5" width="20" height="14" rx="2" stroke="currentColor" stroke-width="2"/>
                <line x1="2" y1="10" x2="22" y2="10" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <div class="menu-content">
              <div class="menu-title">卡密兑换</div>
              <div class="menu-desc">输入卡密兑换体验时间</div>
            </div>
            <div class="menu-arrow">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="m9 18 6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>

          <div class="menu-item" @click="showDonationModal">
            <div class="menu-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="menu-content">
              <div class="menu-title">赞助支持</div>
              <div class="menu-desc">支持开发者，获得更长体验时间</div>
            </div>
            <div class="menu-arrow">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="m9 18 6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>

          <!-- 管理员专用功能 -->
          <div v-if="isAdmin" class="menu-item" @click="goToAdminSettings">
            <div class="menu-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <div class="menu-content">
              <div class="menu-title">管理员设置</div>
              <div class="menu-desc">卡密管理、捐赠管理、Zepp账号管理</div>
            </div>
            <div class="menu-arrow">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="m9 18 6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>

          <div v-if="isAdmin" class="menu-item" @click="goToSystemSettings">
            <div class="menu-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z" stroke="currentColor" stroke-width="2"/>
                <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <div class="menu-content">
              <div class="menu-title">系统设置</div>
              <div class="menu-desc">联系客服内容、系统配置管理</div>
            </div>
            <div class="menu-arrow">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="m9 18 6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
          </div>

          <div class="menu-item" @click="showNoticeModal">
            <div class="menu-icon">📋</div>
            <div class="menu-content">
              <div class="menu-title">注意事项</div>
              <div class="menu-desc">使用须知和常见问题</div>
            </div>
            <div class="menu-arrow">›</div>
          </div>

          <div class="menu-item" @click="showContactModal">
            <div class="menu-icon">💬</div>
            <div class="menu-content">
              <div class="menu-title">联系客服</div>
              <div class="menu-desc">遇到问题？联系我们</div>
            </div>
            <div class="menu-arrow">›</div>
          </div>
        </div>
      </div>


    </div>

    <!-- 底部导航 -->
    <WechatNavBar />

    <!-- 卡密兑换弹窗 -->
    <WechatModal
      v-if="showCardRedeemModal"
      title="卡密兑换"
      :show-cancel="true"
      confirm-text="兑换"
      @confirm="redeemCard"
      @cancel="hideCardModal"
      @close="hideCardModal"
    >
      <div class="card-redeem-form">
        <input
          v-model="cardKey"
          type="text"
          placeholder="请输入卡密"
          class="card-input"
          maxlength="32"
        />
        <p class="card-hint">请输入有效的卡密进行兑换</p>
      </div>
    </WechatModal>

    <!-- 捐赠弹窗 -->
    <DonationModal
      :show="showDonationModalFlag"
      @close="hideDonationModal"
      @success="handleDonationSuccess"
      @failed="handleDonationFailed"
    />

    <!-- 联系客服弹窗 -->
    <ContactModal
      :show="showContactModalState"
      @close="showContactModalState = false"
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import WechatButton from '../components/WechatButton.vue'
import WechatNavBar from '../components/WechatNavBar.vue'
import WechatModal from '../components/WechatModal.vue'
import DonationModal from '../components/DonationModal.vue'
import ContactModal from '../components/ContactModal.vue'

export default {
  name: 'Profile',
  components: {
    WechatButton,
    WechatNavBar,
    WechatModal,
    DonationModal,
    ContactModal
  },
  setup() {
    const router = useRouter()
    const userInfo = ref(null)
    const inviteCount = ref(0)
    const showCardRedeemModal = ref(false)
    const cardKey = ref('')
    const isAdmin = ref(false)
    const showDonationModalFlag = ref(false)

    // 获取用户信息
    const fetchUserInfo = async () => {
      try {
        const response = await fetch('/auth/user', {
          credentials: 'include'
        })
        if (response.ok) {
          userInfo.value = await response.json()
          // 获取用户信息后检查管理员权限
          await checkAdminPermission()
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
      }
    }

    // 检查管理员权限
    const checkAdminPermission = async () => {
      try {
        const response = await fetch('/api/card/check-admin', {
          credentials: 'include'
        })

        if (response.ok) {
          const data = await response.json()
          isAdmin.value = data.is_admin
        } else {
          isAdmin.value = false
        }
      } catch (error) {
        console.error('检查管理员权限失败:', error)
        isAdmin.value = false
      }
    }

    // 获取邀请统计
    const fetchInviteStats = async () => {
      try {
        const response = await fetch('/api/invite/history', {
          credentials: 'include'
        })
        if (response.ok) {
          const data = await response.json()
          inviteCount.value = data.records?.length || 0
        }
      } catch (error) {
        console.error('获取邀请统计失败:', error)
      }
    }

    // 跳转到邀请页面
    const goToInvite = () => {
      router.push('/free-trial')
    }

    // 跳转到管理员设置页面
    const goToAdminSettings = () => {
      router.push('/admin-settings')
    }

    // 跳转到系统设置页面
    const goToSystemSettings = () => {
      router.push('/system-settings')
    }

    // 显示捐赠弹窗
    const showDonationModal = () => {
      showDonationModalFlag.value = true
    }

    // 隐藏捐赠弹窗
    const hideDonationModal = () => {
      showDonationModalFlag.value = false
    }

    // 处理捐赠成功
    const handleDonationSuccess = async () => {
      // 刷新用户信息
      await fetchUserInfo()
    }

    // 处理捐赠失败
    const handleDonationFailed = () => {
      // 可以在这里添加失败处理逻辑
    }

    // 显示卡密兑换弹窗
    const showCardModal = () => {
      cardKey.value = ''
      showCardRedeemModal.value = true
    }

    // 隐藏卡密兑换弹窗
    const hideCardModal = () => {
      showCardRedeemModal.value = false
      cardKey.value = ''
    }

    // 兑换卡密
    const redeemCard = async () => {
      if (!cardKey.value.trim()) {
        window.$toast('请输入卡密', 'warning')
        return
      }

      try {
        const response = await fetch('/api/card/redeem', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include',
          body: JSON.stringify({
            card_key: cardKey.value.trim()
          })
        })

        const data = await response.json()

        if (response.ok && data.success) {
          window.$toast(data.message, 'success')
          hideCardModal()
          fetchUserInfo() // 刷新用户信息
        } else {
          window.$toast(data.message || data.error || '兑换失败', 'error')
        }
      } catch (error) {
        console.error('兑换卡密失败:', error)
        window.$toast('网络错误，请稍后重试', 'error')
      }
    }

    // 显示注意事项
    const showNoticeModal = () => {
      window.$modal({
        title: '注意事项',
        content: `1. 本工具仅供学习交流使用，请勿用于商业用途
2. 修改步数可能需要一定时间生效，请耐心等待
3. 请合理设置步数，避免设置过高的数值
4. 如遇到问题，请及时联系客服
5. 请遵守相关法律法规，文明使用`,
        showCancel: false,
        confirmText: '我知道了'
      })
    }

    // 显示联系客服
    // 联系客服弹窗状态
    const showContactModalState = ref(false)

    const showContactModal = () => {
      showContactModalState.value = true
    }



    onMounted(() => {
      fetchUserInfo()
      fetchInviteStats()
    })

    return {
      userInfo,
      inviteCount,
      showCardRedeemModal,
      cardKey,
      isAdmin,
      showDonationModalFlag,
      goToInvite,
      goToAdminSettings,
      goToSystemSettings,
      showCardModal,
      hideCardModal,
      redeemCard,
      showNoticeModal,
      showContactModal,
      showContactModalState,
      showDonationModal,
      hideDonationModal,
      handleDonationSuccess,
      handleDonationFailed,
      checkAdminPermission
    }
  }
}
</script>

<style lang="scss" scoped>
// 用户资料卡片
.profile-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(135, 206, 235, 0.1);

  .profile-header {
    display: flex;
    align-items: center;
    margin-bottom: 24px;

    .profile-avatar {
      position: relative;
      margin-right: 16px;

      img {
        width: 64px;
        height: 64px;
        border-radius: 50%;
        object-fit: cover;
        border: 3px solid rgba(135, 206, 235, 0.2);
      }
    }

    .profile-info {
      flex: 1;

      .profile-name {
        font-size: 20px;
        font-weight: 600;
        color: #2c3e50;
        margin: 0 0 8px 0;
      }

      .profile-status {
        display: flex;
        align-items: center;
        gap: 8px;

        .status-indicator {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #27ae60;

          .expired & {
            background: #e74c3c;
          }
        }

        .status-text {
          font-size: 14px;
          color: #27ae60;
          font-weight: 500;

          .expired & {
            color: #e74c3c;
          }
        }
      }
    }
  }

  .profile-stats {
    display: flex;
    align-items: center;
    justify-content: space-around;
    padding: 20px 0;
    background: linear-gradient(135deg, rgba(135, 206, 235, 0.05) 0%, rgba(70, 130, 180, 0.02) 100%);
    border-radius: 12px;
    border: 1px solid rgba(135, 206, 235, 0.1);

    .stat-item {
      text-align: center;
      flex: 1;

      .stat-value {
        font-size: 24px;
        font-weight: 700;
        color: #4682B4;
        margin-bottom: 4px;
        line-height: 1;
      }

      .stat-label {
        font-size: 12px;
        color: #7f8c8d;
        font-weight: 500;
      }
    }

    .stat-divider {
      width: 1px;
      height: 40px;
      background: rgba(135, 206, 235, 0.2);
      margin: 0 20px;
    }
  }
}

// 菜单卡片
.menu-card {
  background: white;
  border-radius: 16px;
  padding: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(135, 206, 235, 0.1);
}

.menu-list {
  .menu-item {
    display: flex;
    align-items: center;
    padding: 16px;
    cursor: pointer;
    transition: all 0.2s ease;
    border-radius: 12px;
    margin-bottom: 4px;

    &:last-child {
      margin-bottom: 0;
    }

    &:hover {
      background: linear-gradient(135deg, rgba(135, 206, 235, 0.05) 0%, rgba(70, 130, 180, 0.02) 100%);
      transform: translateX(4px);
    }

    &:active {
      transform: translateX(2px);
    }

    .menu-icon {
      width: 40px;
      height: 40px;
      background: linear-gradient(135deg, rgba(135, 206, 235, 0.1) 0%, rgba(70, 130, 180, 0.05) 100%);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: 16px;
      flex-shrink: 0;

      svg {
        color: #4682B4;
      }
    }

    .menu-content {
      flex: 1;

      .menu-title {
        font-size: 16px;
        font-weight: 500;
        color: #2c3e50;
        margin-bottom: 4px;
      }

      .menu-desc {
        font-size: 14px;
        color: #7f8c8d;
        line-height: 1.3;
      }
    }

    .menu-arrow {
      width: 20px;
      height: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #bdc3c7;
      flex-shrink: 0;

      svg {
        transition: transform 0.2s ease;
      }
    }

    &:hover .menu-arrow svg {
      transform: translateX(2px);
    }
  }
}

.action-buttons {
  margin: $spacing-lg 0;
}

.card-redeem-form {
  .card-input {
    width: 100%;
    padding: $spacing-md;
    border: 1px solid $border-color;
    border-radius: $border-radius-small;
    font-size: $font-size-md;
    margin-bottom: $spacing-sm;

    &:focus {
      border-color: $primary-color;
      box-shadow: 0 0 0 2px rgba($primary-color, 0.2);
    }
  }

  .card-hint {
    font-size: $font-size-sm;
    color: $text-color-secondary;
    text-align: center;
    margin: 0;
  }
}
</style>