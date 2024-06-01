# 智慧打印店 

# 相关课程
* 张红兵教授 信息系统开发方法与工具
* 李慧 管理信息系统
* 软件工程


----
## 代码部分运行指南


#### [在线演示（已被关闭）](https://eminentgu.top/)

#### 更新：2024.6.1 因为实习投递简历需要，域名eminentgu.top被我挪作个人域名，如需检查/使用demo请联系[顾翔（921127940122）](https://eminentgu.top)重新部署

#### 前端负责，更多问题联系：
[沈贝宁（921127940137）](https://github.com/BeningShum)
[顾翔（921127940122）](https://eminentgu.github.io/)


#### 后端负责，更多问题联系：
张瀚宸（921127940156）

---

#### 前端使用Vue，需要安装node
#### 后端使用python 建议安装conda
### 请注意！！！在前端代码中，api请求指向的是服务器地址（eminentgu.top），而不是本地地址，如果想要在本地运行后端程序，请记得修改前端中的axios指向地址
---
## 前端初始化
```
npm install
```

### 本地运行（api调用的是服务器的，也可以使用mocker模拟）
```
npm run serve
```

### 打包
```
npm run build
```
### 其他
* 使用mocker模拟后端
```
mocker ./mocker/index.js
```
### api 标准
* port ： 3721
* 具体使用到的api请求及内容请查看文件：'/mocker/index.js'

---
## 后端初始化
```
pip install django
```
### 本地运行
```
python manage.py startapp myapp
```

