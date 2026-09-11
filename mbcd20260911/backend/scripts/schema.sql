-- Схема БД для проекта "Дом цветов".
-- Порядок создания важен из-за внешних ключей: users и couriers — до orders.

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    max_user_id BIGINT UNIQUE NOT NULL,
    full_name VARCHAR(200) NOT NULL DEFAULT '',
    phone VARCHAR(30) NOT NULL DEFAULT '',
    bonus_balance INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS couriers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    is_available BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS bouquets (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    category VARCHAR(100) NOT NULL,
    description VARCHAR(1000) NOT NULL DEFAULT '',
    price INTEGER NOT NULL,          -- цена в копейках
    photo_url VARCHAR(500) NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    status VARCHAR(50) NOT NULL DEFAULT 'new',
    address VARCHAR(500) NOT NULL,
    delivery_time VARCHAR(100) NOT NULL,
    total_amount INTEGER NOT NULL,   -- сумма в копейках
    courier_id INTEGER REFERENCES couriers(id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id),
    bouquet_id INTEGER NOT NULL REFERENCES bouquets(id),
    quantity INTEGER NOT NULL,
    price_at_order INTEGER NOT NULL  -- цена букета в копейках на момент заказа
);

CREATE INDEX IF NOT EXISTS idx_orders_user_id ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
