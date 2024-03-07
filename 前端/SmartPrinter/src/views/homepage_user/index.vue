<script>

  export default{
    data() {
      return {
        username: '',
        fileList: [],
        centerDialogVisible: false,
      }
    },
    methods:{
      user_logout(){
        this.$router.push({ name: 'login'});
      },
      handleMenuClick(index) {
        if (index === '1') {
          this.$router.push({name:'createPrint', query: {username:this.username}});
        } else if (index === '2') {
          this.$router.push({name:'historyPrint', query: {username:this.username}});
        } else if (index == '3'){
          this.$router.push({name:'showPrice', query: {username:this.username}});
        } else if (index == '4'){
          this.$router.push({name:'login'});
        }
      }
    },
    mounted:function(){
      this.username = this.$route.query.username
    }
  }
</script>

<template>
  <div class="homepage_user">
    <div class="container">
      <div class="center-text"><p>导航</p></div>
      <el-menu
        active-text-color="#E9543B"
        background-color="#FFF4F2"
        class="menu"
        default-active="1"
        text-color="#000"
        @select="handleMenuClick"
      >
        <el-menu-item index="1">
          <el-icon><Printer /></el-icon>
          <span>新建打印订单</span>
          <el-icon><ArrowRight /></el-icon>
        </el-menu-item>
        <el-menu-item index="2">
          <el-icon><AlarmClock /></el-icon>
          <span>历史打印订单</span>
          <el-icon><ArrowRight /></el-icon>
        </el-menu-item>
        <el-menu-item index="3">
          <el-icon><Shop /></el-icon>
          <span>价格公示</span>
          <el-icon><ArrowRight /></el-icon>
        </el-menu-item>
        <el-menu-item index="4">
          <el-icon><setting /></el-icon>
          <span>退出登录</span>
          <el-icon><ArrowRight /></el-icon>
        </el-menu-item>
      </el-menu>
    </div>
  </div>
</template>

<style scoped>
.homepage_user {
  display: flex;
  justify-content: center;
  align-items: center;
  height: center;
  font-family: 'Arial', 'SimHei';
}
.menu {
  border-radius: 20px;
}
.menu .el-menu-item {
  height: 100px;
  width: 300px;
  font-size: 20px;
  font-weight: bold;
}
.center-text {
  text-align: center;
  font-size: 36px;
  font-family: 'Times New Roman', 'SimHei';
  font-weight: bold;
} 
</style>