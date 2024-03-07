<script>
  import axios from 'axios'
  import JSZip from 'jszip';

  export default {
    data() {
        return {
            taskID: "",
            username: "",
            detailData: {},
            fileNames: [],
        };
    },
    methods: {
        backHomepage() {
            this.$router.push({ name: "homepage_admin", query: { username: this.username } });
        },
        getFileNames(taskID) {
          let url = "/api/fileList/"; // 使用另一个API获取文件名列表
          let params = {
              taskID: taskID,
          };
          axios.post(url, params).then(r => {
              if (r.data.status == "ok") {
                  const fileNames = JSON.parse(JSON.stringify(r.data.fileNames));
                  this.downloadFiles(fileNames);
              }
              else {
                  this.fileNames = "error";
              }
          }).catch(e => {});
        }, 
        getDetailData(taskID) {
            let url = "/api/printTask/"; // 使用另一个API获取详情数据
            let params = {
                taskID: taskID,
            };
            axios.post(url, params).then(r => {
                if (r.data.status == "ok") {
                    this.detailData = r.data.detailData;
                }
                else {
                    this.detailData = "error";
                }
            }).catch(e => { });
        },
        finish() {
            let url = "/api/finishTask/";
            let params = {
                taskID: this.taskID,
            };
            axios.post(url, params).then(r => {
                if (r.data.status == "ok") {
                    this.$message({
                        message: "操作成功！",
                        type: "success",
                        showClose: true
                    });
                    this.$router.push({ name: "homepage_admin", query: { username: this.username } });
                }
                else {
                    this.detailData = "error";
                }
            }).catch(e => { });
        },
        async downloadFiles(fileNames){
          try {
            const zip = new JSZip();

            // 根据文件名数组构建files数组
            const files = fileNames.map(name => ({
              name: name,
              url: '/fileList/' + this.taskID + `/${name}`, // 根据文件名构建完整的URL
            }));
            console.log(files);
            // 使用axios并发下载文件
            const responses = await Promise.all(
              files.map(file => axios.get(file.url, { responseType: 'arraybuffer' }))
            );

            // 将文件添加到JSZip实例中
            responses.forEach((response, index) => {
              zip.file(files[index].name, response.data);
            });

            // 生成Zip文件
            const zipBlob = await zip.generateAsync({ type: 'blob' });

            // 创建一个a标签
            const link = document.createElement('a');

            // 设置a标签的href为Zip文件的URL
            link.href = window.URL.createObjectURL(zipBlob);

            // 设置Zip文件的文件名
            link.download = '打印文件.zip'; // 替换为实际文件名

            // 将a标签添加到文档中
            document.body.appendChild(link);

            // 模拟点击a标签进行下载
            link.click();

            // 移除a标签
            document.body.removeChild(link);

            // 释放Blob对象的URL
            window.URL.revokeObjectURL(link.href);
          } catch (error) {
            console.error('下载文件时出错:', error);
          }
        }
    },
    mounted: function () {
        this.taskID = this.$route.query.taskID;
        this.username = this.$route.query.username;
        this.getDetailData(this.taskID);
    },
}
</script>

<template>
  <div class="container">
    <el-button round type="danger" @click="backHomepage">
      <el-icon><ArrowLeftBold /></el-icon>返回</el-button>
    <div class="_container">
      <el-button round type="success" @click="getFileNames(this.taskID)">
        <el-icon><Download /></el-icon>下载所有文件</el-button>
    </div>
    <br>
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
    <br><br>
    <el-popconfirm
      confirm-button-text="确定"
      cancel-button-text="取消"
      icon="InfoFilled"
      icon-color="#626AEF"
      title="请再次确认所有文件是否都打印完毕！"
      @confirm="finish"
    >
      <template #reference>
        <div class="button_container_center">
          <el-button type="danger">
            <el-icon><Finished /></el-icon>&nbsp;打印完成</el-button>
        </div> 
      </template>
    </el-popconfirm>
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
  color: #73BAD6;
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
._container {
  display: flex;
  justify-content: flex-end;
}
.button_container_center {
  display: flex;
  justify-content: center;
}
</style>