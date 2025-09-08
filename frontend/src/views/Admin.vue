<template>
  <div class="page">
    <div class="page-content">
      <div class="card">
        <div class="card-header">
          <h3>管理员面板</h3>
        </div>
        <div class="card-body">
          <p class="admin-desc">
            管理员功能正在开发中，敬请期待！
          </p>
          <div class="admin-features">
            <div class="feature-item">
              <span class="feature-icon">🎫</span>
              <span class="feature-text">卡密生成与管理</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">👥</span>
              <span class="feature-text">用户数据统计</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">📊</span>
              <span class="feature-text">系统监控面板</span>
            </div>
          </div>
          <WechatButton
            type="primary"
            block
            @click="goBack"
          >
            返回首页
          </WechatButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import WechatButton from '../components/WechatButton.vue'

export default {
  name: 'Admin',
  components: {
    WechatButton
  },
  setup() {
    const router = useRouter()

    const goBack = () => {
      router.push('/')
    }

    return {
      goBack
    }
  }
}
</script>

<style lang="scss" scoped>
.admin-desc {
  text-align: center;
  margin-bottom: $spacing-lg;
  color: $text-color-secondary;
}

.admin-features {
  margin-bottom: $spacing-lg;

  .feature-item {
    display: flex;
    align-items: center;
    gap: $spacing-md;
    padding: $spacing-md 0;
    border-bottom: 1px solid $border-color-light;

    &:last-child {
      border-bottom: none;
    }

    .feature-icon {
      font-size: $font-size-lg;
    }

    .feature-text {
      color: $text-color-secondary;
    }
  }
}
</style>