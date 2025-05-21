from  assetclass import *
from method import *


if __name__ == "__main__":

    dirname = "响应数据/2025-03-31"

    dict_domain2depart, dict_domain2company = GetDomainAdditionInfo()

    Fofadata = FofaInfoOrganize(dirname)
    Quakedata = QuakeInfoOrganize(dirname)
    asset = Asset()


    fofa_num = len(Fofadata)
    quake_num = len(Quakedata)

    i = 1

    for item in Fofadata:
        asset.FofaAddSingleAsset(SingleAsset(item))
        print("%s / %s FoFa" % (i,fofa_num))
        i=i+1

    i = 1
    for item in Quakedata:
        asset.QuakeAddSingleAsset(SingleAsset(item))
        print("%s / %s Quake" % (i, quake_num))
        i=i+1
    asset.SaveAsCSV("资产整合0331.csv")
    asset.SaveIncludeVersionData("版本问题0331.csv")
    asset.SaveExpiredCSV("证书过期0331.csv")
    asset.SaveTLSDetectionNeedInfo("基于TLS协议ip0331.csv")


