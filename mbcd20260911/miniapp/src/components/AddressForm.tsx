/** Форма адреса доставки: улица, дом, квартира, комментарий курьеру. */
import type { ChangeEvent } from "react";
interface Props {
  value: string;
  onChange: (value: string) => void;
}

export default function AddressForm({ value, onChange }: Props) {
  return (
    <textarea
      placeholder="Адрес доставки"
      value={value}
      onChange={(e: ChangeEvent<HTMLTextAreaElement>) => onChange(e.target.value)}
    />
  );
}
