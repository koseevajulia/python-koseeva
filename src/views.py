def format_partner_list(partners):
    """Форматирует список партнеров для отображения."""
    if not partners:
        return "Нет партнеров для отображения."

    output = "Список партнеров:\n"
    for partner in partners:
        output += f"- {partner.partner_name} (ID: {partner.partner_id})\n"
    return output

def format_partner_details(partner):
     """Форматирует детали партнера для отображения."""
     if not partner:
          return "Партнер не найден"

     output = f"Детали партнера:\n"
     output += f"ID: {partner.partner_id}\n"
     output += f"Название: {partner.partner_name}\n"
     output += f"Контактное лицо: {partner.contact_person}\n"
     output += f"Номер телефона: {partner.phone_number}\n"
     output += f"Email: {partner.email}\n"
     output += f"Адрес: {partner.address}\n"
     output += f"Номер контракта: {partner.contract_number}\n"
     output += f"Дата добавления: {partner.date_added}\n"
     output += f"Тип партнера: {partner.partner_type}\n"
     return output

def format_sales_history(sales):
    """Форматирует историю продаж для отображения."""
    if not sales:
        return "Нет истории продаж для этого партнера."

    output = "История продаж:\n"
    for sale in sales:
        output += f"- ID продажи: {sale.sale_id}, Дата: {sale.sale_date}, Количество: {sale.quantity}, Сумма: {sale.sale_amount}\n"
    return output
