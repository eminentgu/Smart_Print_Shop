# 注册成功后应重定向到登录页面，登录成功后应重定向到下一页面
from django.shortcuts import render, redirect
from django.db import transaction
from django.db.models import Q, Sum
import uuid
import random
import ast
import time
import pandas as pd
import os
import shutil
from myApp.models import *
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie

# Create your views here.
def Register(request):
    if request.method == 'POST':
        dict_ = eval(request.body)
        username = dict_['username']
        password = dict_['password']
        confirmPassword = dict_['confirmPassword']
        userType = dict_['userType']
        userID = str(uuid.uuid3(uuid.NAMESPACE_DNS, username))[:8]

        if password == '' or confirmPassword == '' or ' ' in username:
            return JsonResponse({'status': 'failed'})
        if confirmPassword != password or userType == 'admin':
            return JsonResponse({'status': 'failed'})
        try:
            isexist1 = UserInfo.objects.get(username=username)
            return JsonResponse({'status': 'failed'})
        except UserInfo.DoesNotExist:
            try:
                isexist2 = AdminInfo.objects.get(adminname=username)
                return JsonResponse({'status': 'failed'})
            except AdminInfo.DoesNotExist:
                user = UserInfo(userID=userID, username=username, password=password)
                user.save()
    
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'failed'})

def Login(request):
    if request.method == 'POST':
        dict_ = eval(request.body)
        username = dict_['username']
        password = dict_['password']
    
        try:
            user = UserInfo.objects.get(username=username)
        except UserInfo.DoesNotExist:
            try:
                admin = AdminInfo.objects.get(adminname=username)
                if password == admin.password:
                    return JsonResponse({'status': 'ok'})
                else:
                    return JsonResponse({'status': 'failed'})
            except AdminInfo.DoesNotExist:
                return JsonResponse({'status': 'failed'})
    
        if user.password != password:
            return JsonResponse({'status': 'failed'})
    
        return JsonResponse({'status': 'ok'})
    else:
        pass

def CalProfits(request):
    if request.method == 'GET':
        queryset = Transactions.objects.filter(transName='打印收入').values('money')
        if queryset.exists():
            df = pd.DataFrame(list(queryset))
            income = df['money'].sum()
        else:
            income = 0

        queryset = Transactions.objects.exclude(transName='打印收入').values('money')
        if queryset.exists():
            df = pd.DataFrame(list(queryset))
            expense = df['money'].sum()
        else:
            expense = 0
        
        return JsonResponse({'status': 'ok', 'profits': round(income - expense, 2)})
    else:
        pass

def ViewPrinterExpense(request):
    if request.method == 'GET':
        printers = list(Printers.objects.all().values('printerName', 'paperVol', 'inkVol'))
        printerNames = []
        paperVols = []
        inkVols = []
        for printer in printers:
            printerNames.append(printer['printerName'])
            paperVols.append(printer['paperVol'])
            inkVols.append(printer['inkVol'])
            
        transc = pd.DataFrame(list(Transactions.objects.all().values('transName', 'money')))
        transc = transc.groupby('transName').agg({'transName': 'first', 'money': 'sum'})
        items = [row.transName for row in transc.itertuples()]
        expense = [{"name": row.transName, "value": round(row.money, 2)} for row in transc.itertuples()]
        
        data = {'printer':{'printerNames': printerNames, 'paperVols': paperVols, 'inkVols': inkVols}, 
                'condition': {'ItemNames': items, 'Itemexpense': expense}}
        
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        pass

def PrinterStatus(request):
    if request.method == "GET":
        statuses = pd.DataFrame(list(Printers.objects.all().values('printerStatus')))['printerStatus']
        status_state = statuses.value_counts()
        bad = status_state.get('故障', 0)
        good = statuses.size - bad
        return JsonResponse({'status': 'ok', 'good': good, 'bad': bad})
    else:
        pass

def SubmitTasks(request):
    if request.method == 'POST':
        dict_ = eval(request.body)
        userID = dict_['username']
        tasksData = dict_['dataStorage']
        appointDate = dict_['appointDate']
        appointTime = dict_['appointTime']

        with transaction.atomic():
            taskID = ''.join(random.choice('0123456789') for _ in range(15))
            pickCode = random.randint(100000, 999999)               # 随机生成6位取件码
            reservedTime = appointDate + ' ' + appointTime
            
            BASE_DIR = '/root/webapp/dist/fileList'
            tmpDir = '/root/fileBuffer'
            if not os.path.exists(BASE_DIR):
                os.makedirs(BASE_DIR)
            files = os.listdir(tmpDir)
            for file in files:
                source = os.path.join(tmpDir, file)
                target_dir = os.path.join(BASE_DIR, str(taskID))
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                if os.path.isfile(source):
                    shutil.move(source, os.path.join(target_dir, file))
            
            for file in tasksData:
                # file = ast.literal_eval(file)
                fileName = file['fileName']
                paper = file['paper']
                color = file['color']
                doubleSided = file['doubleSided']
                note = file['note']
                cost = file['price']
                fileID = str(uuid.uuid4())[:10]
                
                if doubleSided == '1':
                    isdoubleSided = '双面'
                else:
                    isdoubleSided = '单面'
                
                task = Tasks(fileID=fileID, taskID=taskID, userID=userID, fileName=fileName, taskStatus='待打印', pickCode=pickCode,
                             paper=paper, color=color, doubleSided=isdoubleSided, note=note, money=cost, 
                             reservedTime=reservedTime)
                task.save()

        return JsonResponse({'status': 'ok', 'taskID': taskID}, json_dumps_params={'ensure_ascii': False})
    else:
        pass
    
def ProcessTask(request):
    if request.method == 'POST':
        dict_ = eval(request.body)
        taskID = dict_['taskID']
        tasks = Tasks.objects.filter(taskID=taskID)
        tasks.update(taskStatus='待配送')
        cost = tasks.aggregate(total_money=Sum('money'))['total_money']
        if cost is None:
            cost = 0
        
        transactName = '打印收入'
        transactionID = str(uuid.uuid4())[:8].upper()
        transc = Transactions(transactionID=transactionID, transName=transactName, money=cost)
        transc.save()
        
        return JsonResponse({'status': 'ok'})
    else:
        pass

def UserViewTask(request):
    if request.method == 'POST':
        dict_ = eval(request.body)
        userID = dict_['username']
        
        tasks = pd.DataFrame(list(Tasks.objects.filter(userID=userID).values('taskID', 'money', 'taskStatus', 'submitTime', 'pickCode', 'fileName',
                                                                             'reservedTime')))
        
        try:
            tasks = tasks.groupby('taskID').agg({'taskID': 'first', 'money': 'sum', 'taskStatus': 'first', 'submitTime': 'first', 'reservedTime':'first',
                                                'pickCode': 'first', 'fileName': lambda x: '，'.join(x)})
        except:
            response = {'status': 'ok', 'data': 'null'}
            return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})
        
        tasks.rename(columns={'fileName': 'fileNames'}, inplace=True)
        tasks.sort_values(by='submitTime', ascending=False, inplace=True)
        
        taskData = []
        for _, row in tasks.iterrows():
            dict_ = {
                'taskID': row['taskID'],
                'description': {
                    '创建时间': row['submitTime'].strftime('%Y-%m-%d %H:%M:%S'),
                    '预约送达时间': row['reservedTime'],
                    '取件码': row['pickCode'],
                    '订单金额': str(round(row['money'], 2))+' 元',
                    '打印文件': row['fileNames'],
                    '状态': row['taskStatus']
                }
            }
            taskData.append(dict_)
        
        response = {'status': 'ok', 'data': taskData}
        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        pass

def UserViewDetail(request):
    if request.method == 'POST':
        dict_ = eval(request.body)
        taskID = dict_['taskID']
        userID = dict_['username']
        task = list(Tasks.objects.filter(taskID=taskID, userID=userID).values('fileName', 'paper', 'color', 'doubleSided', 'note'))
        
        detailData = []
        for file in task:
            dict_ = {
                'fileName': file['fileName'],
                'description': {
                    'paper': file['paper'],
                    'color': file['color'],
                    'double': file['doubleSided'],
                    'note': file['note']
                }
            }
            detailData.append(dict_)
        
        response = {'status': 'ok', 'detailData': detailData}
        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        pass

def AdminViewDetail(request):
    if request.method == 'POST':
        dict_ = eval(request.body)
        taskID = dict_['taskID']
        task = list(Tasks.objects.filter(taskID=taskID).values('fileName', 'paper', 'color', 'doubleSided', 'note'))
        
        detailData = []
        for file in task:
            dict_ = {
                'fileName': file['fileName'],
                'description': {
                    'paper': file['paper'],
                    'color': file['color'],
                    'double': file['doubleSided'],
                    'note': file['note']
                }
            }
            detailData.append(dict_)
        
        response = {'status': 'ok', 'detailData': detailData}
        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        pass

def AdminViewTask(request):
    if request.method == "GET":
        tasks = pd.DataFrame(list(Tasks.objects.filter(Q(taskStatus='待打印') | Q(taskStatus='待配送')).values('taskID', 'reservedTime', 
                                                                                                              'pickCode', 'taskStatus')))
        tasks = tasks.groupby('taskID').agg({'taskID': 'first', 'reservedTime': 'first', 'pickCode': 'first', 'taskStatus': 'first'})
        tasks.sort_values(by=['taskStatus', 'reservedTime'], inplace=True, ascending=[False, True])
        
        taskData = []
        for _, row in tasks.iterrows():
            dict_ = {
                'taskID': row['taskID'],
                'appointTime': row['reservedTime'],
                'pickCode': row['pickCode'],
                'condition': row['taskStatus']
                }
            taskData.append(dict_)
        
        response = {'status': 'ok', 'data': taskData}
        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        pass

def CallDelievery(request):
    if request.method == 'POST':
        # time.sleep(5)
        dict_ = eval(request.body)
        taskID = dict_['taskID']
        tasks = Tasks.objects.filter(taskID=taskID)
        tasks.update(taskStatus='已完成')
        
        return JsonResponse({'status': 'ok'})
    else:
        pass

def UploadFiles(request):
    BASE_DIR = '/root/fileBuffer'
    if request.method == 'POST':
        file = request.FILES.get('file', None)
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)
        file_path = BASE_DIR + "/{}".format(file.name)
        file_path = file_path.replace(" ", "")
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        return JsonResponse({'status': 'ok'}, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        pass

def DownloadFiles(request):
    if request.method == 'POST':
        dict_ = eval(request.body)
        taskID = dict_['taskID']
        BASE_DIR = '/root/webapp/dist/fileList'
        
        try:
            files = os.listdir(os.path.join(BASE_DIR, str(taskID)))
        except:
            return JsonResponse({'status': 'failed'})
        
        return JsonResponse({'status': 'ok', 'fileNames': files}, json_dumps_params={'ensure_ascii': False})
    else:
        pass

def ClearBuffer(request):
    if request.method == "POST":
        BASE_DIR = '/root/fileBuffer'
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)
        
        for filename in os.listdir(BASE_DIR):
            file_path = os.path.join(BASE_DIR, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except:
                return JsonResponse({'status': 'failed'})
        
        return JsonResponse({'status': 'ok'})
    else:
        pass
