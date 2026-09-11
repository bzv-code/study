/**
 * Оформление заказа: адрес, время доставки, отправка в backend.
 *
 * У MAX нет моста sendData обратно в бота (в отличие от Telegram), поэтому заказ
 * создаётся прямым запросом к backend, а бот узнаёт о новых заказах и меняет статусы
 * через backend (см. bot/bot_app/services/notifications.py).
 */
import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { apiFetch } from "../api/client";
import AddressForm from "../components/AddressForm";
import DeliveryTimePicker from "../components/DeliveryTimePicker";
import { useCartStore } from "../store/cartStore";
import { formatPrice } from "../utils/format";

export default function Checkout() {
  const navigate = useNavigate();
  const { items, total, clear } = useCartStore();

  const [address, setAddress] = useState("");
  const [deliveryTime, setDeliveryTime] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canSubmit = address.trim().length > 0 && deliveryTime.length > 0 && items.length > 0;

  async function handleSubmit() {
    if (!canSubmit || submitting) return;
    setSubmitting(true);
    setError(null);

    try {
      await apiFetch("/orders", {
        method: "POST",
        body: JSON.stringify({
          items: items.map((i) => ({ bouquet_id: i.bouquetId, quantity: i.quantity })),
          address,
          delivery_time: deliveryTime,
        }),
      });
      clear();
      navigate("/success");
    } catch {
      setError("Не получилось оформить заказ. Проверьте адрес и время и попробуйте ещё раз.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="checkout">
      <button className="checkout__back" onClick={() => navigate("/cart")}>
        ← Корзина
      </button>
      <h1 className="checkout__title">Оформление заказа</h1>

      <label className="checkout__label">Адрес доставки</label>
      <AddressForm value={address} onChange={setAddress} />

      <label className="checkout__label">Время доставки</label>
      <DeliveryTimePicker value={deliveryTime} onChange={setDeliveryTime} />

      {error && <p className="checkout__error">{error}</p>}

      <div className="checkout__footer">
        <div className="checkout__total">
          <span>Итого</span>
          <span className="checkout__total-sum">{formatPrice(total())}</span>
        </div>
        <button className="btn-primary" disabled={!canSubmit || submitting} onClick={handleSubmit}>
          {submitting ? "Оформляю…" : "Подтвердить заказ"}
        </button>
      </div>

      <style>{`
        .checkout {
          padding: 16px 16px 32px;
          min-height: 100vh;
          display: flex;
          flex-direction: column;
        }
        .checkout__back {
          background: none;
          border: none;
          color: var(--sage);
          font-weight: 600;
          font-size: 14px;
          padding: 0 0 16px;
          cursor: pointer;
          align-self: flex-start;
        }
        .checkout__title {
          margin: 0 0 20px;
          font-family: var(--font-display);
          font-size: 26px;
          font-weight: 600;
          color: var(--forest);
        }
        .checkout__label {
          font-size: 13px;
          font-weight: 600;
          color: var(--ink-muted);
          margin-bottom: 6px;
          display: block;
        }
        .checkout textarea,
        .checkout select {
          width: 100%;
          border: 1px solid var(--line);
          border-radius: 12px;
          padding: 12px;
          font-size: 14px;
          font-family: var(--font-body);
          background: #fff;
          color: var(--ink);
          margin-bottom: 20px;
          resize: vertical;
          min-height: 44px;
        }
        .checkout__error {
          color: var(--coral-dark);
          font-size: 13px;
          margin: -8px 0 16px;
        }
        .checkout__footer {
          margin-top: auto;
          padding-top: 16px;
          border-top: 1px solid var(--line);
        }
        .checkout__total {
          display: flex;
          justify-content: space-between;
          align-items: baseline;
          margin-bottom: 12px;
          font-size: 14px;
          color: var(--ink-muted);
        }
        .checkout__total-sum {
          font-family: var(--font-display);
          font-size: 22px;
          font-weight: 600;
          color: var(--forest);
        }
        .btn-primary {
          width: 100%;
          background: var(--coral);
          color: #fff;
          border: none;
          border-radius: 999px;
          padding: 14px 24px;
          font-size: 15px;
          font-weight: 600;
          cursor: pointer;
        }
        .btn-primary:disabled {
          background: var(--line);
          color: var(--ink-muted);
          cursor: not-allowed;
        }
      `}</style>
    </div>
  );
}
