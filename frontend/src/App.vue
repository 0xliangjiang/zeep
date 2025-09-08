<template>
  <div id="app">
    <router-view />

    <!-- 全局Toast组件 -->
    <WechatToast
      v-if="toast.show"
      :message="toast.message"
      :type="toast.type"
      @close="hideToast"
    />

    <!-- 全局Modal组件 -->
    <WechatModal
      v-if="modal.show"
      :title="modal.title"
      :content="modal.content"
      :show-cancel="modal.showCancel"
      :confirm-text="modal.confirmText"
      :cancel-text="modal.cancelText"
      @confirm="modal.onConfirm"
      @cancel="modal.onCancel"
      @close="hideModal"
    />
  </div>
</template>

<script>
import { reactive } from 'vue'
import WechatToast from './components/WechatToast.vue'
import WechatModal from './components/WechatModal.vue'

export default {
  name: 'App',
  components: {
    WechatToast,
    WechatModal
  },
  setup() {
    // 全局Toast状态
    const toast = reactive({
      show: false,
      message: '',
      type: 'info'
    })

    // 全局Modal状态
    const modal = reactive({
      show: false,
      title: '',
      content: '',
      showCancel: true,
      confirmText: '确定',
      cancelText: '取消',
      onConfirm: () => {},
      onCancel: () => {}
    })

    // Toast方法
    const showToast = (message, type = 'info') => {
      toast.message = message
      toast.type = type
      toast.show = true

      // 自动隐藏
      setTimeout(() => {
        hideToast()
      }, 3000)
    }

    const hideToast = () => {
      toast.show = false
    }

    // Modal方法
    const showModal = (options) => {
      modal.title = options.title || ''
      modal.content = options.content || ''
      modal.showCancel = options.showCancel !== false
      modal.confirmText = options.confirmText || '确定'
      modal.cancelText = options.cancelText || '取消'
      modal.onConfirm = options.onConfirm || (() => {})
      modal.onCancel = options.onCancel || (() => {})
      modal.show = true
    }

    const hideModal = () => {
      modal.show = false
    }

    // 全局提供方法
    window.$toast = showToast
    window.$modal = showModal

    return {
      toast,
      modal,
      hideToast,
      hideModal
    }
  }
}
</script>

<style lang="scss">
#app {
  min-height: 100vh;
  background-color: $bg-color;
}
</style>