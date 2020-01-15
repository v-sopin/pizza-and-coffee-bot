def parse_details(product, text):
    result_string = str(product['name'].replace('&quot;', '"'))
    if len(product['prices']) == 0:
        price = product['offers'][list(product['offers'].keys())[0]]['price']
    else:
        price = list(product['prices'])[0]["PRICE"]
    try:
        if 'detail' in text.keys():
            print(text.keys())
            if text['detail'] != '' or type(text['detail']) is None:
                result_string += '\n' + text.get('detail')
                print(result_string)
                result_string = result_string.replace('&#40;', '(')
                result_string = result_string.replace('&#41;', ')')
        print(type(result_string))
        result_string += str('\n\nЦена: ' + str(price) + ' руб')
    except TypeError:
        print('hi')
        return result_string
    return result_string
