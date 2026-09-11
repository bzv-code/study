import { useEffect } from "react";
import { Route, Routes, useNavigate } from "react-router-dom";

import BouquetDetail from "./pages/BouquetDetail";
import Cart from "./pages/Cart";
import Catalog from "./pages/Catalog";
import Checkout from "./pages/Checkout";
import OrderSuccess from "./pages/OrderSuccess";
import Orders from "./pages/Orders";
import { useMax } from "./hooks/useMax";

export default function App() {
  const navigate = useNavigate();
  const { webApp } = useMax();

  // Диплинк из бота (?startapp=orders) должен сразу открыть нужный экран,
  // а не всегда каталог — start_param приходит один раз при запуске mini app.
  useEffect(() => {
    const startParam = webApp?.initDataUnsafe?.start_param;
    if (startParam === "orders") {
      navigate("/orders");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <Routes>
      <Route path="/" element={<Catalog />} />
      <Route path="/bouquet/:id" element={<BouquetDetail />} />
      <Route path="/cart" element={<Cart />} />
      <Route path="/checkout" element={<Checkout />} />
      <Route path="/success" element={<OrderSuccess />} />
      <Route path="/orders" element={<Orders />} />
    </Routes>
  );
}
