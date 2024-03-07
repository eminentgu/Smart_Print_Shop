<script>
  let A4Data = [
    {
      Type: '彩色双面',
      Price: '2.2元/张',
    },
    {
      Type: '彩色单面',
      Price: '1.2元/张',
    },
    {
      Type: '黑白双面',
      Price: '0.4元/张',
    },
    {
      Type: '黑白单面',
      Price: '0.25元/张',
    },
  ],
  A3Data = [
    {
      Type: '彩色双面',
      Price: '4.5元/张',
    },
    {
      Type: '彩色单面',
      Price: '2.4元/张',
    },
    {
      Type: '黑白双面',
      Price: '0.8元/张',
    },
    {
      Type: '黑白单面',
      Price: '0.5元/张',
    },
  ]
  export default {
    data() {
      return {
        username: '',
        A4Data,
        A3Data 
      }
    },
    methods:{
      backHomepage() {
        this.$router.push({name: 'homepage_user', query: {username:this.username}})
      },
    },
    mounted:function(){
      this.username = this.$route.query.username
    }
  }
</script>

<template>
  <div class="createPrint">
    <div class="container">
      <el-button round type="danger" @click="backHomepage">
        <el-icon><ArrowLeftBold /></el-icon>返回</el-button>
      <h2>A4</h2>
      <el-table :data="A4Data" stripe style="width: 100%">
        <el-table-column prop="Type" label="类型" width="150" />
        <el-table-column prop="Price" label="价格" align="right" width="150" />
      </el-table>
      <h2>A3</h2>
      <el-table :data="A3Data" stripe style="width: 100%">
        <el-table-column prop="Type" label="类型" width="150" />
        <el-table-column prop="Price" label="价格" align="right" width="150" />
      </el-table>
    </div>
  </div>
</template>

<style>
.createPrint {
  display: flex;
  justify-content: center;
  align-items: center;
  height: center;
  font-family: 'Arial', 'SimHei';
}
</style>