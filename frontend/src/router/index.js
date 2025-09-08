import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import FreeTrial from '../views/FreeTrial.vue'
import Profile from '../views/Profile.vue'
import Bind from '../views/Bind.vue'
import StepRecords from '../views/StepRecords.vue'
import Admin from '../views/Admin.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: '首页',
      requiresAuth: true
    }
  },
  {
    path: '/free-trial',
    name: 'FreeTrial',
    component: FreeTrial,
    meta: {
      title: '免费体验',
      requiresAuth: true
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: {
      title: '个人中心',
      requiresAuth: true
    }
  },
  {
    path: '/bind',
    name: 'Bind',
    component: Bind,
    meta: {
      title: '绑定账号',
      requiresAuth: true
    }
  },
  {
    path: '/records',
    name: 'StepRecords',
    component: StepRecords,
    meta: {
      title: '步数记录',
      requiresAuth: true
    }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
    meta: {
      title: '管理员',
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/system-settings',
    name: 'SystemSettings',
    component: () => import('../views/SystemSettings.vue'),
    meta: {
      title: '系统设置',
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/invite/:code',
    name: 'Invite',
    component: () => import('../views/InviteRedirect.vue'),
    meta: {
      title: '邀请链接'
    }
  },
  {
    path: '/card-manage',
    name: 'CardKeyManage',
    component: () => import('../views/CardKeyManage.vue'),
    meta: {
      title: '卡密管理',
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/donation-manage',
    name: 'DonationManage',
    component: () => import('../views/DonationManage.vue'),
    meta: {
      title: '捐赠管理',
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/admin-settings',
    name: 'AdminSettings',
    component: () => import('../views/AdminSettings.vue'),
    meta: {
      title: '管理员设置',
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/zepp-manage',
    name: 'ZeppManage',
    component: () => import('../views/ZeppManage.vue'),
    meta: {
      title: 'Zepp账号管理',
      requiresAuth: true,
      requiresAdmin: true
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title
  }

  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    try {
      // 检查用户登录状态
      const response = await fetch('/auth/user', {
        credentials: 'include'
      })

      if (response.ok) {
        const userData = await response.json()

        // 管理员权限检查由页面组件自行处理

        next()
      } else {
        // 未登录，跳转到微信授权
        window.location.href = '/auth/wechat'
      }
    } catch (error) {
      console.error('认证检查失败:', error)
      window.location.href = '/auth/wechat'
    }
  } else {
    next()
  }
})

export default router