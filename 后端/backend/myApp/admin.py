from django.contrib import admin
from myApp.models import *

# Register your models here.
class TransManager(admin.ModelAdmin):
    list_display = ['transactionID', 'transName','money','submitTime']
    list_filter = ('transName',)
    ordering = ('-submitTime',)

class PrintersManager(admin.ModelAdmin):
    list_display = ['printerID', 'printerName','paperVol', 'inkVol', 'printerStatus']
    list_filter = ('printerStatus',)
    list_editable = ('paperVol', 'inkVol', 'printerStatus', )

admin.site.site_header = "智慧打印后台管理系统"
admin.site.site_title = "智慧打印后台管理系统"
admin.site.register(Transactions, TransManager)
admin.site.register(Printers, PrintersManager)
