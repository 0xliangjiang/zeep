const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: '/',
  outputDir: 'dist',
  assetsDir: 'static',

  devServer: {
    port: 7000,
    host: 'localhost',
    allowedHosts: 'all',
    proxy: {
      '/auth': {
        target: 'http://localhost:5520',
        changeOrigin: true,
        secure: false
      },
      '/api': {
        target: 'http://localhost:5520',
        changeOrigin: true,
        secure: false
      }
    }
  },

  css: {
    loaderOptions: {
      sass: {
        additionalData: `@import "@/assets/css/variables.scss";`
      }
    }
  },

  chainWebpack: config => {
    config.plugin('html').tap(args => {
      args[0].title = 'WechatZepp - 微信运动步数修改'
      return args
    })
  }
})