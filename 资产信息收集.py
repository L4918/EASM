
from method import *

dirname_fofa,dirname_360 = MakeDir()
n = len(DomainList)
i = 1
for domain in DomainList:
    FofaCollectInfo(domain,dirname_fofa)
    QuakeCollectInfo(domain,dirname_360)
    print("已完成 {} / {}".format(i,n))
    i = i+1