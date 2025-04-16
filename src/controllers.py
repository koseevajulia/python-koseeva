import sqlite3
from src.models import Partner, Product, SaleHistory
from src.config import DB_PATH

def get_all_partners():
    """Получает список всех партнеров из базы данных."""
    partners = []
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM partners")
        rows = cursor.fetchall()
        for row in rows:
            partner = Partner(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            partners.append(partner)
    except sqlite3.Error as e:
        print(f"Ошибка при получении партнеров: {e}")
    finally:
        if conn:
            conn.close()
    return partners

def get_partner_by_id(partner_id):
    """Получает партнера по ID."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM partners WHERE partner_id = ?", (partner_id,))
        row = cursor.fetchone()
        if row:
            partner = Partner(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
            return partner
        else:
            return None
    except sqlite3.Error as e:
        print(f"Ошибка при получении партнера с ID {partner_id}: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_sales_history_by_partner(partner_id):
    """Получает историю продаж партнера."""
    sales = []
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales_history WHERE partner_id = ?", (partner_id,))
        rows = cursor.fetchall()
        for row in rows:
            sale = SaleHistory(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            sales.append(sale)
    except sqlite3.Error as e:
        print(f"Ошибка при получении истории продаж партнера с ID {partner_id}: {e}")
    finally:
        if conn:
            conn.close()
    return sales

# Добавьте функции для добавления, редактирования и удаления партнеров, продуктов и записей о продажах.
# Пример функции добавления партнера:

def add_new_partner(partner_name, contact_person, phone_number, email, address, contract_number, date_added, partner_type):
    """Добавляет нового партнера в базу данных."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO partners (partner_name, contact_person, phone_number, email, address, contract_number, date_added, partner_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (partner_name, contact_person, phone_number, email, address, contract_number, date_added, partner_type))
        conn.commit()
        print(f"Партнер {partner_name} успешно добавлен.")
        return True
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении партнера {partner_name}: {e}")
        return False
    finally:
        if conn:
            conn.close()

# Аналогичные функции для добавления/редактирования/удаления продуктов и истории продаж
