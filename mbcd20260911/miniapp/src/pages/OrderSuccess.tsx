/** Экран успешного оформления заказа: номер заказа, кнопка закрыть mini app. */
import { useMax } from "../hooks/useMax";

export default function OrderSuccess() {
  const { close } = useMax();

  return (
    <div>
      <p>Заказ оформлен! Бот пришлёт подтверждение с деталями в чат.</p>
      <button onClick={close}>Закрыть</button>
    </div>
  );
}
