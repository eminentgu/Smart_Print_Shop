
<script>
  import axios from 'axios'

  //import qs from 'qs' */
  export default {
    name: 'Login',
    data(){
      return {
       username:'',
       password:'',
       confirmPassword:'',
       userType:'user'
      }
    },
    //页面跳转
     methods:{
      backLogin() {
        this.$router.push({name: 'login', query: {username:this.username}})
      },
       doSubmit(){
          let  url='/api/register/';
          let  params={
            username:this.username,
            password:this.password,
            confirmPassword:this.confirmPassword,
            userType:this.userType
          }
 
          axios.post(url,params).then(r=>{
            if(r.data.status == 'ok'){
					  this.$message({
                          message: '注册成功！',
                          type: 'success'
                          });
					  this.$router.push({ path: '/'});
            }
				    else{
              if (this.userType == 'admin'){
                this.$message({
                          message: '管理员注册失败！',
                          type: 'error'
                          });
              }
              else{
                this.$message({
                          message: '两次输入的密码不一致或该用户名已被注册！',
                          type: 'error'
                          });
              }
				        }
          }).catch(e=>{
 
          })
 
       }
     }
  }
</script>
 

<template>
	<div class="login">
		<el-form class="login-container">
      <div class="_container">
      <el-button round type="success" @click="backLogin">
        <el-icon><ArrowLeftBold /></el-icon>返回</el-button>
    </div>
			<h1 class="title">用户注册</h1>
			<el-form-item label="">
				<span>账号</span>
				<el-input type="text" v-model="username" placeholder="请输入账号" autocomplete="off"></el-input>
			</el-form-item>
			<el-form-item label="">
				<span>密码</span>
				<el-input type="password" v-model="password" placeholder="请输入密码" autocomplete="off"></el-input>
			</el-form-item>
			<el-form-item label="">
				<span>确认密码</span>
				<el-input type="password" v-model="confirmPassword" placeholder="请确认密码" autocomplete="off"></el-input>
			</el-form-item>
			<el-form-item label="注册成为">
				<el-radio-group v-model="userType">
					<el-radio label="user">用户</el-radio>
					<el-radio label="admin">管理员</el-radio>
				</el-radio-group>
			</el-form-item>
			<el-form-item>
				<el-button type="primary" style="width:100%;" @click="doSubmit()">提交</el-button>
			</el-form-item>
		</el-form>
	</div>
</template>


 

 
<style scoped>

	.login-container {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    border-radius: 10px;
    width: 350px;
    padding: 30px 35px 15px 35px;
    background: #ffffff;
    border: 1px solid #eaeaea;
    text-align: left;
    box-shadow: 0 0 20px 2px rgba(0, 0, 0, 0.1);
}

	.title {
		margin: 0px auto 40px auto;
		text-align: center;
		color: #505458;
	}
</style>
          