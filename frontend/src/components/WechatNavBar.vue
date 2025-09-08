<template>
  <div class="wechat-navbar">
    <div
      v-for="item in navItems"
      :key="item.name"
      :class="['nav-item', { 'nav-item--active': isActive(item.name) }]"
      @click="handleNavClick(item)"
    >
      <div class="nav-icon">
          <!-- 首页图标 -->
          <svg v-if="item.icon === 'home'" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M9 22V12H15V22" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <!-- 免费体验图标 -->
          <svg v-else-if="item.icon === 'gift'" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <polyline points="20,12 20,22 4,22 4,12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <rect x="2" y="7" width="20" height="5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="12" y1="22" x2="12" y2="7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 7H7.5C6.83696 7 6.20107 6.73661 5.73223 6.26777C5.26339 5.79893 5 5.16304 5 4.5C5 3.83696 5.26339 3.20107 5.73223 2.73223C6.20107 2.26339 6.83696 2 7.5 2C11 2 12 7 12 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M12 7H16.5C17.163 7 17.7989 6.73661 18.2678 6.26777C18.7366 5.79893 19 5.16304 19 4.5C19 3.83696 18.7366 3.20107 18.2678 2.73223C17.7989 2.26339 17.163 2 16.5 2C13 2 12 7 12 7Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <!-- 步数记录图标 -->
          <svg v-else-if="item.icon === 'chart'" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <line x1="18" y1="20" x2="18" y2="10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="12" y1="20" x2="12" y2="4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="6" y1="20" x2="6" y2="14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <!-- 个人中心图标 -->
          <svg v-else-if="item.icon === 'user'" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
      <div class="nav-text">{{ item.text }}</div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

export default {
  name: 'WechatNavBar',
  setup() {
    const router = useRouter()
    const route = useRoute()

    const navItems = [
      {
        name: 'Home',
        text: '首页',
        icon: 'home',
        path: '/'
      },
      {
        name: 'FreeTrial',
        text: '免费体验',
        icon: 'gift',
        path: '/free-trial'
      },
      {
        name: 'StepRecords',
        text: '步数记录',
        icon: 'chart',
        path: '/records'
      },
      {
        name: 'Profile',
        text: '个人中心',
        icon: 'user',
        path: '/profile'
      }
    ]

    const isActive = (name) => {
      return route.name === name
    }

    const handleNavClick = (item) => {
      if (route.path !== item.path) {
        router.push(item.path)
      }
    }



    return {
      navItems,
      isActive,
      handleNavClick
    }
  }
}
</script>

<style lang="scss" scoped>
.wechat-navbar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: $z-index-fixed;

  display: flex;
  background: #ffffff;
  border-top: 1px solid #e1e8ed;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
  padding: 6px 0 calc(6px + env(safe-area-inset-bottom));

  .nav-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    padding: $spacing-sm;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    border-radius: $border-radius-sm;
    margin: 0 2px;
    position: relative;

    &:active {
      transform: scale(0.9);
    }

    .nav-icon {
      font-size: 18px;
      margin-bottom: 2px;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
      transform: scale(1);
    }

    .nav-text {
      font-size: 10px;
      color: $text-color-secondary;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      font-weight: $font-weight-medium;
      line-height: 1;
    }

    &--active {
      .nav-icon {
        color: #007AFF;
        transform: scale(1.1);
      }

      .nav-text {
        color: #007AFF;
        font-weight: 600;
      }
    }

    &:hover:not(&--active) {
      .nav-icon {
        transform: scale(1.05);
      }
    }
  }
}
</style>