class Partner:
    def __init__(self, partner_id, partner_name, contact_person, phone_number, email, address, contract_number, date_added, partner_type):
        self.partner_id = partner_id
        self.partner_name = partner_name
        self.contact_person = contact_person
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.contract_number = contract_number
        self.date_added = date_added
        self.partner_type = partner_type

    def __repr__(self):
        return f"Partner(id={self.partner_id}, name='{self.partner_name}')"


class Product:
    def __init__(self, product_id, product_name, product_description, unit_price, category):
        self.product_id = product_id
        self.product_name = product_name
        self.product_description = product_description
        self.unit_price = unit_price
        self.category = category

    def __repr__(self):
        return f"Product(id={self.product_id}, name='{self.product_name}')"


class SaleHistory:
    def __init__(self, sale_id, partner_id, product_id, sale_date, quantity, sale_amount, discount):
        self.sale_id = sale_id
        self.partner_id = partner_id
        self.product_id = product_id
        self.sale_date = sale_date
        self.quantity = quantity
        self.sale_amount = sale_amount
        self.discount = discount

    def __repr__(self):
        return f"SaleHistory(id={self.sale_id}, date={self.sale_date})"

