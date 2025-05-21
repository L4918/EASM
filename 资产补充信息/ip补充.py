import ipaddress
import csv
import openpyxl as xl
# 定义 CIDR 表示的 IP 段

#注释掉的是2023的那个各基地资产表的
# iplist = ['222.92.231.35/28','153.35.131.146/28','112.25.144.66/28','120.234.48.186/29','58.60.228.146/29',
#           '123.138.71.52/28','222.90.78.202/29','218.64.15.1/23','223.68.160.90/29','112.82.161.26/29',
#           '93.43.56.129/29']
#
# iplist2 = ['122.193.105.162-164','58.250.90.15-16','180.167.38.146-150','58.40.124.58-62','221.6.23.18-22',
#            '122.192.9.106-107','222.242.225.195-202','183.214.98.9-23','222.92.50.90-93']
#
# iplist3 = ['101.95.143.202','36.22.179.166','36.22.181.118','125.35.105.42','218.13.170.2','123.151.192.42',
#            '111.26.59.82','183.136.194.42','58.215.242.130','218.2.156.236','112.4.69.138','119.206.202.224']

#这个是最新的
# iplist = ['202.105.145.73/29','58.60.228.144/29','222.90.78.202/29','123.138.71.52/28',
#            '120.86.122.144/28','120.236.79.225/28','223.68.160.88/29','112.82.161.24/29',
#            '112.25.144.65/28','222.92.231.33/28','153.35.131.145/28','58.210.94.161/29',
#            '112.4.70.9/29','58.211.124.41/29','122.193.105.161/27','120.234.48.184/29','120.234.48.208/29',
#            '101.95.143.202/30','180.167.38.144/29','58.40.124.56/29','36.22.179.166/30','36.22.179.118/30',
#            '123.151.192.42/30','219.150.34.72/29','218.13.170.2/30','121.9.15.178/30','61.145.73.77/30',
#           '213.163.40.0/29','81.93.198.192/29','93.43.56.129/29']
#
# iplist2 = ['222.242.225.195-202','58.250.90.114-118','183.214.98.9-23','221.6.23.18-22','122.192.9.106-107',
#            '222.92.50.90-93']
#
# iplist3 = ['61.146.53.76','58.250.90.15','58.250.90.16','125.35.105.42','111.26.59.82','183.136.194.42',
#            '58.215.242.130','218.2.156.236','112.4.69.138','119.206.202.224']
# def IPNetmask(cidr,data):
#     network = ipaddress.ip_network(cidr, strict=False)
#     # 生成 IP 地址列表
#     ip_list = [str(ip) for ip in network.hosts()]
#     #print(len(ip_list))
#     # 打印 IP 地址列表
#     for ip in ip_list:
#         data.append(ip)
#
#
# def IPrange(ip_range,data):
#     start_ip_str, end_ip_suffix = ip_range.split('-')
#     start_ip_parts = start_ip_str.rsplit('.', 1)
#     start_ip_base = start_ip_parts[0]
#     start_ip = ipaddress.ip_address(start_ip_str)
#     end_ip = ipaddress.ip_address(start_ip_base + '.' + end_ip_suffix)
#
#     # 生成 IP 地址列表
#     ip_list = [str(ipaddress.ip_address(ip)) for ip in range(int(start_ip), int(end_ip) + 1)]
#
#     # 打印 IP 地址列表
#     for ip in ip_list:
#         data.append(ip)

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

