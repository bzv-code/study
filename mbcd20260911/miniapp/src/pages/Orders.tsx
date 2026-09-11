/** «Мои заказы»: история заказов текущего пользователя (GET /orders, авторизация через WebAppData). */
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { apiFetch } from "../api/client";
import { formatPrice } from "../utils/format";

interface OrderItemOut {
  bouquet_id: number;
  quantity: number;
  price_at_order: number;
}

interface OrderOut {
  id: number;
  status: string;
  address: string;
  delivery_time: string;
  total_amount: number;
  items: OrderItemOut[];
}

const STATUS_LABELS: Record<string, string> = {
  new: "Новый",
  accepted: "Принят в работу",
  assembled: "Букет собран",
  on_the_way: "Курьер в пути",
  delivered: "Доставлен",
};

export default function Orders() {
  const navigate = useNavigate();
  const [orders, setOrders] = useState<OrderOut[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiFetch<OrderOut[]>("/orders")
      .then(setOrders)
      .catch(() => setError("Не получилось загрузить заказы. Потяните вниз, чтобы обновить."));
  }, []);

  return (
    <div className="orders">
      <button className="orders__back" onClick={() => navigate("/")}>
        ← Каталог
      </button>
      <h1 className="orders__title">Мои заказы</h1>

      {error && <p className="orders__status orders__status--error">{error}</p>}
      {!error && orders === null && <p className="orders__status">Загружаю…</p>}
      {!error && orders !== null && orders.length === 0 && (
        <p className="orders__status">
          Заказов пока нет — самое время заглянуть в каталог.
        </p>
      )}

      {orders && orders.length > 0 && (
        <div className="orders__list">
          {orders.map((o) => {
            const itemsCount = o.items.reduce((sum, i) => sum + i.quantity, 0);
            return (
              <div key={o.id} className="order-card">
                <div className="order-card__top">
                  <span className="order-card__number">Заказ №{o.id}</span>
                  <span className="order-card__status">
                    {STATUS_LABELS[o.status] ?? o.status}
                  </span>
                </div>
                <p className="order-card__meta">
                  {itemsCount} {itemsCount === 1 ? "букет" : "букета(ов)"} · {o.delivery_time}
                </p>
                <p className="order-card__address">{o.address}</p>
                <p className="order-card__total">{formatPrice(o.total_amount)}</p>
              </div>
            );
          })}
        </div>
      )}

      <style>{`
        .orders {
          padding: 16px 16px 32px;
          min-height: 100vh;
        }
        .orders__back {
          background: none;
          border: none;
          color: var(--sage);
          font-weight: 600;
          font-size: 14px;
          padding: 0 0 16px;
          cursor: pointer;
        }
        .orders__title {
          margin: 0 0 20px;
          font-family: var(--font-display);
          font-size: 26px;
          font-weight: 600;
          color: var(--forest);
        }
        .orders__status {
          color: var(--ink-muted);
          font-size: 14px;
          text-align: center;
          padding: 40px 0;
        }
        .orders__status--error {
          color: var(--coral-dark);
        }
        .orders__list {
          display: flex;
          flex-direction: column;
          gap: 12px;
        }
        .order-card {
          background: #fff;
          border: 1px solid var(--line);
          border-radius: 14px;
          padding: 14px 16px;
        }
        .order-card__top {
          display: flex;
          justify-content: space-between;
          align-items: baseline;
          margin-bottom: 6px;
        }
        .order-card__number {
          font-family: var(--font-display);
          font-size: 16px;
          font-weight: 600;
          color: var(--forest);
        }
        .order-card__status {
          font-size: 12px;
          font-weight: 600;
          color: var(--sage);
          text-transform: uppercase;
          letter-spacing: 0.04em;
        }
        .order-card__meta,
        .order-card__address {
          margin: 0 0 4px;
          font-size: 13px;
          color: var(--ink-muted);
        }
        .order-card__total {
          margin: 8px 0 0;
          font-weight: 600;
          color: var(--forest);
        }
      `}</style>
    </div>
  );
}
