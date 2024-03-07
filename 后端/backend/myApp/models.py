from django.db import models

# Create your models here.
class UserInfo(models.Model):
    userID = models.CharField(max_length=64, primary_key=True)
    username = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=64)

class AdminInfo(models.Model):
    adminID = models.CharField(max_length=64, primary_key=True)
    adminname = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=64)

class WorkerInfo(models.Model):
    workerID = models.CharField(max_length=64, primary_key=True)
    workername = models.CharField(max_length=64, unique=True)
    position = models.CharField(max_length=64)
    contact = models.CharField(max_length=64)

class Printers(models.Model):
    printerID = models.CharField(max_length=64, primary_key=True, verbose_name="打印机ID")
    printerName = models.CharField(max_length=64, verbose_name="打印机名称")
    paperVol = models.IntegerField(verbose_name="剩余纸量（%）")
    inkVol = models.IntegerField(verbose_name="剩余墨量（%）")
    printerStatus = models.CharField(max_length=64, default='空闲', verbose_name="状态")
    
    class Meta:
         verbose_name = "打印机管理"
         verbose_name_plural = "打印机管理"

class Tasks(models.Model):
    fileID = models.CharField(max_length=64, primary_key=True)           # 为每个文件分配一个唯一的ID
    taskID = models.CharField(max_length=64)
    userID = models.CharField(max_length=64)
    fileName = models.CharField(max_length=64)
    submitTime = models.DateTimeField(auto_now_add=True)
    paper = models.CharField(max_length=64)
    color = models.CharField(max_length=64)
    note = models.CharField(max_length=128, null=True)
    doubleSided = models.CharField(max_length=64)
    money = models.FloatField(null=True)   
    taskStatus = models.CharField(max_length=64)
    reservedTime = models.CharField(max_length=64, default="2023-11-16 10:00")
    pickCode = models.CharField(max_length=64)

class Transactions(models.Model):
    transactionID = models.CharField(max_length=64, primary_key=True, verbose_name="项目ID")           # 为每个交易事务分配一个唯一的ID
    transName = models.CharField(max_length=64, verbose_name="收支项目")
    money = models.FloatField(verbose_name="金额")
    submitTime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
         verbose_name = "收支管理"
         verbose_name_plural = "收支管理"


