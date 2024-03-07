<script>
  import axios from 'axios'
  export default {
    data() {
      return {
       taskData: [],
      }
    },
    methods: {
      backHomepage() {
        this.$router.push({name: 'homepage_user', query: {username:this.username}})
      },
      getTaskData(){
        let url='/api/historyPrint/';
        let params={
          username: this.username,
        };
        axios.post(url, params).then(r=>{
            if(r.data.status == 'ok'){
              this.taskData = r.data.data
            }
            else{
              this.taskData = 'error'
            }
          }).catch(e=>{})
      },
      goDetail(taskID){
        this.$router.push({name: 'taskDetails', query: {username:this.username, taskID: taskID}});
      },
    },
    mounted:function(){
      this.username = this.$route.query.username
      this.getTaskData()
    }
  }
</script>
<template>
  <div class="container">
    <div class="_container">
      <el-button round type="danger" @click="backHomepage">
        <el-icon><ArrowLeftBold /></el-icon>返回</el-button>
    </div>
    <br>
    <div>
      <el-space v-if="taskData!='null'" wrap>
        <el-card v-if="taskData!='null'" v-for="(card, index) in taskData" 
          :key="index" 
          class="rounded-card" 
          style="width: 300px" 
          shadow="hover" 
          :header-style="{ backgroundColor: '#FAFAFA', color: '#303133'}"
          :body-style="{ backgroundColor: '#FAFAFA', color: '#303133'}" 
        >
          <template #header>
            <div class="card-header">
              <span>订单号：<br>{{ card.taskID }}</span>
              <el-button text bg round type="success" @click="goDetail(card.taskID)"><el-icon><View /></el-icon>&nbsp;详情</el-button>
            </div>
          </template>
          <div v-for="(V, K) in card.description" :key="K" class="text item">
            {{ K }} : {{ V }}
          </div>
        </el-card>
      </el-space>
      <el-empty v-else description="无历史订单"/>
    </div>
  </div>
</template>

<style scoped>
.container {
    width: 300px;
    margin: 0 auto;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px dashed #ebeef5;
  line-height: 1.5;
  font-size: 16px;
  font-weight: bold;
  font-family:'Times New Roman', 'FangSong';
  margin-bottom: 18px;
  color: #73BAD6
}
.text {
  font-size: 14px;
  font-family:'Times New Roman', 'SimHei';
  color:cadetblue
}
.item {
  margin-bottom: 18px;
}
.rounded-card {
  border-radius: 20px;
  width: 300px;
}
</style>