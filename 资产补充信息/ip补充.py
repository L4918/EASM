import ipaddress
import csv
import openpyxl as xl
# 定义 CIDR 表示的 IP 段


def ReadFromExcel(name):
    workbook = xl.load_workbook(name, data_only=True)
    sheet = workbook['Sheet1']
    iplist = []
    for row in sheet.iter_rows():
        iplist.append(row[0].value)

    iplist = iplist[1:]
    return iplist
def ReadFromCSV(name):
    with open(name)as f:
        reader = csv.reader(f)
        data = []

        for row in reader:
            data.append(row)

        first_column = [row[0] for row in data]
        first_column = first_column[1:]
    return first_column

def SaveAsCVS(filename,data_all):
    csvFile = open(filename, "w+", newline='')
    try:
        writer = csv.writer(csvFile)
        # data为list类型
        # data为list类型
        for ip in data_all:
            writer.writerow([ip])
    finally:
        csvFile.close()


ip_collect = ReadFromCSV('补充AD信息0225.csv')


#ip_addition = ReadFromCSV('ip对应基地.csv')
ip_addition = ReadFromExcel('ip对应基地信息最终.xlsx')


ip_all = ip_addition + ip_collect

# for ip in ip_all:
#     print(type(ip))
# a = []
# IPNetmask('218.64.151.1/23',a)
# print(len(a))
# print(a)
ip_all = list(set(ip_all))
print(len(ip_all))
SaveAsCVS("ip合集0225.csv",ip_all)

