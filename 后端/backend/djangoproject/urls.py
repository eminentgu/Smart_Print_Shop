"""
URL configuration for djangoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myApp.views import *

urlpatterns = [
    # Django后台
    path("admin/", admin.site.urls),
    # 用户/管理员注册
    path("api/register/", Register),
    # 用户/管理员登录
    path("api/login/", Login),
    # 用户提交打印任务
    path("api/submitPrint/", SubmitTasks),
    # 用户查看订单详情
    path("api/printDetail/", UserViewDetail),
    # 用户查看历史订单列表
    path("api/historyPrint/", UserViewTask),
    # 获取当前打印耗材情况和当日收支情况
    path("api/getDrawData/", ViewPrinterExpense),
    # 获取当日盈利额
    path("api/profits/", CalProfits),
    # 获取打印机当前状态
    path("api/printer/", PrinterStatus),
    # 管理员查看待处理订单详情
    path("api/printTask/", AdminViewDetail),
    # 管理员处理订单
    path("api/finishTask/", ProcessTask),
    # 管理员查看待处理订单列表
    path("api/printlist/", AdminViewTask),
    # 模拟打印件配送
    path("api/assignDeliver/", CallDelievery),
    # 接收用户上传的文件并暂存
    path("api/upload/", UploadFiles),
    # 筛选指定订单的文件列表
    path("api/fileList/", DownloadFiles),
    # 清除文件暂存区
    path("api/informBack/", ClearBuffer),
]