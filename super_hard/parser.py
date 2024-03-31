import requests
import json

step = 100

def send_request(page):
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
        'sign': '86d357cb55f0b7c7f7b9572c95fdef3a'
    }

    return requests.get(endpoint, params=params, headers=headers)


def filter_response(resp):
    filtered = []
    for elem in resp['data']['goods']:
        if not elem['isAvailable']:
            continue
        d = {
            'id': elem['id'],
            'article': elem['article'],
            'title': elem['title'],
            'url': elem['webpage'],
            'price': elem['price'],
            'brand': elem['manufacturer']['name']
        }
        filtered.append(d)
    return filtered



def main():
    json_resp = {
        'total': 0,
        'items': []
    }
    cur_page = 0
    while (True):
        resp = send_request(cur_page)
        if resp.status_code != 200:
            print(f"Something went wrong. Status code {resp.status_code}\n"
                  f"{resp.json()}")
            exit(1)
        resp_filtered = filter_response(resp)
        json_resp['items'].extend(resp_filtered)
        json_resp['total'] += len(resp_filtered)
        if (resp['range'] <= json_resp['total']):
            break
        cur_page += step
    with open('result.json', 'w') as f:
        json.dump(json_resp, f, indent=4)


if __name__ == '__main__':
    main()
