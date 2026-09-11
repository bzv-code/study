/** Карточка букета в сетке каталога: фото, название (serif), бирка с ценой, категория. */
import { formatPrice } from "../utils/format";

interface Props {
  title: string;
  price: number;
  photoUrl: string;
  onClick: () => void;
}

export default function BouquetCard({ title, price, photoUrl, onClick }: Props) {
  return (
    <button onClick={onClick} className="bouquet-card">
      <div className="bouquet-card__photo">
        {photoUrl ? (
          <img src={photoUrl} alt={title} loading="lazy" />
        ) : (
          <div className="bouquet-card__placeholder" aria-hidden="true">
            🌿
          </div>
        )}
        <span className="bouquet-card__tag">{formatPrice(price)}</span>
      </div>
      <div className="bouquet-card__title">{title}</div>

      <style>{`
        .bouquet-card {
          display: flex;
          flex-direction: column;
          align-items: flex-start;
          gap: 8px;
          background: none;
          border: none;
          padding: 0;
          cursor: pointer;
          text-align: left;
          width: 100%;
        }
        .bouquet-card__photo {
          position: relative;
          width: 100%;
          aspect-ratio: 1 / 1.1;
          border-radius: 14px;
          overflow: hidden;
          background: var(--sage-light);
        }
        .bouquet-card__photo img {
          width: 100%;
          height: 100%;
          object-fit: cover;
          display: block;
        }
        .bouquet-card__placeholder {
          width: 100%;
          height: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 40px;
        }
        .bouquet-card__tag {
          position: absolute;
          left: 10px;
          bottom: 10px;
          background: var(--coral);
          color: #fff;
          font-family: var(--font-body);
          font-weight: 600;
          font-size: 13px;
          padding: 4px 10px;
          border-radius: 999px;
          box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
        }
        .bouquet-card__title {
          font-family: var(--font-display);
          font-size: 17px;
          font-weight: 500;
          color: var(--ink);
          line-height: 1.25;
        }
      `}</style>
    </button>
  );
}
