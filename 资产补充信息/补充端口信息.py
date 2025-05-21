from ADInfoProcess import AddSingleItem,GetCSV
import openpyxl as xl
import csv

def CollectCSVData(name):
    with open(name) as f:
        reader = csv.reader(f)
        data = []
        for row in reader:
            data.append(row)

    data = data[1:]
    return data



def GetPortScanResult(portFileName):
    # ip_column = []
    # port_column = []
    # protocol_column = []
    # state_column = []
    dict_state = {}
    with open(portFileName) as f:
        reader = csv.reader(f)
        data = []

        for row in reader:
            data.append(row)

    # for row in data:
    #     # ip_column.append(row[0])
    #     # port_column.append(row[1])
    #     # protocol_column.append(row[2])
    #     # state_column.append(row[3])
    #     keys = row[0] + ':' + row[1]
    #     dict_state[keys] = row[3]

    for i in range(len(data)):
        keys = data[i][0] + ':' + data[i][1]
        dict_state[keys] = data[i][3]
        n = len(data[i])
        for j in range(7-n):
            data[i].append('')
        #print(data[i])

    return data,dict_state

def SaveAsCSV(name,data_all):
    csvFile = open(name, "w+", newline='')
    colname = ['IP', '端口', '协议','开放状态', '域名', '内网ip', '内网端口', '内网域名', '标识', '公司名', '服务器', 'URL','响应码',
               '标题', '国家', '地区', '城市',
               'FOFA识别产品', 'FOFA识别产品版本', 'FOFA最后更新日期', 'Quake识别产品', 'Quake识别产品版本',
               'Quake最后更新日期', 'ISP', '责任人']
    try:
        writer = csv.writer(csvFile)

        writer.writerow(colname)

        for i in range(len(data_all)):
            writer.writerow(data_all[i])
    finally:
        csvFile.close()




###################################开始补充端口信息###################################################

collectdata = CollectCSVData('补充AD信息0923.csv')




port_data,port_dict = GetPortScanResult('../端口检测/端口验证加责任人0923.csv')

port_dict_used = {}
port_dict_index = {}


for i in range(len(port_data)):
    key = port_data[i][0] + ':' + port_data[i][1]
    port_dict_used[key] = False
    port_dict_index[key] = i


#对于已存在的端口 在字典used中修改标识为true 提取端口状态信息插入至总表资产信息对应行中
for i in range(len(collectdata)):
    key = collectdata[i][0] + ':' + str(collectdata[i][1])
    port_dict_used[key] = True

    collectdata[i].insert(3,port_dict[key] if key in port_dict.keys() else '')

#对于不存在的端口资产信息（即used字典标识为False的）  补充至总表最后
unused_index_list = []#收集1`
for key in port_dict_used.keys():
    if port_dict_used[key] == False:
        unused_index_list.append(port_dict_index[key])


unused_index_list = unused_index_list[1:]#去掉标题栏
for i in unused_index_list:
    temp = [port_data[i][0], port_data[i][1], port_data[i][2], port_data[i][3],'', port_data[i][4], port_data[i][5], '', '', '',
            '', '','', '', '', '', '', '', '', '', '', '', '', '', port_data[i][6]]
    collectdata.append(temp)
    #print(temp)

SaveAsCSV("补充端口信息0923.csv",collectdata)