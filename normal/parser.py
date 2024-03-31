import requests
import json


step = 100


def send_request(page):
    endpoint = "https://www.auchan.ru/v1/catalog/products"
    params = {
        'merchantId': 1,
        'page': page,
        'perPage': step,
    }
    data = {
        "filter": {
            "category": "plavlenye",
            "promo_only": False,
            "active_only": True,
            "cashback_only": False
        }
    }
    response = requests.get(endpoint, params=params, json=data).json()
    return {'items': response['items'], 'range': response['activeRange']}


def filter_response(resp):
    filtered = []
    for elem in resp:
        if elem['stock']['not_available']:
            continue
        d = {
            'id': elem['id'],
            'productId': elem['productId'],
            'title': elem['title'],
            'price': elem['price'],
            'url': f"https://www.auchan.ru/product/{elem['code']}",
            'oldPrice': elem['oldPrice'],
            'brand': elem['brand']['name']
        }
        filtered.append(d)
    return filtered


def main():
    json_resp = {
        'total': 0,
        'items': []
    }
    cur_page = 1
    while (True):
        resp = send_request(cur_page)
        resp_filtered = filter_response(resp['items'])
        json_resp['items'].extend(resp_filtered)
        json_resp['total'] += len(resp_filtered)
        if (resp['range'] <= json_resp['total']):
            break
        cur_page += 1
    with open('result.json', 'w') as f:
        json.dump(json_resp, f, indent=4)


if __name__ == '__main__':
    main()
