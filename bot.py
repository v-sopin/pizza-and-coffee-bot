import logging
import asyncio
from typing import List

from viberbot.api.messages.picture_message import PictureMessage
from aioviber.bot import Bot
from aioviber.chat import Chat, Carousel, Keyboard
from aioviber.keyboard import Button
from db_commands import Com as db
import messages as ms
import keyboards as kb
import search
import time
import text_parse as parse

logger = logging.getLogger(__name__)
loop = asyncio.get_event_loop()

bot = Bot(
    name='Pizza & coffee',
    avatar='https://media-cdn.tripadvisor.com/media/photo-p/14/3a/c0/60/caption.jpg',
    auth_token="4a9fa7bc7be7d06d-8c8bbe61274fbc68-6304c5f4046657f6",  # Public account auth token
    host="localhost",  # should be available from wide area network
    port=8000,
    webhook='https://04a71268.ngrok.io',  # Webhook url
)

# loop.run_until_complete(db.clear_users(loop))

'''

    Для пользователя

'''


@bot.command('старт')
async def start(chat: Chat, matched):
    first_name = chat.sender.name
    if await db.user_exist(chat.message.sender.id, loop) is True:
        await chat.send_text(ms.welcome2.format(first_name), keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
    else:
        await chat.send_text(ms.welcome2.format(first_name))
        await db.add_user(chat.message.sender.id, '', '', '', 'wait_for_city', loop)
        city = await search.get_city()
        keyboard = []
        for key, value in city:
            if key != 'minsk':
                b = Button(action_body=value["name"], columns=6, rows=1, bg_color="#ffffff", silent=True,
                           action_type="reply",
                           text=value["name"], text_size="regular", text_opacity=60, text_h_align="center",
                           text_v_align="middle")
                keyboard.append(b)
        await chat.send_text(ms.welcome, keyboard=Keyboard(keyboard, bg_color="#FFFFFF"))
        await db.add_user_for_stat(chat.message.sender.id, loop)


'''

    Меню, выбор товарар и добвление в корзину

'''


@bot.command('Меню')
async def test(chat: Chat, matched):
    u_id = chat.message.sender.id
    city = await db.get_city(u_id, loop)
    items = await search.sections(city)
    buttons = []
    for item in items:
        if item['id'] == '25':
            continue
        image = Button(action_body='show_{}'.format(item['id']), columns=6, rows=5, action_type="reply",
                       image=f"https://pizzacoffee.by/{item['picture']}")

        title_and_text = Button(action_body='show_{}'.format(item['id']), columns=6, rows=1, action_type="reply",
                                text=f'<font color=#323232><b>{item["name"]}</b></font>', text_size="medium",
                                text_v_align='middle', text_h_align='center')

        buttons.append(image)
        buttons.append(title_and_text)

    results = Carousel(buttons=buttons)

    await chat.send_rich_media(rich_media=results, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))


async def show_subcat(chat, category_id):
    u_id = chat.message.sender.id
    categories = await search.subcat(category_id)
    print(categories)
    print(categories.keys())
    categories_keys = list(categories.keys())
    buttons = []
    i = 0
    tmp_list = []
    while i < len(categories_keys):
        tmp_category = categories[categories_keys[i]]
        image = Button(action_body='show_' + str(categories_keys[i]), columns=6, rows=5, action_type="reply",
                       image='https://pizzacoffee.by/' + tmp_category['picture'])

        title_and_text = Button(action_body='show_' + str(categories_keys[i]), columns=6, rows=1,
                                action_type="reply",
                                text="<b>{}</b>".format(tmp_category['name'].replace('&quot;', '')),
                                text_size="regular", text_v_align='bottom', text_h_align='middle')
        buttons.append(image)
        buttons.append(title_and_text)
        i += 1
    i *= 2
    while i > 0:
        if i > 11:
            tmp_i = i - 12
        else:
            tmp_i = 0
        count = 0
        while count < 12:
            if count >= i:
                break
            j = 0
            while j < 2:
                tmp_list.append(buttons[tmp_i + count])
                j += 1
                count += 1
        results = Carousel(buttons=tmp_list)
        await chat.send_rich_media(rich_media=results, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
        tmp_list.clear()
        i -= 12
    buttons.clear()


async def show_pizza(chat, products, product_keys, category_id):
    buttons = []
    i = 0
    skip_count = 0
    tmp_list: List[Button] = []
    while i < len(product_keys):
        product = products[product_keys[i]]
        if len(product['prices']) == 0:
            price = product['offers'][list(product['offers'].keys())[0]]['price']
        else:
            price = list(product['prices'])[0]["PRICE"]
        if product.get('name') is None:
            print('skip')
            i += 1
            skip_count += 1
            continue
        image = Button(action_body='product_' + str(category_id) + '_' + str(product_keys[i]), columns=6, rows=4,
                       action_type="reply",
                       image='https://pizzacoffee.by/' + product['picture'])
        title_and_text = Button(action_body='product_' + str(category_id) + '_' + str(product_keys[i]), columns=6,
                                rows=1,
                                action_type="reply",
                                text="<b>{}</b>".format(product['name'].replace('&quot;', '"')), text_size="regular",
                                text_v_align='bottom', text_h_align='middle')
        item_info = Button(action_body='product_' + str(category_id) + '_' + str(product_keys[i]), columns=6, rows=1,
                           action_type="reply",
                           text=str(price), text_size="small",
                           text_v_align='middle',
                           text_h_align='center')
        buttons.append(image)
        buttons.append(title_and_text)
        buttons.append(item_info)
        i += 1
    print(tmp_list)
    print(i)
    i -= skip_count
    i *= 3
    while i > 0:
        if i > 17:
            tmp_i = i - 18
        else:
            tmp_i = 0
        count = 0
        while count < 18:
            if count >= i:
                break
            j = 0
            while j < 3:
                tmp_list.append(buttons[tmp_i + count])
                j += 1
                count += 1
        results = Carousel(buttons=tmp_list)
        await chat.send_rich_media(rich_media=results, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
        tmp_list.clear()
        i -= 18
    buttons.clear()


@bot.command('show_')
async def show_products(chat: Chat, matched):
    # довабить обоаботку на проверку категории ( если такого номера не существует)
    u_id = chat.message.sender.id
    city = await db.get_city(u_id, loop)
    category_id = chat.message.message.text.split('_')[1]
    products = search.get_products(category_id, city)
    product_keys = list(products.keys())
    subcat = ['22', '23']
    if category_id in subcat:
        print('Subcat')
        await show_subcat(chat, category_id)
        return
    pizza_cat = ['35', '36', '41']
    if category_id in pizza_cat:
        await show_pizza(chat, products, product_keys, category_id)
        return
    buttons = []
    i = 0
    skip_count = 0
    tmp_list: List[Button] = []
    while i < len(product_keys):
        product = products[product_keys[i]]
        print(product['prices'])
        if product.get('name') is None:
            print('skip')
            i += 1
            skip_count += 1
            continue
        if len(product['prices']) != 0:
            price = product['prices'][0]['PRICE']
        else:
            price = 0
        image = Button(action_body='product_' + str(category_id) + '_' + str(product_keys[i]), columns=6, rows=4,
                       action_type="reply",
                       image='https://pizzacoffee.by/' + product['picture'])

        title_and_text = Button(action_body='product_' + str(category_id) + '_' + str(product_keys[i]), columns=6,
                                rows=1,
                                action_type="reply",
                                text="<b>{}</b>".format(product['name']), text_size="regular",
                                text_v_align='bottom', text_h_align='middle')

        item_info = Button(action_body='product_' + str(category_id) + '_' + str(product_keys[i]), columns=6, rows=1,
                           action_type="reply",
                           text=str(price), text_size="small",
                           text_v_align='middle',
                           text_h_align='center')

        buttons.append(image)
        buttons.append(title_and_text)
        buttons.append(item_info)
        i += 1
    print(tmp_list)
    print(i)
    i -= skip_count
    i *= 3
    print(tmp_list)
    while i > 0:
        if i > 17:
            tmp_i = i - 18
        else:
            tmp_i = 0
        count = 0
        while count < 18:
            if count >= i:
                break
            j = 0
            while j < 3:
                tmp_list.append(buttons[tmp_i + count])
                j += 1
                count += 1
        results = Carousel(buttons=tmp_list)
        await chat.send_rich_media(rich_media=results, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
        tmp_list.clear()
        i -= 18
    buttons.clear()


@bot.command('product_')
async def show_product(chat: Chat, matched):
    products = search.get_all_products()
    category_id = chat.message.message.text.split('_')[1]
    product_id = chat.message.message.text.split('_')[2]
    if product_id in products:
        product = products[product_id]
        image = 'https://pizzacoffee.by' + products[product_id]['picture']
        text = parse.parse_details(product, product.get('text'))
        title_and_text = [Button(action_body='add-to-basket-{}-{}'.format(category_id, product_id), columns=6, rows=1,
                                 action_type="reply",
                                 text="<b>Добавить в корзину</b>", text_size="regular",
                                 text_v_align='bottom', text_h_align='middle')]
        await bot.api.send_message(chat.message.sender.id, PictureMessage(media=image))
        await chat.send_text(text)
        await chat.send_rich_media(rich_media=Carousel(6, 1, buttons=title_and_text),
                                   keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
    else:
        await chat.send_text('Продукта с таким уникальным номер не сууществует')


@bot.command('add-to-basket-')
async def add(chat: Chat, matched):
    user_id = chat.message.sender.id
    category_id = int(chat.message.message.text.split('-')[3])
    product_id = int(chat.message.message.text.split('-')[4])
    price = await search.get_price(product_id)
    await db.add_item_to_basket(user_id, product_id, category_id, price, loop)
    await db.update_more_info_c_id(user_id, product_id, loop)
    button = [Button(action_body=f'otmena', columns=6, rows=1, action_type="reply",
                     text='<font color=#ffffff>Отмена</font>', text_size="large", text_v_align='middle',
                     text_h_align='center', bg_color='#2F1AB2')]
    result = Carousel(buttons=button, buttons_group_columns=6, buttons_group_rows=1)
    await chat.send_text('Какое количество?')
    await chat.send_rich_media(rich_media=result, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
    await db.update_context(user_id, f'wait-count', loop)


@bot.command('otmena')
async def add(chat: Chat, matched):
    u_id = chat.message.sender.id
    await chat.send_text('Главное меню', keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
    await db.update_context(u_id, '', loop)


'''

    Изменение города

'''


@bot.command('change-city')
async def change_city(chat: Chat, matched):
    u_id = chat.message.sender.id
    city = await search.get_city()
    keyboard = []
    for key, value in city:
        if key != 'minsk':
            b = Button(action_body=value["name"], columns=6, rows=1, bg_color="#ffffff", silent=True,
                       action_type="reply",
                       text=value["name"], text_size="regular", text_opacity=60, text_h_align="center",
                       text_v_align="middle")
            keyboard.append(b)
    keyboard.append(
        Button(action_body='otmena', columns=6, rows=1, bg_color="#ffffff", silent=True, action_type="reply",
               text='<font color=#ffffff>Отмена</font>', text_size="regular", text_opacity=60, text_h_align="center",
               text_v_align="middle"))
    await chat.send_text(ms.change_city, keyboard=Keyboard(keyboard, bg_color="#FFFFFF"))
    await db.update_context(u_id, f'wait_city', loop)


'''

    Работа с корзиной

'''


@bot.command('Корзина')
async def add(chat: Chat, matched):
    u_id = chat.message.sender.id
    categories, items = await db.get_itemd_from_basket(u_id, loop)
    buttons = []
    count = len(items)
    i = 0
    if count != 0:
        if count > 5:
            for category, item in zip(categories, items):
                text, url, key = await search.more_info(item[0])

                image = Button(action_body=f'none', columns=6, rows=4, action_type="reply",
                               image=f"https://pizzacoffee.by/{url}")

                title_and_text = Button(action_body=f'none', columns=6, rows=1, action_type="reply",
                                        text=f'<font color=#323232><b>{text}</b></font>', text_size="medium",
                                        text_v_align='middle', text_h_align='left')

                delete_from_cart = Button(action_body=f"delete-{item[0]}", columns=6, rows=1, action_type="reply",
                                          text=f'Убрать из корзины', text_size="small",
                                          text_v_align='middle',
                                          text_h_align='center')

                buttons.append(image)
                buttons.append(title_and_text)
                buttons.append(delete_from_cart)
                i += 1
                if len(buttons) == 12 and i < len(items):
                    results = Carousel(buttons=buttons)
                    await chat.send_rich_media(rich_media=results)
                    buttons.clear()
                elif len(buttons) != 18 and i == len(items):
                    results = Carousel(buttons=buttons)
                    await chat.send_rich_media(rich_media=results)
                    buttons.clear()
            button = [Button(action_body=f'none', columns=6, rows=1, action_type="reply",
                             text='<font color=#ffffff>Оформить заказ</font>', text_size="large", text_v_align='middle',
                             text_h_align='center', bg_color='#2F1AB2')]
            result = Carousel(buttons=button, buttons_group_columns=6, buttons_group_rows=1)
            await chat.send_rich_media(rich_media=result, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
        else:
            for category, item in zip(categories, items):
                text, url, price = await search.more_info(item[0])
                count = await db.get_count(item[0], loop)
                text += ' x ' + str(count)
                print(text)
                image = Button(action_body=f'none', columns=6, rows=4, action_type="open-url",
                               image=f"https://pizzacoffee.by/{url}")  # resized

                title_and_text = Button(action_body=f'none', columns=6, rows=1, action_type="open-url",
                                        text=f'<font color=#323232><b>{text}</b></font>', text_size="medium",
                                        text_v_align='middle', text_h_align='left')

                delete_from_cart = Button(action_body=f"delete-{category[0]}", columns=6, rows=1, action_type="reply",
                                          text=f'Убрать из корзины', text_size="small",
                                          text_v_align='middle',
                                          text_h_align='center')

                buttons.append(image)
                buttons.append(title_and_text)
                buttons.append(delete_from_cart)
            results = Carousel(buttons=buttons)
            await chat.send_rich_media(rich_media=results)
            button = [Button(action_body=f'of-order', columns=6, rows=1, action_type="reply",
                             text='<font color=#ffffff>Оформить заказ</font>', text_size="large", text_v_align='middle',
                             text_h_align='center', bg_color='#2F1AB2')]
            result = Carousel(buttons=button, buttons_group_columns=6, buttons_group_rows=1)
            await chat.send_rich_media(rich_media=result, keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
    else:
        await chat.send_text('В корзине ничего нет!', keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))


@bot.command('delete-')
async def p(chat: Chat, matched):
    u_id = chat.message.sender.id
    item = chat.message.message.text[7:]
    print(item)
    await db.delete_from_basket(u_id, item, loop)
    await chat.send_text('Товар удален из корзины', keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))


'''

    Оформление заказа

'''


@bot.command('of-order')
async def ord(chat: Chat, matched):
    u_id = chat.message.sender.id
    await chat.send_text('Введите ваше ФИО:')
    await db.update_context(u_id, 'wait_fio', loop)


'''

    Вопросы и ответы

'''


@bot.command('Вопросы и ответы')
async def v_o(chat: Chat, matched):
    await chat.send_text('Выберите вопрос, который вас интересует', keyboard=Keyboard(kb.ask_kb, bg_color="#FFFFFF"))


@bot.command('Как связаться?')
async def nnum(chat: Chat, matched):
    text = 'E-mail - opros.pizza@gmail.com\n\nТелефон - +375336093708'
    await chat.send_text(text, keyboard=Keyboard(kb.ask_kb, bg_color="#FFFFFF"))


@bot.command('Какие условия доставки?')
async def nnum(chat: Chat, matched):
    text = 'Стоимость доставки 2.5 руб\n\nЧасы доставки: 11:00 - 01:00\n\nТелефоны доставки: 7424'
    await chat.send_text(text, keyboard=Keyboard(kb.ask_kb, bg_color="#FFFFFF"))


@bot.command('Какие есть способы оплаты?')
async def nnum(chat: Chat, matched):
    text = 'Способы оплаты при заказе через чат-бота:\n\n-Наличными курьеру\n-Банковской картой курьеру'
    await chat.send_text(text, keyboard=Keyboard(kb.ask_kb, bg_color="#FFFFFF"))


@bot.command('Клубная карта')
async def nnum(chat: Chat, matched):
    text = 'Друзья! С радостью сообщаем Вам о прекрасном изменении: новой системе лояльности в Pizza&Coffee!' \
           ' С ее помощью вы сможете увеличить свой кэшбэк до 30%. Чтобы вы могли досконально во всем разобраться,' \
           ' мы подготовили для вас руководство в формате вопрос-ответ.'
    await chat.send_text(text, keyboard=Keyboard(kb.card, bg_color="#FFFFFF"))


@bot.command('Почему стоит приобрести нашу клубную карту?')
async def nnum(chat: Chat, matched):
    text = 'С ней вы сэкономите свои средства, а также получите многие другие бонусы, доступные только владельцам карт,' \
           ' которые сделают каждое посещение Pizza&Coffee еще более приятным и привычным занятием.'
    await chat.send_text(text, keyboard=Keyboard(kb.card, bg_color="#FFFFFF"))


@bot.command('КАК ОНА РАБОТАЕТ')
async def nnum(chat: Chat, matched):
    text = 'С каждого заказа, который вы сделаете, на карту будет начислено 10% от его суммы в виде баллов.' \
           'Эти средства вы можете накапливать и использовать при оплате следующих заказов.' \
           'Например, вы купили большую 43-сантиметровую пиццу «4 сезона» за 21,90 руб. После оплаты этой суммы, на карте окажется 2,19 рублей (10%)' \
           ' и в следующий раз вы сможете их использовать и сэкономить.' \
           'А можете просто продолжать накапливать баллы. Обратите внимание, что при оформлении одного заказа вы можете либо потратить свои баллы, либо накопить их, но не одновременно!' \
           'Также обладатели клубных карт имеют уникальную возможность принимать участие в акциях, проводимых только для обладателей клубных карт!'
    await chat.send_text(text, keyboard=Keyboard(kb.card, bg_color="#FFFFFF"))


@bot.command('КАКОВА МАКСИМАЛЬНАЯ СКИДКА, КОТОРУЮ ВЫ МОЖЕТЕ ПОЛУЧИТЬ С ПОМОЩЬЮ КАРТЫ')
async def nnum(chat: Chat, matched):
    text = '99,9%. На примере с той же большой пиццей «4 сезона», вы сможете приобрести ее за 2 копейки,' \
           ' если у вас на карте будет накоплено 21,88 балла.' \
           ' Если баллов больше, то оставшиеся не сгорят, а останутся доступными для будущих заказов.'
    await chat.send_text(text, keyboard=Keyboard(kb.card, bg_color="#FFFFFF"))


@bot.command('КАК МНЕ ПРИОБРЕСТИ КЛУБНУЮ КАРТУ')
async def nnum(chat: Chat, matched):
    text = 'Ее можно приобрести в любом заведении «Pizza&Coffee», а также на доставку по телефону 7424.'
    await chat.send_text(text, keyboard=Keyboard(kb.card, bg_color="#FFFFFF"))


@bot.command('СМОГУ ЛИ Я ИСПОЛЬЗОВАТЬ КАРТУ')
async def nnum(chat: Chat, matched):
    text = 'Нет, на карте есть магнитная лента, без проведения карточки мы не сможем ничего на нее зачислить, поэтому старайтесь не забывать!'
    await chat.send_text(text, keyboard=Keyboard(kb.card, bg_color="#FFFFFF"))


@bot.command('КАК УЗНАТЬ')
async def nnum(chat: Chat, matched):
    text = 'Информацию о количестве накопленных балов Вами вы можете узнать, предъявив карту бармену в любом заведении «Pizza&Coffee», а также позвонив по телефону 7424.'
    await chat.send_text(text, keyboard=Keyboard(kb.card, bg_color="#FFFFFF"))


'''

    Для администратора

'''


@bot.command('/admin')
async def admin(chat: Chat, matched):
    u_id = chat.message.sender.id
    button = [Button(action_body=f'otmena', columns=6, rows=1, action_type="reply",
                     text='<font color=#ffffff>Отмена</font>', text_size="large", text_v_align='middle',
                     text_h_align='center', bg_color='#2F1AB2')]
    result = Carousel(buttons=button, buttons_group_columns=6, buttons_group_rows=1)
    await chat.send_text('Введите пароль')
    await chat.send_rich_media(rich_media=result)
    await db.update_context(u_id, 'wait_password', loop)


'''

    Рассылка

'''


@bot.command('send_messages')
async def ras(chat: Chat, matched):
    await chat.send_text('Тип рассылки:', keyboard=Keyboard(kb.ras, bg_color="#FFFFFF"))


@bot.command('no_orders')
async def ras(chat: Chat, matched):
    u_id = chat.message.sender.id
    no_users = []
    users = await db.get_all_users(loop)
    users_from_orders = await db.users_from_orders(loop)
    for user in users:
        if user in users_from_orders:
            a = 0
        else:
            no_users.append(user)
    if len(no_users) == 0:
        await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras, bg_color="#FFFFFF"))
    else:
        await chat.send_text('Какой тип сообщения вы хотите отправить?',
                             keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
        await db.update_more_info_c_id(u_id, 'no-orders', loop)


@bot.command('one-or-more')
async def ras(chat: Chat, matched):
    u_id = chat.message.sender.id
    users_from_orders = await db.users_from_orders(loop)
    if len(users_from_orders) == 0:
        await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras, bg_color="#FFFFFF"))
    else:
        await chat.send_text('Какой тип сообщения вы хотите отправить?',
                             keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
        await db.update_more_info_c_id(u_id, 'one-or-more', loop)


@bot.command('more-n')
async def ras(chat: Chat, matched):
    u_id = chat.message.sender.id
    users_from_orders = await db.users_from_orders(loop)
    if len(users_from_orders) == 0:
        await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras, bg_color="#FFFFFF"))
    else:
        await db.update_context(u_id, 'wait_N', loop)
        await chat.send_text('Больше какого количества заказов?')
        await db.update_more_info_c_id(u_id, 'more-n', loop)


@bot.command('m-or-more-month')
async def ras(chat: Chat, matched):
    u_id = chat.message.sender.id
    users_from_orders = await db.users_from_orders(loop)
    if len(users_from_orders) == 0:
        await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras, bg_color="#FFFFFF"))
    else:
        await db.update_context(u_id, 'wait_N', loop)
        await chat.send_text('Больше какого количества заказов?')
        await db.update_more_info_c_id(u_id, 'm-or-more-month', loop)


@bot.command('sr-sum-more')
async def ras(chat: Chat, matched):
    u_id = chat.message.sender.id
    users_from_orders = await db.users_from_orders(loop)
    if len(users_from_orders) == 0:
        await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras, bg_color="#FFFFFF"))
    else:
        await db.update_context(u_id, 'wait_N', loop)
        await chat.send_text('Больше какой суммы заказа?')
        await db.update_more_info_c_id(u_id, 'sr-sum-more', loop)


@bot.command('sr-sum-less')
async def ras(chat: Chat, matched):
    u_id = chat.message.sender.id
    users_from_orders = await db.users_from_orders(loop)
    if len(users_from_orders) == 0:
        await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras, bg_color="#FFFFFF"))
    else:
        await db.update_context(u_id, 'wait_N', loop)
        await chat.send_text('Меньше какой суммы заказа?')
        await db.update_more_info_c_id(u_id, 'sr-sum-less', loop)


@bot.command('pb-n-more')
async def ras(chat: Chat, matched):
    u_id = chat.message.sender.id
    users_from_orders = await db.users_from_orders(loop)
    if len(users_from_orders) == 0:
        await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras, bg_color="#FFFFFF"))
    else:
        await db.update_context(u_id, 'wait_N', loop)
        await chat.send_text('Больше скольки дней?')
        await db.update_more_info_c_id(u_id, 'pb-n-more', loop)


@bot.command('send-to-all')
async def send_to_all(chat: Chat, matched):
    u_id = chat.message.sender.id
    await chat.send_text('Какой тип сообщения вы хотите отправить?', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
    await db.update_more_info_c_id(u_id, 'one-or-more', loop)


@bot.command('pb-n-less')
async def ras(chat: Chat, matched):
    u_id = chat.message.sender.id
    users_from_orders = await db.users_from_orders(loop)
    if len(users_from_orders) == 0:
        await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras, bg_color="#FFFFFF"))
    else:
        await db.update_context(u_id, 'wait_N', loop)
        await chat.send_text('Меньше скольки дней?')
        await db.update_more_info_c_id(u_id, 'pb-n-less', loop)


@bot.command('ras-photo')
async def ph(chat: Chat, matched):
    u_id = chat.message.sender.id
    await db.update_context(u_id, 'wait_photo', loop)
    button = [Button(action_body=f'otmena', columns=6, rows=1, action_type="reply",
                     text='<font color=#ffffff>Отмена</font>', text_size="large", text_v_align='middle',
                     text_h_align='center', bg_color='#2F1AB2')]
    result = Carousel(buttons=button, buttons_group_columns=6, buttons_group_rows=1)
    await chat.send_text('Ожидаю картинку')
    await chat.send_rich_media(rich_media=result)


@bot.command('ras-text')
async def ph(chat: Chat, matched):
    u_id = chat.message.sender.id
    await db.update_context(u_id, 'wait_text', loop)
    button = [Button(action_body=f'otmena', columns=6, rows=1, action_type="reply",
                     text='<font color=#ffffff>Отмена</font>', text_size="large", text_v_align='middle',
                     text_h_align='center', bg_color='#2F1AB2')]
    result = Carousel(buttons=button, buttons_group_columns=6, buttons_group_rows=1)
    await chat.send_text('Ожидаю текст')
    await chat.send_rich_media(rich_media=result)


@bot.message_handler('picture')
async def sp(chat: Chat):
    u_id = chat.message.sender.id
    context = await db.get_context(u_id, loop)
    if context == 'wait_photo':
        podcontext = await db.get_more_c_id(u_id, loop)
        if podcontext == 'no-orders':
            no_users = []
            users = await db.get_all_users(loop)
            users_from_orders = await db.users_from_orders(loop)
            for user in users:
                if user in users_from_orders:
                    a = 0
                else:
                    no_users.append(user)
            for user in no_users:
                await chat.send_picture_plus(picture=chat.message.message.media, to=str(user))
            await chat.send_text(f'Количество отправленных сообщений: {len(no_users)}',
                                 keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
            await db.update_more_info_c_id(u_id, 0, loop)
        elif podcontext == 'one-or-more':
            users_from_orders = await db.users_from_orders(loop)
            for user in users_from_orders:
                await chat.send_picture_plus(picture=chat.message.message.media, to=str(user))
            await chat.send_text(f'Количество отправленных сообщений: {len(users_from_orders)}',
                                 keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
            await db.update_more_info_c_id(u_id, 0, loop)
        elif podcontext == 'more-n':
            n = await db.get_more_info(u_id, loop)
            res = []
            users_from_orders = await db.users_from_orders(loop)
            for user in users_from_orders:
                sum = await db.users_from_orders_more_n(user, int(n[0]), loop)
                if sum != None and int(sum[0]) >= int(n[0]):
                    res.append(user)
            if len(res) != 0:
                for user in res:
                    await chat.send_picture_plus(picture=chat.message.message.media, to=str(user))
                await chat.send_text(f'Количество отправленных сообщений: {len(res)}',
                                     keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
            else:
                await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
        elif podcontext == 'm-or-more-month':
            n = await db.get_more_info(u_id, loop)
            res = []
            users_from_orders = await db.users_from_orders(loop)
            for user in users_from_orders:
                sum = await db.users_from_orders_more_n_and_date(user, int(n[0]), loop)
                if sum != None and int(sum[0]) >= int(n[0]):
                    res.append(user)
            if len(res) != 0:
                for user in res:
                    await chat.send_picture_plus(picture=chat.message.message.media, to=str(user))
                await chat.send_text(f'Количество отправленных сообщений: {len(res)}',
                                     keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
            else:
                await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
        elif podcontext == 'sr-sum-more':
            n = await db.get_more_info(u_id, loop)
            res = []
            users_from_orders = await db.users_from_orders(loop)
            for user in users_from_orders:
                sum = await db.users_from_orders_more_n_sum(user, int(n[0]), loop)
                if sum != None and float(sum) >= float(n[0]):
                    res.append(user)
            if len(res) != 0:
                for user in res:
                    await chat.send_picture_plus(picture=chat.message.message.media, to=str(user))
                await chat.send_text(f'Количество отправленных сообщений: {len(res)}',
                                     keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
            else:
                await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
        elif podcontext == 'sr-sum-less':
            n = await db.get_more_info(u_id, loop)
            res = []
            users_from_orders = await db.users_from_orders(loop)
            for user in users_from_orders:
                sum = await db.users_from_orders_less_n_sum(user[0], int(n[0]), loop)
                if sum != None and float(sum) <= float(n):
                    res.append(user)
            if len(res) != 0:
                for user in res:
                    await chat.send_picture_plus(picture=chat.message.message.media, to=str(user))
                await chat.send_text(f'Количество отправленных сообщений: {len(res)}',
                                     keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
            else:
                await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
        elif podcontext == 'pb-n-more':
            n = await db.get_more_info(u_id, loop)
            users_from_orders = await db.users_from_orders_more_n_date(n, loop)
            if users_from_orders != None:
                for user in users_from_orders:
                    await chat.send_picture_plus(picture=chat.message.message.media, to=str(user))
                await chat.send_text(f'Количество отправленных сообщений: {len(users_from_orders)}',
                                     keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
            else:
                await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
        elif podcontext == 'pb-n-less':
            n = await db.get_more_info(u_id, loop)
            users_from_orders = await db.users_from_orders_less_n_date(n, loop)
            if users_from_orders != None:
                for user in users_from_orders:
                    await chat.send_picture_plus(picture=chat.message.message.media, to=str(user))
                await chat.send_text(f'Количество отправленных сообщений: {len(users_from_orders)}',
                                     keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
            else:
                await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
        elif podcontext == 'send-to-all':
            all_users = await db.get_all_users(loop)
            for user in all_users:
                await chat.send_picture_plus(picture=chat.message.message.media, to=str(user))
            await chat.send_text(f'Количество отправленных сообщений: {len(all_users)}',
                                 keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
            await db.update_more_info_c_id(u_id, 0, loop)


'''

    Работа с контекстом

'''


@bot.default('')
async def default(chat: Chat):
    if await db.user_exist(chat.message.sender.id, loop) is False:
        await chat.send_text('Для начала работы с ботом необходимо написать Старт или Start')
    else:
        u_id = chat.message.sender.id

        context = await db.get_context(u_id, loop)
        city = await search.get_city()
        if context == 'wait_for_city':
            await chat.send_text(
                f'Вы выбрали {chat.message.message.text}\n\n Ипользуйте кнопки внизу, чтобы взаимодействовать  ⬇️',
                keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
            for key, value in city:
                if value["name"] == chat.message.message.text:
                    await db.update_city(u_id, key, loop)
                    await db.update_context(u_id, ' ', loop)
        elif context == 'wait-count':
            count = chat.message.message.text
            if count.isdigit():
                await chat.send_text('Товар добавлен в корзину!', keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
                i_id = await db.get_more_c_id(u_id, loop)
                print(i_id)
                await db.update_count_to_basket(u_id, i_id, count, loop)
                await db.update_context(u_id, '', loop)
            else:
                await chat.send_text('Пожалуйста введите целое число:')
        elif context == 'wait_password':
            password = chat.message.message.text
            if password == ms.PASSWORD:
                await chat.send_text('Добро пожаловать!', keyboard=Keyboard(kb.adim_kb, bg_color="#FFFFFF"))
                await db.update_context(u_id, '', loop)
            else:
                await chat.send_text('Неверный пароль! Повторите попытку ввода')
        elif context == 'wait_city':
            city = await search.get_city()
            await chat.send_text(f'Ваш город изменен на: {chat.message.message.text}.\nБей по кнопкам!',
                                 keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))
            for key, value in city:
                if value["name"] == chat.message.message.text:
                    await db.update_city(u_id, key, loop)
                    await db.update_context(u_id, ' ', loop)
        elif context == 'wait_N':
            await db.update_more_info(u_id, int(chat.message.message.text), loop)
            await chat.send_text('Какой тип сообщения вы хотите отправить?',
                                 keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))

        elif context == 'wait_text':
            podcontext = await db.get_more_c_id(u_id, loop)
            if podcontext == 'no-orders':
                no_users = []
                users = await db.get_all_users(loop)
                users_from_orders = await db.users_from_orders(loop)
                for user in users:
                    if user in users_from_orders:
                        a = 0
                    else:
                        no_users.append(user)
                for user in no_users:
                    await chat.send_text_plus(to=str(u_id), text=chat.message.message.text)
                await chat.send_text(f'Количество отправленных сообщений: {len(no_users)}',
                                     keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
            if podcontext == 'one-or-more':
                users_from_orders = await db.users_from_orders(loop)
                for user in users_from_orders:
                    await chat.send_text_plus(to=str(u_id), text=chat.message.message.text)
                await chat.send_text(f'Количество отправленных сообщений: {len(users_from_orders)}',
                                     keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
            elif podcontext == 'more-n':
                n = await db.get_more_info(u_id, loop)
                res = []
                users_from_orders = await db.users_from_orders(loop)
                for user in users_from_orders:
                    sum = await db.users_from_orders_more_n(user, int(n[0]), loop)
                    if sum != None and int(sum[0]) >= int(n[0]):
                        res.append(user)
                if len(res) != 0:
                    for user in res:
                        await chat.send_text_plus(to=str(u_id), text=chat.message.message.text)
                    await chat.send_text(f'Количество отправленных сообщений: {len(res)}',
                                         keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                    await db.update_more_info_c_id(u_id, 0, loop)
                else:
                    await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
            elif podcontext == 'm-or-more-month':
                n = await db.get_more_info(u_id, loop)
                res = []
                users_from_orders = await db.users_from_orders(loop)
                for user in users_from_orders:
                    sum = await db.users_from_orders_more_n_and_date(user, int(n[0]), loop)
                    if sum != None and int(sum[0]) >= int(n[0]):
                        res.append(user)
                if len(res) != 0:
                    for user in res:
                        await chat.send_text_plus(to=str(u_id), text=chat.message.message.text)
                    await chat.send_text(f'Количество отправленных сообщений: {len(res)}',
                                         keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                    await db.update_more_info_c_id(u_id, 0, loop)
                else:
                    await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
            elif podcontext == 'sr-sum-more':
                n = await db.get_more_info(u_id, loop)
                res = []
                users_from_orders = await db.users_from_orders(loop)
                for user in users_from_orders:
                    sum = await db.users_from_orders_more_n_sum(user, int(n[0]), loop)
                    if sum != None and float(sum) >= float(n[0]):
                        res.append(user)
                if len(res) != 0:
                    for user in res:
                        await chat.send_text_plus(to=str(u_id), text=chat.message.message.text)
                    await chat.send_text(f'Количество отправленных сообщений: {len(res)}',
                                         keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                    await db.update_more_info_c_id(u_id, 0, loop)
                else:
                    await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
            elif podcontext == 'sr-sum-less':
                n = await db.get_more_info(u_id, loop)
                res = []
                users_from_orders = await db.users_from_orders(loop)
                for user in users_from_orders:
                    sum = await db.users_from_orders_less_n_sum(user, int(n[0]), loop)
                    if sum != None and float(sum) <= float(n):
                        res.append(user)
                if len(res) != 0:
                    for user in res:
                        await chat.send_text_plus(to=str(u_id), text=chat.message.message.text)
                    await chat.send_text(f'Количество отправленных сообщений: {len(res)}',
                                         keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                    await db.update_more_info_c_id(u_id, 0, loop)
                else:
                    await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
            elif podcontext == 'pb-n-less':
                n = await db.get_more_info(u_id, loop)
                users_from_orders = await db.users_from_orders_less_n_date(n, loop)
                if users_from_orders != None:
                    for user in users_from_orders:
                        await chat.send_text_plus(to=str(u_id), text=chat.message.message.text)
                    await chat.send_text(f'Количество отправленных сообщений: {len(users_from_orders)}',
                                         keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                    await db.update_more_info_c_id(u_id, 0, loop)
                else:
                    await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                    await db.update_more_info_c_id(u_id, 0, loop)
            elif podcontext == 'pb-n-more':
                n = await db.get_more_info(u_id, loop)
                users_from_orders = await db.users_from_orders_more_n_date(n, loop)
                if users_from_orders != None:
                    for user in users_from_orders:
                        await chat.send_text_plus(to=str(u_id), text=chat.message.message.text)
                    await chat.send_text(f'Количество отправленных сообщений: {len(users_from_orders)}',
                                         keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                    await db.update_more_info_c_id(u_id, 0, loop)
                else:
                    await chat.send_text('Нет таких пользователей', keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                    await db.update_more_info_c_id(u_id, 0, loop)
            elif podcontext == 'send-to-all':
                all_users = await db.get_all_users(loop)
                for user in all_users:
                    await chat.send_text_plus(to=str(u_id), text=chat.message.message.text)
                await chat.send_text(f'Количество отправленных сообщений: {len(all_users)}',
                                     keyboard=Keyboard(kb.ras_cat, bg_color="#FFFFFF"))
                await db.update_more_info_c_id(u_id, 0, loop)
        elif context == 'wait_fio':
            fio = chat.message.message.text
            await db.update_fio(u_id, fio, loop)
            await chat.send_text('Спасибо! Теперь введите ваш номер телефона:')
            await db.update_context(u_id, 'wait_tel', loop)
        elif context == 'wait_tel':
            tel = chat.message.message.text
            await db.update_tel(u_id, tel, loop)
            await db.update_context(u_id, '', loop)
            #await search.json_(u_id, loop)
            await chat.send_text('Ваш заказ оформлен, ожидайте звонка оператора.',
                                 keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))

        elif context == 'wait_start_date':
            date = chat.message.message.text
            try:
                date = time.strptime(date, '%Y-%m-%d')
                await db.update_context(u_id, 'wait_finish_date', loop)
                await db.update_more_info(u_id, date, loop)
                await chat.send_text('Введите дату конца отчетного периода в формате ГГГГ-ММ-ДД')
            except ValueError:
                await chat.send_text(
                    'Вы ввели неправильный формат даты. Введите пожалуйста в таком формате: ГГГГ-ММ-ДД')
        elif context == 'wait_finish_date':
            f_date = chat.message.message.text
            try:
                f_date = time.strptime(f_date, '%Y-%m-%d')
                await db.update_context(u_id, '', loop)
                s_date = await db.get_more_info(u_id, loop)
                new_users = await db.get_cont_new_users(s_date, f_date, loop)
                out_users = await db.get_cont_out_users(s_date, f_date, loop)
                count_orders = await db.get_cont_orders(s_date, f_date, loop)
                city = ['baranovichi', 'bobruysk', 'volkovisk', 'grodno', 'zhlobin', 'slutsk', 'vitebsk']
                c_count = []
                for c in city:
                    p = await db.get_users_city(c, loop)
                    c_count.append(p[0])
                text = f'Статистика по периоду:\n' \
                       f'\n-Новые пользователи: {new_users[0]};' \
                       f'\n-Ушедшие пользователи: {out_users[0]};' \
                       f'\n-Кол-во оформленных заказов: {count_orders[0]};'
                text_2 = f'Кол-во пользователей по городам:' \
                         f'\n -Барановичи:{c_count[0]};' \
                         f'\n -Бобруйск:{c_count[1]};' \
                         f'\n -Волковыск:{c_count[2]};' \
                         f'\n -Гродно:{c_count[3]};' \
                         f'\n -Жлобин:{c_count[4]};' \
                         f'\n -Слуцк:{c_count[5]};' \
                         f'\n -Витебск:{c_count[6]};'

                await chat.send_text(text)
                await chat.send_text(text_2)
            except ValueError:
                await chat.send_text(
                    'Вы ввели неправильный формат даты. Введите пожалуйста в таком формате: ГГГГ-ММ-ДД')
        else:
            await chat.send_text('Приступай к покупкам!', keyboard=Keyboard(kb.start, bg_color="#FFFFFF"))


'''

    Для статистики

'''


@bot.command('stat-')
async def stat(chat: Chat, matched):
    u_id = chat.message.sender.id
    await chat.send_text('Введите дату начала отчетного периода в формате ГГГГ-ММ-ДД')
    await db.update_context(u_id, 'wait_start_date', loop)


@bot.event_handler('unsubscribed')
async def ev(matched):
    u_id = await bot.api.get_account_info()
    u_id = u_id['members']
    u_id = u_id[0]
    u_id = u_id['id']
    await db.update_user_for_stat(u_id, loop)


if __name__ == '__main__':  # pragma: no branch
    import aiohttp.web

    aiohttp.web.run_app(bot.app, host=bot.host, port=bot.port)
