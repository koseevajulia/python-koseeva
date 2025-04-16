from src.controllers import get_all_partners, get_sales_history_by_partner, get_partner_by_id, add_new_partner
from src.views import format_partner_list, format_sales_history, format_partner_details

def main():
    while True:
        print("\nМеню:")
        print("1. Список партнеров")
        print("2. Информация о партнере по ID")
        print("3. История продаж партнера")
        print("4. Добавить нового партнера")
        print("5. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            partners = get_all_partners()
            print(format_partner_list(partners))
        elif choice == '2':
            partner_id = int(input("Введите ID партнера: "))
            partner = get_partner_by_id(partner_id)
            print(format_partner_details(partner))

        elif choice == '3':
            partner_id = int(input("Введите ID партнера: "))
            sales_history = get_sales_history_by_partner(partner_id)
            print(format_sales_history(sales_history))
        elif choice == '4':
            partner_name = input("Введите название партнера: ")
            contact_person = input("Введите контактное лицо: ")
            phone_number = input("Введите номер телефона: ")
            email = input("Введите email: ")
            address = input("Введите адрес: ")
            contract_number = input("Введите номер контракта: ")
            date_added = input("Введите дату добавления (YYYY-MM-DD): ")
            partner_type = input("Введите тип партнера: ")

            if add_new_partner(partner_name, contact_person, phone_number, email, address, contract_number, date_added, partner_type):
                print("Партнер успешно добавлен!")
            else:
                print("Ошибка при добавлении партнера.")
        elif choice == '5':
            break
        else:
            print("Неверный выбор. Попробуйте еще раз.")

if __name__ == "__main__":
    main()
