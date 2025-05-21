import json
import os
import csv
import datetime

fofa_fmt = "%Y-%m-%d %H:%M:%S"
today = datetime.date.today()
today_dt = datetime.datetime.today()
Expeirdtime = today - datetime.timedelta(days=365)
Expeirdtime = Expeirdtime.strftime("%Y-%m-%d %H:%M:%S")
Expeirdtime = datetime.datetime.strptime(Expeirdtime,"%Y-%m-%d %H:%M:%S")


danger_ports = [21,22,23,135,137,138,139,445,1433,1521,3306,3389,6620,6379,27017]

def GetCollectFile():
    dirname = "高危端口响应数据/2024-11-12"
    files = os.listdir(dirname)
    data = []

    for file in files:
        print(file)
        filename = dirname + "/" + file
        f = open(filename, 'r', encoding='utf-8')
        content = f.read()

        response = json.loads(content)

        results = response["results"]
        for host in results:
            updatetime = datetime.datetime.strptime(host[-1], fofa_fmt)
            if updatetime > Expeirdtime:
                data.append(host)
    return data




def DangerPortSaveAsCVS(filename,data_all):
    csvFile = open(filename, "w+", newline='')
    colname = ['IP', '端口', '协议','URL','OS','service','update']
    try:
        writer = csv.writer(csvFile)
        writer.writerow(colname)
        # data为list类型
        # data为list类型
        for i in range(len(data_all)):
            writer.writerow(data_all[i])

    finally:
        csvFile.close()

a = GetCollectFile()
DangerPortSaveAsCVS('端口信息1031.csv',a)