import csv
import time

import nmap
from ADInfoProcess import GetOut2InDict
def GetCSV(name):

    with open(name)as f:
        reader = csv.reader(f)
        data = []

        for row in reader:
            data.append(row)
    return data


def scan_once(host,port):
    nm = nmap.PortScanner()
    nm.scan(host,port)
    data_single = []
    if nm.has_host(host):
        for proto in nm[host].all_protocols():  # nm[host].all_protocols获取执行的协议['tcp','udp']
            lport = nm[host][proto].keys()  # 获取目标主机所开放的端口赋值给lport
            for port in lport:
                data_single.append(host)
                data_single.append(port)
                data_single.append(nm[host][proto][port]['name'])
                data_single.append(nm[host][proto][port]['state'])

    return data_single

def OrgnizeData(scandata,dict_innerip,dict_innerport,dict_innerresponse):
    num = len(scandata)
    keys = dict_innerip.keys()
    for i in range(num):
        if len(scandata[i])<1:
            continue
        outIDkey = scandata[i][0] + ':' + str(scandata[i][1])

        if outIDkey in keys:
            innerip = dict_innerip[outIDkey]
            innerport = dict_innerport[outIDkey]
            scandata[i].append(innerip)
            scandata[i].append(innerport)
            if len(dict_innerip[outIDkey])==1:
                if dict_innerip[outIDkey][0] in dict_innerresponse.keys():
                    scandata[i].append(dict_innerresponse[dict_innerip[outIDkey][0]])
                else:
                    scandata[i].append('')
            else:
                respersontemp = []
                for ip in dict_innerip[outIDkey]:
                    if ip in dict_innerresponse.keys():
                        respersontemp.append(dict_innerresponse[ip])
                scandata[i].append(respersontemp)
    return

def SaveAsCVS(filename,data_all):
    csvFile = open(filename, "w+", newline='')
    colname = ['IP', '端口', '协议','状态']
    try:
        writer = csv.writer(csvFile)
        writer.writerow(colname)
        # data为list类型
        # data为list类型
        for i in range(len(data_all)):
            if len(data_all[i])>1:
                writer.writerow(data_all[i])
    finally:
        csvFile.close()



data = GetCSV('端口信息1031.csv')


data = data[1:]


hosts = []
ports = []

for i in data:
    # if i[1]=='80'or i[1]=='443':
    #     continue
    hosts.append(i[0])
    ports.append(i[1])

verify_state = []


num = len(ports)
for i in range(num):
    #print(hosts[i] + ':' + ports[i])
    verify_state.append(scan_once(hosts[i],ports[i]))
    time.sleep(3)
    print(str(i+1) + '/' + str(num))

SaveAsCVS("端口验证结果1031.csv",verify_state)


dict_innerip,dict_innerport,_,dict_innerresp = GetOut2InDict()


OrgnizeData(verify_state,dict_innerip,dict_innerport,dict_innerresp)


SaveAsCVS("端口验证加责任人1031.csv",verify_state)

