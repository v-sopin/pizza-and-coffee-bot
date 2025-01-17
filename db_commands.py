import aiomysql
from pymysql import connect
from config import DB_NAME, DB_HOST, DB_PASSWORD, DB_USER
from models import User, Basket
import datetime


async def create_con(loop):
    con = await aiomysql.connect(host=DB_HOST, user=DB_USER, db=DB_NAME, password=DB_PASSWORD, loop=loop)
    cur = await con.cursor()
    return con, cur


def create_sync_con():
    con = connect(host=DB_HOST, user=DB_USER, db=DB_NAME,
                  password=DB_PASSWORD)
    cur = con.cursor()

    return con, cur


class Com:
    @staticmethod
    async def user_exist(id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select count(*) from users where id = %s', id)
        r = await cur.fetchone()
        count = r[0]
        if count > 0:
            return True
        else:
            return False

    @staticmethod
    async def get_user_obj(id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select * from users where id = %s', id)
        user = await cur.fetchone()

        if user is None:
            return None

        return User(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7], user[8], user[9])

    @staticmethod
    async def add_user(id, city, full_name, phone_number, context, loop):
        con, cur = await create_con(loop)
        print(city)
        await cur.execute('insert into users values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                          (id, city, ' ', ' ', context, '', '', ' ', datetime.date.today(), 1))
        await con.commit()
        con.close()

    @staticmethod
    async def add_user_for_stat(id, loop):
        con, cur = await create_con(loop)
        await cur.execute('insert into stat values(%s, %s, %s, %s, %s)',
                          (id, 1, datetime.date.today(), None, None))
        await con.commit()
        con.close()

    @staticmethod
    async def update_user_for_stat(id, loop):
        con, cur = await create_con(loop)
        await cur.execute('update stat set subscr=%s where id = %s', (0, id))
        await con.commit()
        await cur.execute('update stat set out_date=%s where id = %s', (datetime.date.today(), id))
        await con.commit()
        con.close()

    @staticmethod
    async def get_cont_new_users(st_date, f_date, loop):
        con, cur = await create_con(loop)
        await cur.execute("select count(id) from stat where date_sub between %s and %s", (st_date, f_date))
        users = await cur.fetchall()
        con.close()
        if len(users) == 0:
            return 0
        else:
            return users[0]

    @staticmethod
    async def get_cont_out_users(st_date, f_date, loop):
        con, cur = await create_con(loop)
        await cur.execute("select count(id) from stat where subscr = '0' and out_date between %s and %s",
                          (st_date, f_date))
        users = await cur.fetchall()
        con.close()
        if len(users) == 0:
            return 0
        else:
            return users[0]

    @staticmethod
    async def get_cont_orders(st_date, f_date, loop):
        con, cur = await create_con(loop)
        await cur.execute("select count(u_id) from orders where dat between %s and %s",
                          (st_date, f_date))
        users = await cur.fetchall()
        con.close()
        if len(users) == 0:
            return 0
        else:
            return users[0]

    @staticmethod
    async def get_users_city(city, loop):
        con, cur = await create_con(loop)
        await cur.execute("select count(id) from users where city = %s",
                          (city))
        users = await cur.fetchall()
        con.close()
        if len(users) == 0:
            return 0
        else:
            return users[0]

    @staticmethod
    async def update_fio(id, fio, loop):
        con, cur = await create_con(loop)
        await cur.execute('update users set full_name=%s where id = %s', (fio, id))
        await con.commit()
        con.close()

    @staticmethod
    async def update_tel(id, tel, loop):
        con, cur = await create_con(loop)
        await cur.execute('update users set phone_number=%s where id = %s', (tel, id))
        await con.commit()
        con.close()

    @staticmethod
    async def update_address(id, tel, loop):
        con, cur = await create_con(loop)
        await cur.execute('update users set address=%s where id = %s', (tel, id))
        await con.commit()
        con.close()

    @staticmethod
    async def update_house(id, house, loop):
        con, cur = await create_con(loop)
        await cur.execute('update users set house=%s where id = %s', (house, id))
        await con.commit()
        con.close()

    @staticmethod
    async def add_item_to_basket(id, i_id, c_id, price, name, loop):
        con, cur = await create_con(loop)

        if price == '' or price == ' ':
            await cur.execute('insert into basket (u_id, i_id, c_id, count, price, name) values(%s, %s, %s, %s, %s, %s)', (id, i_id, c_id, 0, 0, name))
            await con.commit()
            con.close()
        else:
            await cur.execute('insert into basket (u_id, i_id, c_id, count, price, name) values(%s, %s, %s, %s, %s, %s)', (id, i_id, c_id, 0, float(price), name))
            await con.commit()
            con.close()

    @staticmethod
    async def check_pizza_in_basket(user_id, category_id, product_id, offer_id, border_id, loop):
        con, cur = await create_con(loop)

        await cur.execute(('select name from basket where (u_id = %s and c_id = %s and i_id = %s and offer_id = %s and border_id = %s)'), (user_id, category_id, product_id, offer_id, border_id))
        await con.commit()
        count = await cur.fetchone()
        if not count:
            return False
        else:
            return True

    @staticmethod
    async def add_pizza_to_basket(id, i_id, c_id, price, offer_id, border_id, name, loop):
        con, cur = await create_con(loop)

        if price == '' or price == ' ':
            await cur.execute('insert into basket values(%s, %s, %s, %s, %s, %s, %s, %s)', (id, i_id, c_id, 0, 0, offer_id, border_id, name))
            await con.commit()
            con.close()
        else:
            await cur.execute('insert into basket values(%s, %s, %s, %s, %s, %s, %s, %s)', (id, i_id, c_id, 0, float(price), offer_id, border_id, name))
            await con.commit()
            con.close()

    @staticmethod
    async def get_user_basket_items(u_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select * from basket where u_id = %s', u_id)
        items = await cur.fetchall()

        result = []
        for item in items:
            result.append(Basket(item[0], item[1], item[2], item[3], item[4], item[5]))
        return result

    @staticmethod
    async def get_offer(product_id, user_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select offer_id, border_id from basket where (u_id = %s and i_id = %s)', (user_id, product_id))
        offer_id = await cur.fetchall()
        if len(offer_id) is 0 or offer_id[0][0] is None:
            return 0, 0
        else:
            return offer_id[0][0], offer_id[0][1]

    @staticmethod
    async def update_count_to_basket(id, c_id, count, loop):
        con, cur = await create_con(loop)
        await cur.execute('update basket set count=%s where u_id = %s and i_id = %s', (count, id, c_id))
        await con.commit()
        con.close()

    @staticmethod
    async def append_count_to_basket(id, c_id, count, loop):
        con, cur = await create_con(loop)
        await cur.execute('update basket set count= count + %s where u_id = %s and i_id = %s', (count, id, c_id))
        await con.commit()
        con.close()

    @staticmethod
    async def get_itemd_from_basket(id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select i_id from basket where u_id = %s', (id))
        items = await cur.fetchall()
        await cur.execute('select c_id from basket where u_id = %s', (id))
        products = await cur.fetchall()
        con.close()
        return products, items

    @staticmethod
    async def get_count(product_id, viber_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select count from basket where i_id = %s and u_id = %s', (product_id, viber_id))
        count = await cur.fetchone()
        con.close()
        return count[0]

    @staticmethod
    async def get_for_json(id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select phone_number from users where id = %s', (id))
        phone = await cur.fetchall()
        await cur.execute('select full_name from users where id = %s', (id))
        name = await cur.fetchall()
        await cur.execute('select i_id from basket where u_id = %s', (id))
        items = await cur.fetchall()
        await cur.execute('select c_id from basket where u_id = %s', (id))
        products = await cur.fetchall()
        await cur.execute('select count from basket where u_id = %s', (id))
        counts = await cur.fetchall()
        con.close()
        return phone[0], name[0], products, items, counts

    @staticmethod
    async def delete_from_basket(id, item_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('delete from basket where u_id = %s and i_id = %s', (id, str(item_id)))
        await con.commit()
        con.close()

    @staticmethod
    async def delete_from_basket_pizza(id, item_id, offer_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('delete from basket where(u_id = %s and i_id = %s and offer_id = %s)', (id, str(item_id), offer_id))
        await con.commit()
        con.close()

    @staticmethod
    async def clear_user_basket(id, loop):
        con, cur = await create_con(loop)
        await cur.execute('delete from basket where u_id = %s', (id))
        await con.commit()
        con.close()

    @staticmethod
    async def clear_users(loop):
        con, cur = await create_con(loop)
        await cur.execute('delete from users')
        await con.commit()
        con.close()

    @staticmethod
    async def get_user(id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select * from users where id = %s', (id))
        user = await cur.fetchone()
        con.close()

        if user is None:
            return None

        return user

    @staticmethod
    async def get_user_no_orders(id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select * from orders where id = %s', (id))
        user = await cur.fetchall()
        con.close()

        if user is None:
            return None

        return user

    @staticmethod
    async def get_all_users(loop):
        con, cur = await create_con(loop)
        await cur.execute('select id from users')
        users = await cur.fetchall()
        con.close()
        return users

    @staticmethod
    async def add_order(u_id, sum, loop):
        con, cur = await create_con(loop)
        datetime_now = datetime.datetime.today().date()
        await cur.execute('insert into orders values(%s, %s, %s)', (u_id, sum, datetime_now))
        await con.commit()
        con.close()

    @staticmethod
    async def users_from_orders(loop):
        con, cur = await create_con(loop)
        await cur.execute('select DISTINCT u_id from orders')
        users = await cur.fetchall()
        con.close()
        return users

    @staticmethod
    async def users_from_orders_more_n(u_id, n, loop):
        con, cur = await create_con(loop)
        await cur.execute('select count(u_id) from orders where u_id=%s', (u_id))
        users = await cur.fetchone()
        con.close()
        if int(users[0]) >= n:
            return users
        else:
            return None

    @staticmethod
    async def users_from_orders_more_n_and_date(u_id, n, loop):
        con, cur = await create_con(loop)
        await cur.execute(
            'select count(u_id) from orders where u_id=%s and dat > DATE_SUB(CURRENT_DATE, INTERVAL 30 DAY)', (u_id))
        users = await cur.fetchone()
        con.close()
        if int(users[0]) >= n:
            return users
        else:
            return None

    @staticmethod
    async def users_from_orders_more_n_date(n, loop):
        con, cur = await create_con(loop)
        await cur.execute(
            'SELECT id from users where DATEDIFF (CURDATE(),date) >= %s', (n))
        users = await cur.fetchone()
        con.close()
        return users

    @staticmethod
    async def add_options(user_id, product_id, offer_id, name, size, loop):
        con, cur = await create_con(loop)
        await cur.execute('insert into pizza_options values(%s, %s, %s, %s, %s)', (user_id, product_id, offer_id, name, size))
        await con.commit()
        con.close()

    @staticmethod
    async def users_from_orders_less_n_date(n, loop):
        con, cur = await create_con(loop)
        await cur.execute(
            'SELECT id from users where DATEDIFF (CURDATE(),date) <= %s', (n))
        users = await cur.fetchall()
        con.close()
        if len(users) == 0:
            return None
        else:
            return users

    @staticmethod
    async def users_from_orders_more_n_sum(u_id, n, loop):
        con, cur = await create_con(loop)
        res = []
        await cur.execute('select sum(summ) from orders where u_id=%s', (u_id))
        users = await cur.fetchall()
        con.close()
        user = users[0]
        if float(user[0]) >= n:
            return user[0]
        else:
            return None

    @staticmethod
    async def users_from_orders_less_n_sum(u_id, n, loop):
        con, cur = await create_con(loop)
        res = []
        await cur.execute('select sum(summ) from orders where u_id=%s', (u_id))
        users = await cur.fetchall()
        con.close()
        user = users[0]
        if float(user[0]) <= n:
            return user[0]
        else:
            return None

    @staticmethod
    async def update_context(id, context, loop):
        con, cur = await create_con(loop)
        await cur.execute(f'update users set context = %s where id = %s', (context, id))
        await con.commit()
        con.close()

    @staticmethod
    async def update_more_info(id, p_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('update users set p_id = %s where id = %s', (p_id, id))
        await con.commit()
        con.close()

    @staticmethod
    async def update_more_info_c_id(id, p_id, loop):
        con, cur = await create_con(loop)
        await cur.execute('update users set c_id = %s where id = %s', (p_id, id))
        await con.commit()
        con.close()

    @staticmethod
    async def get_more_info(id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select p_id from users where id = %s', (id))
        context = await cur.fetchone()
        con.close()
        return context[0]

    @staticmethod
    async def get_more_c_id(id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select c_id from users where id = %s', (id))
        context = await cur.fetchone()
        con.close()
        return context[0]

    @staticmethod
    async def get_context(id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select context from users where id = %s', (id))
        context = await cur.fetchone()
        con.close()
        return context[0]

    @staticmethod
    async def get_city(id, loop):
        con, cur = await create_con(loop)
        await cur.execute('select city from users where id = %s', (id))
        context = await cur.fetchone()
        con.close()
        return context[0]

    @staticmethod
    def sync_get_context(tel_id):
        con, cur = create_sync_con()
        cur.execute('select context from users where tel_id = {0}'.format(tel_id))
        context = cur.fetchone()
        con.close()

        if context is None:
            return None
        else:
            return context[0]

    @staticmethod
    async def update_city(id, city, loop):
        con, cur = await create_con(loop)
        await cur.execute('update users set city = %s where id = %s', (city, id))
        await con.commit()
        con.close()
