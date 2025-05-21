#0:ip;  1:port; 2:协议;   3:国家缩写; 4:国家全名;
# 5:地区; 6:城市;   7:主机名;  8:域名;   9:操作系统;
# 10:服务器;   11:备案号; 12:标题
#13:jarm指纹; 14:banner;  15:证书;  16:链接;  17:tls_ja3s;    18:tls版本
# 19:所有探测到的产品;  20:产品分类;    21:产品版本;    22:最后更新日期
#colname = ['IP','端口','协议','域名','服务器','URL','国家','地区','城市','所有产品','产品版本','最后更新日期']
import csv
import datetime
import re
from method import ConnectTest

fofa_fmt = "%Y-%m-%d %H:%M:%S"
today = datetime.date.today()
today_dt = datetime.datetime.today()
Expeirdtime = today - datetime.timedelta(days=185)
Expeirdtime = Expeirdtime.strftime("%Y-%m-%d %H:%M:%S")
Expeirdtime = datetime.datetime.strptime(Expeirdtime,"%Y-%m-%d %H:%M:%S")
#Expeirdtime = datetime.datetime.strptime("2023-01-01 00:00:00","%Y-%m-%d %H:%M:%S")

class Asset:
    def __init__(self):

        self.certexpiredata = []
        self.ports = []
        self.ips = []
        self.protocol = []


        self.domain = []
        self.server = []
        self.URL = []
        self.location_country = []
        self.location_region = []
        self.location_city = []

        self.Fofaproduct = []
        self.Fofaversion = []
        self.Quakeproduct = []
        self.Quakeversion = []

        self.Fofaupdatetime = []
        self.Quakeupdatetime = []


        #self.depart = []
        #self.company = []
        self.title = []
        self.isp = []

        self.innerip = []
        self.innerport = []
        self.innerdomain = []
        self.cert = []
        self.cert_date_vaild = []
        self.innerresperson = []

        self.responseCode = []

    # def __contains__(self, item):
    #     if item in self.id:
    #         return True
    #     else:
    #         return False

    #处理UTC时间
    def parse_utc_time(self,time_str):
        formats = ['%Y-%m-%dT%H:%M:%S.%fZ', '%Y-%m-%dT%H:%M:%SZ']
        for fmt in formats:
            try:
                return datetime.datetime.strptime(time_str, fmt)
            except ValueError:
                pass
        raise ValueError("时间格式不匹配")

    #检查是否包含具体的版本信息
    def check_version(self,string):
        pattern = r'\b\d+\.\d+(\.\d+)?\b'
        if re.search(pattern, string):
            return True
        else:
            return False

    #从证书字符串中提取起始日期和结束日期，若无效或不存在则返回None
    def FOFAget_cert_expiry(self,cert_string):
        # 通过正则表达式提取有效期信息
        not_before_match = re.search(r'Not Before: (.+)', cert_string)
        not_after_match = re.search(r'Not After : (.+)', cert_string)

        if not_before_match and not_after_match:
            not_before_str = not_before_match.group(1)
            not_after_str = not_after_match.group(1)

            # 将字符串转换为日期时间对象
            not_before = datetime.datetime.strptime(not_before_str, '%Y-%m-%d %H:%M %Z')
            not_after = datetime.datetime.strptime(not_after_str, '%Y-%m-%d %H:%M %Z')

            return not_before, not_after
        else:
            return None, None

    #fofa收集到的证书有效期信息提取
    def CertExpiredJudge(self,cert,source):   #1有效，2无效，3无证书信息
        if source == 1:
            not_before,not_after = self.FOFAget_cert_expiry(cert)
            self.certexpiredata.append(not_after)
        else:
            not_before, not_after = self.Quakeget_cert_expiry(cert)
            self.certexpiredata.append(not_after)

        if not_before == None or not_after == None:
            return 3
        if not_after>today_dt:
            return 1
        else:
            return 2
    #Quake收集到的证书有效期信息提取
    def Quakeget_cert_expiry(self,cert_string):
        # 使用正则表达式提取有效期信息
        match = re.search(r'Not Before: (.+)\n\s+Not After : (.+)\n', cert_string)
        if match:
            not_before_str, not_after_str = match.group(1), match.group(2)
            # 解析日期字符串并转换为 datetime 对象
            not_before = datetime.datetime.strptime(not_before_str, '%b %d %H:%M:%S %Y %Z')
            not_after = datetime.datetime.strptime(not_after_str, '%b %d %H:%M:%S %Y %Z')
            return not_before, not_after
        else:
            return None, None

    def FofaAddSingleAsset(self,single):

        if single.title == "很抱歉，您访问的域名不存在！":
            return

        updatetime = datetime.datetime.strptime(single.update, fofa_fmt)
        if updatetime < Expeirdtime:
            return


        for i in range(len(self.ips)):
            if single.ip == self.ips[i] and single.port == self.ports[i] and single.URL == self.URL[i]:
                return


        self.ips.append(single.ip)
        self.ports.append(single.port)

        self.URL.append(single.URL)
        self.responseCode.append(ConnectTest(single.URL))

        self.protocol.append(single.protocol)
        self.domain.append(single.domain)
        self.server.append(single.server)
        self.location_country.append(single.location_country)
        self.location_region.append(single.location_region)
        self.location_city.append(single.location_city)

        self.Fofaproduct.append(single.product)
        self.Fofaversion.append(single.version)
        self.Fofaupdatetime.append(single.update)

        self.Quakeproduct.append('')
        self.Quakeversion.append('')
        self.Quakeupdatetime.append('')

        #self.depart.append(single.depart)
        #self.company.append(single.company)
        self.title.append(single.title)
        self.isp.append(single.isp)

        self.innerip.append(single.innerip)
        self.innerport.append(single.innerport)
        self.innerdomain.append(single.innerdomain)
        self.innerresperson.append(single.innerresperson)

        self.cert.append(single.cert)
        self.cert_date_vaild.append(self.CertExpiredJudge(single.cert,1))

        return

    def QuakeAddSingleAsset(self, single):
        #检测是否不存在域名
        if single.title == "很抱歉，您访问的域名不存在！":
            return
        #检测是否过期太久
        updatetime = self.parse_utc_time(single.update)
        if updatetime < Expeirdtime:
            return


        if single.URL[-1]=='/':
            single.URL=single.URL[:-1]
        for i in range(len(self.ips)):

            if single.ip == self.ips[i] and single.port == self.ports[i] and single.URL == self.URL[i]:
                if self.Quakeupdatetime[i] != '':
                    return
                else:
                    self.Quakeproduct[i] = single.product
                    self.Quakeversion[i] = single.version
                    self.Quakeupdatetime[i] = single.update
                    self.isp[i] = single.isp
                    return

        self.ips.append(single.ip)
        self.ports.append(single.port)


        self.URL.append(single.URL)
        self.responseCode.append(ConnectTest(single.URL))

        self.protocol.append(single.protocol)
        self.domain.append(single.domain)
        self.server.append(single.server)
        self.location_country.append(single.location_country)
        self.location_region.append(single.location_region)
        self.location_city.append(single.location_city)

        self.Fofaproduct.append('')
        self.Fofaversion.append('')
        self.Fofaupdatetime.append('')

        self.Quakeproduct.append(single.product)
        self.Quakeversion.append(single.version)
        self.Quakeupdatetime.append(single.update)

        #self.depart.append(single.depart)
        #self.company.append(single.company)
        self.title.append(single.title)
        self.isp.append(single.isp)

        self.innerip.append(single.innerip)
        self.innerport.append(single.innerport)
        self.innerdomain.append(single.innerdomain)
        self.innerresperson.append(single.innerresperson)

        self.cert.append(single.cert)
        self.cert_date_vaild.append(self.CertExpiredJudge(single.cert,2))

        return

    def SaveAsCSV(self,name):

        n = len(self.ips)
        data_all = []
        for i in range(n):
            data = []
            data.append(self.ips[i])
            data.append(self.ports[i])
            data.append(self.protocol[i])
            data.append(self.domain[i])

            if len(self.innerip[i])==1:
                data.append(self.innerip[i][0])
                data.append(self.innerport[i][0])
                data.append(self.innerdomain[i][0])
            else:
                data.append(self.innerip[i])
                data.append(self.innerport[i])
                data.append(self.innerdomain[i])


            #data.append(self.depart[i])
            #data.append(self.company[i])
            data.append(self.server[i])
            data.append(self.URL[i])

            data.append(self.responseCode[i])

            data.append(self.title[i])
            data.append(self.location_country[i])
            data.append(self.location_region[i])
            data.append(self.location_city[i])

            data.append(self.Fofaproduct[i])
            data.append(self.Fofaversion[i])
            data.append(self.Fofaupdatetime[i])

            data.append(self.Quakeproduct[i])
            data.append(self.Quakeversion[i])
            data.append(self.Quakeupdatetime[i])

            data.append(self.isp[i])
            data.append(self.innerresperson[i])

            data_all.append(data)


        csvFile = open(name, "w+", newline='')
        colname = ['IP', '端口', '协议', '域名','内网ip','内网端口','内网域名','标识', '公司名', '服务器', 'URL', '响应码','标题', '国家', '地区', '城市',
                   'FOFA识别产品', 'FOFA识别产品版本','FOFA最后更新日期','Quake识别产品','Quake识别产品版本','Quake最后更新日期','ISP','责任人']
        try:
            writer = csv.writer(csvFile)
            writer.writerow(colname)
            # data为list类型
            # data为list类型
            for i in range(len(data_all)):
                try:
                    writer.writerow(data_all[i])
                except:
                    data_all[i][8] = '编码格式问题无法显示'
                    i = i - 1
                    continue
        finally:
            csvFile.close()

    def SaveIncludeVersionData(self,name):
        n = len(self.ips)
        data_all = []
        for i in range(n):

            if self.check_version(self.Fofaversion[i]) or self.check_version(self.Quakeversion[i]):
                data = []
                data.append(self.ips[i])
                data.append(self.ports[i])
                data.append(self.protocol[i])
                data.append(self.domain[i])

                if len(self.innerip[i]) == 1:
                    data.append(self.innerip[i][0])
                    data.append(self.innerport[i][0])
                    data.append(self.innerdomain[i][0])
                else:
                    data.append(self.innerip[i])
                    data.append(self.innerport[i])
                    data.append(self.innerdomain[i])
                #data.append(self.depart[i])
                #data.append(self.company[i])
                data.append(self.server[i])
                data.append(self.URL[i])


                data.append(self.title[i])
                data.append(self.location_country[i])
                data.append(self.location_region[i])
                data.append(self.location_city[i])


                version = self.Fofaversion[i] + " " + self.Quakeversion[i]
                data.append(version)


                data.append(self.isp[i])

                data_all.append(data)

        csvFile = open(name, "w+", newline='')
        colname = ['IP', '端口', '协议', '域名', '内网ip', '内网端口', '内网域名', '标识', '公司名', '服务器', 'URL',
                   '标题', '国家', '地区', '城市','产品版本', 'ISP']
        try:
            writer = csv.writer(csvFile)
            writer.writerow(colname)
            # data为list类型
            # data为list类型
            for i in range(len(data_all)):
                try:
                    writer.writerow(data_all[i])
                except:
                    data_all[i][8] = '编码格式问题无法显示'
                    i = i - 1
                    continue
        finally:
            csvFile.close()

    def SaveExpiredCSV(self,name):
        n = len(self.ips)
        data_all = []
        for i in range(n):
            data = []
            if self.cert_date_vaild[i]==2:
                data.append(self.ips[i])
                data.append(self.ports[i])
                data.append(self.URL[i])
                data.append(self.innerip[i])
                data.append(self.innerport[i])
                data.append(self.certexpiredata[i])
                data_all.append(data)
        csvFile = open(name, "w+", newline='')
        colname = ['外网IP', '外网端口', 'URL',  '内网ip', '内网端口','TLS证书截止日期']
        try:
            writer = csv.writer(csvFile)
            writer.writerow(colname)
            # data为list类型
            # data为list类型
            for i in range(len(data_all)):
                writer.writerow(data_all[i])
        finally:
            csvFile.close()

    def SaveTLSDetectionNeedInfo(self,name):
        n = len(self.ips)
        data_all = []
        for i in range(n):
            data = []
            if self.protocol[i] == 'https' or self.protocol[i] == 'http/ssl':
                data.append(self.ips[i])
                data.append(self.ports[i])
                data.append(self.URL[i])
                data.append(self.innerip[i])
                data.append(self.innerport[i])
                data_all.append(data)
        csvFile = open(name, "w+", newline='')
        colname = ['外网IP', '外网端口', 'URL', '内网ip', '内网端口']
        try:
            writer = csv.writer(csvFile)
            writer.writerow(colname)
            # data为list类型
            # data为list类型
            for i in range(len(data_all)):
                writer.writerow(data_all[i])
        finally:
            csvFile.close()

class SingleAsset:
    def __init__(self,list):
        print(list)
        self.ip = list[0].strip()
        self.port = str(list[1])
        self.protocol = list[2]
        self.domain = list[3]
        # self.depart = list[4]
        # self.company = list[5]
        self.server = list[4]
        self.URL = list[5].strip()
        self.title = list[6].strip()
        self.location_country = list[7]
        self.location_region = list[8]
        self.location_city = list[9]
        self.product = list[10]
        self.version = list[11]
        self.update = list[12]
        self.isp = list[13]
        self.sign = list[14]
        self.innerip = list[15]
        self.innerport = list[16]
        self.innerdomain = list[17]
        self.innerresperson = list[18]
        self.cert = list[19]





