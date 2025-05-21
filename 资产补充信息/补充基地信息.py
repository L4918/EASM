import csv


def ReadFromCSV(name):
    with open(name)as f:
        reader = csv.reader(f)
        data = []

        for row in reader:
            data.append(row)
    data = data[1:]
    return data

def SaveAsCSV(name,data_all):
    csvFile = open(name, "w+", newline='')
    colname = ['IP', '端口', '协议','开放状态', '域名', '内网ip', '内网端口', '内网域名', '标识', '公司名', '服务器', 'URL','响应码',
               '标题', '国家', '地区', '城市',
               'FOFA识别产品', 'FOFA识别产品版本', 'FOFA最后更新日期', 'Quake识别产品', 'Quake识别产品版本',
               'Quake最后更新日期', 'ISP', '责任人','对应基地']
    try:
        writer = csv.writer(csvFile)

        writer.writerow(colname)

        for i in range(len(data_all)):
            writer.writerow(data_all[i])
    finally:
        csvFile.close()



collect_data = ReadFromCSV('补充端口信息0923.csv')

base_data = ReadFromCSV('ip对应基地.csv')

base_dict = {}
used_dict = {}
for item in base_data:
    base_dict[item[0]] = item[1]
    used_dict[item[0]] = False
for i in range(len(collect_data)):
    if collect_data[i][0] in base_dict.keys():
        collect_data[i].append(base_dict[collect_data[i][0]])
        used_dict[i] = True
    else:
        collect_data[i].append('')

###############补充之前没收集到的
ip_list = list(used_dict.keys())

for i in range(len(ip_list)):
    if not used_dict[ip_list[i]]:
        temp = [ip_list[i],'', '', '', '', '',
                '', '', '', '',
                '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',base_dict[ip_list[i]]]
        collect_data.append(temp)

SaveAsCSV('最后补充对应基地0923-2.csv',collect_data)

