<script>
  import axios from 'axios'
  import * as echarts from 'echarts'

 export default {
  data() {

    return {
      username: '', // 这里是变量文本
      profits:'',
      good_printer : '',
      bad_printer : '',
      tableData:'',
      dialogVisible: false,
      taskID: 166622,
    };
  },
    methods:{
      admin_logout(){
        this.$router.push({ name: 'login'});
      },
      getProfits(){  // 获取今日收支
        let  url='/api/profits/';
        axios.get(url).then(r=>{
            if(r.data.status == 'ok'){
              this.profits = r.data.profits
            }
				    else{
					    this.profits = 'error'
				        }
          }).catch(e=>{})
      },
     getPrinter(){  // 获取打印机状态
        let  url='/api/printer/';
        axios.get(url).then(r=>{
            if(r.data.status == 'ok'){
              this.good_printer = r.data.good
              this.bad_printer = r.data.bad
            }
				    else{
					    this.good_printer = 'error'
              this.bad_printer = 'error'
				        }
          }).catch(e=>{})
      },
      getPrintlist(){
        let  url='/api/printlist/';
        axios.get(url).then(r=>{
            if(r.data.status == 'ok'){  // 后端筛选出未打印和未配送的任务，返回给tableleData
              this.tableData = r.data.data;
            }
          }).catch(e=>{})
      },
      goToDetails(condition, taskID) {
        if (condition == '待打印') {
          this.$router.push({ name: 'adminPrint',query:{username: this.username, taskID: taskID}});
        }
        else {  // 分配骑手的对话框visible设置为True，对话框可以设计为仅仅一句话：已分配骑手，骑手姓名为xxx
          this.dialogVisible = true;
          this.taskID = taskID;
        }
      },
      assignDeliver(taskID){
        this.dialogVisible = false;
        this.$notify({
          title: '操作成功',
          message: '已为订单' + taskID + '分配专送员<br>姓名：xxx，联系电话：13442960333',
          type: 'success',
          position: 'bottom-left',
          dangerouslyUseHTMLString: true,
        });
        let url = '/api/assignDeliver/';
        let params = {
          taskID: taskID,
        };
        axios.post(url, params).then(r=>{}).catch(e=>{});  // 告知后端配送员已分配完毕
        this.getPrintlist();  // 更新订单列表
      },
      show(){
        let url = '/api/getDrawData/';
        axios.get(url).then(r=>{
          const printerData = JSON.parse(JSON.stringify(r.data.printer));
          const conditionData = JSON.parse(JSON.stringify(r.data.condition));
          this.draw(printerData, conditionData);
          }).catch(e=>{
            this.$message.error("提交失败");})
      },
      draw(printerData, conditionData){
        const printerContainer = this.$refs.printerChart;
        const conditionContainer = this.$refs.conditionChart;
        const printChart = echarts.init(printerContainer);
        const conditionChart = echarts.init(conditionContainer);
        var printerOption = {
          "animation": true,
          "animationThreshold": 2000,
          "animationDuration": 1000,
          "animationEasing": "cubicOut",
          "animationDelay": 0,
          "animationDurationUpdate": 300,
          "animationEasingUpdate": "cubicOut",
          "animationDelayUpdate": 0,
          "aria": {
            "enabled": false
          },
          "color": [
            "#73c0de",
            "#3ba272",
            "#fc8452",
            "#9a60b4",
            "#ea7ccc"
          ],
          "series": [
            {
              "type": "bar",
              "name": "\u5269\u4f59\u7eb8\u91cf\uff08%\uff09",
              "legendHoverLink": true,
              "data": printerData.paperVols,
              "realtimeSort": false,
              "showBackground": false,
              "stackStrategy": "samesign",
              "cursor": "pointer",
              "barMinHeight": 0,
              "barCategoryGap": "20%",
              "barGap": "30%",
              "large": false,
              "largeThreshold": 400,
              "seriesLayoutBy": "column",
              "datasetIndex": 0,
              "clip": true,
              "zlevel": 0,
              "z": 2,
              "label": {
                "show": true,
                "position": "top",
                "margin": 8,
                "fontSize": 10
              },
              "rippleEffect": {
                "show": true,
                "brushType": "stroke",
                "scale": 2.5,
                "period": 4
              }
            },
            {
              "type": "bar",
              "name": "\u5269\u4f59\u58a8\u91cf\uff08%\uff09",
              "legendHoverLink": true,
              "data": printerData.inkVols,
              "realtimeSort": false,
              "showBackground": false,
              "stackStrategy": "samesign",
              "cursor": "pointer",
              "barMinHeight": 0,
              "barCategoryGap": "20%",
              "barGap": "30%",
              "large": false,
              "largeThreshold": 400,
              "seriesLayoutBy": "column",
              "datasetIndex": 0,
              "clip": true,
              "zlevel": 0,
              "z": 2,
              "label": {
                "show": true,
                "position": "top",
                "margin": 8,
                "fontSize": 10
              },
              "rippleEffect": {
                "show": true,
                "brushType": "stroke",
                "scale": 2.5,
                "period": 4
              }
            }
          ],
          "legend": [
            {
              "data": [
                "\u5269\u4f59\u7eb8\u91cf\uff08%\uff09",
                "\u5269\u4f59\u58a8\u91cf\uff08%\uff09"
              ],
              "textStyle": {
                "fontSize": 10
              },
              "selected": {},
              "show": true,
              "padding": 5,
              "itemGap": 10,
              "itemWidth": 25,
              "itemHeight": 14,
              "backgroundColor": "transparent",
              "borderColor": "#ccc",
              "borderWidth": 1,
              "borderRadius": 0,
              "pageButtonItemGap": 5,
              "pageButtonPosition": "end",
              "pageFormatter": "{current}/{total}",
              "pageIconColor": "#2f4554",
              "pageIconInactiveColor": "#aaa",
              "pageIconSize": 15,
              "animationDurationUpdate": 800,
              "selector": false,
              "selectorPosition": "auto",
              "selectorItemGap": 7,
              "selectorButtonGap": 10
            }
          ],
          "tooltip": {
            "show": true,
            "trigger": "item",
            "triggerOn": "mousemove|click",
            "axisPointer": {
              "type": "line"
            },
            "showContent": true,
            "alwaysShowContent": false,
            "showDelay": 0,
            "hideDelay": 100,
            "enterable": false,
            "confine": false,
            "appendToBody": false,
            "transitionDuration": 0.4,
            "textStyle": {
              "fontSize": 10
            },
            "borderWidth": 0,
            "padding": 5,
            "order": "seriesAsc"
          },
          "xAxis": [
            {
              "show": true,
              "scale": false,
              "nameLocation": "end",
              "nameGap": 15,
              "gridIndex": 0,
              "axisLabel": {
                "show": true,
                "margin": 8,
                "fontSize": 8
              },
              "inverse": false,
              "offset": 0,
              "splitNumber": 5,
              "minInterval": 0,
              "splitLine": {
                "show": true,
                "lineStyle": {
                  "show": true,
                  "width": 1,
                  "opacity": 1,
                  "curveness": 0,
                  "type": "solid"
                }
              },
              "data": printerData.printerNames
            }
          ],
          "yAxis": [
            {
              "show": true,
              "scale": false,
              "nameLocation": "end",
              "nameGap": 15,
              "gridIndex": 0,
              "inverse": false,
              "offset": 0,
              "splitNumber": 5,
              "max": 100,
              "minInterval": 0,
              "axisLabel": {
                "fontSize": 10
              },
              "splitLine": {
                "show": true,
                "lineStyle": {
                  "show": true,
                  "width": 1,
                  "opacity": 1,
                  "curveness": 0,
                  "type": "solid"
                }
              }
            }
          ],
          "title": [
            {
              "show": true,
              "target": "blank",
              "subtarget": "blank",
              "padding": 5,
              "itemGap": 10,
              "textAlign": "auto",
              "textVerticalAlign": "auto",
              "triggerEvent": false
            }
          ]
        };
        var conditionOption = {
          "animation": true,
          "animationThreshold": 2000,
          "animationDuration": 1000,
          "animationEasing": "cubicOut",
          "animationDelay": 0,
          "animationDurationUpdate": 300,
          "animationEasingUpdate": "cubicOut",
          "animationDelayUpdate": 0,
          "aria": {
            "enabled": false
          },
          "color": [
            "#5470c6",
            "#91cc75",
            "#fac858",
            "#ee6666",
            "#73c0de",
            "#3ba272",
            "#fc8452",
            "#9a60b4",
            "#ea7ccc"
          ],
          "series": [
            {
              "type": "pie",
              "colorBy": "data",
              "legendHoverLink": true,
              "selectedMode": false,
              "selectedOffset": 10,
              "clockwise": true,
              "startAngle": 90,
              "minAngle": 0,
              "minShowLabelAngle": 0,
              "avoidLabelOverlap": true,
              "stillShowZeroSum": true,
              "percentPrecision": 2,
              "showEmptyCircle": true,
              "emptyCircleStyle": {
                "color": "lightgray",
                "borderColor": "#000",
                "borderWidth": 0,
                "borderType": "solid",
                "borderDashOffset": 0,
                "borderCap": "butt",
                "borderJoin": "bevel",
                "borderMiterLimit": 10,
                "opacity": 1
              },
              "data": conditionData.Itemexpense,
              "radius": [
                "40%",
                "75%"
              ],
              "center": [
                "50%",
                "50%"
              ],
              "label": {
                "show": true,
                "position": "inside",
                "margin": 8,
                "fontSize": 12,
              },
              "labelLine": {
                "show": true,
                "showAbove": false,
                "length": 15,
                "length2": 15,
                "smooth": false,
                "minTurnAngle": 90,
                "maxSurfaceAngle": 90
              },
              "tooltip": {
                "show": true,
                "trigger": "item",
                "triggerOn": "mousemove|click",
                "axisPointer": {
                  "type": "line"
                },
                "showContent": true,
                "alwaysShowContent": false,
                "showDelay": 0,
                "hideDelay": 100,
                "enterable": false,
                "confine": false,
                "appendToBody": false,
                "transitionDuration": 0.4,
                "formatter": function(params) {return params.name + ': ' + params.value + '元';},
                "textStyle": {
                  "fontSize": 14
                },
                "borderWidth": 0,
                "padding": 5,
                "order": "seriesAsc"
              },
              "rippleEffect": {
                "show": true,
                "brushType": "stroke",
                "scale": 2.5,
                "period": 4
              }
            }
          ],
          "legend": [
            {
              "data": conditionData.ItemNames,
              "selected": {}
            }
          ],
          "tooltip": {
            "show": true,
            "trigger": "item",
            "triggerOn": "mousemove|click",
            "axisPointer": {
              "type": "line"
            },
            "showContent": true,
            "alwaysShowContent": false,
            "showDelay": 0,
            "hideDelay": 100,
            "enterable": false,
            "confine": false,
            "appendToBody": false,
            "transitionDuration": 0.4,
            "textStyle": {
              "fontSize": 14
            },
            "borderWidth": 0,
            "padding": 5,
            "order": "seriesAsc"
          }
        };
        printChart.setOption(printerOption);
        conditionChart.setOption(conditionOption);
      }
    },
    
    mounted:function() {
      this.username = this.$route.query.username
      this.getProfits();
      this.getPrinter();
      this.getPrintlist();
      this.show();
    },        
  }
</script>

<template>
  <div class="homepage_admin">
    <div class="container">
      <div class="button_container">
        <el-button class="align-right" type="primary" @click="admin_logout">退出登录</el-button>
      </div>
      <div class="style1 current-cashier">当前店员： <span class="current-username">{{username}}</span> </div>
      <div class="style1 today-revenue">本月收支：<span class="current-profits">{{profits}} 元</span></div>
      <!-- <div class="profit-image">
          <el-image style="width: 300px; height: 200px" :src="require('@/assets/profits.png')" :fit='scale-down' />
      </div> -->
      <div ref="conditionChart" style="width: 300px; height: 300px;"></div>
        
      <div class="style1 device-status">设备状态:  <span class="good_printer">😊&nbsp;{{good_printer}}&nbsp;&nbsp;</span>  <span class="bad_printer">🤯&nbsp;{{bad_printer}}</span></div>
      <!-- <div class="condition-image">
          <el-image style="width: 300px; height: 200px" :src="require('@/assets/printers.jpg')" :fit='scale-down' />
      </div> -->
      <div ref="printerChart" style="width: 300px; height: 300px;"></div>

      <div class="style1 device-status">订单管理</div>
      <el-table
        :data="tableData"
        stripe style="width: 100%"
        height="250"
        :header-cell-style="{'text-align':'center'}"
        :row-class-name="tableRowClassName"
      >
        <el-table-column prop="taskID" label="订单号" width="90" align="center"/>
        <el-table-column prop="appointTime" label="预定交付时间" width="150" align="center"/>
        <el-table-column prop="pickCode" label="客户取件码" width="100" align="center"/>
        <el-table-column prop="condition" label="状态" width="70" fixed="right" align="center">  <!--condition一共两种：待打印、待配送-->
          <template #default="scope">
            <el-link type="primary" @click="goToDetails(scope.row.condition, scope.row.taskID)">{{ scope.row.condition }}</el-link>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
  <el-dialog v-model="dialogVisible" :taskID="taskID" title="" width="50%" center>
    <span>
      确定为该打印订单分配专送员吗？
    </span>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="assignDeliver(taskID)">确定</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style>
.homepage_admin {
  display: flex;
  justify-content: center;
  align-items: center;
  height: center;
  font-family:'Arial', san-serif
}
.container {
  width: 300px; 
  background: #FFFFFF;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  padding: 20px;
  border-radius: 30px;
  text-align: left;
}

.button_container {
  display: flex;
  justify-content: flex-end;
}

.style1 {
  font-size: 28px;
  margin: 20px 0;
  color: #515253;
  font-weight: bold;
  text-transform: uppercase;
}

.current-username {
  color: #52a0c9;
}
.current-profits {
  color: #20b841;
}
.good_printer {
  color: #20b841;
}
.bad_printer {
  color: #e0473c;
}

.device-status {
  font-size: 28px; /* 为设备状态设置不同的字体大小 */
}
</style>

