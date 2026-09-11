/** Корзина: список позиций, итоговая сумма, переход к оформлению заказа. */
import { useNavigate } from "react-router-dom";

import CartItem from "../components/CartItem";
import { useCartStore } from "../store/cartStore";
import { formatPrice } from "../utils/format";

export default function Cart() {
  const navigate = useNavigate();
  const { items, total, removeItem } = useCartStore();

  return (
    <div className="cart">
      <button className="cart__back" onClick={() => navigate("/")}>
        ← Каталог
      </button>
      <h1 className="cart__title">Корзина</h1>

      {items.length === 0 ? (
        <p className="cart__empty">
          Пока пусто. Выберите букет в каталоге — он появится здесь.
        </p>
      ) : (
        <>
          <div className="cart__list">
            {items.map((item) => (
              <CartItem key={item.bouquetId} item={item} onRemove={() => removeItem(item.bouquetId)} />
            ))}
          </div>

          <div className="cart__footer">
            <div className="cart__total">
              <span>Итого</span>
              <span className="cart__total-sum">{formatPrice(total())}</span>
            </div>
            <button className="btn-primary" onClick={() => navigate("/checkout")}>
              Оформить заказ
            </button>
          </div>
        </>
      )}

      <style>{`
        .cart {
          padding: 16px 16px 32px;
          min-height: 100vh;
          display: flex;
          flex-direction: column;
        }
        .cart__back {
          background: none;
          border: none;
          color: var(--sage);
          font-weight: 600;
          font-size: 14px;
          padding: 0 0 16px;
          cursor: pointer;
          align-self: flex-start;
        }
        .cart__title {
          margin: 0 0 16px;
          font-family: var(--font-display);
          font-size: 26px;
          font-weight: 600;
          color: var(--forest);
        }
        .cart__empty {
          color: var(--ink-muted);
          font-size: 14px;
          text-align: center;
          padding: 40px 0;
        }
        .cart__list {
          flex: 1;
        }
        .cart__footer {
          position: sticky;
          bottom: 0;
          background: var(--paper);
          padding-top: 16px;
          border-top: 1px solid var(--line);
          margin-top: 16px;
        }
        .cart__total {
          display: flex;
          justify-content: space-between;
          align-items: baseline;
          margin-bottom: 12px;
          font-size: 14px;
          color: var(--ink-muted);
        }
        .cart__total-sum {
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
      `}</style>
    </div>
  );
}
