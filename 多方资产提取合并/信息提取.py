import csv

import openpyxl as xl


def ReadDataFromCSV(filename):
    with open(filename)as f:
        reader = csv.reader(f)
        data = []
        for row in reader:
            data.append(row)
    return data


def ReadDataFromExcel(xlsxname):
    workbook = xl.load_workbook(xlsxname, data_only=True)
    sheet = workbook['Sheet1']
    data = []
    for row in sheet.iter_rows():
        temp = []
        for i in row:
            temp.append(i.value)
        data.append(temp)
    return data


def SaveAsCVS(filename,data_all):
    csvFile = open(filename, "w+", newline='')
    #colname = ['IP', '端口', '协议','URL','OS','service','update']
    try:
        writer = csv.writer(csvFile)
        #writer.writerow(colname)
        # data为list类型
        # data为list类型
        for i in range(len(data_all)):
            writer.writerow(data_all[i])

    finally:
        csvFile.close()



#####################################################################
#从青藤云数据获取内网ip对应的应用版本信息

HostSecData = ReadDataFromExcel('主机应用软件信息0226.xlsx')

HostSecData = HostSecData[1:]

HostSecDict_softv = {}
HostSecDict_sysname = {}
for host in HostSecData:
    software_version = host[4] + ':' + str(host[5])
    if host[0] not in HostSecDict_softv.keys():
        HostSecDict_softv[host[0]] = [software_version]
        HostSecDict_sysname[host[0]] = host[2]
    else:
        HostSecDict_softv[host[0]].append(software_version)
HostSecIP = HostSecDict_sysname.keys()
#####################################################################
#从goby中获取外网ip:端口对应的
GobyDict_ip2softv = {}
GobyDict_iport2softv = {}
GobyDict_iport2server = {}
GobyDict_iportUsed = {}
GobyData = ReadDataFromExcel('20250226资产-asset.xlsx')
GobyData = GobyData[1:]
for host in GobyData:
    softinfo = []
    for i in [5,6,7,8,9]:
        if host[i] != '-':
            softinfo.append(host[i])

    if host[1] == '-':
        GobyDict_ip2softv[host[0]] = softinfo
        continue
    ip_port = host[0] + ':' + host[1]
    if ip_port not in GobyDict_iport2softv.keys():
        GobyDict_iport2softv[ip_port] = softinfo
        GobyDict_iport2server[ip_port] = host[2]
        GobyDict_iportUsed[ip_port] = False

Gobyiport = GobyDict_iport2softv.keys()
#####################################################################
#补充基地信息数据
BaseData = ReadDataFromExcel('IP对应基地信息最终.xlsx')
BaseData = BaseData[1:]
BaseDict = {}
BaseUsedDict = {}
for host in BaseData:
    BaseDict[host[0]] = host[1]
    BaseUsedDict[host[0]] = False

BaseIP = BaseDict.keys()
#####################################################################
#从FOFA收集的信息中提取需要的数据

FOFADATA_OUTIP_INDEX = 0
FOFADATA_OUTPORT_INDEX = 1
FOFADATA_PROTO_INDEX = 2
FOFADATA_DOMAIN_INDEX = 3
FOFADATA_INNERIP_INDEX = 4
FOFADATA_INNERPORT_INDEX = 5
FOFADATA_INNERDOMAIN_INDEX = 6
FOFADATA_SERVER_INDEX = 7
FOFADATA_URL_INDEX = 8
FOFADATA_RESPONESECODE_INDEX = 9
FOFADATA_TITLE_INDEX = 10
FOFADATA_FOFAPRODUCT_INDEX = 11
FOFADATA_FOFAPRODUCTVERSION_INDEX = 12
FOFADATA_QUAKEPRODUCT_INDEX = 13
FOFADATA_QUAKEPRODUCTVERSION_INDEX = 14

#Fofadata = ReadDataFromCSV('资产整合1031.csv')
Fofadata = ReadDataFromCSV('补充AD信息0225.csv')

#以FOFA收集到的数据为基底 补充GoBy和主机安全额外数据
for i in range(len(Fofadata)):
    #主机安全信息补充
    Inner_ip = Fofadata[i][FOFADATA_INNERIP_INDEX]
    Out_ip = Fofadata[i][FOFADATA_OUTIP_INDEX]
    Out_port = str(Fofadata[i][FOFADATA_OUTPORT_INDEX])
    Out_iport = Out_ip + ':' + Out_port

    # 主机安全信息补充
    if Inner_ip in HostSecIP:
        Fofadata[i].append(HostSecDict_sysname[Inner_ip])
        Fofadata[i].append(HostSecDict_softv[Inner_ip])
    else:
        Fofadata[i].append('None')
        Fofadata[i].append('None')
    # Goby信息补充
    if Out_iport in Gobyiport:
        Fofadata[i][FOFADATA_SERVER_INDEX] = Fofadata[i][FOFADATA_SERVER_INDEX] + '/' + GobyDict_iport2server[Out_iport]
        Fofadata[i].append(GobyDict_iport2softv[Out_iport])
        GobyDict_iportUsed[Out_iport] = True
    else:
        Fofadata[i].append('GobyNone')
    #基地信息补充
    if Out_ip in BaseIP:
        Fofadata[i].append(BaseDict[Out_ip])
    else:
        Fofadata[i].append('基地信息暂无')

#根据Goby存活数据补充基底FOFA
for hostport in GobyDict_iportUsed.keys():
    if not GobyDict_iportUsed[hostport]:
        ip,port = hostport.split(':')
        datatemp = [ip,port,GobyDict_iport2server[hostport],'','','','','','','','','','','','','','',GobyDict_iport2softv[hostport]]
        if ip in BaseUsedDict.keys():
            BaseUsedDict[ip] = True
        Fofadata.append(datatemp)

#根据整理的所有基地数据补充基底FOFA
for host in BaseUsedDict.keys():
    if not BaseUsedDict[host]:
        datatemp = [host,'','','','','','','','','','','','','','','','','',BaseDict[host]]
        Fofadata.append(datatemp)


SaveAsCVS('合并结果0226.csv',Fofadata)
