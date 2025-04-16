DROP TABLE IF EXISTS sales_history;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS partners;

-- 2. Создание таблицы партнеров (partners)
CREATE TABLE partners (
    partner_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Уникальный идентификатор партнера
    partner_name TEXT NOT NULL,                      -- Название партнера (обязательно)
    contact_person TEXT,                           -- Контактное лицо
    phone_number TEXT,                             -- Номер телефона
    email TEXT,                                    -- Адрес электронной почты
    address TEXT,                                  -- Адрес партнера (добавлено)
    contract_number TEXT UNIQUE,                   -- Номер контракта (добавлено, UNIQUE чтобы избежать дубликатов)
    date_added DATE DEFAULT (date('now')),          -- Дата добавления партнера (добавлено, по умолчанию текущая дата)
    partner_type TEXT                               -- Тип партнера (добавлено: поставщик, дилер и т.д.)
);

-- 3. Создание таблицы продуктов (products)
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Уникальный идентификатор продукта
    product_name TEXT NOT NULL,                      -- Название продукта (обязательно)
    product_description TEXT,                        -- Описание продукта (добавлено)
    unit_price REAL,                                  -- Цена за единицу (добавлено)
    category TEXT                                    -- Категория продукта (добавлено)
);

-- 4. Создание таблицы истории продаж (sales_history)
CREATE TABLE sales_history (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,     -- Уникальный идентификатор продажи
    partner_id INTEGER NOT NULL,                     -- Идентификатор партнера (обязательно)
    product_id INTEGER NOT NULL,                     -- Идентификатор продукта (обязательно)
    sale_date DATE NOT NULL,                        -- Дата продажи (обязательно)
    quantity INTEGER NOT NULL,                        -- Количество проданного товара (обязательно)
    sale_amount REAL,                               -- Общая сумма продажи (добавлено, можно вычислять)
    discount REAL DEFAULT 0.0,                      -- Размер скидки (добавлено, по умолчанию 0)
    FOREIGN KEY (partner_id) REFERENCES partners (partner_id),  -- Внешний ключ к таблице partners
    FOREIGN KEY (product_id) REFERENCES products (product_id)    -- Внешний ключ к таблице products
);

-- 5. Создание индексов (для повышения производительности)
CREATE INDEX idx_partners_name ON partners (partner_name);
CREATE INDEX idx_sales_history_partner_id ON sales_history (partner_id);
CREATE INDEX idx_sales_history_product_id ON sales_history (product_id);
CREATE INDEX idx_sales_history_date ON sales_history (sale_date);

-- 6. Добавление триггера для автоматического вычисления sale_amount
-- (Пример - можно убрать, если вычисляете сумму в Python)
CREATE TRIGGER calculate_sale_amount
AFTER INSERT ON sales_history
BEGIN
    UPDATE sales_history
    SET sale_amount = (
        SELECT p.unit_price * NEW.quantity * (1 - NEW.discount)
        FROM products p
        WHERE p.product_id = NEW.product_id
    )
    WHERE sale_id = NEW.sale_id;
END;

import sqlite3
import csv
from datetime import datetime

def import_partners(db_path, csv_file):
    """Импортирует данные о партнерах из CSV-файла в таблицу partners."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Проверка на наличие необходимых полей и их непустоту
                    if not all(key in row and row[key] for key in ['partner_name', 'contract_number']):
                        print(f"Пропущена запись партнера из-за отсутствия обязательных полей: {row}")
                        continue

                    cursor.execute('''
                        INSERT INTO partners (partner_name, contact_person, phone_number, email, address, contract_number, date_added, partner_type)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row['partner_name'],
                        row['contact_person'],
                        row['phone_number'],
                        row['email'],
                        row['address'],
                        row['contract_number'],
                        row.get('date_added', datetime.now().strftime('%Y-%m-%d')), # Если нет даты, ставим текущую
                        row.get('partner_type', 'Default Type') # Если нет типа, ставим значение по умолчанию
                    ))
                except sqlite3.Error as e:
                    print(f"Ошибка при импорте партнера {row['partner_name']}: {e}") # Более подробная информация об ошибке
        conn.commit()
        print("Данные о партнерах успешно импортированы.")

    except FileNotFoundError:
        print(f"Ошибка: Файл {csv_file} не найден.")
    except sqlite3.Error as e:
        print(f"Ошибка базы данных при импорте партнеров: {e}")
    finally:
        if conn:
            conn.close()

def import_products(db_path, csv_file):
    """Импортирует данные о продуктах из CSV-файла в таблицу products."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Проверка на наличие обязательных полей
                    if not all(key in row and row[key] for key in ['product_name', 'unit_price']):
                        print(f"Пропущена запись продукта из-за отсутствия обязательных полей: {row}")
                        continue

                    cursor.execute('''
                        INSERT INTO products (product_name, product_description, unit_price, category)
                        VALUES (?, ?, ?, ?)
                    ''', (
                        row['product_name'],
                        row.get('product_description', ''), # Если нет описания, ставим пустую строку
                        float(row['unit_price']),  # Преобразование цены к float
                        row.get('category', 'Default Category') # Если нет категории, ставим значение по умолчанию
                    ))
                except ValueError:
                    print(f"Ошибка: Неверный формат цены для продукта {row['product_name']}")
                except sqlite3.Error as e:
                     print(f"Ошибка при импорте продукта {row['product_name']}: {e}")

        conn.commit()
        print("Данные о продуктах успешно импортированы.")

    except FileNotFoundError:
        print(f"Ошибка: Файл {csv_file} не найден.")
    except sqlite3.Error as e:
        print(f"Ошибка базы данных при импорте продуктов: {e}")
    finally:
        if conn:
            conn.close()


def import_sales_history(db_path, csv_file):
    """Импортирует данные об истории продаж из CSV-файла в таблицу sales_history."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Проверка наличия обязательных полей
                    if not all(key in row and row[key] for key in ['partner_id', 'product_id', 'sale_date', 'quantity']):
                        print(f"Пропущена запись о продаже из-за отсутствия обязательных полей: {row}")
                        continue

                    # Преобразование даты из строки в объект datetime
                    sale_date = datetime.strptime(row['sale_date'], '%Y-%m-%d').date()  # Подставьте свой формат даты

                    # Вычисление sale_amount перед вставкой
                    cursor.execute("SELECT unit_price FROM products WHERE product_id = ?", (int(row['product_id']),))
                    product_price = cursor.fetchone()
                    if product_price is None:
                        print(f"Не найден продукт с ID {row['product_id']} для продажи с ID {row['sale_id']}")
                        continue
                    sale_amount = product_price[0] * int(row['quantity']) * (1 - float(row.get('discount', 0.0)))

                    cursor.execute('''
                        INSERT INTO sales_history (partner_id, product_id, sale_date, quantity, sale_amount, discount)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        int(row['partner_id']),   # Преобразование ID к integer
                        int(row['product_id']),     # Преобразование ID к integer
                        sale_date,
                        int(row['quantity']),     # Преобразование количества к integer
                        sale_amount,  # Вычисленная сумма продажи
                        float(row.get('discount', 0.0))  # Преобразование скидки к float, если есть
                    ))
                except ValueError as ve:
                    print(f"Ошибка: Неверный формат данных для продажи с ID {row['sale_id']}: {ve}")
                except sqlite3.Error as e:
                    print(f"Ошибка при импорте истории продаж для ID {row['sale_id']}: {e}")

        conn.commit()
        print("Данные об истории продаж успешно импортированы.")

    except FileNotFoundError:
        print(f"Ошибка: Файл {csv_file} не найден.")
    except sqlite3.Error as e:
        print(f"Ошибка базы данных при импорте истории продаж: {e}")
    finally
        if conn:
            conn.close()


if __name__ == "__main__":
    db_path = 'db/partner_management.db'  
    partners_csv = 'resources/partners.csv'
    products_csv = 'resources/products.csv'
    sales_csv = 'resources/sales_history.csv'

    import_partners(db_path, partners_csv)
    import_products(db_path, products_csv)
    import_sales_history(db_path, sales_csv)
