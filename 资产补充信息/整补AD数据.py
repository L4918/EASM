from ADInfoProcess import AddSingleItem,GetCSV
import openpyxl as xl
import csv

def CollectCSVData(name):

    with open(name)as f:
        reader = csv.reader(f)
        data = []
        for row in reader:
            data.append(row)
    return data

def CollectExcelData(name):
    workbook = xl.load_workbook(name, data_only=True)
    sheet = workbook['Sheet1']
    data = []
    for row in sheet.iter_rows():
        temp = []
        for i in row:
            temp.append(i.value)
        data.append(temp)

    # iplist = iplist[1:]
    return data

def SaveAsCSV(name,data_all):
    csvFile = open(name, "w+", newline='')
    # colname = ['IP', '端口', '协议','开放状态', '域名', '内网ip', '内网端口', '内网域名', '标识', '公司名', '服务器', 'URL','响应码',
    #            '标题', '国家', '地区', '城市',
    #            'FOFA识别产品', 'FOFA识别产品版本', 'FOFA最后更新日期', 'Quake识别产品', 'Quake识别产品版本',
    #            'Quake最后更新日期', 'ISP', '责任人']
    try:
        writer = csv.writer(csvFile)
        # writer.writerow(colname)

        for i in range(len(data_all)):
            writer.writerow(data_all[i])
    finally:
        csvFile.close()


# adcsvdata = CollectCSVData('../对外发布.csv')
# adcsvdata = adcsvdata[1:]
adexceldata = CollectExcelData('../AD信息0226.xlsx')
adexceldata = adexceldata[1:]


addata = []
collectdata = []

#addata存储AD表里的信息
for item in adexceldata:
    AddSingleItem(item,addata)

collectdata = CollectCSVData('../资产整合0225.csv') #获取收集到的第一版资产

dictkey = {} #用来标识资产是否已经存在了
dictindex = {} #用来标识原始资产的序号


for i in range(len(addata)):
    key = addata[i][1] + ":" + str(addata[i][2])
    dictkey[key] = False
    dictindex[key] = i

for i in range(len(collectdata)):
    key = collectdata[i][0] + ":" + str(collectdata[i][1])
    if key in dictkey.keys():
        dictkey[key] = True

complement_list = []

for key in dictkey.keys():
    if dictkey[key]==False:
        complement_list.append(dictindex[key])





for index in complement_list:
    temp = [addata[index][1],addata[index][2],'','',addata[index][3],addata[index][4],'','Inovance','',
            '',addata[index][0],'中国','','','','','','','','','',addata[index][5]]
    #print(temp)
    collectdata.append(temp)




SaveAsCSV("补充AD信息0225.csv",collectdata)

