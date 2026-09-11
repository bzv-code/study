/** Главный экран mini app: категории (бирки) + сетка букетов из backend /catalog/bouquets. */
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { apiFetch } from "../api/client";
import { Bouquet, categoryLabel } from "../api/types";
import BouquetCard from "../components/BouquetCard";
import { useCartStore } from "../store/cartStore";

export default function Catalog() {
  const navigate = useNavigate();
  const cartCount = useCartStore((s) => s.items.length);

  const [bouquets, setBouquets] = useState<Bouquet[] | null>(null);
  const [categories, setCategories] = useState<string[]>([]);
  const [activeCategory, setActiveCategory] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiFetch<string[]>("/catalog/categories")
      .then(setCategories)
      .catch(() => {
        /* список категорий необязателен для работы страницы — молча пропускаем */
      });
  }, []);

  useEffect(() => {
    setBouquets(null);
    setError(null);
    const query = activeCategory ? `?category=${encodeURIComponent(activeCategory)}` : "";

    apiFetch<Bouquet[]>(`/catalog/bouquets${query}`)
      .then(setBouquets)
      .catch(() => setError("Не получилось загрузить каталог. Потяните вниз, чтобы обновить."));
  }, [activeCategory]);

  return (
    <div className="catalog">
      <header className="catalog__header">
        <div>
          <p className="catalog__eyebrow">Дом цветов</p>
          <h1 className="catalog__title">Каталог</h1>
        </div>
        <div className="catalog__header-actions">
          <button className="catalog__link-btn" onClick={() => navigate("/orders")}>
            Мои заказы
          </button>
          <button className="catalog__cart-btn" onClick={() => navigate("/cart")}>
            Корзина{cartCount > 0 ? ` · ${cartCount}` : ""}
          </button>
        </div>
      </header>

      {categories.length > 0 && (
        <div className="catalog__pills">
          <button
            className={`pill ${activeCategory === null ? "pill--active" : ""}`}
            onClick={() => setActiveCategory(null)}
          >
            Все
          </button>
          {categories.map((c) => (
            <button
              key={c}
              className={`pill ${activeCategory === c ? "pill--active" : ""}`}
              onClick={() => setActiveCategory(c)}
            >
              {categoryLabel(c)}
            </button>
          ))}
        </div>
      )}

      {error && <p className="catalog__error">{error}</p>}

      {!error && bouquets === null && <p className="catalog__status">Загружаю букеты…</p>}

      {!error && bouquets !== null && bouquets.length === 0 && (
        <p className="catalog__status">В этой категории пока пусто. Загляните позже.</p>
      )}

      {bouquets && bouquets.length > 0 && (
        <div className="catalog__grid">
          {bouquets.map((b) => (
            <BouquetCard
              key={b.id}
              title={b.title}
              price={b.price}
              photoUrl={b.photo_url}
              onClick={() => navigate(`/bouquet/${b.id}`)}
            />
          ))}
        </div>
      )}

      <style>{`
        .catalog {
          padding: 16px 16px 32px;
          min-height: 100vh;
        }
        .catalog__header {
          display: flex;
          align-items: flex-end;
          justify-content: space-between;
          margin-bottom: 16px;
        }
        .catalog__eyebrow {
          margin: 0;
          font-size: 12px;
          letter-spacing: 0.08em;
          text-transform: uppercase;
          color: var(--sage);
          font-weight: 600;
        }
        .catalog__title {
          margin: 2px 0 0;
          font-family: var(--font-display);
          font-size: 28px;
          font-weight: 600;
          color: var(--forest);
        }
        .catalog__header-actions {
          display: flex;
          align-items: center;
          gap: 8px;
        }
        .catalog__link-btn {
          background: none;
          border: none;
          color: var(--forest);
          font-size: 13px;
          font-weight: 600;
          cursor: pointer;
          text-decoration: underline;
          text-underline-offset: 2px;
          white-space: nowrap;
        }
        .catalog__cart-btn {
          background: var(--forest);
          color: #fff;
          border: none;
          border-radius: 999px;
          padding: 9px 16px;
          font-size: 13px;
          font-weight: 600;
          cursor: pointer;
          white-space: nowrap;
        }
        .catalog__pills {
          display: flex;
          gap: 8px;
          overflow-x: auto;
          padding-bottom: 4px;
          margin-bottom: 20px;
          scrollbar-width: none;
        }
        .catalog__pills::-webkit-scrollbar {
          display: none;
        }
        .pill {
          flex: 0 0 auto;
          background: var(--sage-light);
          color: var(--forest);
          border: 1px solid transparent;
          border-radius: 999px;
          padding: 7px 14px;
          font-size: 13px;
          font-weight: 500;
          cursor: pointer;
        }
        .pill--active {
          background: var(--forest);
          color: #fff;
        }
        .catalog__grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 20px 14px;
        }
        .catalog__status,
        .catalog__error {
          color: var(--ink-muted);
          font-size: 14px;
          padding: 24px 0;
          text-align: center;
        }
        .catalog__error {
          color: var(--coral-dark);
        }
      `}</style>
    </div>
  );
}
