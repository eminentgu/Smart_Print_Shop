<script>
  import axios from 'axios'
  import QrcodeVue from 'qrcode.vue';

  export default {
    data() {
      return {
        username: '',
        dialogVisible: false,
        payVisible: false,
        qrContent: '支付功能将在系统正式上线运营后开放',
        qrOptions: {
          size : 20,
        },
        uploadedFiles: [],
        currentID: -1,
        activeStep: 0,
        date: '',
        time: '',
        isAdding: false,
        optionName: '',
        value: '',
        addressList:[],
        address: '',
        totalPrice: 0,
        settingsForm:{
          paper: '',
          color: '',
          doubleSided: '',
          copies: 1,
          startPage: 1,
          endPage: 1,
          note: '',
        },
        dataStorage: []
      }
    },
    components: {
      QrcodeVue,
    },
    methods:{
      backHomepage() { // 返回用户主页
        this.$router.push({name: 'homepage_user', query: {username:this.username}});
      },
      disablePastDates(time) {  // 规定预约日期不能早于当前日期
        return time.getTime() < Date.now() - 8.64e7;
      },
      onConfirm(){
        if (this.optionName) {
          this.addressList.push({
            label: this.optionName,
            value: this.optionName,
          })
          this.clear()
        }
      },
      onAddOption(){
        this.isAdding = true
      },
      clear(){
        this.optionName = ''
        this.isAdding = false
      },
      getPrice(i) {  // 计算id为i的文件的打印价格
        let price = 0;
        let pages = this.dataStorage[i].endPage - this.dataStorage[i].startPage + 1
        let copies = this.dataStorage[i].copies;
        if (this.dataStorage[i].paper == 'A4'){
          if (this.dataStorage[i].color == '黑白'){
            if (this.dataStorage[i].doubleSided == '1'){
              price += 0.4;
            }
            else{
              price += 0.25;
            }
          }
          else{
            if (this.dataStorage[i].doubleSided == '1'){
              price += 2.2;
            }
            else{
              price += 1.2;
            }
          }
        }
        else{
          if (this.dataStorage[i].color == '黑白'){
            if (this.dataStorage[i].doubleSided == '1'){
              price += 0.8;
            }
            else{
              price += 0.5;
            }
          }
          else{
            if (this.dataStorage[i].doubleSided == '1'){
              price += 4.5;
            }
            else{
              price += 2.4;
            }
          }
        }          
        price *= pages;
        price *= copies;
        price = parseFloat(price.toFixed(2));
        return price;
      },
      beforeUpload(file, fileList) {  // 将用户上传的待打印文件存储到uploadedFiles中
        var dotIndex = file.name.lastIndexOf(".");
        const fileName = file.name.substring(0, dotIndex);
        let fileType = 'Unknown';
        const fileExtension = file.name.split('.').pop().toLowerCase();
        if (['jpg', 'jpeg', 'png', 'gif'].includes(fileExtension)) {
          fileType = '图片';
        } else if (['doc', 'docx', 'pdf', 'txt'].includes(fileExtension)) {
          fileType = '文档';
        } else if (['xls', 'xlsx', 'csv'].includes(fileExtension)) {
          fileType = '电子表格';
        }
        let fileID = this.uploadedFiles.length;
        this.uploadedFiles.push({id: fileID, name: fileName, type: fileType, settings: '配置'});
        return true;
      },
      submitUpload() {  // 提交上传文件到后端
        this.$refs.uploadRef.submit();
        if (this.uploadedFiles.length == 0){
          this.$message({
            message: '未选择要打印的文件！',
            type: 'error',
            showClose: true
          });
        }
      },
      submitSuccess(){  // 处理文件上传成功的逻辑
        this.$message({
          message: '文件上传成功！',
          type: 'success',
          showClose: true
        });
        if (this.activeStep == 1){
          this.activeStep = 2;
        }
      },
      submitFailed(){  // 处理文件上传失败的逻辑
        this.$message({
          message: '文件上传失败！',
          type: 'error',
          showClose: true
        });
      },
      printSettings(id){  // 开启打印设置对话框
        this.currentID = id;
        const currentSettings = this.dataStorage[id] || {};
        this.settingsForm.paper = currentSettings.paper || 'A4';
        this.settingsForm.color = currentSettings.color || '黑白';
        this.settingsForm.doubleSided = currentSettings.doubleSided || '0';
        this.settingsForm.note = currentSettings.note || '';
        this.settingsForm.copies = currentSettings.copies || 1;
        this.settingsForm.startPage = currentSettings.startPage || 1;
        this.settingsForm.endPage = currentSettings.endPage || 1;
        this.dialogVisible = true;
      },
      saveSettings() {  // 保存对应文件的打印设置
        const linkId = this.currentID;
        this.dataStorage[linkId] = {
          fileName: this.uploadedFiles[linkId].name,
          paper: this.settingsForm.paper,
          color: this.settingsForm.color,
          doubleSided: this.settingsForm.doubleSided,
          copies: this.settingsForm.copies,
          startPage: this.settingsForm.startPage,
          endPage: this.settingsForm.endPage,
          price: 0,
          note: this.settingsForm.note
        };
        this.dataStorage[linkId].price = this.getPrice(linkId);
        this.totalPrice = 0;
        for (let i = 0; i < this.dataStorage.length; i++){
          this.totalPrice += this.getPrice(i);
        }
        this.totalPrice = this.totalPrice.toFixed(2);
        this.dialogVisible = false;
      },
      showPay() {  // 展示用户付款对话框
        if (this.dataStorage.length === 0) {
          this.$message({
            message: '打印文件未上传/打印设置未完成！',
            type: 'error',
            showClose: true
          });
          return;
        }
        if (this.date == '' || this.time == ''){
          this.$message({
            message: '您未选择预约送达日期/时间！',
            type: 'error',
            showClose: true
          });
          return;
        }
        if (this.activeStep == 2){
          this.activeStep = 3;
        }
        this.payVisible = true;
      },
      payCancel() {  // 处理用户取消付款的逻辑
        if (this.activeStep == 3){
          this.activeStep = 2;
        }
        this.payVisible = false;
      },
      submitTask(){  // 提交打印任务
        let url='/api/submitPrint/';
        let params={
          username: this.username,
          appointDate: this.date,
          appointTime: this.time,
          address: this.value,
          totalPrice: this.totalPrice,
          dataStorage: this.dataStorage
        }
        axios.post(url,params).then(r=>{  // 提交打印任务，后端返回任务ID
          if(r.data.status == 'ok'){
            this.$message({
              message: '打印任务已提交！',
              type: 'success',
              showClose: true
            });
            this.$router.push({name: 'taskDetails', query: {username:this.username, taskID: r.data.taskID, fromCreate: true}});
          }else {
            this.$message.error("提交失败");
          }
        }).catch(e=>{
          this.$message.error("提交失败");})
      }
    },
    mounted:function(){
      this.username = this.$route.query.username;
      let url='/api/informBack/';
      axios.post(url).then(r=>{}).catch(e=>{});
      url='/api/getAddressList/';
      let params={
        username: this.username,
      };
      axios.post(url, params).then(r=>{
        if(r.data.status == 'ok'){
          this.addressList = r.data.addressList;
        }
        else{
          this.addressList = 'error';
        }
      }).catch(e=>{});
    }
  }
</script>

<template>
  <div class="createPrint">
    <div class="container">
      <div class="_container">
        <el-button round type="danger" @click="backHomepage">
          <el-icon><ArrowLeftBold /></el-icon>返回</el-button>
      </div>
      <br>
      <el-steps :active="activeStep" finish-status="success" align-center>
        <el-step title="步骤1" description="选择文件" icon="Document"></el-step>
        <el-step title="步骤2" description="开始上传" icon="Upload"></el-step>
        <el-step title="步骤3" description="提交打印" icon="Promotion"></el-step>
      </el-steps>
      <el-upload
        ref="uploadRef"
        class="upload-demo"
        accept=".pdf, .png, .jpg, .jpeg, .doc, .docx, .csv, .xls, .xlsx"
        action="/api/upload/"
        multiple
        :auto-upload="false"
        :before-upload="beforeUpload" 
        :on-success="submitSuccess"
        :on-error="submitFailed"
      >
        <template #tip>
          <div class="uploadTip">
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;支持各类文档、图片及Excel电子表格打印，单个文件大小不超过50MB.
          </div>
        </template>
        <template #trigger>
          <el-button round type="success" @click="() => activeStep = activeStep === 0 ? 1 : activeStep">
            <el-icon><Document /></el-icon>&nbsp;选择文件</el-button>
        </template>
      </el-upload>
      <div class="button_container">
        <el-button round type="success" @click="submitUpload">
          开始上传<el-icon class="el-icon--right"><Upload /></el-icon>
        </el-button>
      </div>
      <h3>寄送地址：</h3>
      <el-select v-model="value" placeholder="选择寄送地址" size="small">
        <el-option
          v-for="item in addressList"
          :key="item.value"
          :label="item.label"
          :value="item.value"
        />
        <template #footer>
          <el-button v-if = "!this.isAdding" text bg size="small" @click="onAddOption">新增地址</el-button>
          <template v-else>
            <el-input
              v-model="optionName"
              class="option-input"
              placeholder="请输入新地址"
              size="small"
            />
            <el-button type="primary" size="small" @click="onConfirm">确定</el-button>
            <el-button size="small" @click="clear">取消</el-button>
          </template>
        </template>
      </el-select>
      <h3>预约送达时间：</h3>
      <el-date-picker
        v-model="date"
        :disabled-date="disablePastDates"
        type="date"
        placeholder="选择日期"
        size="small"
        value-format="YYYY-MM-DD"
        style="width: 150px;"
      />
      &nbsp;
      <el-time-select
        v-model="time"
        placeholder="上门时间"
        start="08:30"
        step="00:30"
        end="20:30"
        size="small"
        style="width: 120px;"
      />
      <h3>已上传文件：</h3>
      <div>
        <el-table :data="uploadedFiles" v-if="uploadedFiles.length > 0" stripe  :header-cell-style="{'text-align':'center'}">
          <el-table-column label="文件名" prop="name" align="center"></el-table-column>
          <el-table-column label="文件类型" prop="type" align="center"></el-table-column>
          <el-table-column label="打印设置" prop="settings" align="center">
            <template #default="scope">
                <el-link type="primary" @click="printSettings(scope.row.id)">{{ scope.row.settings }}</el-link>
            </template>
          </el-table-column>
        </el-table>
        <el-empty v-else description="无文件上传"/>
      </div>
      <h3>合计：{{ this.totalPrice }} 元</h3>
      <div class="button_container_center">
        <el-button type="danger" @click="showPay">
          <el-icon><Promotion /></el-icon>&nbsp;提交打印</el-button>
      </div> 
    </div>
  </div>
  <el-dialog
    width="70%"
    draggable
    title="打印设置"
    v-model="dialogVisible"
  >
    <el-form :model="settingsForm" :rules="rules" label-width="80px">
      <el-form-item label="纸型">
        <el-radio-group v-model="settingsForm.paper">
          <el-radio label="A4">A4</el-radio>
          <el-radio label="A3">A3</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="颜色">
        <el-radio-group v-model="settingsForm.color">
          <el-radio-button label="黑白">黑白</el-radio-button>
          <el-radio-button label="彩色">彩色</el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="单双面">
        单&nbsp;&nbsp;&nbsp;<el-switch v-model="settingsForm.doubleSided" active-value="1" inactive-value="0" active-color="#13ce66" inactive-color="#ff4949"></el-switch>&nbsp;&nbsp;&nbsp;双
      </el-form-item>
      <el-form-item label="打印范围">
        <el-input-number v-model="settingsForm.startPage" :min="1" :max="settingsForm.endPage" :step="1" style="width: 70px" controls-position="right" />~
        <el-input-number v-model="settingsForm.endPage" :min="settingsForm.startPage" :step="1" style="width: 75px" controls-position="right" />
      </el-form-item>
      <el-form-item label="份数">
        <el-input-number v-model="settingsForm.copies" :min="1" :max="100" :step="1" style="width: 100px;" />
      </el-form-item>
      <el-form-item label="备注">
        <el-input v-model="settingsForm.note" autocomplete="off" placeholder="其他打印信息"/>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="saveSettings" >确认</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
  <el-dialog
    width="70%"
    draggable
    center
    title="支付"
    v-model="payVisible"
  >
    <div class="qrContainer">
      <qrcode-vue :value="qrContent" :options="qrOptions"></qrcode-vue>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="payCancel">取消支付</el-button>
        <el-button type="primary" @click="submitTask">
          已完成支付，继续
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style scoped>
.container {
    width: 300px;
    margin: 0 auto;
}

.button_container {
  display: flex;
  justify-content: flex-end;
}

.button_container_center {
  display: flex;
  justify-content: center;
}
.qrContainer {
  display: flex;
  justify-content: center;
  align-items: center;
}
.uploadTip{
  font-family: 'Times New Roman', 'SimHei';
  font-size: 14px;
  color: rgb(206, 12, 12);
  line-height: 1.5;
}
</style>