import datetime
import os
import base64
import requests
import openpyxl as xl
import json
from ADInfoProcess import *

# 老域名
# DomainList = ["inovance.com","inovance.xyz","inovance.cn","inovance-automotive.com","iotdataserver.cn",
#               "iotdataserver.net","dataserver.cn","szmctc.com","shbst.com","inovance-iv.cn","jskwt.com",
#               "esto.cn","zdkj-dl.cn","inovance.eu","inovance.ind.in","sbclinear.co.kr",
#               "eksys.cn","inomag.cn","sh-laien.com","mobst.cn","inova-automation.com"]

#2/25新域名统计
DomainList = ["inovance.com", "inovance.xyz", "dataserver.cn","inocube.net","powerautomation.cn", "powerautomation.com.cn","inovance.net", "inovance.mobi",
              "inovance.cn", "inovance-automotive.com", "szmctc.com", "shbst.com", "inovance-iv.cn", "jskwt.com", "asconast.com",
              "esto.cn", "weton-inc.com", "weton.net", "zdkj-dl.cn", "eksys.cn", "inomag.cn", "sh-laien.com", "mobst.cn",
              "inova-automation.com", "inovance.de", "inovance.ch", "inovance.hk", "inovance.it", "inovance.hu", "inovance.eu",
              "inovance.ind.in", "sbclinear.co.kr", "iotdataserver.net", "iotdataserver.cn", "inoecloud.com",
              "eksys.com", "inoplanet.com", "shbstcloud.com", "smart-driving.com.cn", "zkltvision.com"]


Fofasign = 1
Quakesign = 2



def GetDomainAdditionInfo():
    workbook = xl.load_workbook('域名附加信息.xlsx')
    sheet = workbook['Sheet1']
    dict_domain2depart = {}
    dict_domain2company = {}
    dict_domain2cname = {}
    for row in sheet.iter_rows():
        dict_domain2depart[row[0].value] = row[1].value
        dict_domain2company[row[0].value] = row[2].value
        dict_domain2cname[row[0].value] = row[4].value

    return dict_domain2depart,dict_domain2company


def MakeDir():
    date_str = str(datetime.date.today())
    new_dir_name = "响应数据/" + date_str
    new_dir_name_fofa = new_dir_name + "/FOFA"
    new_dir_name_360 = new_dir_name + "/360Quake"

    if not os.path.exists(new_dir_name):
        os.makedirs(new_dir_name)

    if not os.path.exists(new_dir_name_fofa):
        os.makedirs(new_dir_name_fofa)

    if not os.path.exists(new_dir_name_360):
        os.makedirs(new_dir_name_360)
    return new_dir_name_fofa,new_dir_name_360



######################################################################
'''
        FOFA信息收集
'''

def FofaCollectInfo(domain,fofa_dir_name):
    email = r'ITsec@inovance.com'
    api_key = r'91622b0473aefc9511f463a272484ad9'
    api = r'https://fofa.info/api/v1/search/all?email={}&key={}&qbase64={}&size={}&fields={}&full={}'
    fields = ("ip,port,protocol,country,country_name,region,city,host,domain,os,server,icp,title,"
              "jarm,banner,cert,link,tls_ja3s,tls_version,product,product_category,version,lastupdatetime,cname")
    arg_domain1 = "domain=\""
    arg_domain2 = domain
    arg_domain3 = "\""
    arg_domain = arg_domain1 + arg_domain2 + arg_domain3
    full = "false"
    flag = base64.b64encode(arg_domain.encode()).decode()
    size = "2000"

    complete_reuest = api.format(email, api_key, flag, size, fields, full)

    response = requests.get(complete_reuest)
    content = response.content

    filename = domain + ".txt"
    filepathname = fofa_dir_name + "/" +filename
    with open(filepathname, "wb") as file:
        file.write(content)
    return

def FofaSingleResponseProcess(filename,data,dict_domain2depart,dict_domain2company,dict_innerip,dict_innerport,dict_innerdomain,dict_innerresperson):
    f = open(filename, 'r', encoding='utf-8')
    content = f.read()

    response = json.loads(content)

    results = response["results"]
    print("{}共搜索到{}条记录！".format(filename,len(results)))
    host_info = []

    # 0:ip;  1:port; 2:协议;   3:国家缩写; 4:国家全名;
    # 5:地区; 6:城市;   7:主机名;  8:域名;   9:操作系统;
    # 10:服务器;   11:备案号; 12:标题
    # 13:jarm指纹; 14:banner;  15:证书;  16:链接;  17:tls_ja3s;    18:tls版本
    # 19:所有探测到的产品;  20:产品分类;    21:产品版本;    22:最后更新日期

    for host in results:
        host_info = []
        # host_info.clear()
        host_info.append(host[0])  # ip
        host_info.append(host[1])  # 端口
        host_info.append(host[2])  # 协议
        host_info.append(host[8])  # 域名
        #host_info.append(dict_domain2depart[host[8]])   #标识
        #host_info.append(dict_domain2company[host[8]])  #公司名
        host_info.append(host[10])  # 服务器
        host_info.append(host[16])  # URL
        host_info.append(host[12])  #标题
        host_info.append(host[4])  # 国家
        host_info.append(host[5])  # 地区
        host_info.append(host[6])  # 城市
        host_info.append(host[19])  # 所有产品
        host_info.append(host[21])  # 产品版本
        #host_info.append(host[14])  #banner
        host_info.append(host[22])  # 最后更新日期
        #print(host[14])
        host_info.append('') #ISP信息，fofa暂不具备，填充空补齐格式

        host_info.append(Fofasign) #来源标识，数据来源于FoFa还是Quake

        #检测是否有内网对应ip
        IDkey = host[0] + ":" + str(host[1])
        if IDkey in dict_innerip.keys():
            host_info.append(dict_innerip[IDkey])
            host_info.append(dict_innerport[IDkey])
            host_info.append(dict_innerdomain[IDkey])

            # if dict_innerip[IDkey] in dict_innerresperson.keys():
            #     host_info.append(dict_innerresperson[dict_innerip[IDkey]])
            # else:
            #     host_info.append('')
            if len(dict_innerip[IDkey])==1:
                if dict_innerip[IDkey][0] in dict_innerresperson.keys():
                    host_info.append(dict_innerresperson[dict_innerip[IDkey][0]])
                else:
                    host_info.append('')
            else:
                respersontemp = []
                for ip in dict_innerip[IDkey]:
                    if ip in dict_innerresperson.keys():
                        respersontemp.append(dict_innerresperson[ip])
                host_info.append(respersontemp)

        else:
            host_info.append('')
            host_info.append('')
            host_info.append('')
            host_info.append('')  #没匹配到对应内网地址，责任人置空

        host_info.append(host[15])  # 添加证书信息，用于后续证书有效期识别

        data.append(host_info)

        # 检测是否有内网对应责任人


    return



def FofaInfoOrganize(dirname):
    dirname = dirname + "/" + "FOFA"
    files = os.listdir(dirname)
    data = []
    dict_domain2depart, dict_domain2company = GetDomainAdditionInfo()
    dict_innerip, dict_innerport, dict_innerdomain,dict_innerresperson = GetOut2InDict()
    for file in files:
        filename = dirname + "/" + file
        FofaSingleResponseProcess(filename,data,dict_domain2depart,dict_domain2company,dict_innerip, dict_innerport, dict_innerdomain,dict_innerresperson)
    return data



######################################################################
'''
        360Quake信息收集
'''


def QuakeCollectInfo(domain,quake_dir_name):
    headers = {
        "X-QuakeToken": "ddfb0e1a-0026-40f3-9417-b187c304b9a2"
    }
    request_domain = "domain:" + domain
    data = {
        "query": request_domain,
        "start": 0,
        "size": 6000
    }
    response = requests.post(url="https://quake.360.net/api/v3/search/quake_service", headers=headers, json=data)

    content = response.content

    filename = domain + ".txt"
    filepathname = quake_dir_name + "/" + filename
    with open(filepathname, "wb") as file:
        file.write(content)
    return

def QuakeSingleResponseProcess(filename,data_all,dict_domain2depart,dict_domain2company,dict_innerip,dict_innerport,dict_innerdomain,dict_innerresperson):
    f = open(filename, 'r+', encoding='utf-8')
    content = f.read()
    print(filename)
    response = json.loads(content)

    results = response["data"]
    print("{}共搜索到{}条记录！".format(filename,len(results)))

    for item in results:
        data = []
        data.append(item['ip'])
        data.append(item['port'])
        data.append(item['service']['name'])
        domain = item['domain']

        # Quake的域名都是三级或四级域名，这里需要二级域名与FOFA收集到的保持一致，同时需要使用二级域名从表中搜索公司表示信息
        domain_split = domain.split('.')
        domain_name = domain_split[-2] + '.' + domain_split[-1]

        if domain_name == 'ind.in':
            domain_name = 'inovance.ind.in'

        if domain_name == 'co.kr':
            domain_name = 'sbclinear.co.kr'

        data.append(domain_name)

        #data.append(dict_domain2depart[domain_name])
        #data.append(dict_domain2company[domain_name])
        data.append(item['service']['http']['server'])
        data.append(item['service']['http']['http_load_url'][0])

        title = item['service']['http']['title']

        # if title == '\u200e':
        #     title = ''

        data.append(title)
        data.append(item['location']['country_cn'])
        data.append(item['location']['province_cn'])
        data.append(item['location']['city_cn'])

        product = ""
        version = ""

        if 'components' in item.keys():
            for component in item['components']:
                product = product + component['product_level'] + ":" + component['product_name_cn'] + "\n"
                version = version + component['product_name_cn'] + ":" + component['version'] + "\n"
        else:
            product = ""
            version = ""

        data.append(product)
        data.append(version)
        data.append(item['time'])
        data.append(item['location']['isp'])
        data.append(Quakesign) #来源标识

        #检测是否有对应内网
        IDkey =item['ip'] + ":" + str(item['port'])
        if IDkey in dict_innerip.keys():
            data.append(dict_innerip[IDkey])
            data.append(dict_innerport[IDkey])
            data.append(dict_innerdomain[IDkey])


            if len(dict_innerip[IDkey]) == 1:
                if dict_innerip[IDkey][0] in dict_innerresperson.keys():
                    data.append(dict_innerresperson[dict_innerip[IDkey][0]])
                else:
                    data.append('')
            else:
                respersontemp = []
                for ip in dict_innerip[IDkey]:
                    if ip in dict_innerresperson.keys():
                        respersontemp.append(dict_innerresperson[ip])
                data.append(respersontemp)

        else:
            data.append('')
            data.append('')
            data.append('')
            data.append('')

        if 'cert' in item['service'].keys():
            data.append(item['service']['cert'])
        else:
            data.append('')
        data_all.append(data)
    return


def QuakeInfoOrganize(dirname):
    dirname = dirname + "/" + "360Quake"
    files = os.listdir(dirname)
    data = []
    dict_domain2depart, dict_domain2company = GetDomainAdditionInfo()
    dict_innerip, dict_innerport, dict_innerdomain,dict_innerresperson = GetOut2InDict()
    for file in files:
        filename = dirname + "/" + file
        QuakeSingleResponseProcess(filename,data,dict_domain2depart,dict_domain2company,dict_innerip, dict_innerport, dict_innerdomain,dict_innerresperson)
    return data



def PortProcess(portstring):
    numbers = portstring.split(",")

    result = []

    for number in numbers:
        # 检查是否为范围形式，例如“2034-2040”
        if "-" in number:
            start, end = number.split("-")
            # 将范围内的数字添加到结果中
            result.extend(range(int(start), int(end) + 1))
        else:
            # 直接将数字添加到结果中
            result.append(int(number))


def ConnectTest(URL):
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接

    result = {}

    domainurl = URL
    print(" 开始请求 %s " % (domainurl))
    try:
        resp = s.get(domainurl,allow_redirects=False)
    except Exception:
        print("%s 请求失败 " % (domainurl))
        result[domainurl] = "请求失败"
    else:
        print("%s 返回的请求码为：%s " % (domainurl, resp.status_code))
        result[domainurl] = str(resp.status_code)
    s.close()
    return result[domainurl]