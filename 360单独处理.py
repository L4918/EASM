import requests


def QuakeCollectInfo(domain):
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
    with open(filename, "wb") as file:
        file.write(content)
    return

QuakeCollectInfo("dataserver.cn")