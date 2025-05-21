import csv
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
    return result

def GetCSV():
    # file = open("对外发布.csv",quoting=csv.QUOTE_NONE)
    # filedata = file.readlines()
    #
    # data = []
    # for item in filedata:
    #
    #     data.append(item)
    with open("对外发布.csv")as f:
        reader = csv.reader(f)
        data = []
        for row in reader:
            data.append(row)
    return data

def AddSingleItem(CSVsinglelist,data):

    if CSVsinglelist[3]=='NULL':
        return

    domain = CSVsinglelist[4]
    OutIP = CSVsinglelist[0]
    portoutstr = str(CSVsinglelist[1])
    OutPort = PortProcess(portoutstr)
    InnerIP = CSVsinglelist[2]
    portinstr = str(CSVsinglelist[3])
    InnerPort = PortProcess(portinstr)
    resperson_id = CSVsinglelist[5]
    resperson_name = CSVsinglelist[6]
    resperson_comp = CSVsinglelist[7]
    resperson_depart1 = CSVsinglelist[8]
    resperson_depart2 = CSVsinglelist[9]





    nofop = len(OutPort)
    nofip = len(InnerPort)

    if nofop != nofip:
        print("这一条端口对不上：")
        print("%s,%s".format(domain,OutIP))
        return

    for i in range(nofop):
        temp = []
        temp.append(domain)
        temp.append(OutIP)
        temp.append(OutPort[i])
        temp.append(InnerIP)
        temp.append(InnerPort[i])
        if resperson_id=="NULL":
            temp.append('')
        else:
            temp.append([resperson_id,resperson_name,resperson_comp,resperson_depart1,resperson_depart2])
        data.append(temp)
    return


def List2Dict(datalistall):
    IDkey2domain = {}
    IDkey2InnerIP = {}
    IDkey2InnerPort = {}

    InnerIP2resperson = {}

    for datalist in datalistall:
        IDkey = datalist[1] + ':' + str(datalist[2])

        if IDkey in IDkey2domain.keys():

            IDkey2domain[IDkey].append(datalist[0])
            IDkey2InnerIP[IDkey].append(datalist[3])
            IDkey2InnerPort[IDkey].append(datalist[4])

            continue


        domain = datalist[0]
        innerip = datalist[3]
        innerport = datalist[4]

        IDkey2domain[IDkey] = []
        IDkey2domain[IDkey].append(domain)
        IDkey2InnerIP[IDkey] = []
        IDkey2InnerIP[IDkey].append(innerip)
        IDkey2InnerPort[IDkey] = []
        IDkey2InnerPort[IDkey].append(innerport)

        if datalist[5]!='' and datalist[3] not in InnerIP2resperson.keys():
            InnerIP2resperson[datalist[3]] = datalist[5]


    return IDkey2InnerIP,IDkey2InnerPort,IDkey2domain,InnerIP2resperson

def GetOut2InDict():
    data = GetCSV()
    data = data[1:]
    result = []
    for item in data:
        AddSingleItem(item,result)

    domain,IP,Port,resperson = List2Dict(result)
    return domain,IP,Port,resperson


def AddSingleItem(CSVsinglelist,data):
    print(CSVsinglelist)
    if CSVsinglelist[3]=='NULL':
        return

    domain = CSVsinglelist[0]
    OutIP = CSVsinglelist[1]
    portoutstr = str(CSVsinglelist[2])
    OutPort = PortProcess(portoutstr)

    InnerIP = CSVsinglelist[3]
    portinstr = str(CSVsinglelist[4])
    InnerPort = PortProcess(portinstr)
    resperson_id = CSVsinglelist[11]
    resperson_name = CSVsinglelist[10]
    resperson_comp = CSVsinglelist[9]
    resperson_depart1 = CSVsinglelist[5]
    resperson_depart2 = CSVsinglelist[6]





    nofop = len(OutPort)
    nofip = len(InnerPort)

    if nofop != nofip:
        print("这一条端口对不上：")
        print("%s,%s".format(domain,OutIP))
        return

    for i in range(nofop):
        temp = []
        temp.append(domain)
        temp.append(OutIP)
        temp.append(OutPort[i])
        temp.append(InnerIP)
        temp.append(InnerPort[i])
        if resperson_id=="NULL":
            temp.append('')
        else:
            temp.append([resperson_id,resperson_name,resperson_comp,resperson_depart1,resperson_depart2])
        data.append(temp)
    return


if __name__ == "__main__":
    data = GetCSV()

    data = data[1:]
    result = []

    for item in data:
        AddSingleItem(item,result)

    a,b,c,d = List2Dict(result)

    for item in b.keys():
        # if len(b[item]) > 1:
        #     print(b[item])
        print(item)
    print(len(b.keys()))


