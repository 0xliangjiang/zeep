<template>
  <div class="skeleton-loader">
    <div v-for="n in rows" :key="n" class="skeleton-row">
      <div class="skeleton-item" :style="getItemStyle(n)"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SkeletonLoader',
  props: {
    rows: {
      type: Number,
      default: 3
    },
    type: {
      type: String,
      default: 'default' // default, card, profile
    }
  },
  setup(props) {
    const getItemStyle = (index) => {
      if (props.type === 'card') {
        return {
          height: index === 1 ? '60px' : '20px',
          width: index === 1 ? '100%' : `${60 + Math.random() * 40}%`
        }
      } else if (props.type === 'profile') {
        return {
          height: index === 1 ? '80px' : '16px',
          width: index === 1 ? '80px' : `${40 + Math.random() * 50}%`,
          borderRadius: index === 1 ? '50%' : '4px'
        }
      } else {
        return {
          height: '16px',
          width: `${50 + Math.random() * 40}%`
        }
      }
    }

    return {
      getItemStyle
    }
  }
}
</script>

<style lang="scss" scoped>
.skeleton-loader {
  .skeleton-row {
    margin-bottom: 12px;
    
    &:last-child {
      margin-bottom: 0;
    }
    
    .skeleton-item {
      background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
      background-size: 200% 100%;
      animation: skeleton-loading 1.5s infinite;
      border-radius: 4px;
      height: 16px;
    }
  }
}

@keyframes skeleton-loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>
