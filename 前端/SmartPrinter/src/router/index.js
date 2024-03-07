//import Vue from 'vue'
//import VueRouter from 'vue-router'

import Homepage_admin from '@/views/homepage_admin' //主页*/ 
import Homepage_user from '@/views/homepage_user' //主页*/
import Login from "@/views/login" //登陆
import Register from "@/views/register"; //注册
import showPrice from "@/views/showPrice" //登陆
import createPrint from "@/views/createPrint" //登陆
import historyPrint from "@/views/historyPrint" //登陆
import taskDetails from "@/views/taskDetails" //登陆
import adminPrint from "@/views/adminPrint" //登陆

//Vue.use(VueRouter)
import {createRouter, createWebHistory} from 'vue-router'
 
const routerHistory = createWebHistory()
 


const routes = [{
        path: '/',
        name: 'login',
        component: Login
    },
    
    {
        path: '/register',
        name: 'register',
        component: Register
    },

     {
        path: '/homepage_admin',
        name: 'homepage_admin',
        component: Homepage_admin
    },
    {
        path: '/homepage_user',
        name: 'homepage_user',
        component: Homepage_user
    },
    {
        path: '/showPrice',
        name: 'showPrice',
        component: showPrice
    },
    {
        path:'/createPrint',
        name:'createPrint',
        component:createPrint
    },
    {
        path:'/historyPrint',
        name:'historyPrint',
        component:historyPrint        
    },
    {
        path:'/taskDetails',
        name:'taskDetails',
        component:taskDetails
    },
    {
        path: '/adminPrint',
        name: 'adminPrint',
        component: adminPrint
    }
]


const router = createRouter({
    history: routerHistory,
    base: process.env.BASE_URL,
    routes
     /*
      *   在这里和vue2一样写路由配置
     */
})
/*

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

*/

export default router
