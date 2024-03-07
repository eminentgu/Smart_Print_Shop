
<script>
  import axios from 'axios'

  export default {
    name: 'Login',
    data(){
      return {
       username:'',
       password:''
      }
    },
    methods:{
      gotoRegister(){
        this.$router.push({ name: 'register' });
      },
      doSubmit(){
        let  url='/api/login/';
        let  params={
          username:this.username,
          password:this.password
        }

        axios.post(url,params).then(r=>{
          if(r.data.status == 'ok'){
            if(r.data.userType == 'admin'){
              this.$message({
                message: '登录成功！',
                type: 'success',
                showClose: true
              });
              this.$router.push({ name: 'homepage_admin',query:{username: this.username}});
            }
            else{
              this.$message({
                message: '登录成功！',
                type: 'success',
                showClose: true
              });
              this.$router.push({ name: 'homepage_user', query: {username: this.username}});
            }
              
          }
          else {
            this.$message.error("用户名/密码错误！");
          }
        }).catch(e=>{})

      }
    }
  }
</script>
 


<template>
	<div class="login">
		<el-form class="login-container">
			<h1 class="title">智慧打印店</h1>
			<el-form-item label="">
        <span>账号</span>
				<el-input type="text" v-model="username" placeholder="键入用户名" autocomplete="off"></el-input>
			</el-form-item>
			<el-form-item label="">
        <span>密码</span>
				<el-input type="password" v-model="password" placeholder="键入密码" autocomplete="off"></el-input>
			</el-form-item>
			<el-form-item>
				<el-button type="primary" style="width:100%;" @click="doSubmit()">提交</el-button>
			</el-form-item>
			<el-row style="text-align: center;margin-top:-10px">
				<el-link type="primary" @click="gotoRegister()">用户注册</el-link>
			</el-row>
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
          