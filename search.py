import urllib.request
import aiohttp
import json
import requests
from db_commands import Com as db


def get_all_products():
    with urllib.request.urlopen('https://pizzacoffee.by/api/?e=products&token=1') as url:
        data = json.loads(url.read())
        return data


def get_products(categories, city):
    with urllib.request.urlopen('https://pizzacoffee.by/api/?e=products&parent=' + categories +
                                '&token=1&city=' + city) as url:
        data = json.loads(url.read())
        print(data)
        return data


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json(content_type='text/html')


async def sections(city):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, f'https://pizzacoffee.by/api/?e=sections&token=1&city={city}')
        result = []
        for key, value in html.items():
            if value["show_main"] == "1":
                result.append(value)
    return result


async def subcat(p_id):
    with urllib.request.urlopen(f'https://pizzacoffee.by/api/?e=sections&parent={p_id}&token=1') as url:
        data = json.loads(url.read())
        print(data)
        return data


async def subcat_pizza(p_id):
    async with aiohttp.ClientSession() as session:
        w = 50
        html = await fetch(session,
                           f'https://pizzacoffee.by/api/?e=products&parent={p_id}&token=1')
        result = []
        keys = []
        print(p_id)
        for key, value in html.items():
            if value == None or value['name'] == None:
                print('NNNN')
            else:
                result.append(value)
                keys.append(key)
    return result, keys


async def more_info_pizza(p_id, c_id):
    async with aiohttp.ClientSession() as session:
        p_id = int(p_id)
        c_id = c_id
        html = await fetch(session, f'https://pizzacoffee.by/api/?e=products&parent={p_id}&token=1')
        result = []
        url = ''
        s = ''
        for keys, value in html.items():
            if keys == str(c_id):
                url = value['picture']
                result.append(value['text'])
        for item in result:
            s = item['preview']
    return s, url


async def more_info(product_id):
    products = get_all_products()
    product = products[product_id]
    text = product['name'].replace('&quot;', '"')
    url = product['picture']
    if len(product['prices']) == 0:
        price = product['offers'][list(product['offers'].keys())[0]]['price']
    else:
        price = list(product['prices'])[0]["PRICE"]
    return text, url, price


async def get_price(product_id):
    products = get_all_products()
    print(products.keys())
    product = products[str(product_id)]
    if len(product['prices']) == 0:
        price = product['offers'][list(product['offers'].keys())[0]]['price']
    else:
        price = list(product['prices'])[0]["PRICE"]

    return price


async def get():
    items, keys = await subcat_pizza(35)
    for value in items:
        print("value:", value['name'])


async def get_city():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, f'https://pizzacoffee.by/api/?e=city&token=1')
    return html.items()


async def name_i(p_id, c_id):
    async with aiohttp.ClientSession() as session:
        p_id = int(p_id)
        c_id = c_id
        html = await fetch(session, f'https://pizzacoffee.by/api/?e=products&parent={p_id}&token=1')
        name = ''
        for keys, value in html.items():
            if keys == str(c_id):
                name = value['name']
    return name


async def json_(u_id, loop):
    user = await db.get_user_obj(u_id, loop)
    items = await db.get_user_basket_items(u_id, loop)

    r = []
    for item in items:
        r.append({"id": item.i_id, "name": item.name, "price": item.price, "quantity": item.count})
    res = json.dumps(r)
    link = f"https://pizzacoffee.by/api/?e=order&login={user.phone_number}&password={user.phone_number}&username={user.full_name}&phone={user.phone_number}&products={res}&token=1"
    new_link = str(link.replace('[', ''))
    new_link = new_link.replace(']', '')
    print(new_link)
    responce = requests.post(new_link, verify=False)
    print(responce.json())
