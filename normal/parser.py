import requests
import json


step = 100


def send_request(page):
    endpoint = "https://www.auchan.ru/v1/catalog/products"
    params = {
        'merchantId': 1,
        'page': page,
        'perPage': step,
        'orderField': 'discountPercent',
        'orderDirection': 'desc',
    }
    data = {
        "filter": {
            "category": "ashan_zolotaya_ptica",
            "promo_only": False,
            "active_only": True,
            "cashback_only": False
        }
    }
    response = requests.get(endpoint, params=params, json=data).json()
    return {'items': response['items'], 'range': response['range']}


def filter_response(resp):
    filtered = []
    for elem in resp:
        if elem['stock']['not_available']:
            continue
        d = {
            'id': elem['id'],
            'productId': elem['productId'],
            'title': elem['title'],
            'mediaUrls': elem['mediaUrls'],
            'price': elem['price'],
            'oldPrice': elem['oldPrice'],
            'brand': elem['brand']['name']
        }
        filtered.append(d)
    return filtered


def main():
    json_resp = {
        'items': [],
        'total': 0
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
