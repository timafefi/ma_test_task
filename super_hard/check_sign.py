import hashlib
import hmac
import requests
import json

step = 10


def send_request(page=1):
    headers = {
        'cookie': "selected_city_code=0000073738; selected_city_code=0000073738",
        'accept-encoding': "gzip",
        'authorization': "Basic NGxhcHltb2JpbGU6eEo5dzFRMyhy",
        'connection': "Keep-Alive",
        'host': "4lapy.ru",
        'user-agent': "v4.3.3(Android 11, Google sdk_gphone_x86)",
        'version-build': "203",
        'x-apps-additionally': "200",
        'x-apps-build': "4.3.3(203)",
        'x-apps-device': "Google sdk_gphone_x86",
        'x-apps-location': "lat:null,lon:null",
        'x-apps-os': "11",
        'x-apps-screen': "2712x1344"
        }
    endpoint = "https://4lapy.ru/api/v2/catalog/product/list"
    params = {
        'sort': 'popular',
        'category_id': 1,
        'page': page,
        'count': step,
        'token': '07c2139058f44b375d352821d4e78db3',
        # 'sign': '86d357cb55f0b7c7f7b9572c95fdef3a'
    }

    request = requests.Request('POST', endpoint, params=params,
                               headers=headers)
    prepped = request.prepare()
    signature = hmac.new(b'NGxhcHltb2JpbGU6eEo5dzFRMyhy', prepped.body, digestmod=hashlib.sha512)
    prepped.headers['sign'] = signature.hexdigest()
    print(prepped.headers['sign'])
    print(prepped.headers)



send_request()
