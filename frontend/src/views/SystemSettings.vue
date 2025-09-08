<template>
  <div class="page">
    <div class="page-content">
      <!-- 系统设置卡片 -->
      <div class="settings-card">
        <div class="settings-header">
          <h2>系统设置</h2>
          <p class="settings-subtitle">管理系统全局配置</p>
        </div>

        <!-- 联系客服弹窗内容设置 -->
        <div class="setting-item">
          <div class="setting-label">
            <h3>联系客服弹窗内容</h3>
            <p class="setting-desc">设置用户点击"联系客服"时显示的内容</p>
          </div>
          
          <div class="setting-content">
            <textarea
              v-model="contactContent"
              class="contact-textarea"
              placeholder="请输入联系客服的内容，支持中英文数字特殊符号等任何字符..."
              rows="8"
            ></textarea>
            
            <div class="setting-actions">
              <WechatButton
                type="primary"
                @click="saveContactContent"
                :loading="saving"
              >
                保存设置
              </WechatButton>
              
              <WechatButton
                type="secondary"
                @click="previewContent"
              >
                预览效果
              </WechatButton>
            </div>
          </div>
        </div>

        <!-- 首页公告设置 -->
        <div class="setting-item">
          <div class="setting-label">
            <h3>首页公告设置</h3>
            <p class="setting-desc">设置首页显示的公告内容</p>
          </div>

          <div class="setting-content">
            <textarea
              v-model="announcementContent"
              class="contact-textarea"
              placeholder="请输入首页公告内容..."
              rows="4"
            ></textarea>

            <div class="setting-actions">
              <WechatButton
                type="primary"
                @click="saveAnnouncementContent"
                :loading="savingAnnouncement"
              >
                保存公告
              </WechatButton>

              <WechatButton
                type="secondary"
                @click="previewAnnouncement"
              >
                预览效果
              </WechatButton>
            </div>
          </div>
        </div>

        <!-- 其他系统设置可以在这里添加 -->
        <div class="setting-item">
          <div class="setting-label">
            <h3>其他设置</h3>
            <p class="setting-desc">更多系统设置功能开发中...</p>
          </div>

          <div class="setting-content">
            <div class="coming-soon">
              <div class="coming-soon-icon">🚧</div>
              <div class="coming-soon-text">功能开发中，敬请期待</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部导航 -->
    <WechatNavBar />

    <!-- 预览弹窗 -->
    <ContactModal
      :show="showPreview"
      @close="showPreview = false"
    />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import WechatButton from '../components/WechatButton.vue'
import WechatNavBar from '../components/WechatNavBar.vue'
import ContactModal from '../components/ContactModal.vue'

export default {
  name: 'SystemSettings',
  components: {
    WechatButton,
    WechatNavBar,
    ContactModal
  },
  setup() {
    const contactContent = ref('')
    const saving = ref(false)
    const showPreview = ref(false)

    const announcementContent = ref('')
    const savingAnnouncement = ref(false)

    // 获取当前联系客服内容
    const fetchContactContent = async () => {
      try {
        const response = await fetch('/api/admin/system-settings/contact-content', {
          method: 'GET',
          credentials: 'include'
        })
        
        if (response.ok) {
          const data = await response.json()
          if (data.success) {
            contactContent.value = data.content || ''
          }
        }
      } catch (error) {
        console.error('获取联系客服内容失败:', error)
      }
    }

    // 保存联系客服内容
    const saveContactContent = async () => {
      saving.value = true
      
      try {
        const response = await fetch('/api/admin/system-settings/contact-content', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include',
          body: JSON.stringify({
            content: contactContent.value
          })
        })
        
        const data = await response.json()
        
        if (response.ok && data.success) {
          window.$toast('联系客服内容保存成功', 'success')
        } else {
          window.$toast(data.error || '保存失败', 'error')
        }
      } catch (error) {
        console.error('保存联系客服内容失败:', error)
        window.$toast('保存失败', 'error')
      } finally {
        saving.value = false
      }
    }

    // 获取公告内容
    const fetchAnnouncementContent = async () => {
      try {
        const response = await fetch('/api/admin/system-settings/home-announcement', {
          method: 'GET',
          credentials: 'include'
        })

        if (response.ok) {
          const data = await response.json()
          if (data.success) {
            announcementContent.value = data.content || ''
          }
        }
      } catch (error) {
        console.error('获取公告内容失败:', error)
      }
    }

    // 保存公告内容
    const saveAnnouncementContent = async () => {
      savingAnnouncement.value = true

      try {
        const response = await fetch('/api/admin/system-settings/home-announcement', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          credentials: 'include',
          body: JSON.stringify({
            content: announcementContent.value
          })
        })

        const data = await response.json()

        if (response.ok && data.success) {
          window.$toast('首页公告保存成功', 'success')
        } else {
          window.$toast(data.error || '保存失败', 'error')
        }
      } catch (error) {
        console.error('保存公告内容失败:', error)
        window.$toast('保存失败', 'error')
      } finally {
        savingAnnouncement.value = false
      }
    }

    // 预览公告效果
    const previewAnnouncement = () => {
      if (!announcementContent.value.trim()) {
        window.$toast('请先输入公告内容', 'warning')
        return
      }
      window.$toast(`公告预览：${announcementContent.value}`, 'info')
    }

    // 预览效果
    const previewContent = () => {
      showPreview.value = true
    }

    onMounted(() => {
      fetchContactContent()
      fetchAnnouncementContent()
    })

    return {
      contactContent,
      saving,
      showPreview,
      saveContactContent,
      previewContent,

      announcementContent,
      savingAnnouncement,
      saveAnnouncementContent,
      previewAnnouncement
    }
  }
}
</script>

<style lang="scss" scoped>
.settings-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(135, 206, 235, 0.1);
  
  .settings-header {
    margin-bottom: 32px;
    text-align: center;
    
    h2 {
      font-size: 24px;
      font-weight: 600;
      color: #2c3e50;
      margin: 0 0 8px 0;
    }
    
    .settings-subtitle {
      font-size: 14px;
      color: #7f8c8d;
      margin: 0;
    }
  }
  
  .setting-item {
    margin-bottom: 32px;
    
    &:last-child {
      margin-bottom: 0;
    }
    
    .setting-label {
      margin-bottom: 16px;
      
      h3 {
        font-size: 18px;
        font-weight: 500;
        color: #2c3e50;
        margin: 0 0 4px 0;
      }
      
      .setting-desc {
        font-size: 14px;
        color: #7f8c8d;
        margin: 0;
        line-height: 1.4;
      }
    }
    
    .setting-content {
      .contact-textarea {
        width: 100%;
        min-height: 120px;
        padding: 16px;
        border: 1px solid #e1e8ed;
        border-radius: 8px;
        font-size: 14px;
        line-height: 1.5;
        resize: vertical;
        font-family: inherit;
        
        &:focus {
          outline: none;
          border-color: #4682B4;
          box-shadow: 0 0 0 3px rgba(70, 130, 180, 0.1);
        }
        
        &::placeholder {
          color: #bdc3c7;
        }
      }
      
      .setting-actions {
        display: flex;
        gap: 12px;
        margin-top: 16px;
        
        .wechat-button {
          flex: 1;
        }
      }
      
      .coming-soon {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, rgba(135, 206, 235, 0.05) 0%, rgba(70, 130, 180, 0.02) 100%);
        border-radius: 12px;
        border: 1px solid rgba(135, 206, 235, 0.1);
        
        .coming-soon-icon {
          font-size: 32px;
          margin-bottom: 12px;
        }
        
        .coming-soon-text {
          font-size: 14px;
          color: #7f8c8d;
        }
      }
    }
  }
}
</style>
