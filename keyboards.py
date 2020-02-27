from aioviber import Keyboard, Button
import search

menu_button_jpg = 'https://i.ibb.co/PGnTj7c/psd-png.jpg'
cart_button_jpg = 'https://i.ibb.co/2q9NB0k/png.jpg'
faq_button_jpg = 'https://i.ibb.co/6vzq6k1/image.jpg'
change_city_button_jpg = 'https://i.ibb.co/BBHmQVZ/png.jpg'

how_contact_button_jpg = 'https://i.ibb.co/pzJ6SHb/png.jpg'
payment_types_button_jpg = 'https://i.ibb.co/XXXxzrw/png.jpg'
delivery_types_button_jpg = 'https://i.ibb.co/4m19XKm/png.jpg'
club_card_button_jpg = 'https://i.ibb.co/SfMKtr6/image.jpg'

how_buy_club_card_jpg = 'https://i.ibb.co/fXyypgJ/image.jpg'
how_many_points_jpg = 'https://i.ibb.co/56kwXyj/image.jpg'
the_biggest_discount_jpg = 'https://i.ibb.co/vQscXZB/image.jpg'
why_buy_card_jpg = 'https://i.ibb.co/VVf1WTq/image.jpg'
can_i_use_card_jpg = 'https://i.ibb.co/1XTWxFd/image.jpg'
what_is_club_card_jpg = 'https://i.ibb.co/fvKHy0Z/image.jpg'

big_go_back_jpg = 'https://i.ibb.co/DD3tzpw/image.jpg'
little_go_back_jpg = 'https://i.ibb.co/HGJPVrv/image.jpg'

big_blank_button_jpg = 'https://i.ibb.co/kx5qVKm/image.jpg'
little_blank_button_jpg = 'https://i.ibb.co/txCGd4s/image.jpg'

start = [Button(action_body="Меню", columns=6, rows=1, silent=True, action_type="reply", text='Меню', text_size= "regular", text_opacity=1, bg_media=menu_button_jpg, bg_media_type='picture'),
         Button(action_body="Вопросы и ответы", columns=3, rows=1, silent=True, action_type="reply", text='Вопросы и ответы', text_opacity=1, bg_media=faq_button_jpg, bg_media_type='picture'),
         Button(action_body="change-city", columns=3, rows=1, silent=True, action_type="reply", text='Изменить город', text_opacity=1, bg_media=change_city_button_jpg, bg_media_type='picture'),
         Button(action_body="Корзина", columns=6, rows=1, silent=True, action_type="reply", text='Корзина', text_opacity=1, bg_media=cart_button_jpg, bg_media_type='picture')]

adim_kb = [Button(action_body="send_messages", columns=6, rows=1, bg_color="#ffffff", silent=True, action_type="reply", text='Сделать рассылку', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
         Button(action_body="stat-", columns=6, rows=1, bg_color="#ffffff", silent=True, action_type="reply", text='Статистика', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
         Button(action_body="otmena", columns=6, rows=1, bg_color="#ffffff", silent=True, action_type="reply", text='Назад', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle")]

ask_kb = [Button(action_body="Как связаться?", columns=6, rows=1, silent=True, action_type="reply", text='Как с вами связаться?', text_opacity=1, bg_media=how_contact_button_jpg, bg_media_type='picture'),
         Button(action_body="Какие условия доставки?", columns=6, rows=1, silent=True, action_type="reply", text='Какие условия доставки?', text_opacity=1, bg_media=delivery_types_button_jpg, bg_media_type='picture'),
         Button(action_body="Какие есть способы оплаты?", columns=6, rows=1, silent=True, action_type="reply", text='Какие есть способы оплаты?', text_opacity=1, bg_media=payment_types_button_jpg, bg_media_type='picture'),
         Button(action_body="Клубная карта", columns=6, rows=1, silent=True, action_type="reply", text='Клубная карта', text_opacity=1, bg_media=club_card_button_jpg, bg_media_type='picture'),
         Button(action_body="otmena", columns=6, rows=1, silent=True, action_type="reply", text='Назад', text_opacity=1, bg_media=big_go_back_jpg, bg_media_type='picture')]

card = [Button(action_body="Почему стоит приобрести нашу клубную карту?", columns=6, rows=1, silent=True, action_type="reply", text='Почему стоит приобрести нашу клубную карту?', text_opacity=1, bg_media=why_buy_card_jpg, bg_media_type='picture'),
        Button(action_body="КАК ОНА РАБОТАЕТ?", columns=6, rows=1, silent=True, action_type="reply", text='Что такое клубная карта и как она работает?', text_opacity=1, bg_media=what_is_club_card_jpg, bg_media_type='picture'),
        Button(action_body="КАКОВА МАКСИМАЛЬНАЯ СКИДКА, КОТОРУЮ ВЫ МОЖЕТЕ ПОЛУЧИТЬ С ПОМОЩЬЮ КАРТЫ", columns=6, rows=1, silent=True, action_type="reply", text='Какова максимальная скидка, которую вы можете получить с помощью карты?', text_opacity=1, bg_media=the_biggest_discount_jpg, bg_media_type='picture'),
        Button(action_body="КАК МНЕ ПРИОБРЕСТИ КЛУБНУЮ КАРТУ", columns=6, rows=1, silent=True, action_type="reply", text='Как мне приобрести клубную карту?', text_opacity=1, bg_media=how_buy_club_card_jpg, bg_media_type='picture'),
        Button(action_body="СМОГУ ЛИ Я ИСПОЛЬЗОВАТЬ КАРТУ", columns=6, rows=1, silent=True, action_type="reply", text='Смогу ли я использовать карту, если забыл е дома, лишь назвав свое имя?', text_opacity=1, bg_media=can_i_use_card_jpg, bg_media_type='picture'),
        Button(action_body="КАК УЗНАТЬ", columns=6, rows=1, silent=True, action_type="reply", text='Как узнать, сколько баллов у меня уже есть?', text_opacity=1, bg_media=how_many_points_jpg, bg_media_type='picture'),
        Button(action_body="otmena", columns=6, rows=1, silent=True, action_type="reply", text='Назад', text_size="regular", text_opacity=1, bg_media=big_go_back_jpg, bg_media_type='picture')]


ras = [Button(action_body="no_orders", columns=6, rows=1, bg_color="#ffffff", silent=True, action_type="reply", text='Нет заказов', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
         Button(action_body="one-or-more", columns=6, rows=1, bg_color="#ffffff", silent=True, action_type="reply", text='1 или более заказов', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
         Button(action_body="more-n", columns=6, rows=1, bg_color="#ffffff", silent=True, action_type="reply", text='Более N кол-ва заказов', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
         Button(action_body="m-or-more-month", columns=6, rows=1, bg_color="#ffffff", silent=True, action_type="reply", text='N или более заказов за последний месяц', text_size= "regular", text_opacity=60, text_h_align="center", text_v_align= "middle"),
       Button(action_body="sr-sum-more", columns=6, rows=1, bg_color="#ffffff", silent=True, action_type="reply",
              text='Средняя сумма заказов больше N', text_size="regular", text_opacity=60, text_h_align="center",
              text_v_align="middle"),
Button(action_body="sr-sum-less", columns=6, rows=1, bg_color="#ffffff", silent=True, action_type="reply",
              text='Средняя сумма заказов меньше N', text_size="regular", text_opacity=60, text_h_align="center",
              text_v_align="middle"),
Button(action_body="pb-n-less", columns=6, rows=1, bg_color="#ffffff", silent=True, action_type="reply",
              text='Пользуются ботом меньше N дней', text_size="regular", text_opacity=60, text_h_align="center",
              text_v_align="middle"),
Button(action_body="pb-n-more", columns=6, rows=1, bg_color="#ffffff", silent=True, action_type="reply",
              text='Пользуются ботом больше N дней', text_size="regular", text_opacity=60, text_h_align="center",
              text_v_align="middle"),
Button(action_body="send-to-all", columns=6, rows=1, bg_color="#ffffff", silent=True, action_type="reply",
              text='Всем пользователям', text_size="regular", text_opacity=60, text_h_align="center",text_v_align="middle"),
       Button(action_body="back-to-admin", columns=6, rows=1, bg_color="#ffffff", silent=True, action_type="reply",
              text='Назад', text_size="regular", text_opacity=60, text_h_align="center", text_v_align="middle")]

ras_cat = [Button(action_body="ras-photo", columns=6, rows=1, bg_color="#ffffff", silent=True, action_type="reply",
              text='Картинка', text_size="regular", text_opacity=60, text_h_align="center", text_v_align="middle"),
           Button(action_body="ras-text", columns=6, rows=1, bg_color="#ffffff", silent=True, action_type="reply",
                  text='Текст', text_size="regular", text_opacity=60, text_h_align="center", text_v_align="middle"),
Button(action_body="back-to-admin", columns=6, rows=1, bg_color="#ffffff", silent=True, action_type="reply",
              text='Назад', text_size="regular", text_opacity=60, text_h_align="center", text_v_align="middle")
           ]

back_to_admin = Button(action_body="back-to-admin", columns=6, rows=1, bg_color="#ffffff", silent=True, action_type="reply",
              text='Назад', text_size="regular", text_opacity=60, text_h_align="center", text_v_align="middle")


async def items_keyboard(category):
    items, keys = await search.subcat_pizza(category)
    buttons = []
    for item, key in zip(items, keys):
        s = item["name"]

        image = Button(action_body=f"get-more-info-{key}", columns=6, rows=5, action_type="reply",
                       image=f"https://pizzacoffee.by/{item['picture']}")

        title_and_text = Button(action_body=f"get-more-info-{key}", columns=6, rows=1, action_type="reply",
                                text=f'<font color=#323232><b>{s}</b></font>', text_size="medium",
                                text_v_align='middle', text_h_align='left')

        buttons.append(image)
        buttons.append(title_and_text)

    return buttons


async def to_subcategory(category, loop):
    items = await search.subcat(category)
    buttons = []
    for item in items:
        s = item["name"]
        if s == '&quot;Double Pizza&quot; пиццы с двойным сырным дном ':
            s = 'Пиццы с двойным сырным дном'

        image = Button(action_body=f'to-subcat-{item["id"]}', columns=6, rows=5, text=s, text_opacity=1, action_type="reply",
                       image=f"https://pizzacoffee.by/{item['picture']}")

        title_and_text = Button(action_body=f'to-subcat-{item["id"]}', columns=6, rows=1, action_type="reply",
                                text=f'<font color=#323232><b>{s}</b></font>', text_size="medium",
                                text_v_align='middle', text_h_align='center')
        buttons.append(image)
        buttons.append(title_and_text)

    return buttons


async def pizza_keyboard(p_id):
    items, keys = await search.subcat_pizza(p_id)
    buttons = []
    for item, key in zip(items, keys):
        s = str(item['name'])
        s = s.replace("&quot;", "'")
        image = Button(action_body=f"get-more-info-{key}", columns=6, rows=5, action_type="reply",
                       image=f"https://pizzacoffee.by/{item['picture']}", text=item['name'], text_opacity=1)

        title_and_text = Button(action_body=f"get-more-info-{key}", columns=6, rows=1, action_type="reply",
                                text=f'<font color=#323232><b>{s}</b></font>', text_size="medium",
                                text_v_align='middle', text_h_align='left')

        buttons.append(image)
        buttons.append(title_and_text)
    return buttons