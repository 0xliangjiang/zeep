import { ref, computed } from 'vue'

// 节日主题配置
const festivals = [
  {
    name: '春节',
    startDate: '2025-01-28',
    endDate: '2025-02-11',
    colors: {
      primary: '#ff4757',
      secondary: '#ffa502',
      background: 'linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%)'
    },
    decorations: ['🧧', '🎆', '🏮', '🐉'],
    greeting: '新年快乐，步步高升！'
  },
  {
    name: '情人节',
    startDate: '2025-02-14',
    endDate: '2025-02-14',
    colors: {
      primary: '#ff3838',
      secondary: '#ff6b9d',
      background: 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)'
    },
    decorations: ['💕', '💖', '🌹', '💝'],
    greeting: '爱要大声说出来，也要用行动表达！'
  },
  {
    name: '清明节',
    startDate: '2025-04-04',
    endDate: '2025-04-06',
    colors: {
      primary: '#2ed573',
      secondary: '#7bed9f',
      background: 'linear-gradient(135deg, #70a1ff 0%, #5352ed 100%)'
    },
    decorations: ['🌸', '🌿', '🕊️', '🌱'],
    greeting: '春暖花开，踏青好时节！'
  },
  {
    name: '劳动节',
    startDate: '2025-05-01',
    endDate: '2025-05-03',
    colors: {
      primary: '#ffa502',
      secondary: '#ff6348',
      background: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)'
    },
    decorations: ['💪', '⚒️', '🏗️', '👷'],
    greeting: '劳动最光荣，运动更健康！'
  },
  {
    name: '端午节',
    startDate: '2025-05-31',
    endDate: '2025-06-02',
    colors: {
      primary: '#2ed573',
      secondary: '#1dd1a1',
      background: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)'
    },
    decorations: ['🐉', '🚣', '🎋', '🥟'],
    greeting: '端午安康，龙舟竞渡！'
  },
  {
    name: '中秋节',
    startDate: '2025-10-06',
    endDate: '2025-10-06',
    colors: {
      primary: '#ffa502',
      secondary: '#ff7675',
      background: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)'
    },
    decorations: ['🌕', '🥮', '🏮', '🌙'],
    greeting: '月圆人团圆，步数也要圆满！'
  },
  {
    name: '国庆节',
    startDate: '2025-10-01',
    endDate: '2025-10-07',
    colors: {
      primary: '#ff4757',
      secondary: '#ffa502',
      background: 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)'
    },
    decorations: ['🇨🇳', '🎆', '🎊', '🏮'],
    greeting: '祖国生日快乐，健康运动不停歇！'
  },
  {
    name: '圣诞节',
    startDate: '2025-12-24',
    endDate: '2025-12-25',
    colors: {
      primary: '#ff4757',
      secondary: '#2ed573',
      background: 'linear-gradient(135deg, #ff9a9e 0%, #a8edea 100%)'
    },
    decorations: ['🎄', '🎅', '🎁', '⭐'],
    greeting: 'Merry Christmas! 圣诞快乐！'
  }
]

const currentTheme = ref(null)

export function useTheme() {
  // 获取当前日期
  const getCurrentDate = () => {
    return new Date().toISOString().split('T')[0]
  }

  // 检查是否在节日期间
  const isInFestival = (festival) => {
    const today = getCurrentDate()
    return today >= festival.startDate && today <= festival.endDate
  }

  // 获取当前节日主题
  const getCurrentFestival = () => {
    return festivals.find(festival => isInFestival(festival))
  }

  // 应用主题
  const applyTheme = (festival) => {
    if (!festival) return

    const root = document.documentElement
    root.style.setProperty('--festival-primary', festival.colors.primary)
    root.style.setProperty('--festival-secondary', festival.colors.secondary)
    root.style.setProperty('--festival-background', festival.colors.background)
    
    currentTheme.value = festival
  }

  // 移除主题
  const removeTheme = () => {
    const root = document.documentElement
    root.style.removeProperty('--festival-primary')
    root.style.removeProperty('--festival-secondary')
    root.style.removeProperty('--festival-background')
    
    currentTheme.value = null
  }

  // 初始化主题
  const initTheme = () => {
    const festival = getCurrentFestival()
    if (festival) {
      applyTheme(festival)
    } else {
      removeTheme()
    }
  }

  // 获取节日装饰
  const getFestivalDecorations = computed(() => {
    return currentTheme.value ? currentTheme.value.decorations : []
  })

  // 获取节日问候语
  const getFestivalGreeting = computed(() => {
    return currentTheme.value ? currentTheme.value.greeting : ''
  })

  // 是否有节日主题
  const hasFestivalTheme = computed(() => {
    return currentTheme.value !== null
  })

  return {
    currentTheme,
    festivals,
    getCurrentFestival,
    applyTheme,
    removeTheme,
    initTheme,
    getFestivalDecorations,
    getFestivalGreeting,
    hasFestivalTheme
  }
}
