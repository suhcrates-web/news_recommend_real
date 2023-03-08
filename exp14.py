import re

import requests
import json

url ='https://analytics.google.com/analytics/web/getPage'#?explorer-table.plotKeys=%5B%5D&explorer-table.rowStart=0&explorer-table.rowCount=5000&id=content-pages&ds=a59562926w93775237p97683542&cid=explorer-motionChart%2Cexplorer-table%2Cexplorer-table%2CtimestampMessage&hl=ko&authuser=0'


data = {
'explorer-table.plotKeys': '[]',
'explorer-table.rowStart': '0',
'explorer-table.rowCount': '5000',
'id': 'content-pages',
'ds': 'a59562926w93775237p97683542',
'cid': 'explorer-motionChart,explorer-table,explorer-table,timestampMessage',
'hl': 'ko',
'authuser': '0'
}

headers = {
'accept': '*/*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7,ru;q=0.6',
'content-length': '56',
'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
'cookie': 'GA_XSRF_TOKEN=AO6Y7m-4Z0efwyYm0dpbFPEIu3_c9DEI-w:1677834999194; __utma=231532751.1014418027.1677834941.1677835133.1677835133.1; __utmc=231532751; __utmz=231532751.1677835133.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmb=231532751.0.10.1677835133; _ga=GA1.3-2.1014418027.1677834941; _gid=GA1.3-2.281637089.1677834941; SEARCH_SAMESITE=CgQI15cB; AEC=ARSKqsIpIqMXL_c5TzdUvEgW3C1qBSvzK1Os9zltq3xTSAoIQkNANgZkYQ; 1P_JAR=2023-03-03-06; _gid=GA1.3.281637089.1677834941; S=analytics-realtime-frontend=JGem7EYkjRiSiAsHGV-LmIUw6e4sNoxf; SID=TwjhDUcYhkT_qL3C8z-vfMG6TepCeHScjXMcYsOlUl85YIVnmKdqwEnpOxdXYFs13gpdWg.; __Secure-1PSID=TwjhDUcYhkT_qL3C8z-vfMG6TepCeHScjXMcYsOlUl85YIVnovlihwV2oAh9qAyWJ96T2g.; __Secure-3PSID=TwjhDUcYhkT_qL3C8z-vfMG6TepCeHScjXMcYsOlUl85YIVnuITpFY-TauAtlQCIh8dhaQ.; HSID=ABYgroqy9wt2faUKd; SSID=Aw98HZWrz2Z3p0ni8; APISID=wge_l5_mWGYx2XLF/ACXP-n2iNzAPsH9Zt; SAPISID=691SCsTCS9f4itSR/AYMKPUIHz4gM7Bjm4; __Secure-1PAPISID=691SCsTCS9f4itSR/AYMKPUIHz4gM7Bjm4; __Secure-3PAPISID=691SCsTCS9f4itSR/AYMKPUIHz4gM7Bjm4; _ga_0V7JNYGWCC=GS1.1.1677834946.1.0.1677835006.0.0.0; _ga=GA1.3.1014418027.1677834941; NID=511=sU_YquSQll7gbw3Pr5CmWcmUrAxsc91WGSEf-SWjvN4R5_XU-GxpcuTifZwAKdpAyn2nuCqUjU6XdfW83Umza_TdAejMrLkRmRzijpmQPHp6ROqToPQrBMzaY2Z2FxKxwApa3-HBgu5iFmn51W2rzmwo3b-W2rh91nEd9x_xgtKgzHr50cfAt9JioZpWsHtOqv_5pmlXF4V7YNkkXfv0cRtA5gP5IfoSbFgFBjf3jKTQ1iGq0XqIYsjxR_f6dJ5R3LT7_5l0wD8D; _ga_X6LMX9VR0Y=GS1.1.1677901923.2.1.1677903093.0.0.0; _ga_B8SKQ9HHPZ=GS1.1.1677901923.2.1.1677903093.0.0.0; _ga_58GG1QVC8C=GS1.1.1677901922.2.1.1677903100.0.0.0; SIDCC=AFvIBn-B7p5_uP9ZHdjkbIncZmOyuilt4lkGPijm9gSPAQtedOI9zpsexl1-CF0z5JsV05f6Hw; __Secure-1PSIDCC=AFvIBn8Q8tVmccDLu7_XbpF-oJNM-Ru_aVMskMKrEZmWzeB7HEZyRnXYUKgktuhKVD5Da-ybgAk; __Secure-3PSIDCC=AFvIBn_O6urAipYCTLc6QdCKxfm3uZwu7wvT5f-RiSJABXgOirNXGTTm9pBDWwVmr07fbhC0Sg',
'galaxy-ajax': 'true',
'origin': 'https://analytics.google.com',
'referer': 'https://analytics.google.com/analytics/app/',
'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"Windows"',
'sec-fetch-dest': 'empty',
'sec-fetch-mode': 'cors',
'sec-fetch-site': 'same-origin',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
'x-client-data': """CJO2yQEIpLbJAQjEtskBCKmdygEIlOTKAQiWocsBCMjJzAEI1PXMAQjwgM0BCLOGzQEI3onNAQj1i80BCI+MzQEI043NAQi5kc0BCIyTzQEI4JXNAQinls0BCNLhrAI= Decoded: message ClientVariations {// Active client experiment variation IDs. repeated int32 variation_id = [3300115, 3300132, 3300164, 3313321, 3322388, 3330198, 3351752, 3357396, 3358832, 3359539, 3359966, 3360245, 3360271, 3360467, 3360953, 3361164, 3361504, 3361575, 4927698];}""",
'x-gafe4-xsrf-token': 'AO6Y7m-rxKCtapx1GA--Zbac02qI4R-tng:1677901905055'
}
temp = requests.post(url, data=data, headers=headers)
temp = json.loads(temp.content.decode('utf-8')[5:])
# print(temp.keys()) # 멘 처음 키
# print(temp['components'][0]['dataTable']['rowCluster']) # 컨텐츠 있는 열

articles =temp['components'][0]['dataTable']['rowCluster']
# print(articles)
for ar in articles:
    label = ar['label']
    url = ar['rowKey'][0]['displayKey']
    if 'article' in url:

        print(re.findall(r'\d{8}/\d+',url))


        print(label)
        print(url)
        for row in ar['row'][0]['rowValue']:
            print(row['dataValue'])
            # 페이지뷰, 순페이지뷰,  머문시간, 방문수, 이탈률, 종료율, 페이지값