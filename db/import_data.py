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

