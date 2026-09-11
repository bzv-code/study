/** Карточка букета: фото, состав, цена, кнопка «Добавить в корзину». */
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { apiFetch } from "../api/client";
import { Bouquet, categoryLabel } from "../api/types";
import { useCartStore } from "../store/cartStore";
import { formatPrice } from "../utils/format";

export default function BouquetDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const addItem = useCartStore((s) => s.addItem);

  const [bouquet, setBouquet] = useState<Bouquet | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [added, setAdded] = useState(false);

  useEffect(() => {
    apiFetch<Bouquet>(`/catalog/bouquets/${id}`)
      .then(setBouquet)
      .catch(() => setError("Этот букет не нашёлся — возможно, его уже убрали из каталога."));
  }, [id]);

  function handleAddToCart() {
    if (!bouquet) return;
    addItem({
      bouquetId: bouquet.id,
      title: bouquet.title,
      price: bouquet.price,
      quantity: 1,
    });
    setAdded(true);
  }

  if (error) {
    return (
      <div className="detail detail--message">
        <p>{error}</p>
        <button className="btn-secondary" onClick={() => navigate("/")}>
          Назад в каталог
        </button>
      </div>
    );
  }

  if (!bouquet) {
    return <div className="detail detail--message">Загружаю…</div>;
  }

  return (
    <div className="detail">
      <button className="detail__back" onClick={() => navigate("/")}>
        ← Каталог
      </button>

      <div className="detail__photo">
        {bouquet.photo_url ? (
          <img src={bouquet.photo_url} alt={bouquet.title} />
        ) : (
          <div className="detail__placeholder" aria-hidden="true">
            🌿
          </div>
        )}
      </div>

      <p className="detail__category">{categoryLabel(bouquet.category)}</p>
      <h1 className="detail__title">{bouquet.title}</h1>
      <p className="detail__description">{bouquet.description}</p>

      <div className="detail__footer">
        <span className="detail__price">{formatPrice(bouquet.price)}</span>
        <button
          className={`btn-primary ${added ? "btn-primary--done" : ""}`}
          onClick={handleAddToCart}
        >
          {added ? "Добавлено ✓" : "В корзину"}
        </button>
      </div>

      <style>{`
        .detail {
          padding: 16px 16px 32px;
          min-height: 100vh;
        }
        .detail--message {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          gap: 16px;
          text-align: center;
          color: var(--ink-muted);
          font-size: 14px;
        }
        .detail__back {
          background: none;
          border: none;
          color: var(--sage);
          font-weight: 600;
          font-size: 14px;
          padding: 0 0 16px;
          cursor: pointer;
        }
        .detail__photo {
          width: 100%;
          aspect-ratio: 1 / 1;
          border-radius: 18px;
          overflow: hidden;
          background: var(--sage-light);
          margin-bottom: 16px;
        }
        .detail__photo img {
          width: 100%;
          height: 100%;
          object-fit: cover;
          display: block;
        }
        .detail__placeholder {
          width: 100%;
          height: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 64px;
        }
        .detail__category {
          margin: 0 0 4px;
          font-size: 12px;
          letter-spacing: 0.08em;
          text-transform: uppercase;
          color: var(--sage);
          font-weight: 600;
        }
        .detail__title {
          margin: 0 0 10px;
          font-family: var(--font-display);
          font-size: 26px;
          font-weight: 600;
          color: var(--forest);
        }
        .detail__description {
          margin: 0 0 24px;
          color: var(--ink-muted);
          font-size: 15px;
          line-height: 1.5;
        }
        .detail__footer {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 12px;
        }
        .detail__price {
          font-family: var(--font-display);
          font-size: 22px;
          font-weight: 600;
          color: var(--forest);
        }
        .btn-primary {
          background: var(--coral);
          color: #fff;
          border: none;
          border-radius: 999px;
          padding: 13px 24px;
          font-size: 15px;
          font-weight: 600;
          cursor: pointer;
        }
        .btn-primary--done {
          background: var(--forest);
        }
        .btn-secondary {
          background: var(--sage-light);
          color: var(--forest);
          border: none;
          border-radius: 999px;
          padding: 10px 20px;
          font-size: 14px;
          font-weight: 600;
          cursor: pointer;
        }
      `}</style>
    </div>
  );
}
