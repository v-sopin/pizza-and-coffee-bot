class Basket:
    def __init__(self, u_id, i_id, c_id, count, price, name):
        self.u_id = u_id
        self.i_id = i_id
        self.c_id = c_id
        self.count = count
        self.price = price
        self.name = name


class User:
    def __init__(self, id, city, full_name, phone_number, context, p_id, c_id, address, date, house):
        self.id = id
        self.city = city
        self.full_name = full_name
        self.phone_number = phone_number
        self.context = context
        self.p_id = p_id
        self.c_id = c_id
        self.address = address
        self.date = date
        self.house = house
