const { defineConfig } = require('@vue/cli-service')
//only for test
const apiMocker = require('mocker-api')
const path = require('path')
/*
module.exports = defineConfig({
  lintOnSave:false, 
  transpileDependencies: true
})
*/

module.exports = {
  lintOnSave:false, 
  devServer: {
    proxy: {
      '/': {
        target: 'http://108.61.7.16:3721/',// 后端接口
        changeOrigin: true, // 是否跨域
        ws: false,
        pathRewrite: {
          '/': ''
        }
      }
    }
  }
}