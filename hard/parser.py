import requests
import json

step = 100

def send_request(page):
    endpoint = "https://api.metro-cc.ru/products-api/graph"
    headers = {"Content-Type": 'application/json'}
    # removed extra fieds from browser query that are not needed
    query = "\n query Query($storeId: Int!, $slug: String!, "\
        "$attributes:[AttributeFilter], $filters: [FieldFilter], $from: "\
        "Int!, $size: Int!, $sort: InCategorySort, $in_stock: Boolean, "\
        "$eshop_order: Boolean, $is_action: Boolean, $price_levels: "\
        "Boolean) {\n  category (storeId: $storeId, slug: $slug, inStock: "\
        "$in_stock, eshopAvailability: $eshop_order, isPromo: $is_action, "\
        "priceLevels: $price_levels) {\n   total\n   products("\
        "attributeFilters: $attributes, from: $from, size: $size, sort: "\
        "$sort, fieldFilters: $filters) {\n    id\n    name\n    article\n"\
        "    url\n    manufacturer {\n     name\n    }\n    stocks {\n    "\
        "value\n     text\n     eshop_availability\n     scale\n     "\
        "prices {\n price\n old_price\n     }\n    }\n   }\n  }\n }\n"\

    variables = {
        "isShouldFetchOnlyProducts": True,
        "slug": "syry",
        "storeId": 10,
        "sort": "default",
        "size": 100,
        "from": 0,
        "filters": [
            {
                "field": "main_article",
                "value": "0"
            }
        ],
        "attributes": [],
        "in_stock": True,  # guarantees that response products are in stock
        "eshop_order": False
    }

    response = requests.post(endpoint, headers=headers, json={'query': query,
                             'variables': variables}).json()
    return {'items': response['data']['category']['products'],
            'range': response['data']['category']['total']}


def filter_response(resp):
    filtered = []
    for elem in resp:
        d = {
            'id': elem['id'],
            'article': elem['article'],
            'title': elem['name'],
            'url': elem['url'],
            'price': elem['stocks'][0]['prices']['price'],
            'oldPrice': elem['stocks'][0]['prices']['old_price'],
            'brand': elem['manufacturer']['name']
        }
        filtered.append(d)
    return filtered



def main():
    json_resp = {
        'total': 0,
        'items': []
    }
    cur_offset = 0
    while (True):
        resp = send_request(cur_offset)
        resp_filtered = filter_response(resp['items'])
        json_resp['items'].extend(resp_filtered)
        json_resp['total'] += len(resp_filtered)
        if (resp['range'] <= json_resp['total']):
            break
        cur_offset += step
    with open('result.json', 'w') as f:
        json.dump(json_resp, f, indent=4)


if __name__ == '__main__':
    main()
