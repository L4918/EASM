import base64
import requests
import datetime
import os

ip = "93.43.56.133"

email = r'ITsec@inovance.com'
api_key = r'91622b0473aefc9511f463a272484ad9'
api = r'https://fofa.info/api/v1/search/all?email={}&key={}&qbase64={}&size={}&fields={}&full={}'
fields = ("ip,port,protocol,host,os,server,lastupdatetime")
arg_domain1 = "ip=\""
arg_domain2 = ip
arg_domain3 = "\""
arg_domain = arg_domain1 + arg_domain2 + arg_domain3
full = "false"
flag = base64.b64encode(arg_domain.encode()).decode()
size = "2000"

complete_reuest = api.format(email, api_key, flag, size, fields, full)

response = requests.get(complete_reuest)
content = response.content

date_str = str(datetime.date.today())
new_dir_name = "高危端口响应数据/" + date_str
if not os.path.exists(new_dir_name):
    os.makedirs(new_dir_name)
filename = ip + ".txt"
filepathname = new_dir_name + "/" + filename
with open(filepathname, "wb") as file:
    file.write(content)