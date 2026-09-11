/** Выбор даты и интервала времени доставки. */
import type { ChangeEvent } from "react";
interface Props {
  value: string;
  onChange: (value: string) => void;
}

export default function DeliveryTimePicker({ value, onChange }: Props) {
  return (
    <select value={value} onChange={(e: ChangeEvent<HTMLSelectElement>) => onChange(e.target.value)}>
      <option value="">Выберите время</option>
      <option value="today_12_15">Сегодня, 12:00–15:00</option>
      <option value="today_15_18">Сегодня, 15:00–18:00</option>
      <option value="tomorrow_10_13">Завтра, 10:00–13:00</option>
    </select>
  );
}
