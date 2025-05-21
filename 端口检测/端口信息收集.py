import base64
import time
import csv
import requests
import json
import openpyxl as xl
import os
import datetime

#通过查询单独ip进行端口收集
def FofaCollectInfo(ip):
    email = r'XXXXXXXX'
    api_key = r'XXXXXXXXX'
    api = r'https://fofa.info/api/v1/search/all?email={}&key={}&qbase64={}&size={}&fields={}&full={}'
    fields = ("ip,port,protocol,host,os,server,lastupdatetime")
    arg_domain1 = "ip=\""
    arg_domain2 = ip
    arg_domain3 = "\""
    arg_domain = arg_domain1 + arg_domain2 + arg_domain3
    full = "false"
    flag = base64.b64encode(arg_domain.encode()).decode()
    size = "2000"

    complete_reuest = api.format(email, api_key, flag, size, fields, full)

    response = requests.get(complete_reuest)
    content = response.content

    date_str = str(datetime.date.today())
    new_dir_name = "高危端口响应数据/" + date_str
    if not os.path.exists(new_dir_name):
        os.makedirs(new_dir_name)
    filename = ip + ".txt"
    filepathname = new_dir_name + "/" + filename
    with open(filepathname, "wb") as file:
        file.write(content)
    return


def ExcelReadIp(xlsxname):


    workbook = xl.load_workbook(xlsxname,data_only=True)
    sheet = workbook['Sheet1']
    iplist = []
    for row in sheet.iter_rows():
        iplist.append(row[0].value)

    #iplist = iplist[1:]
    return iplist
def CSVReadIP(name):
    with open(name)as f:
        reader = csv.reader(f)
        data = []

        for row in reader:
            data.append(row)

        first_column = [row[0] for row in data]
        first_column = first_column[1:]
    return first_column

data = CSVReadIP('../资产补充信息/ip合集1031.csv')
j = 0
n = str(len(data))
for i in data:
    j = j+1
    FofaCollectInfo(i)
    print(i + '     ' + str(j)+'/' + n)