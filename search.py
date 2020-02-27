import urllib.request
import aiohttp
import json
import requests
from db_commands import Com as db


def get_products(categories, city):
    url = 'https://pizzacoffee.by/api/?e=products&parent=' + categories + '&token=1&city=' + city + '&resized_picture=w:700,h:500'
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read())
        return data


def get_products_no_resized(categories, city):
    url = 'https://pizzacoffee.by/api/?e=products&parent=' + categories + '&token=1&city=' + city
    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read())
        return data


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json(content_type='text/html')


async def sections(city):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, f'https://pizzacoffee.by/api/?e=sections&token=1&city={city}&resized_picture=w:700,h:500')
        result = []
        for key, value in html.items():
            if value["show_main"] == "1":
                result.append(value)
    return result


async def subcat(p_id):
    with urllib.request.urlopen(f'https://pizzacoffee.by/api/?e=sections&parent={p_id}&token=1&resized_picture=w:700,h:500') as url:
        data = json.loads(url.read())
        return data


async def subcat_pizza(p_id):
    async with aiohttp.ClientSession() as session:
        w = 50
        html = await fetch(session,
                           f'https://pizzacoffee.by/api/?e=products&parent={p_id}&token=1&resized_picture=w:700,h:500')
        result = []
        keys = []
        for key, value in html.items():
            if value == None or value['name'] == None:
                pass
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


async def more_info(product_id, category_id, city):
    products = get_products(category_id, city)
    product = products[product_id]
    text = product['name'].replace('&quot;', '"')
    url = product['picture_resized']['src']
    if len(product['prices']) == 0:
        price = product['offers'][list(product['offers'].keys())[0]]['price']
    else:
        price = list(product['prices'])[0]["PRICE"]
    return text, url, price


async def more_info_non_priced(product_id, category_id, city, user_id, loop):
    products = get_products(category_id, city)
    product = products[product_id]
    offer_id, border_id = await db.get_offer(product_id, user_id, loop)
    if offer_id == 0:
        name = product['name'].replace('&quot;', '"')
    else:
        text = product['name'].replace('&quot;', '"')
        name_pizza = products[product_id]['offers'][str(offer_id)]['borders'][str(border_id)]['name']
        size = name_pizza.split(' ')
        name = text + ' ' + str(size[-2]) + ' см'
    url = product['picture_resized']['src']
    return name, url


async def get():
    items, keys = await subcat_pizza(35)
    for value in items:
        pass


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
        offer_id, border_id = await db.get_offer(item.i_id, u_id, loop)
        if border_id is not None:
            product_data = {"id": item.i_id, "name": item.name, "price": item.price, "quantity": item.count, "properties": {"border": border_id}}
        else:
            product_data = {"id": item.i_id, "name": item.name, "price": item.price, "quantity": item.count}
        r.append(product_data)
    res = json.dumps(r)

    link = f"https://pizzacoffee.by/api/?e=order&city={user.city}&street={user.address}&house={user.house}&apartments=0&deliveryAddress={user.address + ' ' + str(user.house)}&login={user.phone_number}&password={user.phone_number}&username={user.full_name}&phone={user.phone_number}&products={res}&token=1"

    new_link = str(link.replace('[', ''))
    new_link = new_link.replace(']', '')

    async with aiohttp.ClientSession() as session:
        html = await fetch(session, new_link)
        if html.get('success') is not None:
            return True, ''
        if html.get('error') is not None:
            return False, html['error']

        return True, ''

