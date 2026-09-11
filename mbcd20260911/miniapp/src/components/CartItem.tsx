/** Строка позиции в корзине: название, количество, цена, удаление. */
import type { CartItem as CartItemType } from "../store/cartStore";
import { formatPrice } from "../utils/format";

interface Props {
  item: CartItemType;
  onRemove: () => void;
}

export default function CartItem({ item, onRemove }: Props) {
  return (
    <div className="cart-item">
      <div>
        <p className="cart-item__title">{item.title}</p>
        <p className="cart-item__qty">{item.quantity} шт · {formatPrice(item.price)}</p>
      </div>
      <div className="cart-item__right">
        <span className="cart-item__sum">{formatPrice(item.price * item.quantity)}</span>
        <button className="cart-item__remove" onClick={onRemove} aria-label="Убрать из корзины">
          ✕
        </button>
      </div>

      <style>{`
        .cart-item {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 14px 0;
          border-bottom: 1px solid var(--line);
        }
        .cart-item__title {
          margin: 0 0 4px;
          font-family: var(--font-display);
          font-size: 16px;
          color: var(--ink);
        }
        .cart-item__qty {
          margin: 0;
          font-size: 13px;
          color: var(--ink-muted);
        }
        .cart-item__right {
          display: flex;
          align-items: center;
          gap: 12px;
        }
        .cart-item__sum {
          font-weight: 600;
          font-size: 14px;
          color: var(--forest);
        }
        .cart-item__remove {
          background: none;
          border: none;
          color: var(--ink-muted);
          font-size: 16px;
          cursor: pointer;
          padding: 4px;
        }
      `}</style>
    </div>
  );
}
