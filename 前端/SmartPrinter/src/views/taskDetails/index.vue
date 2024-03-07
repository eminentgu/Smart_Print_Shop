<script>
  import axios from 'axios'

  export default {
    data() {
      return {
        username: '',
        taskID: '',
        fromCreate: false,
        detailData: {},
      }
    },
    methods: {
      backLogic() {
        if (this.fromCreate) {
          this.$router.push({name: 'homepage_user', query: {username:this.username}})
        }
        else {
          this.$router.push({name: 'historyPrint', query: {username:this.username}})
        }
      },
      getDetailData(username, taskID) {
        let url='/api/printDetail/';
        let params={
          taskID: taskID,
          username: username,
        };
        axios.post(url, params).then(r=>{
            if(r.data.status == 'ok'){
              this.detailData = r.data.detailData
            }
            else{
              this.detailData = 'error'
            }
          }).catch(e=>{})
      }
    },
    mounted:function(){
      this.username = this.$route.query.username;
      this.taskID = this.$route.query.taskID;
      this.fromCreate = this.$route.query.fromCreate;
      this.getDetailData(this.username, this.taskID);
    }
  }

</script>
<template>
  <div class="container">
    <div class="_container">
      <el-button round type="danger" @click="backLogic">
        <el-icon><ArrowLeftBold /></el-icon>返回</el-button>
    </div>
    <div class="center-text"><p>订单详情</p></div>
    <el-space wrap>
      <el-card v-for="(card, index) in detailData" 
      :key="index" 
      class="rounded-card" 
      style="width: 300px" 
      shadow="hover" 
      :header-style="{ backgroundColor: '#FAFAFA', color: '#303133'}"
      :body-style="{ backgroundColor: '#FAFAFA', color: '#303133'}" 
      >
        <template #header>
          <div class="card-header">
            <span>
              文件{{index + 1}}：{{ card.fileName }}
            </span>
          </div>
        </template>
        <div v-for="item in card.description" :key="item" class="text item">
          {{ item }}
        </div>
      </el-card>
    </el-space>
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
  font-size: 16px;
  font-weight: bold;
  font-family:'Times New Roman', 'FangSong';
  color: #73BAD6
}
.text {
  font-size: 14px;
  font-family:Cambria, Cochin, Georgia, Times, 'Times New Roman', 'SimHei';
  color:cadetblue
}
.item {
  margin-bottom: 18px;
}
.rounded-card {
  border-radius: 20px;
  width: 250px;
}
.center-text {
  text-align: center;
  font-size: 28px;
  font-family: 'Times New Roman', 'KaiTi';
  font-weight: bold;
} 
</style>